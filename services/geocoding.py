import httpx
from services.interfaces import IGeocoder


class OpenStreetMapGeocoder(IGeocoder):
    async def get_coordinates(self, city_name: str):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city_name,
            "format": "json",
            "limit": 1
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            if not data:
                return None
            return {
                "latitude": float(data[0]["lat"]),
                "longitude": float(data[0]["lon"])
            }

    async def get_suggestions(self, city_part: str):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city_part,
            "format": "json",
            "limit": 5,
            "addressdetails": 1,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            suggestions = []
            for item in data:
                display_name = item.get("display_name", "")
                suggestions.append(display_name)
            return suggestions
