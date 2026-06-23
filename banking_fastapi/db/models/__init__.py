"""banking_fastapi models."""

from collections.abc import Sequence

from beanie import Document

from banking_fastapi.db.models.transaction_model import TransactionModel
from banking_fastapi.db.models.user_model import UserModel


def load_all_models() -> Sequence[type[Document]]:
    """Load all models from this folder."""
    return [UserModel, TransactionModel]
