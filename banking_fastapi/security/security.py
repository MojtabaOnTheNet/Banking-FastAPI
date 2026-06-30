import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from beanie import PydanticObjectId
from jose import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from banking_fastapi.settings import settings

ALGORITHM = "HS256"


def create_access_token(user_id: PydanticObjectId, expires_delta: timedelta) -> str:
    """Generate an access token with expiration date."""
    expire = datetime.now(UTC) + expires_delta
    to_encode = {"exp": expire, "sub": str(user_id)}
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def create_refresh_token() -> str:
    """Generate a refresh token."""
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    """Hash the refresh token."""
    return hashlib.sha256(token.encode()).hexdigest()


password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Turn a normal password into a hashed_password."""
    return password_hash.hash(password)


def create_password_reset_code() -> str:
    """Generates a 5 digit verification code."""
    return f"{secrets.randbelow(90000) + 10000}"
