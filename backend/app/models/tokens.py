import time
from typing import NamedTuple

from jose import jwt

from app.core.settings import settings

DEFAULT_VALIDATION_OPTIONS = {
    'verify_signature': True,
    'verify_aud': True,
    'verify_iat': True,
    'verify_exp': True,
    'verify_nbf': True,
    'verify_iss': True,
    'verify_sub': True,
    'verify_jti': True,
    'verify_at_hash': True,
    'require_aud': False,
    'require_iat': False,
    'require_exp': False,
    'require_nbf': False,
    'require_iss': False,
    'require_sub': False,
    'require_jti': False,
    'require_at_hash': False,
    'leeway': 0,
}

SKIP_VALIDATION = {
    'verify_signature': False,
    'verify_aud': False,
    'verify_iat': False,
    'verify_exp': False,
    'verify_nbf': False,
    'verify_iss': False,
    'verify_sub': False,
    'verify_jti': False,
    'verify_at_hash': False,
    'require_aud': False,
    'require_iat': False,
    'require_exp': False,
    'require_nbf': False,
    'require_iss': False,
    'require_sub': False,
    'require_jti': False,
    'require_at_hash': False,
    'leeway': 0,
}


class AccessToken(NamedTuple):
    body: str

    @property
    def payload(self) -> dict:
        return jwt.decode(self.body, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options=SKIP_VALIDATION)

    @property
    def sub(self) -> str:
        payload = self.payload
        return payload.get("sub")

    @property
    def user_id(self) -> int:
        return int(self.sub)

    @property
    def expire_at(self) -> float:
        return self.payload.get("exp")

    @property
    def is_active(self) -> bool:
        return time.time() < self.expire_at

    def validate(self, **options):
        options = DEFAULT_VALIDATION_OPTIONS.copy() | options
        jwt.decode(self.body, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options=options)
