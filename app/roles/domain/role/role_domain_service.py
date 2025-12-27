
from .role_repository import RoleRepositoryDomain, UserRoleRepositoryDomain, RolePermissionRepositoryDomain
from .role import Role, UserRole, RolePermission
from ..exceptions import CustomException

class RoleDomainService:
    def __init__(self, repo: RoleRepositoryDomain):
        self.repo = repo
    
    def create_role(self, role: Role) -> Role:
        if self.repo.get_by_name(role.name):
            raise CustomException("El role ya existe")
        return self.repo.save(role)


class UserRoleDomainService:
    def __init__(self, repo: UserRoleRepositoryDomain):
        self.repo = repo
    
    def add_user_role(self, user_role: UserRole) -> UserRole:
        existing = self.repo.get_by_role_user_id(user_role.role_id, user_role.user_id)
        if existing:
            return existing
        return self.repo.add_user_role(user_role)


class RolePermissionDomainService:
    def __init__(self, repo: RolePermissionRepositoryDomain):
        self.repo = repo
    
    def add_role_permission(self, role_permission: RolePermission) -> RolePermission:
        existing = self.repo.get_by_role_permission_id(role_permission.role_id, role_permission.permission_id)
        if existing:
            return existing
        return self.repo.add_role_permission(role_permission)
        