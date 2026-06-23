from datetime import UTC, datetime

from beanie import Document, PydanticObjectId


class TransferModel(Document):
    """Model for a transfer."""

    sender_user_id: PydanticObjectId
    receiever_user_id: PydanticObjectId
    amount: float
    created_at: datetime = datetime.now(UTC)

    class Settings:
        name = "transfers"
