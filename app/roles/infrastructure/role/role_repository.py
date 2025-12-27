from dataclasses import asdict
from typing import Optional
from sqlmodel import Session, select

from ...domain.role.role import Role, UserRole, RolePermission
from ...domain.role.role_repository import RoleRepositoryDomain, UserRoleRepositoryDomain, RolePermissionRepositoryDomain

from ..role_model import Role as RoleModel
from ..role_model import UserRole as UserRoleModel
from ..role_model import RolePermission as RolePermissionModel

class RoleRepositoryImpl(RoleRepositoryDomain):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_role: Optional[RoleModel]) -> Optional[Role]:
        return Role(**db_role.model_dump()) if db_role else None

    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self._to_domain(self.session.get(RoleModel, role_id))
    
    def get_by_name(self, name: str) -> Optional[Role]:
        stmt = select(RoleModel).where(RoleModel.name == name)
        return self._to_domain(self.session.exec(stmt).first())
    
    def get_all(self) -> list[Role]:
        return [self._to_domain(role) for role in self.session.exec(select(RoleModel))]
    
    def save(self, role: Role) -> Role:
        db_role = RoleModel(**asdict(role))
        self.session.add(db_role)
        self.session.commit()
        self.session.refresh(db_role)
        return self._to_domain(db_role)
    
class UserRoleRepositoryImpl(UserRoleRepositoryDomain):
    def __init__(self, session: Session):
        self.session = session
        
    def _to_domain(self, db_user_role: Optional[UserRoleModel]) -> Optional[UserRole]:
        return UserRole(**db_user_role.model_dump()) if db_user_role else None
    
    def get_by_role_user_id(self, role_id: int, user_id: int) -> Optional[UserRole]:
        stmt = select(UserRoleModel).where(
            UserRoleModel.role_id == role_id,
            UserRoleModel.user_id == user_id
        )
        return self._to_domain(self.session.exec(stmt).first())
    
    def delete_all_by_user_id(self, user_id: int) -> None:
        stmt = select(UserRoleModel).where(UserRoleModel.user_id == user_id)
        roles = self.session.exec(stmt).all()
        for r in roles:
            self.session.delete(r)
        self.session.commit()
    
    def add_user_role(self, user_role: UserRole) -> UserRole:
        db_user_role = UserRoleModel(**asdict(user_role))
        self.session.add(db_user_role)
        self.session.commit()
        self.session.refresh(db_user_role)
        return self._to_domain(db_user_role)
    
class RolePermissionRepositoryImpl(RolePermissionRepositoryDomain):
    def __init__(self, session: Session):
        self.session = session
        
    def _to_domain(self, db_role_permission: Optional[RolePermissionModel]) -> Optional[RolePermission]:
        return RolePermission(**db_role_permission.model_dump()) if db_role_permission else None
    
    def get_by_role_permission_id(self, role_id: int, permission_id: int) -> Optional[RolePermission]:
        stmt = select(RolePermissionModel).where(
            RolePermissionModel.role_id == role_id,
            RolePermissionModel.permission_id == permission_id
        )
        return self._to_domain(self.session.exec(stmt).first())
    
    def delete_all_by_role_id(self, role_id: int) -> None:
        stmt = select(RolePermissionModel).where(RolePermissionModel.role_id == role_id)
        permissions = self.session.exec(stmt).all()
        for p in permissions:
            self.session.delete(p)
        self.session.commit()
    
    def add_role_permission(self, role_permission: RolePermission) -> RolePermission:
        db_role_permission = RolePermissionModel(**asdict(role_permission))
        self.session.add(db_role_permission)
        self.session.commit()
        self.session.refresh(db_role_permission)
        return self._to_domain(db_role_permission)