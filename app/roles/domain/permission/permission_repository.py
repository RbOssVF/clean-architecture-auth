from abc import ABC, abstractmethod
from typing import Optional
from .permission import Permission

class PermissionRepositoryDomain(ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Permission]:
        pass
    
    @abstractmethod
    def get_all(self) -> list[Permission]:
        pass
    
    @abstractmethod
    def save(self, permission: Permission) -> Permission:
        pass
    
    @abstractmethod
    def get_by_id(self, permission_id: int) -> Optional[Permission]:
        pass