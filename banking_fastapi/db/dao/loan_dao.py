from beanie import PydanticObjectId

from banking_fastapi.db.models.loan_model import LoanModel
from banking_fastapi.db.schemas.loan_schema import LoanModelInputDTO


class LoanDAO:
    """Class of accessing loan table."""

    async def insert(self, loan: LoanModelInputDTO) -> None:
        """Add single loan to session."""
        await LoanModel.insert_one(
            LoanModel(user_id=loan.user_id, amount=loan.amount, interest_rate=0.1)
        )

    async def get_all_private(
        self,
        user_id: PydanticObjectId,
    ) -> list[LoanModel]:
        """Get all loans for one user."""
        return await LoanModel.find(
            LoanModel.user_id == user_id,
        ).to_list()
