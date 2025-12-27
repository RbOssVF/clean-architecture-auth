import bcrypt
from fastapi import APIRouter, Request
from pydantic import ValidationError
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union
from .utils import get_hora_peru
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .database import in_transaction, simple_session, get_session
from .security.jwt_service import JWTService
import inspect

class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=get_hora_peru, nullable=False)
    updated_at: datetime = Field(
        default_factory=get_hora_peru,
        sa_column_kwargs={"onupdate": get_hora_peru},
        nullable=False
    )
    
class MixinResponse:
    def return_json(
        self,
        est: bool = False,
        ico: str = "",
        msg: str = "",
        data: Any = None,
        status_code: int = 200
    ):
        """
        Devuelve un JSONResponse estándar con serialización automática.
        """
        content = {
            "estado": est,
            "icono": ico,
            "message": msg,
            "data": data
        }
        return JSONResponse(content=content, status_code=status_code)

class MixinTryExcept(MixinResponse):
    async def try_except(self, func, **kwargs):
        try:
            if inspect.iscoroutinefunction(func):
                return await func(**kwargs)
            return func(**kwargs)

        except Exception as e:
            # Aquí luego puedes inyectar logger
            return self.return_json(
                est=False,
                ico="error",
                msg=str(e),
                status_code=500,
            )

class MixinTransaction(MixinTryExcept): 
    async def execute(self, func, *, method: str = "GET", **kwargs):

        method = method.upper()

        async def logic_wrapper():
            if method in ["POST", "PUT", "DELETE", "PATCH"]:
                async with in_transaction():
                    if inspect.iscoroutinefunction(func):
                        return await func(**kwargs)
                    return func(**kwargs)
            else:
                async with simple_session():
                    if inspect.iscoroutinefunction(func):
                        return await func(**kwargs)
                    return func(**kwargs)

        return await self.try_except(logic_wrapper)

class FormDataParser:
    @staticmethod
    async def parse(request: Request) -> Dict[str, Any]:
        form = await request.form()
        data = {}

        for key in form.keys():
            values = form.getlist(key)
            if len(values) == 1:
                data[key] = values[0]
            else:
                data[key] = values

        return data

class MixinValidadorPydantic(MixinResponse):
    async def validate_body(self, request: Request, body_model: Type[BaseModel]):
        try:
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                data = await request.json()
            elif "form-data" in content_type:
                data = await FormDataParser.parse(request)
            else:
                data = {}

            parsed_body = body_model(**data)
            request.state.body = parsed_body
            return parsed_body

        except ValidationError as e:
            return self.return_json(
                est=False,
                ico="error",
                data=e.errors(),
                msg="Error de validación en los datos enviados.",
                status_code=400,
            )

class MixinAuth(MixinResponse):
    async def validate_auth(self, request: Request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return self.return_json(
                est=False, ico="error", 
                msg="No se proporcionó un token de seguridad.", status_code=401
            )
        
        token = auth_header.split(" ")[1]
        payload = JWTService.validate_token(token)
        
        if not payload:
            return self.return_json(
                est=False, 
                ico="error", 
                msg="Token inválido o expirado.", 
                status_code=401
            )
        
        request.state.usuario = payload
        return payload


class BaseUseCaseHandler(MixinTransaction, MixinValidadorPydantic, MixinAuth):
    """
    Base para handlers de casos de uso.
    - Maneja la orquestación de validación y ejecución.
    """

    @property
    def session(self):
        return get_session()

    async def handle_request(
        self, 
        request: Request, 
        handler_func,
        schema: Optional[Type[BaseModel]] = None,
        method: str = "GET",
        protected: bool = False,
        required_permissions: Optional[List[str]] = None,
        required_roles: Optional[List[str]] = None,
        **kwargs
    ):
        # 1. Autenticación
        if protected:
            auth_result = await self.validate_auth(request)
            if isinstance(auth_result, JSONResponse):
                return auth_result
            
            user_auth = auth_result
            kwargs["user_auth"] = user_auth

            user_roles = set(user_auth.get("roles", []))
            user_permissions = set(user_auth.get("permisos", []))

            if required_roles:
                if not user_roles.intersection(required_roles):
                    return self.return_json(
                        est=False,
                        ico="error",
                        msg="No tiene el rol necesario para acceder a este recurso.",
                        status_code=403
                    )
                    
            if required_permissions:
                if "admin.full_access" not in user_permissions:
                    if not set(required_permissions).issubset(user_permissions):
                        return self.return_json(
                            est=False,
                            ico="error",
                            msg="No tiene los permisos necesarios para esta acción.",
                            status_code=403
                        )

        # 4. Validar body si hay schema
        if schema:
            validation_result = await self.validate_body(request, schema)
            if isinstance(validation_result, JSONResponse):
                return validation_result

        return await self.execute(
            handler_func,
            method=method,
            request=request,
            **kwargs
        )
    

class ValidadorRutasInteligentes(APIRouter):
    """
    Router inteligente orientado a casos de uso.
    - Valida body con Pydantic si se define
    - Ejecuta el caso de uso a través del handler base
    """

    def add_use_case(
        self,
        path: str,
        method: str,
        handler_instance: BaseUseCaseHandler,
        handler_method: str,
        schema: Optional[Type[BaseModel]] = None,
        name: Optional[str] = None,
        protected: bool = False,
        required_roles: Optional[List[str]] = None,
        required_permissions: Optional[List[str]] = None
    ):
        async def endpoint(request: Request):           
            path_params = dict(request.path_params)
            query_params = dict(request.query_params)
            kwargs = {**path_params, **query_params}

            func = getattr(handler_instance, handler_method)

            return await handler_instance.handle_request(
                request=request,
                handler_func=func,
                schema=schema,
                method=method,
                protected=protected,
                required_roles=required_roles,
                required_permissions=required_permissions,
                **kwargs
            )

        self.add_api_route(
            path,
            endpoint,
            methods=[method.upper()],
            name=name or handler_method,
        )

        
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))