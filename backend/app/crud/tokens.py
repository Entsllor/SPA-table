import time

from jose import jwt

from app import models
from app.core.settings import settings


class AccessTokenCRUD:
    @staticmethod
    async def create_with_custom_data(data: dict = None, expire_delta: int = None) -> models.AccessToken:
        if not isinstance(data, dict):
            data = dict()
        else:
            data = data.copy()
        if expire_delta is None:
            expire_delta = settings.REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = time.time() + expire_delta
        data["exp"] = expire_at
        body = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return models.AccessToken(body=body)

    async def create(self, user_id: int, expire_delta: int = None) -> models.AccessToken:
        return await self.create_with_custom_data(data={'sub': str(user_id)}, expire_delta=expire_delta)


AccessTokens = AccessTokenCRUD()
