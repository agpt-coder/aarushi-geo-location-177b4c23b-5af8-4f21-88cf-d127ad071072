import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserRateLimitResponse(BaseModel):
    """
    Response model confirming the update of a user or API key's rate limit settings.
    """

    user_id: str
    limit: int
    windowSec: int
    status: str


async def update_user_rate_limit(
    user_id: str, limit: int, windowSec: int
) -> UpdateUserRateLimitResponse:
    """
    Updates rate limit settings for a specific user or API key.

    Args:
      user_id (str): The unique identifier of the user or API key whose rate limit settings are to be updated.
      limit (int): The new maximum number of requests allowed in the defined window of time.
      windowSec (int): The duration (in seconds) of the rate limit window for which the limit applies.

    Returns:
      UpdateUserRateLimitResponse: Response model confirming the update of a user or API key's rate limit settings.
    """
    try:
        await prisma.models.RateLimit.prisma().update_many(
            where={"key": user_id}, data={"limit": limit, "windowSec": windowSec}
        )
        return UpdateUserRateLimitResponse(
            user_id=user_id,
            limit=limit,
            windowSec=windowSec,
            status="Rate limit settings updated successfully.",
        )
    except Exception as e:
        return UpdateUserRateLimitResponse(
            user_id=user_id,
            limit=0,
            windowSec=0,
            status=f"Failed to update rate limit settings: {e}",
        )
