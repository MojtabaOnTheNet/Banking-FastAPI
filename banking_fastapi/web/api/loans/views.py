from fastapi import APIRouter, Depends, HTTPException

from banking_fastapi.db.dao.loan_dao import LoanDAO
from banking_fastapi.db.models.loan_model import LoanModel
from banking_fastapi.db.schemas.loan_schema import (
    LoanModelDTO,
    LoanModelInputDTO,
    LoanModelRequestDTO,
)
from banking_fastapi.services.loan_service import (
    Loanservice,
)
from banking_fastapi.web.api.deps import CurrentUser

router = APIRouter()


@router.get("/", response_model=list[LoanModelDTO])
async def get_loans(
    current_user: CurrentUser,
    loan_dao: LoanDAO = Depends(),
) -> list[LoanModel]:
    """Retrieve all loan objects from the database for the logged user."""

    return await loan_dao.get_all_private(user_id=current_user.id)


@router.post("/", status_code=201)
async def create_loan(
    loan: LoanModelRequestDTO,
    current_user: CurrentUser,
    loan_service: Loanservice = Depends(),
) -> None:
    """Create a new loan."""
    try:
        loan_input = LoanModelInputDTO(**loan.model_dump(), user_id=current_user.id)
        await loan_service.create_loan(loan=loan_input)
    except Exception as error:
        raise HTTPException(404, str(error)) from error
