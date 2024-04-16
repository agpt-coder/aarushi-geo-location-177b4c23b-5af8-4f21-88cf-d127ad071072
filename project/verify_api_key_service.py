import prisma
import prisma.models
from pydantic import BaseModel


class VerifyAPIKeyResponse(BaseModel):
    """
    Model for the response after verifying an API key. Indicates if the key is valid and, potentially, additional information about the key.
    """

    isValid: bool
    message: str


async def verify_api_key(api_key: str) -> VerifyAPIKeyResponse:
    """
    Verifies if the provided API key is valid and active.

    Args:
    api_key (str): The API key to be verified.

    Returns:
    VerifyAPIKeyResponse: Model for the response after verifying an API key. Indicates if the key is valid and, potentially, additional information about the key.
    """
    api_key_record = await prisma.models.APIKey.prisma().find_unique(
        where={"key": api_key}
    )
    if api_key_record is None:
        return VerifyAPIKeyResponse(isValid=False, message="API key does not exist.")
    if not api_key_record.active:
        return VerifyAPIKeyResponse(isValid=False, message="API key is inactive.")
    return VerifyAPIKeyResponse(isValid=True, message="API key is valid and active.")
