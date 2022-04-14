import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

from .core.settings import settings
from .utils import dependencies, exceptions
from .routers import users, auth, table_rows

app = FastAPI(dependencies=[Depends(dependencies.get_db)])
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(table_rows.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(exceptions.BaseAppException)
async def app_exception_handler(request, exc: exceptions.BaseAppException):
    return await http_exception_handler(request, exc.as_http)


if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
