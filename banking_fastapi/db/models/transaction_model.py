import enum
from datetime import UTC, datetime

from beanie import Document, PydanticObjectId


class TransactionType(enum.StrEnum):
    """Literall for types of a transaction."""

    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    LOAN = "Loan"


class TransactionModel(Document):
    """Model for a transaction."""

    user_id: PydanticObjectId
    transaction_type: TransactionType  # Add error handling for it later
    amount: float
    created_at: datetime = datetime.now(UTC)

    class Settings:
        name = "transactions"
