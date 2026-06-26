from beanie import PydanticObjectId
from beanie.operators import Or

from banking_fastapi.db.models.transfer_model import TransferModel
from banking_fastapi.db.schemas.transfer_schema import TransferModelInputDTO


class TransferDAO:
    """Class of accessing transfer table."""

    async def insert(self, transfer: TransferModelInputDTO) -> None:
        """Add single transfer to session."""
        await TransferModel.insert_one(
            TransferModel(
                sender_user_id=transfer.sender_user_id,
                receiever_user_id=transfer.receiever_user_id,
                amount=transfer.amount,
            )
        )

    async def get_all_private(
        self,
        user_id: PydanticObjectId,
    ) -> list[TransferModel]:
        """Get all transfers for one user."""
        return await TransferModel.find(
            Or(
                TransferModel.sender_user_id == user_id,
                TransferModel.receiever_user_id == user_id,
            )
        ).to_list()
