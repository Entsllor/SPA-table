from pydantic import BaseModel


class AccessTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthTokensBodies(AccessTokenOut):
    refresh_token: str
