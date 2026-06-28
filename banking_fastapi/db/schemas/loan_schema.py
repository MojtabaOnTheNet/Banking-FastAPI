from datetime import UTC, datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class LoanModelDTO(BaseModel):
    """
    DTO for loans.

    It's returned when accessing loans from the API.
    """

    id: PydanticObjectId
    user_id: PydanticObjectId
    amount: float
    interest_rate: float = Field(default=0.1)  # 10%
    created_at: datetime = datetime.now(UTC)


class LoanModelRequestDTO(BaseModel):
    """DTO for requesting new loan."""

    amount: float


class LoanModelInputDTO(LoanModelRequestDTO):
    """DTO for creating new loan."""

    user_id: PydanticObjectId
