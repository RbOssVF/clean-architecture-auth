from dataclasses import asdict
from typing import Optional, List, Tuple
from sqlmodel import Session, select

from app.users.application.user_dtos import UserWithRolesDTO
from ..domain.user import User
from ..domain.user_repository import UserRepository
from .user_model import User as UserModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_user: Optional[UserModel]) -> Optional[User]:
        return User(**db_user.model_dump()) if db_user else None

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._to_domain(self.session.get(UserModel, user_id))

    def get_by_email(self, email: str) -> Optional[User]:
        return self._to_domain(self.session.exec(select(UserModel).where(UserModel.email == email)).first())

    def get_by_email_except_id(self, email: str, user_id: int) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email, UserModel.id != user_id)
        return self._to_domain(self.session.exec(stmt).first())

    def save(self, user: User) -> User:
        db_user = UserModel(**asdict(user))
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return self._to_domain(db_user)

    def update(self, user: User) -> User:
        db_user = self.session.get(UserModel, user.id)
        if not db_user: return None
        for key, val in asdict(user).items():
            if val is not None: setattr(db_user, key, val)
        self.session.commit()
        self.session.refresh(db_user)
        return self._to_domain(db_user)