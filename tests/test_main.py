import pytest
from httpx import AsyncClient
from httpx import ASGITransport
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app


@pytest.mark.asyncio
async def test_index():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "Weather Forecast" in response.text


@pytest.mark.asyncio
async def test_weather_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/weather", params={"city": "London"})
        assert response.status_code == 200
        assert "7-Day Forecast" in response.text


@pytest.mark.asyncio
async def test_weather_city_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/weather", params={"city": "SomeNonexistentCityThatDoesNotExist"})
        assert response.status_code == 200
        assert "City not found" in response.text


@pytest.mark.asyncio
async def test_user_history():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        user_id = response.cookies.get("user_id")
        assert user_id is not None

        await client.get("/weather", params={"city": "Paris"}, cookies={"user_id": user_id})

        response = await client.get("/user_history", cookies={"user_id": user_id})
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_stats():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/stats")
        assert response.status_code == 200
