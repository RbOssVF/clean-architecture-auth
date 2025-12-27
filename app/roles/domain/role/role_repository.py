from abc import ABC, abstractmethod
from typing import Optional

from .role import Role, UserRole, RolePermission

class RoleRepositoryDomain(ABC):
    @abstractmethod
    def get_by_id(self, role_id: int) -> Optional[Role]:
        pass
    
    @abstractmethod
    def save(self, role: Role) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[Role]:
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Role]:
        pass

class UserRoleRepositoryDomain(ABC):

    @abstractmethod
    def delete_all_by_user_id(self, user_id: int) -> None:
        pass

    @abstractmethod
    def add_user_role(self, user_role: UserRole) -> UserRole:
        pass
    
    @abstractmethod
    def get_by_role_user_id(self, role_id: int, user_id: int) -> Optional[UserRole]:
        pass

class RolePermissionRepositoryDomain(ABC):
    @abstractmethod
    def delete_all_by_role_id(self, role_id: int) -> None:
        pass
    
    @abstractmethod
    def add_role_permission(self, role_permission: RolePermission) -> RolePermission:
        pass

    @abstractmethod
    def get_by_role_permission_id(self, role_id: int, permission_id: int) -> Optional[RolePermission]:
        pass