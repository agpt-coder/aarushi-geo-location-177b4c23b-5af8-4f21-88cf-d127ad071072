import logging
from contextlib import asynccontextmanager
from typing import List

import project.bulk_geolocation_query_service
import project.create_api_key_service
import project.get_geolocation_data_service
import project.get_user_rate_limit_service
import project.update_user_rate_limit_service
import project.verify_api_key_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="aarushi-geo-location-1",
    lifespan=lifespan,
    description="Based on the interview, the user requires an API endpoint designed with FastAPI that handles geolocation data retrieval based on IP addresses. The following key points were highlighted during the discussions:\n\n- The API should be asynchronous (async) to ensure scalability and handle the anticipated volume of up to 1000 requests per second. This aids in maintaining an efficient and responsive service.\n- Specific data to be retrieved from the geolocation database includes the country, city, latitude, longitude, and, ideally, the Internet Service Provider (ISP) information. These data points are essential for location-based services, content personalization, technical analytics, and assessing access rights.\n- Performance goals are set to achieve response times of less than 200 milliseconds, thereby ensuring a smooth user experience without noticeable delays.\n- The need to support bulk IP address queries was also emphasized. This feature will significantly lower the number of requests sent by clients requiring data for multiple IP addresses simultaneously, thus enhancing the overall performance.\n\nTo address these requirements, the following technical stack components were identified as suitable choices:\n- **Programming Language:** Python, for its simplicity and asynchronous capabilities.\n- **API Framework:** FastAPI, noted for its ease of use for creating asynchronous APIs, built-in OpenAPI support for comprehensive documentation, and its dependency injection system which contributes to cleaner, more maintainable code.\n- **Database:** PostgreSQL, due to its robustness and the capability to store and efficiently query geolocation data. Specific aspects such as using IP network data types (INET or CIDR) for accurate IP range queries and creating indexes on IP address columns for performance optimization were recommended.\n- **ORM:** Prisma, while it doesn't natively support PostgreSQL's geolocation data types such as 'point', can still be utilized by employing raw SQL queries or mapping these specific data types to string or binary fields and manually handling them within the application logic.\n\nIn terms of design and development best practices, the project will leverage asynchronous request handling, implement authentication and data validation (utilizing Pydantic models), and consider scalability from the outset to effectively manage the expected load. The database setup will include importing a suitable geolocation database into PostgreSQL, with regular updates to ensure data accuracy.",
)


@app.get(
    "/geolocation/{ip_address}",
    response_model=project.get_geolocation_data_service.GeolocationDataResponse,
)
async def api_get_get_geolocation_data(
    ip_address: str,
) -> project.get_geolocation_data_service.GeolocationDataResponse | Response:
    """
    Retrieves geolocation data for a given IP address.
    """
    try:
        res = await project.get_geolocation_data_service.get_geolocation_data(
            ip_address
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/apikey/create",
    response_model=project.create_api_key_service.CreateApiKeyResponse,
)
async def api_post_create_api_key(
    user_id: str,
) -> project.create_api_key_service.CreateApiKeyResponse | Response:
    """
    Generates a new API key for authenticated users.
    """
    try:
        res = await project.create_api_key_service.create_api_key(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/ratelimit/{user_id}",
    response_model=project.get_user_rate_limit_service.GetUserRateLimitResponse,
)
async def api_get_get_user_rate_limit(
    user_id: str,
) -> project.get_user_rate_limit_service.GetUserRateLimitResponse | Response:
    """
    Retrieves the current rate limit settings for a specific user or API key.
    """
    try:
        res = await project.get_user_rate_limit_service.get_user_rate_limit(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/ratelimit/update/{user_id}",
    response_model=project.update_user_rate_limit_service.UpdateUserRateLimitResponse,
)
async def api_patch_update_user_rate_limit(
    user_id: str, limit: int, windowSec: int
) -> project.update_user_rate_limit_service.UpdateUserRateLimitResponse | Response:
    """
    Updates rate limit settings for a specific user or API key.
    """
    try:
        res = await project.update_user_rate_limit_service.update_user_rate_limit(
            user_id, limit, windowSec
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/geolocation/bulk",
    response_model=project.bulk_geolocation_query_service.BulkGeolocationQueryResponse,
)
async def api_post_bulk_geolocation_query(
    ip_addresses: List[str],
) -> project.bulk_geolocation_query_service.BulkGeolocationQueryResponse | Response:
    """
    Processes a list of IP addresses and returns their geolocation data.
    """
    try:
        res = await project.bulk_geolocation_query_service.bulk_geolocation_query(
            ip_addresses
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/auth/verify/{api_key}",
    response_model=project.verify_api_key_service.VerifyAPIKeyResponse,
)
async def api_get_verify_api_key(
    api_key: str,
) -> project.verify_api_key_service.VerifyAPIKeyResponse | Response:
    """
    Verifies if the provided API key is valid and active.
    """
    try:
        res = await project.verify_api_key_service.verify_api_key(api_key)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
