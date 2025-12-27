from shared.base import BaseUseCaseHandler

from ...infrastructure.permission.permission_repository import PermissionRepositoryImpl

from ...domain.permission.permission_domain_service import PermissionDomainService
from ...domain.exceptions import CustomException
from ...domain.permission.permission import Permission

from ...presentation.permission.schemas import *

from fastapi import Request

class PermissionService(BaseUseCaseHandler):
    
    async def get_all(self, request: Request):
        repo = PermissionRepositoryImpl(self.session)
        all_permissions = repo.get_all()
        permissions = []
        for p in all_permissions:
            permissions.append({
                "id": p.id,
                "name": p.name,
                "description": p.description
            })
        return self.return_json(est=True, ico="success", msg="Permisos obtenidos correctamente", data=permissions)

    async def create_permission(self, request: Request):
        body: CreatePermissionSchema = request.state.body
        repo = PermissionRepositoryImpl(self.session)
        domain_service = PermissionDomainService(repo)
        try:
            permission = domain_service.create_permission(Permission(name=body.name, description=body.description))
        except CustomException as e:
            return self.return_json(est=False, ico="warning", msg=str(e), status_code=409)

        return self.return_json(
            est=True, ico="success", 
            msg="Permiso creado correctamente", data={
                "id": permission.id,
                "name": permission.name,
                "description": permission.description
            }
        )

    