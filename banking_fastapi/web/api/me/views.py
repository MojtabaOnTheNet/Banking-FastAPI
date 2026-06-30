from fastapi import APIRouter, HTTPException, Request
from fastapi.param_functions import Depends

from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.models.user_model import UserModel
from banking_fastapi.db.schemas.password_schema import PasswordInputDTO
from banking_fastapi.db.schemas.user_schema import UserModelDTO
from banking_fastapi.limiter import limiter
from banking_fastapi.services.email_service import EmailService
from banking_fastapi.web.api.deps import CurrentUser

router = APIRouter()


@router.get("/", response_model=UserModelDTO, status_code=200)
@limiter.limit("100/minute")
async def get_user(
    request: Request,
    current_user: CurrentUser,
    user_dao: UserDAO = Depends(),
) -> UserModel:
    """Retrieve user from database."""
    try:
        return await user_dao.get_by_id(current_user.id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/password-reset", status_code=200)
@limiter.limit("5/minute")
async def reset_user_password(
    request: Request, current_user: CurrentUser, email_service: EmailService = Depends()
) -> dict[str, str]:
    """Send an email for password reset verification."""
    try:
        await email_service.password_reset(current_user.email)
        return {"detail": "Verification code sent through existing email."}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/password-reset-verify", status_code=201)
@limiter.limit("5/minute")
async def reset_password_verify(
    request: Request,
    current_user: CurrentUser,
    password_input: PasswordInputDTO,
    email_service: EmailService = Depends(),
) -> dict[str, str]:
    """Verify the code and update password."""
    try:
        await email_service.verify_password_reset(
            password_input.code,
            new_password=password_input.new_password,
            confirm_new_password=password_input.confirm_new_password,
            user=UserModel(**current_user.model_dump()),
        )
        return {"detail": "Password updated successfully."}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
