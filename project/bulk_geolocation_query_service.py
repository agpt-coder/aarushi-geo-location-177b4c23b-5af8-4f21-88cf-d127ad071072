from typing import List, Optional

import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class GeolocationInfo(BaseModel):
    """
    Model representing geolocation information for an IP address.
    """

    ip_address: str
    country: str
    city: Optional[str] = None
    latitude: float
    longitude: float
    ISP: Optional[str] = None


class BulkGeolocationQueryResponse(BaseModel):
    """
    Response model encapsulating geolocation data for multiple IP addresses.
    """

    geolocation_data: List[GeolocationInfo]


async def bulk_geolocation_query(
    ip_addresses: List[str],
) -> BulkGeolocationQueryResponse:
    """
    Processes a list of IP addresses and returns their geolocation data.

    Args:
    ip_addresses (List[str]): A list of IP addresses (IPv4 or IPv6) for which geolocation data is requested.

    Returns:
    BulkGeolocationQueryResponse: Response model encapsulating geolocation data for multiple IP addresses.

    """
    if not ip_addresses:
        raise HTTPException(status_code=400, detail="No IP addresses provided.")
    geolocations = []
    for ip in ip_addresses:
        geo_data = await prisma.models.GeolocationData.prisma().find_unique(
            where={"ipAddress": ip}
        )
        if geo_data:
            geolocations.append(
                GeolocationInfo(
                    ip_address=ip,
                    country=geo_data.country,
                    city=geo_data.city,
                    latitude=geo_data.latitude,
                    longitude=geo_data.longitude,
                    ISP=geo_data.ISP,
                )
            )
        else:
            continue
    return BulkGeolocationQueryResponse(geolocation_data=geolocations)
