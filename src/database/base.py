from pymongo import MongoClient
from src.core.config import settings

class PyMongoBaseRepo:
    def __init__(self, mongo: MongoClient):
        self._mongo = mongo
        self.database = self._mongo[settings.MONGO_DATABASE]

    @property
    def mongo_client(self) -> MongoClient:
        return self._mongo
