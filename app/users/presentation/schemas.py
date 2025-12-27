from pydantic import BaseModel
from typing import Optional

class CreateUserSchema(BaseModel):
    email: str
    password: str
    
class UpdateUserSchema(BaseModel):
    email: str
    password: Optional[str] = None

class LoginSchema(BaseModel):
    email: str
    password: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str