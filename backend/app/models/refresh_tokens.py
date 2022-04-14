import time

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"
    body = Column(String(length=63), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="refresh_tokens")
    expire_at = Column(Integer, index=True)  # Unix time

    @property
    def is_active(self):
        return time.time() < self.expire_at
