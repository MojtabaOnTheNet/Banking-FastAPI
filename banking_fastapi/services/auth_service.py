import logging
from datetime import UTC, datetime, timedelta

from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.models.auth_model import RefreshModel
from banking_fastapi.db.schemas.auth_schema import (
    AccessTokenDTO,
    LoginInputDTO,
    RegisterInputDTO,
    TokenPairDTO,
)
from banking_fastapi.db.schemas.user_schema import UserModelInputDTO
from banking_fastapi.security.security import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    verify_password,
)

logger = logging.getLogger(__name__)


class AuthService:
    """Auth for authentication functionality."""

    def __init__(self) -> None:
        self.user_dao = UserDAO()

    async def register(self, data: RegisterInputDTO) -> None:
        """Validate and add user to the database."""
        existing = await self.user_dao.get_by_phone(data.phone)
        if existing:
            raise ValueError("Phone number already registered")
        user = UserModelInputDTO(
            phone=data.phone,
            full_name=data.full_name,
            password=data.password,
        )
        await self.user_dao.insert(user)

    async def login(self, data: LoginInputDTO) -> TokenPairDTO:
        """Validate and create access and refresh tokens."""
        user = await self.user_dao.get_by_phone(data.phone)
        if not user:
            raise ValueError("Wrong phone number")
        if user.id is None:
            raise ValueError("User ID missing")
        if not user.is_active:
            raise ValueError("Inactive user")
        if not verify_password(data.password, user.hashed_password):
            raise ValueError("Wrong password")
        access_token = create_access_token(
            user_id=user.id, expires_delta=timedelta(minutes=5)
        )
        refresh_token = create_refresh_token()
        refresh_session = RefreshModel(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=datetime.now(UTC) + timedelta(days=30),
        )
        await refresh_session.insert()
        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)

    async def revoke(self, token_session: RefreshModel) -> None:
        """Receieve and revoke refresh token(session)."""
        token_session.revoked = True
        await token_session.save()

    async def refresh(self, token_session: RefreshModel) -> AccessTokenDTO:
        """Create a new access token."""
        new_access_token = create_access_token(
            user_id=token_session.user_id, expires_delta=timedelta(minutes=5)
        )
        return AccessTokenDTO(access_token=new_access_token)
