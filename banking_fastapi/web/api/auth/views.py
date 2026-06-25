import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from banking_fastapi.db.schemas.auth_schema import (
    AccessTokenDTO,
    LoginInputDTO,
    RegisterInputDTO,
)
from banking_fastapi.services.auth_service import AuthService
from banking_fastapi.web.api.deps import CurrentRefreshSession

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", status_code=201)
async def register_user(
    register_input: RegisterInputDTO, auth_service: AuthService = Depends()
) -> None:
    """Endpoint for registering a new user."""
    try:
        await auth_service.register(register_input)
    except Exception as error:
        raise HTTPException(401, str(error)) from error


@router.post("/login", status_code=200)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    auth_service: AuthService = Depends(),
) -> AccessTokenDTO:
    """Endpoint for user login and receieving access token."""
    try:
        tokens = await auth_service.login(
            LoginInputDTO(phone=form_data.username, password=form_data.password)
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 30,  # 30 Days
        )
        logger.info("Hello")
        return AccessTokenDTO(access_token=tokens.access_token)
    except Exception as error:
        raise HTTPException(401, str(error)) from error


@router.post("/refresh", status_code=200)
async def refresh(
    token_session: CurrentRefreshSession, auth_service: AuthService = Depends()
) -> AccessTokenDTO:
    """Endpoint for getting a new access token using refresh token(session)."""
    try:
        return await auth_service.refresh(token_session)
    except Exception as error:
        raise HTTPException(401, str(error)) from error
