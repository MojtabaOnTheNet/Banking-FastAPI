from banking_fastapi.db.dao.transaction_dao import TransactionDAO
from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.schemas.transaction_schema import TransactionModelInputDTO


class UserNotFoundError(Exception):
    """Error for when user not found."""


class InsufficientBalanceError(Exception):
    """Error for when balance is not enough."""


class TransactionService:
    """Service for making transactions."""

    def __init__(self) -> None:
        self.user_dao = UserDAO()
        self.transaction_dao = TransactionDAO()

    async def create_transaction(self, transaction: TransactionModelInputDTO) -> None:
        """
        Handles full transaction workflow.

        - validate user
        - validate business rules
        - update balance
        - insert transaction record
        """

        # 1. Get user
        user = await self.user_dao.get_by_id(transaction.user_id)
        if not user:
            raise UserNotFoundError("User not found")

        # 3. Business rules
        if transaction.transaction_type == "Withdrawal":
            if user.balance < transaction.amount:
                raise InsufficientBalanceError("Insufficient balance")

            await self.user_dao.update_balance(user, -transaction.amount)

        elif transaction.transaction_type == "Deposit":
            await self.user_dao.update_balance(user, transaction.amount)

        # 4. Persist transaction record
        await self.transaction_dao.insert(transaction)
