from fastapi import APIRouter, Depends, HTTPException

from banking_fastapi.db.dao.transaction_dao import TransactionDAO
from banking_fastapi.db.models.transaction_model import TransactionModel
from banking_fastapi.db.schemas.transaction_schema import (
    TransactionModelDTO,
    TransactionModelInputDTO,
)

router = APIRouter()


@router.get("/", response_model=list[TransactionModelDTO])
async def get_transactions(
    limit: int = 10,
    offset: int = 0,
    transaction_dao: TransactionDAO = Depends(),
) -> list[TransactionModel]:
    """
    Retrieve all transaction objects from the database.

    :param limit: limit of transaction objects, defaults to 10.
    :param offset: offset of transaction objects, defaults to 0.
    :param transaction_dao: DAO for transaction models.
    :return: list of transaction objects from database.
    """
    return await transaction_dao.get_all_transactions(limit=limit, offset=offset)


@router.post("/", status_code=200)
async def create_transaction(
    transaction: TransactionModelInputDTO,
    transaction_dao: TransactionDAO = Depends(),
) -> None:
    """Create a new transaction."""
    try:
        await transaction_dao.create_transaction(transaction)
    except Exception as err:
        raise HTTPException(status_code=400, detail=err) from err
