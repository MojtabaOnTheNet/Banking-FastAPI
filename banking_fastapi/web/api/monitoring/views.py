import mailtrap as mt
from fastapi import APIRouter

from banking_fastapi.settings import settings

router = APIRouter()


@router.get("/health")
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.

    Also sends a test email through Mailtrap.
    """
    mail = mt.Mail(
        sender=mt.Address(email=settings.smtp_host, name="Mailtrap Test"),
        to=[mt.Address(email=settings.smtp_reciever)],
        subject="You are awesome!",
        text="Congrats for sending test email with Mailtrap!",
        category="Integration Test",
    )
    client = mt.MailtrapClient(token=settings.smtp_key)
    client.send(mail)
