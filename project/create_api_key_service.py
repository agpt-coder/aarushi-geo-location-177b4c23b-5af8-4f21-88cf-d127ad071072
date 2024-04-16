import uuid
from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class CreateApiKeyResponse(BaseModel):
    """
    Contains the details of the newly created API key for the user.
    """

    api_key: str
    creation_date: datetime
    status: str


async def create_api_key(user_id: str) -> CreateApiKeyResponse:
    """
    Generates a new API key for authenticated users.

    This function generates a unique API key for a user based on their user_id. It stores this API key in the database
    within the APIKey model linked to the User model by the user's ID. The function ensures that the generated API key
    is unique and retries if a collision occurs. It finally returns the API key details in a CreateApiKeyResponse model.

    Args:
    user_id (str): The unique identifier of the user requesting a new API key. This could be validated against the
    authenticated user session.

    Returns:
    CreateApiKeyResponse: Contains the details of the newly created API key for the user, including the API key,
    creation date, and status of creation.
    """
    api_key = uuid.uuid4().hex
    creation_date = datetime.now()
    retry = True
    while retry:
        try:
            await prisma.models.APIKey.prisma().create(
                data={"key": api_key, "userId": user_id}
            )
            retry = False
        except Exception as e:
            api_key = uuid.uuid4().hex
    return CreateApiKeyResponse(
        api_key=api_key, creation_date=creation_date, status="Success"
    )
