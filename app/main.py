from fastapi import FastAPI
from app.users.presentation.user_routes import router as user_router
from app.roles.presentation.role.role_routes import router as role_router
from app.roles.presentation.permission.permission_routes import router as permission_router

app = FastAPI()

app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
