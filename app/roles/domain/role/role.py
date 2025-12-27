from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Role:
    name: str
    description: Optional[str] = None
    id: Optional[int] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class UserRole:
    user_id: Optional[int] = None
    role_id: Optional[int] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
@dataclass
class RolePermission:
    role_id: Optional[int] = None
    permission_id: Optional[int] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None    

