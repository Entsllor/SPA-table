from fastapi import Depends
from fastapi.params import Query

from app import models
from app.core.database import async_session, AsyncSession, db_context
from app.services.auth import oauth2_scheme, get_user_by_access_token
from app.utils.options import GetManyOptions


async def get_db() -> AsyncSession:
    """Open a new db session and then save this session object
    as a context variable"""
    session = async_session()
    try:
        db_context.set(session)
        yield session
    except Exception as exc:
        db_context.set(None)
        await session.rollback()
        raise exc
    else:
        await session.commit()
    finally:
        await session.close()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    return await get_user_by_access_token(token_body=token, only_active=False)


async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> models.User:
    return await get_user_by_access_token(token_body=token, only_active=True)


def get_many_options(limit: int = 100, offset: int = 0, ordering_fields: list[str] = Query(None)) -> GetManyOptions:
    return GetManyOptions(limit=limit, offset=offset, ordering_fields=ordering_fields)
