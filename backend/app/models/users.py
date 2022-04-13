from datetime import datetime

from sqlalchemy import Column, Integer, Text, String, DateTime, Boolean

from app.core.database import Base
from app.utils.passwords import verify_password


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, index=True, unique=True)
    hashed_password = Column(String(length=255))
    created_at = Column(DateTime, index=True, default=datetime.now)
    is_active = Column(Boolean, default=True)
    email = Column(String(length=255))

    def password_match(self, plain_password: str) -> bool:
        return verify_password(plain_password=plain_password, hashed_password=self.hashed_password)
