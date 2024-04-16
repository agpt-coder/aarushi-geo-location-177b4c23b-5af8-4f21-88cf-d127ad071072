from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class GetUserRateLimitResponse(BaseModel):
    """
    Response model containing the retrieved rate limit settings for the user or API key.
    """

    user_id: str
    limit: int
    windowSec: int
    createdAt: datetime
    updatedAt: datetime


async def get_user_rate_limit(user_id: str) -> GetUserRateLimitResponse:
    """
    Retrieves the current rate limit settings for a specific user or API key.

    This function queries the 'prisma.models.RateLimit' table to find the rate limit settings associated with the given user_id.
    If no settings are found, it returns a default rate limit response.

    Args:
        user_id (str): Unique identifier for the user or API key to retrieve rate limit settings for.

    Returns:
    GetUserRateLimitResponse: Response model containing the retrieved rate limit settings for the user or API key.
    """
    rate_limit = await prisma.models.RateLimit.prisma().find_unique(
        where={"key": user_id}
    )
    if rate_limit:
        return GetUserRateLimitResponse(
            user_id=user_id,
            limit=rate_limit.limit,
            windowSec=rate_limit.windowSec,
            createdAt=rate_limit.createdAt,
            updatedAt=rate_limit.updatedAt,
        )
    else:
        return GetUserRateLimitResponse(
            user_id=user_id,
            limit=100,
            windowSec=3600,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
