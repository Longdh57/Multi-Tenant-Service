from datetime import datetime, timedelta
from typing import Any, Optional, Union

import jwt
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from starlette.requests import Request

from app.core.config import settings
from app.helpers.api_handler import call_api

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class IAMHTTPBearer(HTTPBearer):
    def __init__(self, *, role: Optional[str] = None, bearerFormat: Optional[str] = None,
                 scheme_name: Optional[str] = None,
                 auto_error: bool = True):
        super().__init__(bearerFormat=bearerFormat,
                         scheme_name=scheme_name, auto_error=auto_error)
        self._api_endpoint = settings.AUTHENTICATION_SERVICE

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        await super().__call__(request)

        resp = call_api(url=self._api_endpoint + '/userinfo',
                        token_iam=request.headers["Authorization"])
        resp = resp.json()

        return resp['email']


oauth2_scheme = IAMHTTPBearer()


def create_access_token(user_id: Union[int, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    to_encode = {
        "exp": expire, "user_id": str(user_id)
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
