from shared.base import ValidadorRutasInteligentes
from app.users.application.user_service import UserService
from app.users.presentation.schemas import *

from app.users.application.auth_service import AuthService

router = ValidadorRutasInteligentes(prefix="/users", tags=["Users"])
user_service = UserService()
auth_service = AuthService()

# Rutas de Autenticación
router.add_use_case(
    path="/login",
    method="POST",
    handler_instance=auth_service,
    handler_method="login",
    schema=LoginSchema,
    name="login"
)

router.add_use_case(
    path="/refresh",
    method="POST",
    handler_instance=auth_service,
    handler_method="refresh_token",
    schema=RefreshTokenSchema,
    name="refresh"
)

router.add_use_case(
    path="/all",
    method="GET",
    handler_instance=user_service,
    handler_method="get_all_users_with_roles",
    name="get_all_users_with_roles"
)

# Ejemplo de GET (Protegido)
router.add_use_case(
    path="/{id_user}",
    method="GET",
    handler_instance=user_service,
    handler_method="get_user_by_id",
    name="get_user",
    protected=True,
    required_roles=["Administrador"]
)

# Ejemplo de POST
router.add_use_case(
    path="/",
    method="POST",
    handler_instance=user_service,
    handler_method="create_user",
    name="post_user",
    schema=CreateUserSchema
)

# Ejemplo de PUT
router.add_use_case(
    path="/{id_user}",
    method="PUT",
    handler_instance=user_service,
    handler_method="update_user",
    name="put_user",
    schema=UpdateUserSchema
)
