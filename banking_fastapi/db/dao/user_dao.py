from beanie import PydanticObjectId

from banking_fastapi.db.models.user_model import UserModel
from banking_fastapi.db.schemas.user_schema import UserModelInputDTO
from banking_fastapi.security.security import password_hash

# ruff: noqa: ERA001 (Remove later)
# class DummyDAO:
#     """Class for accessing dummy table."""

#     async def create_dummy_model(self, name: str) -> None:
#         """
#         Add single dummy to session.

#         :param name: name of a dummy.
#         """
#         await DummyModel.insert_one(DummyModel(name=name))

#     async def get_all_dummies(self, limit: int, offset: int) -> list[DummyModel]:
#         """
#         Get all dummy models with limit/offset pagination.

#         :param limit: limit of dummies.
#         :param offset: offset of dummies.
#         :return: stream of dummies.
#         """
#         return await DummyModel.find_all(skip=offset, limit=limit).to_list()

#     async def filter(self, name: str | None = None) -> list[DummyModel]:
#         """
#         Get specific dummy model.

#         :param name: name of dummy instance.
#         :return: dummy models.
#         """
#         if name is None:
#             return []
#         return await DummyModel.find(DummyModel.name == name).to_list()

#     async def delete_dummy_model_by_name(
#         self,
#         name: str,
#     ) -> DummyModel | None:
#         """
#         Delete a dummy model by name.

#         :param name: name of dummy instance.
#         :return: option of a dummy model.
#         """
#         res = await DummyModel.find_one(DummyModel.name == name)
#         if res is None:
#             return res
#         await res.delete()
#         return res


class UserDAO:
    """Class of accessing user table."""

    async def insert(self, user: UserModelInputDTO) -> None:
        """Add single user to session."""
        await UserModel.insert(
            UserModel(
                phone=user.phone,
                full_name=user.full_name,
                hashed_password=password_hash.hash(user.password),
            )
        )

    async def get_all(self, limit: int, offset: int) -> list[UserModel]:
        """Get all users with limit/offset pagination."""
        return await UserModel.find_all(skip=offset, limit=limit).to_list()

    async def get_by_id(self, user_id: PydanticObjectId) -> UserModel | None:
        """Get single user."""
        return await UserModel.get(user_id)

    async def get_by_phone(self, input_phone: str) -> UserModel | None:
        """Get single user."""
        return await UserModel.find_one(UserModel.phone == input_phone)

    async def update_balance(self, user: UserModel, transaction_amount: float) -> None:
        """Update user balance."""
        await user.update({"$inc": {"balance": transaction_amount}})
