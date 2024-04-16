from typing import Optional

import prisma
import prisma.models
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class GeolocationDataResponse(BaseModel):
    """
    Response model containing detailed geolocation information for a given IP address.
    """

    country: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ISP: Optional[str] = None


app = FastAPI()


@app.get("/geolocation/{ip_address}", response_model=GeolocationDataResponse)
async def get_geolocation_data(ip_address: str) -> GeolocationDataResponse:
    """
    Retrieves geolocation data for a given IP address.

    This function queries the database for the geolocation information associated
    with the specified IP address. If the information is found, it is returned as
    a response model. Otherwise, an HTTP exception is raised indicating that the
    data could not be found.

    Args:
    ip_address (str): The IP address (IPv4 or IPv6 format) for which geolocation data is being requested.

    Returns:
    GeolocationDataResponse: Response model containing detailed geolocation information for a given IP address.

    Raises:
    HTTPException: If no geolocation data are found for the given IP address.
    """
    geolocation_data = await prisma.models.GeolocationData.prisma().find_unique(
        where={"ipAddress": ip_address}
    )
    if geolocation_data:
        return GeolocationDataResponse(
            country=geolocation_data.country,
            city=geolocation_data.city,
            latitude=geolocation_data.latitude,
            longitude=geolocation_data.longitude,
            ISP=geolocation_data.ISP,
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Geolocation data not found for IP address: {ip_address}",
        )
