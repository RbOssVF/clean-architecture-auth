from .permission_repository import PermissionRepositoryDomain
from .permission import Permission
from ..exceptions import CustomException

class PermissionDomainService:
    def __init__(self, repo: PermissionRepositoryDomain):
        self.repo = repo
    
    def create_permission(self, permission: Permission) -> Permission:
        if self.repo.get_by_name(permission.name):
            raise CustomException("El permiso ya existe")
        return self.repo.save(permission)