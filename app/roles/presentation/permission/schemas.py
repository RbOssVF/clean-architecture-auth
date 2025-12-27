from pydantic import BaseModel

class CreatePermissionSchema(BaseModel):
    name: str
    description: str