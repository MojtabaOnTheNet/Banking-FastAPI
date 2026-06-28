from banking_fastapi.db.dao.loan_dao import LoanDAO
from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.schemas.loan_schema import LoanModelInputDTO


class UserNotFoundError(Exception):
    """Error for when user not found."""


class InsufficientBalanceError(Exception):
    """Error for when balance is not enough."""


class Loanservice:
    """Service for making loans."""

    def __init__(self) -> None:
        self.user_dao = UserDAO()
        self.loan_dao = LoanDAO()

    async def create_loan(self, loan: LoanModelInputDTO) -> None:
        """Handles full loan workflow."""

        user = await self.user_dao.get_by_id(loan.user_id)
        if not user:
            raise UserNotFoundError("User not found")

        # check if user has it least ten percent the amount of the requested loan
        if loan.amount < user.balance:
            raise InsufficientBalanceError(
                "Loan most be greater than the user's balance"
            )
        if user.balance < loan.amount * 0.1:
            await self.loan_dao.insert(loan)
            await self.user_dao.update_balance(user, loan.amount)
        else:
            raise InsufficientBalanceError("Insufficient balance")
