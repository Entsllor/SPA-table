import contextvars

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from .settings import settings


def create_db_engine(db_url):
    connect_args = {}
    if 'sqlite' in db_url:
        connect_args["check_same_thread"] = False
    return create_async_engine(
        url=db_url,
        future=True,
        echo=True,
        connect_args=connect_args
    )


engine = create_db_engine(settings.DB_URL)
async_session = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine, class_=AsyncSession)
Base = declarative_base()
db_context = contextvars.ContextVar('db_context', default=None)


def get_session() -> AsyncSession | None:
    return db_context.get()
