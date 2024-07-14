from src.models.transaction import Transaction
from src.schemas.transaction import list_transaction, individual_transaction, TransactionOut
from src.database.base import PyMongoBaseRepo
from src.repositories.fund import FundRepository
from pymongo import MongoClient, WriteConcern
from src.core.config import settings
from bson import ObjectId
from typing import List
from src.models.fund import Fund

class TransactionRepository(PyMongoBaseRepo):
    def __int__(self, mongo: MongoClient):
        super().__init__(mongo)
        self._mongo = mongo

    def create_transaction(self, transaction: Transaction) -> Transaction:
        transaction_dict = transaction.model_dump()
        transaction_dict["_id"] = ObjectId()
        self.database[settings.MONGO_COLLECTION_TRANSACTION]\
            .with_options(write_concern=WriteConcern(w="majority"))\
            .insert_one(transaction_dict)
        return transaction

    def get_transactions_by_user_id(self, user_id: str) -> List[TransactionOut]:
        transactions = list_transaction(self.database[settings.MONGO_COLLECTION_TRANSACTION].find({"user_id": user_id}).sort("created_at", -1).limit(20))

        fund_repo = FundRepository(self._mongo)
        result = []

        found_funds: List[Fund] = []
        for transaction in transactions:
            if len(found_funds) > 0 and transaction['fund_id'] in map(lambda x: x['id'], found_funds):
                fund = next(filter(lambda x: x['id'] == transaction['fund_id'], found_funds))
            else:
                fund = fund_repo.get_fund_by_id(transaction['fund_id'])
                found_funds.append(fund)

            transaction['fund'] = fund
            del transaction['fund_id']
            del transaction['user_id']
            result.append(transaction)

        return result

    def get_last_transaction_by_fund_id(self, fund_id: str) -> dict:
        transaction = self.database[settings.MONGO_COLLECTION_TRANSACTION].find_one(
            {"fund_id": fund_id},
            sort=[("created_at", -1)]
        )
        return individual_transaction(transaction) if transaction else None

    def get_last_transaction_by_user_id(self, user_id: str) -> dict:
        transaction = self.database[settings.MONGO_COLLECTION_TRANSACTION].find_one(
            {"user_id": user_id},
            sort=[("created_at", -1)]
        )
        return individual_transaction(transaction) if transaction else None