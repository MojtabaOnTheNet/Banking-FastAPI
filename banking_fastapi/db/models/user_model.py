import re
from datetime import UTC, datetime
from typing import Annotated

from beanie import Document, Indexed
from pydantic import EmailStr, field_validator
from pymongo import IndexModel


class UserModel(Document):
    """Model for a user."""

    phone: Annotated[str, Indexed(unique=True)]
    email: EmailStr | None = None
    full_name: str
    hashed_password: str
    balance: float = 1000.0
    created_at: datetime = datetime.now(UTC)
    is_active: bool = True
    is_admin: bool = False

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        """Validate and normalize phone number format."""
        value = value.strip()

        pattern = r"^09\d{9}$"  # IR format
        if not re.match(pattern, value):
            raise ValueError("Invalid phone number. Example: 09126236231")
        return value

    class Settings:
        name = "users"
        IndexModel(
            [("email", 1)],
            unique=True,
            partialFilterExpression={
                "email": {"$type": "string"},
            },
        )
