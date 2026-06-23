from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.models.user_model import UserModel
from banking_fastapi.db.schemas.user_schema import UserModelDTO, UserModelInputDTO

router = APIRouter()


@router.get("/", response_model=list[UserModelDTO])
async def get_users(
    limit: int = 10,
    offset: int = 0,
    user_dao: UserDAO = Depends(),
) -> list[UserModel]:
    """
    Retrieve all user objects from the database.

    :param limit: limit of user objects, defaults to 10.
    :param offset: offset of user objects, defaults to 0.
    :param user_dao: DAO for user models.
    :return: list of user objects from database.
    """
    return await user_dao.get_all(limit=limit, offset=offset)


@router.post("/", status_code=201)
async def insert(
    new_user: UserModelInputDTO,
    user_dao: UserDAO = Depends(),
) -> None:
    """
    Creates user in the database.

    :param new_user: new user item.
    :param user_dao: DAO for users.
    """
    try:
        await user_dao.insert(new_user)
    except ValueError as err:
        raise HTTPException(status_code=403, detail=err) from err
