from shared.base import ValidadorRutasInteligentes
from ...application.permission.permission_service import PermissionService
from .schemas import *

router = ValidadorRutasInteligentes(prefix="/permissions", tags=["Permissions"])
permission_service = PermissionService()

router.add_use_case(
    path="/",
    method="GET",
    handler_instance=permission_service,
    handler_method="get_all",
    schema=None,
    name="get_all"
)

router.add_use_case(
    path="/",
    method="POST",
    handler_instance=permission_service,
    handler_method="create_permission",
    schema=CreatePermissionSchema,
    name="create_permission"
)