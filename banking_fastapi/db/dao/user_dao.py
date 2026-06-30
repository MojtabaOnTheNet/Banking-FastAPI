from beanie import PydanticObjectId

from banking_fastapi.db.models.user_model import UserModel
from banking_fastapi.db.schemas.user_schema import UserModelInputDTO
from banking_fastapi.security.security import password_hash


class UserDAO:
    """Class of accessing user table."""

    async def insert(self, user: UserModelInputDTO) -> None:
        """Add single user to session."""
        await UserModel.insert(
            UserModel(
                phone=user.phone,
                email=user.email,
                full_name=user.full_name,
                hashed_password=password_hash.hash(user.password),
            )
        )

    async def get_all(self, limit: int, offset: int) -> list[UserModel]:
        """Get all users with limit/offset pagination."""
        return await UserModel.find_all(skip=offset, limit=limit).to_list()

    async def get_by_id(self, user_id: PydanticObjectId) -> UserModel:
        """Get single user."""
        user = await UserModel.get(user_id)
        if user is None:
            raise ValueError("user not found")
        return user

    async def get_by_phone(self, input_phone: str) -> UserModel:
        """Get single user."""
        user = await UserModel.find_one(UserModel.phone == input_phone)
        if user is None:
            raise ValueError("user not found")
        return user

    async def update_balance(self, user: UserModel, transaction_amount: float) -> None:
        """Update user balance."""
        await user.update({"$inc": {"balance": transaction_amount}})

    async def update_password(self, user: UserModel, password: str) -> None:
        """Update user password."""
        await user.update({"$set": {"hashed_password": password_hash.hash(password)}})
