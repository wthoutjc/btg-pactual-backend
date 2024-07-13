from src.models.transaction import Transaction
from src.schemas.transaction import list_transaction
from src.database.base import PyMongoBaseRepo
from pymongo import MongoClient
from src.core.config import settings
from bson import ObjectId
from typing import List

class TransactionRepository(PyMongoBaseRepo):
    def __int__(self, mongo: MongoClient):
        super().__init__(mongo)

    def create_transaction(self, transaction: Transaction) -> Transaction:
        transaction_dict = transaction.model_dump()
        transaction_dict["_id"] = ObjectId()
        self.database[settings.MONGO_COLLECTION_TRANSACTION].insert_one(transaction_dict)
        return transaction

    def get_transactions_by_user_id(self, user_id: str) -> List[Transaction]:
        return list_transaction(self.database[settings.MONGO_COLLECTION_TRANSACTION].find({"user_id": user_id}).sort("created_at", -1))

    def get_last_transaction_by_user_id(self, user_id: str) -> Transaction:
        transaction = self.database[settings.MONGO_COLLECTION_TRANSACTION].find_one({"user_id": user_id}, sort=[("created_at", -1)])
        return transaction if transaction else None
