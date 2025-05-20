from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode
from jwt import exceptions as jwt_exceptions
from common.config import settings

bearer_scheme = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
    except (jwt_exceptions.ExpiredSignatureError, jwt_exceptions.DecodeError, jwt_exceptions.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload