from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


def verify_password(
    plain_password: str, hashed_password: str
) -> tuple[bool, str | None]:
    """Verify a plaintext password against a hashed password."""
    return password_hash.verify_and_update(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Turn a normal password into a hashed_password."""
    return password_hash.hash(password)
