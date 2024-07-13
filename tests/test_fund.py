import pytest
from httpx import AsyncClient
from app import app

@pytest.mark.asyncio
async def test_subscribe_to_fund():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/funds/subscribe", json={"id": "123", "amount": 1000})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_unsubscribe_from_fund():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/funds/unsubscribe/123")
    assert response.status_code == 200