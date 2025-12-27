from sqlmodel import Field, Relationship
from typing import Optional, List
from shared.base import BaseModel
from app.roles.infrastructure.role_model import Role, UserRole

class User(BaseModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, max_length=100, unique=True)
    password: str = Field(nullable=False, max_length=250)
    is_active: bool = Field(default=True)

    roles: List[Role] = Relationship(
        back_populates="users",
        link_model=UserRole
    )
    

