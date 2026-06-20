from bson import ObjectId
from pydantic import BaseModel, ConfigDict, field_validator


class UserModelDTO(BaseModel):
    """
    DTO for users.

    It returned when accessing users from the API.
    """

    id: str
    full_name: str
    phone: str

    @field_validator("id", mode="before")
    @classmethod
    def parse_object_id(cls, document_id: ObjectId) -> str:
        """
        Validator that converts `ObjectId` to json serializable `str`.

        :param document_id: Bson Id for this document.
        :return: The converted str.
        """
        return str(document_id)

    model_config = ConfigDict(from_attributes=True)


class UserModelInputDTO(BaseModel):
    """DTO for creating new user."""

    phone: str
    full_name: str
    password: str
