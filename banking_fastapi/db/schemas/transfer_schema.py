from datetime import UTC, datetime

from beanie import PydanticObjectId
from pydantic import BaseModel


class TransferModelDTO(BaseModel):
    """
    DTO for transfers.

    It's returned when accessing transfers from the API.
    """

    id: PydanticObjectId
    sender_user_id: PydanticObjectId
    receiever_user_id: PydanticObjectId
    amount: float
    created_at: datetime = datetime.now(UTC)


class TransferModelRequestDTO(BaseModel):
    """DTO for requesting new transfer."""

    receiever_user_id: PydanticObjectId
    amount: float


class TransferModelInputDTO(TransferModelRequestDTO):
    """DTO for creating new transfer."""

    sender_user_id: PydanticObjectId
