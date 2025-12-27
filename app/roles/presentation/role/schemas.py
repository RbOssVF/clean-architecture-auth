from pydantic import BaseModel

class CreateRoleSchema(BaseModel):
    name: str
    description: str
    
class AddRoleToUserSchema(BaseModel):
    user_id: int
    roles_id: list[int]
    
class AddPermissionToRoleSchema(BaseModel):
    role_id: int
    permissions_id: list[int]