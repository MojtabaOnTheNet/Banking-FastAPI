from pydantic import BaseModel


class PasswordInputDTO(BaseModel):
    """DTO for reseting password."""

    code: str
    new_password: str
    confirm_new_password: str
