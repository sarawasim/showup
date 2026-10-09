"""Access tokens. The login endpoint issues them, get_current_user reads them.

Contract: a JWT signed with JWT_SECRET (HS256) whose `sub` is the user id as a string.
Sent by the app as `Authorization: Bearer <token>`.
"""

from datetime import UTC, datetime, timedelta

import jwt

from app.config import settings

ALGORITHM = "HS256"


def create_access_token(user_id: int) -> str:
    now = datetime.now(UTC)
    claims = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(claims, settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int:
    """Returns the user id. Raises jwt.PyJWTError on a bad signature, expiry or shape."""
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    try:
        return int(payload["sub"])
    except (KeyError, ValueError, TypeError) as exc:
        raise jwt.InvalidTokenError("missing or malformed sub") from exc
