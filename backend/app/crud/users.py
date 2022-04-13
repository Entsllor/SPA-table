from sqlalchemy import or_

from .. import models
from ..utils import exceptions
from ..utils.passwords import get_password_hash
from .base import create_instance, BaseCrudDB, get_one_by_query


class UsersCRUD(BaseCrudDB):
    model = models.User

    async def get_one_by_username_or_email(self, username: str = None, email: str = None) -> models.User:
        query = self._select.where(or_(self.model.username == username, self.model.email == email))
        return await get_one_by_query(query)

    async def create(self, username: str, email: str, password: str) -> models.User:
        hashed_password = get_password_hash(password)
        user_with_same_username_or_password = await self.get_one_by_username_or_email(username, email)
        if user_with_same_username_or_password:
            if user_with_same_username_or_password.username == username:
                raise exceptions.ExpectedUniqueUsername
            raise exceptions.ExpectedUniqueUsername
        else:
            user = models.User(username=username, hashed_password=hashed_password, email=email)
            return await create_instance(instance=user)


Users = UsersCRUD()
