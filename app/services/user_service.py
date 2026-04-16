from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreate) -> UserRead:
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("User with this email already exists")

        user = self.repo.create(data)
        return UserRead.model_validate(user)

    def get_user(self, user_id: int) -> UserRead:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return UserRead.model_validate(user)
