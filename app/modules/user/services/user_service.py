import bcrypt
from sqlalchemy.orm import Session
from app.modules.user.repositories import user_repository
from app.modules.user.models.user_model import User

DEFAULT_EMAIL = "cerrado@admin.com"
DEFAULT_PASSWORD = "cerrado123"


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def get_or_create_default_user(db: Session) -> User:
    user = user_repository.get_by_email(db, DEFAULT_EMAIL)
    if not user:
        user = user_repository.create_user(db, DEFAULT_EMAIL, hash_password(DEFAULT_PASSWORD))
    return user


def get_default_user(db: Session) -> User | None:
    return user_repository.get_by_email(db, DEFAULT_EMAIL)
