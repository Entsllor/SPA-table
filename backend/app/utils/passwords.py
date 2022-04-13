from passlib.context import CryptContext
from app.core.settings import settings

pwd_context = CryptContext(schemes=settings.HASHING_SCHEMAS, deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)
