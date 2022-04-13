from app.core.database import async_session, AsyncSession, db_context


async def get_db() -> AsyncSession:
    """Open new db session and then save this session object
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
