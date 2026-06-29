from fastapi import APIRouter, Depends, HTTPException, Request

from banking_fastapi.db.dao.transfer_dao import TransferDAO
from banking_fastapi.db.models.transfer_model import TransferModel
from banking_fastapi.db.schemas.transfer_schema import (
    TransferModelDTO,
    TransferModelInputDTO,
    TransferModelRequestDTO,
)
from banking_fastapi.limiter import limiter
from banking_fastapi.services.transfer_service import (
    TransferService,
)
from banking_fastapi.web.api.deps import CurrentUser

router = APIRouter()


@router.get("/", response_model=list[TransferModelDTO])
@limiter.limit("100/minute")
async def get_transfers(
    request: Request,
    current_user: CurrentUser,
    transfer_dao: TransferDAO = Depends(),
) -> list[TransferModel]:
    """Retrieve all transfer objects from the database for the logged user.

    - either sender or reciever.
    """
    return await transfer_dao.get_all_private(user_id=current_user.id)


@router.post("/", status_code=201)
@limiter.limit("100/minute")
async def create_transfer(
    request: Request,
    transfer: TransferModelRequestDTO,
    current_user: CurrentUser,
    transfer_service: TransferService = Depends(),
) -> None:
    """Create a new transfer."""
    try:
        transfer_input = TransferModelInputDTO(
            **transfer.model_dump(), sender_user_id=current_user.id
        )
        await transfer_service.create_transfer(transfer=transfer_input)
    except Exception as error:
        raise HTTPException(404, str(error)) from error
