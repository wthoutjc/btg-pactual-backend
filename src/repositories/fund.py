from src.models.fund import Fund
from src.schemas.fund import individual_fund, list_fund
from src.database.base import PyMongoBaseRepo
from pymongo import MongoClient
from src.core.config import settings
from typing import List, Union
from bson import ObjectId

class FundRepository(PyMongoBaseRepo):
    def __int__(self, mongo: MongoClient):
        super().__init__(mongo)

    def get_funds(self) -> List[Fund]:
        return list_fund(self.database[settings.MONGO_COLLECTION_FUND].find({}))

    def get_fund_by_id(self, fund_id: str) -> Union[dict, None]:
        fund = self.database[settings.MONGO_COLLECTION_FUND].find_one({"_id": ObjectId(fund_id)})
        return individual_fund(fund) if fund else None

    def create_fund(self, fund: Fund) -> Fund:
        self.database[settings.MONGO_COLLECTION_FUND].insert_one(fund.model_dump())
        return fund
