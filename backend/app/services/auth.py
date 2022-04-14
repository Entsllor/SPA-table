from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app import models
from app.crud import Users
from app.utils import exceptions
from app.utils.options import GetOneOptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def authorize_by_username_and_password(username: str, password: str) -> models.User:
    user = await Users.get_by_username(username=username)
    if not user or not user.password_match(plain_password=password):
        raise exceptions.IncorrectLoginOrPassword
    return user


async def get_user_by_access_token(token_body=Depends(oauth2_scheme), only_active=True) -> models.User:
    try:
        access_token = models.AccessToken(body=token_body)
        access_token.validate()
        user_id = access_token.user_id
        user = await Users.get_by_id(user_id=user_id, options=GetOneOptions(raise_if_none=True))
        if only_active and not user.is_active:
            raise exceptions.InactiveUser
    except JWTError:
        raise exceptions.CredentialsException
    except exceptions.InstanceNotFound:
        raise exceptions.UserNotFoundError
    return user
