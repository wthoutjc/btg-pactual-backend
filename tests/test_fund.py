import pytest
from httpx import AsyncClient
from app import app
from src.schemas.transaction import TransactionType

@pytest.mark.asyncio
async def test_get_funds():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/funds/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_subscribe_to_fund():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/funds/subscribe", json={"fund_id": "60b6c6f2f1d2c10017eae6b2"})
    assert response.status_code == 200
    transaction = response.json()
    assert transaction["transaction_type"] == TransactionType.SUBSCRIBE.value

@pytest.mark.asyncio
async def test_subscribe_to_fund_insufficient_balance():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/funds/subscribe", json={"fund_id": "60b6c6f2f1d2c10017eae6b2"})
    assert response.status_code == 400
    assert response.json()["detail"] == "No tiene saldo disponible para vincularse al fondo"

@pytest.mark.asyncio
async def test_subscribe_to_fund_active_subscription():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/funds/subscribe", json={"fund_id": "60b6c6f2f1d2c10017eae6b2"})
    assert response.status_code == 400
    assert response.json()["detail"] == "The user already has an active subscription to this fund."

@pytest.mark.asyncio
async def test_unsubscribe_from_fund():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/api/v1/funds/unsubscribe/60b6c6f2f1d2c10017eae6b2")
    assert response.status_code == 200
    transaction = response.json()
    assert transaction["transaction_type"] == TransactionType.UNSUBSCRIBE.value

@pytest.mark.asyncio
async def test_unsubscribe_from_fund_no_active_subscription():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/api/v1/funds/unsubscribe/60b6c6f2f1d2c10017eae6b2")
    assert response.status_code == 400
    assert response.json()["detail"] == "No active subscription found to unsubscribe from."
