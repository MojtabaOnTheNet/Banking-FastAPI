from datetime import UTC, datetime

from beanie import Document, PydanticObjectId


class LoanModel(Document):
    """Model for a loan."""

    user_id: PydanticObjectId
    amount: float
    interest_rate: float
    created_at: datetime = datetime.now(UTC)

    class Settings:
        name = "loans"
