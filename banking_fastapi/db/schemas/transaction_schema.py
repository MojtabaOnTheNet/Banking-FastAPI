from datetime import UTC, datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from banking_fastapi.db.models.transaction_model import TransactionType


class TransactionModelDTO(BaseModel):
    """
    DTO for transactions.

    It's returned when accessing transactions from the API.
    """

    id: PydanticObjectId
    user_id: PydanticObjectId
    transaction_type: TransactionType
    amount: float
    created_at: datetime = datetime.now(UTC)


class TransactionModelInputDTO(BaseModel):
    """DTO for creating new transaction."""

    user_id: PydanticObjectId
    transaction_type: TransactionType
    amount: float
