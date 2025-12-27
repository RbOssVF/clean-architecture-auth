from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from app.roles.application.role.role_dtos import PermissionDTO

@dataclass
class RolesDTO:
    id: int
    name: str
    permissions: List[PermissionDTO]
    description: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class UserWithRolesDTO:
    id: int
    email: str
    roles: List[RolesDTO]
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
