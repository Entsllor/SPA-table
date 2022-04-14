from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from app.core.settings import settings
from app.schemas.tokens import AccessTokenOut
from app.services import auth
from app.utils import exceptions

router = APIRouter()
LOGIN_URL = "/login/"
REVOKE_REFRESH_TOKEN_URL = "/revoke/"


@router.post(LOGIN_URL, response_model=AccessTokenOut)
async def login_by_password(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth.authorize_by_username_and_password(form_data.username, form_data.password)
    access_token, refresh_token = await auth.create_auth_token_pair(user.id)
    response.set_cookie(
        key="client_id",
        value=str(access_token.user_id),
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        path=REVOKE_REFRESH_TOKEN_URL
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token.body,
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        path=REVOKE_REFRESH_TOKEN_URL
    )
    return AccessTokenOut(access_token=access_token.body,)


@router.post(REVOKE_REFRESH_TOKEN_URL, response_model=AccessTokenOut)
async def revoke_token(response: Response, client_id: int = Cookie(None), refresh_token: str = Cookie(None)):
    access_token, refresh_token = await auth.revoke_tokens(user_id=client_id, refresh_token_body=refresh_token)
    response.set_cookie(
        key="client_id",
        value=str(access_token.user_id),
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        path=REVOKE_REFRESH_TOKEN_URL
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token.body,
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        path=REVOKE_REFRESH_TOKEN_URL
    )
    return AccessTokenOut(access_token=access_token.body)
