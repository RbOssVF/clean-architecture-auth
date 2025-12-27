from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class PermissionDTO:
    id: int
    name: str
    description: Optional[str]
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class RoleWithPermissionsDTO:
    id: int
    name: str
    permissions: List[PermissionDTO]
    description: Optional[str]
    
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None