from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.models.user_model import UserModel
from banking_fastapi.db.schemas.user_schema import UserModelDTO
from banking_fastapi.web.api.deps import CurrentUser

router = APIRouter()


@router.get("/", response_model=UserModelDTO)
async def get_user(
    current_user: CurrentUser,
    user_dao: UserDAO = Depends(),
) -> UserModel:
    """Retrieve user from database."""
    try:
        return await user_dao.get_by_id(current_user.id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
