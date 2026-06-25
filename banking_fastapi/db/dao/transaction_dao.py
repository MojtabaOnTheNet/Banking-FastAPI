from beanie import PydanticObjectId

from banking_fastapi.db.models.transaction_model import TransactionModel
from banking_fastapi.db.schemas.transaction_schema import TransactionModelInputDTO


class TransactionDAO:
    """Class of accessing transaction table."""

    async def insert(self, transaction: TransactionModelInputDTO) -> None:
        """Add single transaction to session."""
        await TransactionModel.insert_one(
            TransactionModel(
                user_id=transaction.user_id,
                amount=transaction.amount,
                transaction_type=transaction.transaction_type,
            )
        )

    async def get_all(self, limit: int, offset: int) -> list[TransactionModel]:
        """Get all transactions with limit/offset pagination."""
        return await TransactionModel.find_all(skip=offset, limit=limit).to_list()

    async def get_all_private(
        self, user_id: PydanticObjectId
    ) -> list[TransactionModel]:
        """Get all transactions for one user."""
        return await TransactionModel.find(
            TransactionModel.user_id == user_id
        ).to_list()
