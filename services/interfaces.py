from abc import ABC, abstractmethod


class IGeocoder(ABC):
    @abstractmethod
    async def get_coordinates(self, city_name: str):
        pass

    @abstractmethod
    async def get_suggestions(self, city_part: str):
        pass


class IWeatherProvider(ABC):
    @abstractmethod
    async def get_forecast(self, coords):
        pass
