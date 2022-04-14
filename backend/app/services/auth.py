from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app import models
from app.crud import Users, AccessTokens, RefreshTokens
from app.utils import exceptions
from app.utils.options import GetOneOptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def authorize_by_username_and_password(username: str, password: str) -> models.User:
    user = await Users.get_one(username=username)
    if not user or not user.password_match(plain_password=password):
        raise exceptions.IncorrectLoginOrPassword
    return user


async def get_user_by_access_token(token_body=Depends(oauth2_scheme), only_active=True) -> models.User:
    try:
        access_token = models.AccessToken(body=token_body)
        access_token.validate()
        user_id = access_token.user_id
        user = await Users.get_one(id=user_id, _options=GetOneOptions(raise_if_none=True))
        if only_active and not user.is_active:
            raise exceptions.InactiveUser
    except JWTError:
        raise exceptions.CredentialsException
    except exceptions.InstanceNotFound:
        raise exceptions.UserNotFoundError
    return user


async def create_auth_token_pair(user_id: int) -> tuple[models.AccessToken, models.RefreshToken]:
    access_token = await AccessTokens.create(user_id)
    refresh_token = await RefreshTokens.create(user_id)
    return access_token, refresh_token


async def revoke_tokens(user_id: int, refresh_token_body: str) -> tuple[models.AccessToken, models.RefreshToken]:
    try:
        await RefreshTokens.get_valid_token(user_id=user_id, body=refresh_token_body)
    except (JWTError, exceptions.InstanceNotFound):
        raise exceptions.CredentialsException
    return await create_auth_token_pair(user_id)
