from src.models.fund import Fund
from src.schemas.fund import individual_fund
from src.database.base import PyMongoBaseRepo
from pymongo import MongoClient
from src.core.config import settings

class FundRepository(PyMongoBaseRepo):
    def __int__(self, mongo: MongoClient):
        super().__init__(mongo)

    def get_fund_by_id(self, fund_id: str) -> Fund:
        return individual_fund(self.database[settings.MONGO_COLLECTION_FUND].find_one({"_id": fund_id}))

    def create_fund(self, fund: Fund) -> Fund:
        self.database[settings.MONGO_COLLECTION_FUND].insert_one(fund.model_dump())
        return fund
