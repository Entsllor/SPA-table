import asyncio
from asyncio import AbstractEventLoop

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from app.core.database import create_db_engine, Base, db_context
from app.core.settings import settings
from app.main import app
from app.utils.dependencies import get_db


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
