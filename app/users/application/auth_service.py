from .user_query import GetUserWithRolesService
from .user_dtos import UserWithRolesDTO
from shared.base import BaseUseCaseHandler, check_password
from ..infrastructure.user_repository import UserRepositoryImpl
from shared.security.jwt_service import JWTService
from ..presentation.schemas import *
from fastapi import Request

class AuthService(BaseUseCaseHandler):
    async def login(self, request: Request, **kwargs):
        body: LoginSchema = request.state.body # Asumiendo que se usa un schema de Login
        repo = UserRepositoryImpl(self.session)
        
        user = repo.get_by_email(body.email)
        if not user or not check_password(body.password, user.password):
            return self.return_json(
                est=False, ico="error", 
                msg="Credenciales inválidas.", status_code=401
            )
        
        user_roles = GetUserWithRolesService(self.session).execute(user.id)
        set_permisos = set([p.name for r in user_roles.roles for p in r.permissions])
        user_data = {"sub": str(user_roles.id), "id": user_roles.id, "email": user_roles.email, "roles": [r.name for r in user_roles.roles], "permisos": list(set_permisos)}
        access_token = JWTService.create_access_token(user_data)
        refresh_token = JWTService.create_refresh_token(user_data)
        
        return self.return_json(
            est=True, ico="success", msg="Login exitoso.",
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user_roles.id,
                    "email": user_roles.email,
                    "roles": [r.name for r in user_roles.roles]
                }
            }
        )

    async def refresh_token(self, request: Request, **kwargs):
        body: RefreshTokenSchema = request.state.body # Asumiendo que envía el refresh_token
        
        payload = JWTService.validate_token(body.refresh_token, expected_type="refresh")
        if not payload:
            return self.return_json(
                est=False, ico="error", 
                msg="Refresh token inválido o expirado.", status_code=401
            )
        
        # Generar nuevo access token con roles y permisos actualizados
        user_id = int(payload["sub"])
        user_roles = GetUserWithRolesService(self.session).execute(user_id)
        set_permisos = set([p.name for r in user_roles.roles for p in r.permissions])
        
        user_data = {
            "sub": str(user_roles.id), 
            "id": user_roles.id, 
            "email": user_roles.email, 
            "roles": [r.name for r in user_roles.roles], 
            "permisos": list(set_permisos)
        }
        
        new_access_token = JWTService.create_access_token(user_data)

        
        return self.return_json(
            est=True, ico="success", msg="Token renovado.",
            data={"access_token": new_access_token}
        )
