import pytest
import httpx
from starlette.testclient import TestClient
from src.schemas.transaction import TransactionType
from src.core.config import settings
from app import get_application
from motor.motor_asyncio import AsyncIOMotorClient

app = get_application()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module", autouse=True)
def setup_mongo():
    app.state.mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.db = app.state.mongo_client[settings.MONGO_DATABASE]
    yield
    app.state.mongo_client.close()

def test_get_funds(client: httpx.AsyncClient):
        response_user = client.get(f"{settings.API_V1_STR}/user/me")
        user = response_user.json()

        client.put(f"{settings.API_V1_STR}/user/{user['_id']}", json={**user, "amount": 500000})
        response = client.get(f"{settings.API_V1_STR}/funds/all")
        assert response.status_code == 200
        funds = response.json()
        assert len(funds) == 5

def test_subscribe_to_fund(client: httpx.AsyncClient):
        response_funds = client.get(f"{settings.API_V1_STR}/funds/all")
        funds = response_funds.json()

        fund = funds[0]
        fund_id = fund["id"]

        response = client.post(f"{settings.API_V1_STR}/funds/subscribe", json={"fund_id": fund_id })
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["transaction_type"] == TransactionType.SUBSCRIBE.value

def test_subscribe_to_fund_active_subscription(client: httpx.AsyncClient):
        response_funds = client.get(f"{settings.API_V1_STR}/funds/all")
        funds = response_funds.json()

        fund = funds[0]
        fund_id = fund["id"]

        response = client.post(f"{settings.API_V1_STR}/funds/subscribe", json={"fund_id": fund_id})
        assert response.status_code == 400
        assert "Ya tiene una suscripción activa" in response.json()["errors"][0]

def test_unsubscribe_from_fund(client: httpx.AsyncClient):
        response_funds = client.get(f"{settings.API_V1_STR}/funds/all")
        funds = response_funds.json()

        fund = funds[0]
        fund_id = fund["id"]

        response = client.put(f"{settings.API_V1_STR}/funds/unsubscribe/{fund_id}")
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["transaction_type"] == TransactionType.UNSUBSCRIBE.value

def test_unsubscribe_from_fund_no_active_subscription(client: httpx.AsyncClient):
        response_funds = client.get(f"{settings.API_V1_STR}/funds/all")
        funds = response_funds.json()

        fund = funds[0]
        fund_id = fund["id"]

        response = client.put(f"{settings.API_V1_STR}/funds/unsubscribe/{fund_id}")
        assert response.status_code == 400
        assert "No tiene una suscripción activa" in response.json()["errors"][0]

def test_subscribe_to_fund_insufficient_balance(client: httpx.AsyncClient):
        response_user = client.get(f"{settings.API_V1_STR}/user/me")
        user = response_user.json()

        client.put(f"{settings.API_V1_STR}/user/{user['_id']}", json={**user, "amount": 0})

        response_funds = client.get(f"{settings.API_V1_STR}/funds/all")
        funds = response_funds.json()

        fund = funds[0]
        fund_id = fund["id"]

        response = client.post(f"{settings.API_V1_STR}/funds/subscribe", json={"fund_id": fund_id})
        assert response.status_code == 400
        assert "No tiene saldo disponible para vincularse al fondo" in response.json()["errors"][0]