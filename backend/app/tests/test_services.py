import pytest

from app import crud, models
from app.crud import RefreshTokens, AccessTokens
from app.crud.base import update_instance
from app.services.auth import get_user_by_access_token, revoke_tokens, authorize_by_username_and_password
from app.tests.conftest import DEFAULT_USER_PASS
from app.utils import exceptions


@pytest.mark.asyncio
async def test_get_user_by_access_token(token_pair, default_user):
    found_user = await get_user_by_access_token(token_pair.access_token)
    assert found_user.id == default_user.id
    assert isinstance(found_user, models.User)


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_invalid_token(token_pair, default_user):
    with pytest.raises(exceptions.CredentialsException):
        await get_user_by_access_token(token_pair.access_token + "_invalid")


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_user_not_exist(db, token_pair, default_user):
    await db.delete(default_user)
    with pytest.raises(exceptions.UserNotFoundError):
        await get_user_by_access_token(token_pair.access_token)


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_token_expired(default_user):
    new_token = await crud.AccessTokens.create(default_user.id, expire_delta=-100)
    with pytest.raises(exceptions.CredentialsException):
        await get_user_by_access_token(token_body=new_token.body)


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_user_is_not_active(default_user, token_pair):
    await update_instance(default_user, is_active=False)
    with pytest.raises(exceptions.InactiveUser):
        await get_user_by_access_token(token_body=token_pair.access_token)


@pytest.mark.asyncio
async def test_revoke_tokens(default_user):
    refresh_token = await RefreshTokens.create(user_id=default_user.id)
    access_token = await AccessTokens.create(user_id=default_user.id)
    new_access_token, new_refresh_token = await revoke_tokens(
        user_id=default_user.id,
        refresh_token_body=refresh_token.body
    )
    assert isinstance(new_access_token, models.AccessToken)
    assert isinstance(new_refresh_token, models.RefreshToken)
    assert refresh_token.body != new_refresh_token.body
    assert access_token.body != new_access_token.body


@pytest.mark.asyncio
async def test_failed_revoke_tokens_invalid_refresh_token(default_user):
    refresh_token = await RefreshTokens.create(user_id=default_user.id)
    with pytest.raises(exceptions.CredentialsException):
        await revoke_tokens(user_id=default_user.id, refresh_token_body=refresh_token.body + "_invalid")


@pytest.mark.asyncio
async def test_failed_revoke_tokens_expired_refresh_token(default_user):
    refresh_token = await RefreshTokens.create(user_id=default_user.id, expire_delta=-100)
    with pytest.raises(exceptions.CredentialsException):
        await revoke_tokens(user_id=default_user.id, refresh_token_body=refresh_token.body)


@pytest.mark.asyncio
async def test_failed_revoke_tokens_if_wrong_user_id(default_user):
    refresh_token = await RefreshTokens.create(user_id=default_user.id)
    with pytest.raises(exceptions.CredentialsException):
        await revoke_tokens(user_id=99999999, refresh_token_body=refresh_token.body)


@pytest.mark.asyncio
async def test_authorize_by_username_and_password(default_user):
    user = await authorize_by_username_and_password(default_user.username, DEFAULT_USER_PASS)
    assert isinstance(user, models.User)
    assert user.id == default_user.id


@pytest.mark.asyncio
async def test_failed_authorize_by_username_and_password_with_incorrect_password(default_user):
    with pytest.raises(exceptions.IncorrectLoginOrPassword):
        await authorize_by_username_and_password(default_user.username, DEFAULT_USER_PASS + "_invalid")


@pytest.mark.asyncio
async def test_failed_authorize_by_username_and_password_with_incorrect_username(default_user):
    with pytest.raises(exceptions.IncorrectLoginOrPassword):
        await authorize_by_username_and_password("another" + default_user.username, DEFAULT_USER_PASS)
