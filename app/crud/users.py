from typing import Optional
from sqlalchemy.orm.session import Session

from app.core.auth import verify_password
from .base import CRUDBase

from app.models import User
from app.schemas.users import UserCreateSchema, UserUpdateSchema


class CRUDUser(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    def get_by_email(self, database: Session, *, email: str) -> Optional[User]:
        return database.query(User).filter(User.email == email).first()

    def authenticate(self, database: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(database=database, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

user = CRUDUser(User)
