import logging

import mailtrap as mt
import redis

from banking_fastapi.db.dao.user_dao import UserDAO
from banking_fastapi.db.models.user_model import UserModel
from banking_fastapi.security.security import create_password_reset_code
from banking_fastapi.settings import settings

logger = logging.getLogger(__name__)
r = redis.Redis(host="redis", port=6379, decode_responses=True)


class EmailService:
    """Service for email verification functionality."""

    def __init__(self) -> None:
        self.user_dao = UserDAO()

    async def password_reset(self, email: str) -> None:
        """Handle sending a password reset verfication code through email."""

        if email is None:
            raise ValueError("Email not found")

        code = create_password_reset_code()

        mail = mt.Mail(
            sender=mt.Address(email=settings.smtp_host, name="Mailtrap Test"),
            to=[mt.Address(email=email)],
            subject="Password Reset Request",
            text=f"You're password reset verification code: {code}",
        )
        client = mt.MailtrapClient(token=settings.smtp_key)
        client.send(mail)

        r.set(
            f"verify:{email}",
            code,
            ex=300,  # 5 minutes until expiration
        )

    async def verify_password_reset(
        self, code: str, new_password: str, confirm_new_password: str, user: UserModel
    ) -> None:
        """Handle verifying a password reset."""

        stored_code = r.get(f"verify:{user.email}")

        if stored_code is None:
            raise ValueError("Verification code expired")

        if stored_code != code:
            raise ValueError("Invalid verification code")

        if new_password != confirm_new_password:
            raise ValueError("Passwords do not match")

        logger.info("Hello")

        r.delete(f"verify:{user.email}")
        await self.user_dao.update_password(user=user, password=new_password)
