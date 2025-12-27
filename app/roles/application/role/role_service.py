from app.roles.infrastructure.permission.permission_repository import PermissionRepositoryImpl
from app.users.infrastructure.user_repository import UserRepositoryImpl
from shared.base import *

from ...domain.role.role import Role, UserRole, RolePermission
from ...domain.role.role_domain_service import RoleDomainService, UserRoleDomainService, RolePermissionDomainService
from ...domain.exceptions import CustomException

from ...infrastructure.role.role_repository import RoleRepositoryImpl, UserRoleRepositoryImpl, RolePermissionRepositoryImpl
from ...presentation.role.schemas import *

from .role_query import GetRolesWithPermissionsQuery

from fastapi import Request

class RoleService(BaseUseCaseHandler):
    
    async def get_all(self, request: Request):
        all_roles = GetRolesWithPermissionsQuery(self.session).execute()
        roles = []
        for r in all_roles:
            roles.append({
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "permissions_id": [p.id for p in r.permissions],
                "permissions": [{
                    "id": p.id,
                    "name": p.name,
                    "description": p.description
                } for p in r.permissions]
            })
        return self.return_json(est=True, ico="success", msg="Roles obtenidos correctamente", data=roles)
    
    async def create_role(self, request: Request):
        body: CreateRoleSchema = request.state.body
        
        repo = RoleRepositoryImpl(self.session)
        domain_service = RoleDomainService(repo)
        try:
            role = domain_service.create_role(Role(name=body.name, description=body.description))
        except CustomException as e:
            return self.return_json(est=False, ico="warning", msg=str(e), status_code=409)
   
        return self.return_json(
            est=True, ico="success", 
            msg="Role creado correctamente", data={
                "id": role.id,
                "name": role.name,
                "description": role.description
            }
        )
        
class UserRoleService(BaseUseCaseHandler):
    
    async def add_role_to_user(self, request: Request):
        body: AddRoleToUserSchema = request.state.body
        role_ids = body.roles_id
        
        repo = UserRoleRepositoryImpl(self.session)
        repo_role = RoleRepositoryImpl(self.session)
        repo_user = UserRepositoryImpl(self.session)
        
        domain_service = UserRoleDomainService(repo)
       
        user = repo_user.get_by_id(body.user_id)
        if not user:
            raise CustomException(f"El user con id {body.user_id} no existe")
       
        for role_id in role_ids:            
            role = repo_role.get_by_id(role_id)
            if not role or not user:
                raise CustomException(f"El rol con id {role_id} no existe")
        
        repo.delete_all_by_user_id(body.user_id)
        for role_id in role_ids:
            domain_service.add_user_role(
                UserRole(
                    user_id=body.user_id,
                    role_id=role_id
                )
            )

        return self.return_json(
            est=True,
            ico="success",
            msg="Roles asignados correctamente"
        )

class RolePermissionService(BaseUseCaseHandler):
    
    async def add_permission_to_role(self, request: Request):
        body: AddPermissionToRoleSchema = request.state.body
        permission_ids = body.permissions_id
        
        repo = RolePermissionRepositoryImpl(self.session)
        repo_permission = PermissionRepositoryImpl(self.session)
        repo_role = RoleRepositoryImpl(self.session)
        
        domain_service = RolePermissionDomainService(repo)
        
        role = repo_role.get_by_id(body.role_id)
        if not role:
            raise CustomException(f"El role con id {body.role_id} no existe")
        
        for permission_id in permission_ids:            
            permission = repo_permission.get_by_id(permission_id)
            if not permission or not role:
                raise CustomException(f"La permission con id {permission_id} no existe")
        
        repo.delete_all_by_role_id(body.role_id)
        for permission_id in permission_ids:
            domain_service.add_role_permission(
                RolePermission(
                    role_id=body.role_id,
                    permission_id=permission_id
                )
            )

        return self.return_json(
            est=True,
            ico="success",
            msg="Permisos asignados correctamente"
        )