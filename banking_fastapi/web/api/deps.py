import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import ValidationError

from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.schemas.user_schema import UserModelDTO
from banking_fastapi.security import security
from banking_fastapi.settings import settings

logger = logging.getLogger(__name__)

reuseable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(reuseable_oauth2), user_dao: UserDAO = Depends()
) -> UserModelDTO:
    """Dependency for getting the current user."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[security.ALGORITHM]
        )
    except ExpiredSignatureError as error:
        raise HTTPException(
            status_code=401,
            detail="Expired token",
        ) from error
    except (JWTError, ValidationError) as error:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        ) from error

    user = await user_dao.get_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[UserModelDTO, Depends(get_current_user)]
