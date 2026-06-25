from datetime import UTC, datetime

from beanie import Document, PydanticObjectId


class RefreshModel(Document):
    """Model for Refresh tokens."""

    user_id: PydanticObjectId
    token_hash: str
    created_at: datetime = datetime.now(UTC)
    expires_at: datetime
    revoked: bool = False

    class Settings:
        name = "refresh_session"
