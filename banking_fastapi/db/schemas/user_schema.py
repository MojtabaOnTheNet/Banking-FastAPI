from datetime import UTC, datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr


class UserModelDTO(BaseModel):
    """
    DTO for users.

    It's returned when accessing users from the API.
    """

    id: PydanticObjectId
    full_name: str
    balance: float
    phone: str
    email: EmailStr
    created_at: datetime = datetime.now(UTC)


class UserModelInputDTO(BaseModel):
    """DTO for creating new user."""

    phone: str
    email: EmailStr
    full_name: str
    password: str
