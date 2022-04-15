import asyncio
from asyncio import AbstractEventLoop

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from app.core.database import create_db_engine, Base, db_context
from app.core.settings import settings
from app.utils.dependencies import get_db
from app import models, crud
from app.crud import Users, AccessTokens, RefreshTokens
from app.schemas.users import UserCreate
from app.schemas.tokens import AuthTokensBodies

from app.main import app

DEFAULT_USER_PASS = "SomeUserPassword"
DEFAULT_USER_EMAIL = "defaultUser@example.com"
DEFAULT_USER_NAME = "SomeUserName"
USER_CREATE_DATA = UserCreate(username=DEFAULT_USER_NAME, password=DEFAULT_USER_PASS, email=DEFAULT_USER_EMAIL)


def auth_header(token: str | models.AccessToken) -> dict:
    if not isinstance(token, str):
        token = token.body
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_engine(event_loop) -> AsyncConnection:
    engine = create_db_engine(settings.TEST_DB_URL)
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield conn
        await conn.run_sync(Base.metadata.drop_all)
    engine.dispose()


@pytest.fixture(scope="function")
def db(db_engine, event_loop: AbstractEventLoop) -> AsyncSession:
    session = AsyncSession(bind=db_engine)
    try:
        db_context.set(session)
        yield session
    finally:
        db_context.set(None)
        event_loop.run_until_complete(session.rollback())
        event_loop.run_until_complete(session.close())


@pytest.fixture(scope="function")
async def client(db) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def default_user(db) -> models.User:
    yield await Users.create(**USER_CREATE_DATA.dict())


@pytest.fixture(scope='function')
async def access_token(default_user) -> models.AccessToken:
    yield await AccessTokens.create(user_id=default_user.id)


@pytest.fixture(scope="function")
async def token_pair(access_token, client) -> AuthTokensBodies:
    refresh_token = await RefreshTokens.create(user_id=access_token.user_id)
    yield AuthTokensBodies(access_token=access_token.body, refresh_token=refresh_token.body)


@pytest.fixture(scope="function")
async def default_table_row(db) -> models.TableRow:
    yield await crud.TableRows.create("default_table_row", quantity=5, distance=10)


@pytest.fixture(scope="function")
async def table(db) -> [models.TableRow]:
    yield [
        await crud.TableRows.create("row_1", quantity=1, distance=1),
        await crud.TableRows.create("row_2", quantity=2, distance=2),
        await crud.TableRows.create("row_3", quantity=3, distance=3),
    ]
