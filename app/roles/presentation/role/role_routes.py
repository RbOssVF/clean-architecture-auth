from shared.base import ValidadorRutasInteligentes
from ...application.role.role_service import RoleService, UserRoleService, RolePermissionService
from .schemas import *

router = ValidadorRutasInteligentes(prefix="/roles", tags=["Roles"])
role_service = RoleService()
user_role_service = UserRoleService()
role_permission_service = RolePermissionService()

router.add_use_case(
    path="/",
    method="GET",
    handler_instance=role_service,
    handler_method="get_all",
    schema=None,
    name="get_all"
)

router.add_use_case(
    path="/",
    method="POST",
    handler_instance=role_service,
    handler_method="create_role",
    schema=CreateRoleSchema,
    name="create_role"
)

router.add_use_case(
    path="/users",
    method="POST",
    handler_instance=user_role_service,
    handler_method="add_role_to_user",
    schema=AddRoleToUserSchema,
    name="add_role_to_user"
)

router.add_use_case(
    path="/permissions",
    method="POST",
    handler_instance=role_permission_service,
    handler_method="add_permission_to_role",
    schema=AddPermissionToRoleSchema,
    name="add_permission_to_role"
)