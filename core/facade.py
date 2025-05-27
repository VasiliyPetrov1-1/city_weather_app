from services.interfaces import IGeocoder, IWeatherProvider


class WeatherFacade:
    def __init__(self, geocoder: IGeocoder, weather_provider: IWeatherProvider):
        self.geocoder = geocoder
        self.weather_provider = weather_provider

    async def geocode(self, city_name: str):
        return await self.geocoder.get_coordinates(city_name)

    async def get_weather(self, coords):
        return await self.weather_provider.get_forecast(coords)

    async def geocode_suggestions(self, city_part: str):
        return await self.geocoder.get_suggestions(city_part)
