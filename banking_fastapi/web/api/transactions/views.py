from fastapi import APIRouter, Depends, HTTPException

from banking_fastapi.db.dao.transaction_dao import TransactionDAO
from banking_fastapi.db.models.transaction_model import TransactionModel
from banking_fastapi.db.schemas.transaction_schema import (
    TransactionModelDTO,
    TransactionModelInputDTO,
    TransactionModelRequestDTO,
)
from banking_fastapi.services.transaction_service import (
    TransactionService,
)
from banking_fastapi.web.api.deps import CurrentUser

router = APIRouter()


@router.get("/", response_model=list[TransactionModelDTO])
async def get_transactions(
    current_user: CurrentUser,
    transaction_dao: TransactionDAO = Depends(),
) -> list[TransactionModel]:
    """Retrieve all transaction objects from the database for the logged user."""
    return await transaction_dao.get_all_private(user_id=current_user.id)


@router.post("/", status_code=201)
async def create_transaction(
    transaction: TransactionModelRequestDTO,
    current_user: CurrentUser,
    transaction_service: TransactionService = Depends(),
) -> None:
    """Create a new transaction."""
    try:
        transaction_input = TransactionModelInputDTO(
            **transaction.model_dump(), user_id=current_user.id
        )
        await transaction_service.create_transaction(transaction=transaction_input)
    except Exception as error:
        raise HTTPException(404, str(error)) from error
