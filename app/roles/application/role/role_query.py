from sqlmodel import Session, select
from .role_dtos import RoleWithPermissionsDTO
from ...infrastructure.role_model import Role as RoleModel

class GetRolesWithPermissionsQuery:
    def __init__(self, session: Session):
        self.session = session
        
    def execute(self) -> list[RoleWithPermissionsDTO]:
        roles = self.session.exec(select(RoleModel)).all()
        result = []

        for role in roles:
            result.append(
                RoleWithPermissionsDTO(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    permissions=[p for p in role.permissions]
                )
            )

        return result