from ..domain.exceptions import UserAlreadyExistsError
from ..domain.user_domain_service import UserDomainService
from ..domain.user import User
from shared.base import *
from ..infrastructure.user_repository import UserRepositoryImpl
from fastapi import Request
from ..presentation.schemas import *
from .user_dtos import UserWithRolesDTO
from .user_query import GetUsersWithRolesService, GetUserWithRolesService

class UserService(BaseUseCaseHandler):
    
    async def get_user_by_id(self, request: Request, **kwargs):
        """
        Caso de uso para obtener un usuario por su ID.
        """
        repo = UserRepositoryImpl(self.session)
        print(request.state.usuario)
        id_user = kwargs["id_user"] if kwargs["id_user"] not in [0, "0"] else request.state.usuario["id"]
        user = GetUserWithRolesService(self.session).execute(id_user)
        
        if not user:
            return self.return_json(
                est=False,
                ico="warning",
                msg="Usuario no encontrado",
                status_code=404
            )
        
        datos_user = {
            "id": user.id,
            "email": user.email,
            "roles": [{"id": r.id, "name": r.name, "permisos": [{"id": p.id, "name": p.name} for p in r.permissions]} for r in user.roles]
        }

        return self.return_json(
            est=True,
            ico="success",
            msg="Usuario obtenido correctamente",
            data=datos_user
        )
    
    async def get_all_users_with_roles(self, request: Request):
        """
        Lista todos los usuarios con sus respectivos nombres de roles.
        """
        service = GetUsersWithRolesService(self.session)
        all_users: list[UserWithRolesDTO] = service.execute()
        users = []
        for u in all_users:
            users.append({
                "id": u.id,
                "email": u.email,
                "roles_id": [{"id": r.id, "permissions_id": [p.id for p in r.permissions]} for r in u.roles],
                "roles": [{
                    "id": r.id,
                    "name": r.name,
                    "permissions": [p.name for p in r.permissions]
                } for r in u.roles]
            })
        
        return self.return_json(
            est=True,
            ico="success",
            msg="Usuarios obtenidos correctamente",
            data=users
        )
    
    async def create_user(self, request: Request):

        body: CreateUserSchema = request.state.body

        repo = UserRepositoryImpl(self.session)
        domain_service = UserDomainService(repo)

        try:
            user = domain_service.create_user(
                User(
                    email=body.email,
                    password=hash_password(body.password)
                )
            )
        except UserAlreadyExistsError as e:
            return self.return_json(
                est=False,
                ico="warning",
                msg=str(e),
                status_code=409
            )

        return self.return_json(
            est=True,
            ico="success",
            msg="Usuario creado correctamente",
            data={
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active
            },
            status_code=201
        )

    async def update_user(self, request: Request, **kwargs):
        body: UpdateUserSchema = request.state.body
        id_user = kwargs["id_user"]

        repo = UserRepositoryImpl(self.session)
        domain_service = UserDomainService(repo)

        try:
            password_hash = hash_password(body.password) if body.password else None
            user = domain_service.update_user(
                User(
                    id=id_user,
                    email=body.email,
                    password=password_hash
                )
            )
        except UserAlreadyExistsError as e:
            return self.return_json(
                est=False,
                ico="warning",
                msg=str(e),
                status_code=409
            )

        return self.return_json(
            est=True,
            ico="success",
            msg="Usuario actualizado correctamente",
            data={
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active
            },
            status_code=200
        )
    