from pydantic import BaseModel


class RegisterInputDTO(BaseModel):
    """DTO for registering a new user."""

    phone: str
    password: str
    full_name: str


class LoginInputDTO(BaseModel):
    """DTO for user login."""

    phone: str
    password: str


class AccessTokenDTO(BaseModel):
    """DTO for returned access token."""

    access_token: str


class TokenPairDTO(BaseModel):
    """DTO for returned access and refresh tokens."""

    access_token: str
    refresh_token: str
