from pydantic import BaseSettings

from pathlib import Path

BASE_PATH = Path(__file__).parent.parent


class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    LOG_LEVEL: str = "debug"
    DB_URL: str = f"sqlite+aiosqlite:///{BASE_PATH}/db.sqlite3"
    TEST_DB_URL: str = f"sqlite+aiosqlite:///{BASE_PATH}/test_db.sqlite3"
    JWT_ALGORITHM: str = "HS256"
    SECRET_KEY: str = "YOUR-SECRET_KEY"  # should delete default value
    ALLOWED_ORIGINS: list = ["https://localhost:3000", "http://localhost:3000"]
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 20
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30
    HASHING_SCHEMAS: list = ["bcrypt"]

    class Config:
        case_sensitive = True
        env_file = BASE_PATH.joinpath('.env')
        env_prefix = "APP_"


settings = Settings()
