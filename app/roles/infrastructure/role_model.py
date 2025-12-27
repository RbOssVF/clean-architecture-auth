from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from shared.base import BaseModel

class UserRole(BaseModel, table=True):
    __tablename__ = "user_roles"

    user_id: Optional[int] = Field(
        default=None,
        foreign_key="users.id",
        primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None,
        foreign_key="roles.id",
        primary_key=True
    )
    

class RolePermission(BaseModel, table=True):
    __tablename__ = "role_permissions"

    role_id: Optional[int] = Field(
        default=None,
        foreign_key="roles.id",
        primary_key=True
    )
    permission_id: Optional[int] = Field(
        default=None,
        foreign_key="permissions.id",
        primary_key=True
    )
    
class Permission(BaseModel, table=True):
    __tablename__ = "permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=100)
    description: Optional[str] = Field(nullable=True)

    roles: List["Role"] = Relationship(
        back_populates="permissions",
        link_model=RolePermission
    )

class Role(BaseModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=100)
    description: Optional[str] = Field(nullable=True)

    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=UserRole
    )
    permissions: List[Permission] = Relationship(
        back_populates="roles",
        link_model=RolePermission
    )