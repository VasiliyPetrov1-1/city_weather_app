import httpx
from services.interfaces import IWeatherProvider


class OpenMeteoWeatherProvider(IWeatherProvider):
    async def get_forecast(self, coords):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,weathercode",
            "timezone": "auto"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            return data.get("daily")
