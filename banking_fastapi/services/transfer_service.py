from banking_fastapi.db.dao.transfer_dao import TransferDAO
from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.schemas.transfer_schema import TransferModelInputDTO


class UserNotFoundError(Exception):
    """Error for when user not found."""


class UserInvalidError(Exception):
    """Error for when user is invalid."""


class InsufficientBalanceError(Exception):
    """Error for when balance is not enough."""


class TransferService:
    """Service for making transfers."""

    def __init__(self) -> None:
        self.user_dao = UserDAO()
        self.transfer_dao = TransferDAO()

    async def create_transfer(self, transfer: TransferModelInputDTO) -> None:
        """Handles full transfer workflow."""

        sender_user = await self.user_dao.get_by_id(transfer.sender_user_id)
        reciever_user = await self.user_dao.get_by_id(transfer.receiever_user_id)
        if not sender_user:
            raise UserNotFoundError("Sender user not found")
        if not reciever_user:
            raise UserNotFoundError("Reciever user not found")
        if sender_user.id == reciever_user.id:
            raise UserInvalidError("Sender and Reciever can't be the same")

        if sender_user.balance < transfer.amount:
            raise InsufficientBalanceError("Insufficient balance")

        # Reduce the balance for the sender user
        # Add the balance for the receieving user
        await self.user_dao.update_balance(sender_user, -transfer.amount)
        await self.user_dao.update_balance(reciever_user, transfer.amount)

        await self.transfer_dao.insert(transfer)
