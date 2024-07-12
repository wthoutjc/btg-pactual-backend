from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client.btg_pactual
