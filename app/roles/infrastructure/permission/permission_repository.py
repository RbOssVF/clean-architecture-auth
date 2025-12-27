from dataclasses import asdict
from typing import Optional
from sqlmodel import Session, select

from ...domain.permission.permission import Permission
from ...domain.permission.permission_repository import PermissionRepositoryDomain
from ..role_model import Permission as PermissionModel

class PermissionRepositoryImpl(PermissionRepositoryDomain):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_permission: Optional[PermissionModel]) -> Optional[Permission]:
        return Permission(**db_permission.model_dump()) if db_permission else None
    
    def get_by_id(self, permission_id: int) -> Optional[Permission]:
        return self._to_domain(self.session.get(PermissionModel, permission_id))
    
    def get_by_name(self, name: str) -> Optional[Permission]:
        stmt = select(PermissionModel).where(PermissionModel.name == name)
        return self._to_domain(self.session.exec(stmt).first())
    
    def get_all(self) -> list[Permission]:
        return [self._to_domain(permission) for permission in self.session.exec(select(PermissionModel))]
    
    def save(self, permission: Permission) -> Permission:
        db_permission = PermissionModel(**asdict(permission))
        self.session.add(db_permission)
        self.session.commit()
        self.session.refresh(db_permission)
        return self._to_domain(db_permission)
