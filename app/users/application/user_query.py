from collections import defaultdict
from sqlmodel import Session, select
from .user_dtos import UserWithRolesDTO, RolesDTO
from app.roles.application.role.role_dtos import PermissionDTO
from ..infrastructure.user_model import User as UserModel
from app.roles.infrastructure.role_model import Role as RoleModel, UserRole as UserRoleModel, RolePermission as RolePermissionModel, Permission as PermissionModel


class GetUsersWithRolesService:
    def __init__(self, session: Session):
        self.session = session

    def execute(self) -> list[UserWithRolesDTO]:
        users = self.session.exec(select(UserModel)).all()

        # Roles por usuario
        stmt = (
            select(
                UserRoleModel.user_id,
                RoleModel.id,
                RoleModel.name,
                RoleModel.description
            )
            .join(RoleModel, RoleModel.id == UserRoleModel.role_id)
        )
        rows = self.session.exec(stmt).all()

        # Permisos por rol
        stmt = (
            select(
                RolePermissionModel.role_id,
                PermissionModel.id,
                PermissionModel.name,
                PermissionModel.description
            )
            .join(PermissionModel, PermissionModel.id == RolePermissionModel.permission_id)
        )
        permissions = self.session.exec(stmt).all()

        roles_permissions = defaultdict(list)
        for role_id, perm_id, perm_name, perm_desc in permissions:
            roles_permissions[role_id].append(
                PermissionDTO(
                    id=perm_id,
                    name=perm_name,
                    description=perm_desc
                )
            )

        user_roles = defaultdict(list)
        for user_id, role_id, role_name, role_desc in rows:
            user_roles[user_id].append(
                RolesDTO(
                    id=role_id,
                    name=role_name,
                    description=role_desc,
                    permissions=roles_permissions.get(role_id, [])
                )
            )

        result = []
        for user in users:
            result.append(
                UserWithRolesDTO(
                    id=user.id,
                    email=user.email,
                    roles=user_roles.get(user.id, [])
                )
            )

        return result
    
class GetUserWithRolesService:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, user_id: int) -> UserWithRolesDTO:
        user = self.session.get(UserModel, user_id)

        stmt = (
            select(
                UserRoleModel.user_id,
                RoleModel.id,
                RoleModel.name,
                RoleModel.description
            )
            .join(RoleModel, RoleModel.id == UserRoleModel.role_id)
        )
        rows = self.session.exec(stmt).all()    

        stmt = (
            select(
                RolePermissionModel.role_id,
                PermissionModel.id,
                PermissionModel.name,
                PermissionModel.description
            )
            .join(PermissionModel, PermissionModel.id == RolePermissionModel.permission_id)
        )
        permissions = self.session.exec(stmt).all()
        
        roles_permissions = defaultdict(list)
        for role_id, perm_id, perm_name, perm_desc in permissions:
            roles_permissions[role_id].append(
                PermissionDTO(
                    id=perm_id,
                    name=perm_name,
                    description=perm_desc
                )
            )

        user_roles = defaultdict(list)
        for user_id, role_id, role_name, role_desc in rows:
            user_roles[user_id].append(
                RolesDTO(
                    id=role_id,
                    name=role_name,
                    description=role_desc,
                    permissions=roles_permissions.get(role_id, [])
                )
            )

        return UserWithRolesDTO(
            id=user.id,
            email=user.email,
            roles=user_roles.get(user.id, []),
        )