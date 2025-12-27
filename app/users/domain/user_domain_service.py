from app.users.domain.user_repository import UserRepository
from app.users.domain.user import User
from app.users.domain.exceptions import UserAlreadyExistsError

class UserDomainService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        existing = self.user_repository.get_by_email(user.email)
        if existing:
            raise UserAlreadyExistsError("El email del usuario ya existe")

        return self.user_repository.save(user)
    
    def update_user(self, user: User) -> User:
        existing = self.user_repository.get_by_id(user.id)
        existing_email = self.user_repository.get_by_email_except_id(user.email, user.id)
        if not existing:
            raise UserAlreadyExistsError("El usuario no existe")

        if existing_email:
            raise UserAlreadyExistsError("El email del usuario ya existe")

        return self.user_repository.update(user)