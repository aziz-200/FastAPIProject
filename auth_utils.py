# auth_utils.py
import datetime
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "0f5a06de53d4318e8c3d1c4fb2f8dfdd932265812538d5f54e8acdaca22f9cbc"  # move to env var in production
ALGORITHM = "HS256"

security_scheme = HTTPBearer()


def create_token(subject: str, expires_delta: datetime.timedelta, token_type: str = "access") -> str:

    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_subject(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    expected_type: str = "access",
) -> str:

    payload = decode_token(credentials.credentials)
    if payload.get("type") != expected_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Expected a {expected_type} token")
    return payload["sub"]


def get_current_subject_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> str:
    return get_current_subject(credentials, expected_type="refresh")