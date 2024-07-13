from src.database.base import PyMongoBaseRepo
from src.core.config import settings
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from src.schemas.fund import FundCategory, list_fund
from src.schemas.user import individual_user, NotifyType

funds = [
    {
        "_id": ObjectId(),
        "name": "FPV_BTG_PACTUAL_RECAUDADORA",
        "minimum_amount": 75000.0,
        "category": FundCategory.FPV.value
    },
    {
        "_id": ObjectId(),
        "name": "FPV_BTG_PACTUAL_ECOPETROL",
        "minimum_amount": 125000.0,
        "category": FundCategory.FPV.value
    },
    {
        "_id": ObjectId(),
        "name": "DEUDAPRIVADA",
        "minimum_amount": 50000.0,
        "category": FundCategory.FIC.value
    },
    {
        "_id": ObjectId(),
        "name": "FDO-ACCIONES",
        "minimum_amount": 250000.0,
        "category": FundCategory.FIC.value
    },
    {
        "_id": ObjectId(),
        "name": "FPV_BTG_PACTUAL_DINAMICA",
        "minimum_amount": 100000.0,
        "category": FundCategory.FPV.value
    },
]

user = {
    "_id": ObjectId(),
    "name": "Default User",
    "amount": 500000.0,
    "notify": {
        "type": NotifyType.EMAIL.value,
        "value": "juancamilorr2012@hotmail.com"
    },
    "created_at": datetime.now()
}

class RunSeed(PyMongoBaseRepo):
    def __init__(self):
        super().__init__(mongo=MongoClient(settings.MONGODB_URL))

    def seed(self):
        existing_funds = list_fund(self.database[settings.MONGO_COLLECTION_FUND].find({
            "name": {"$in": [fund["name"] for fund in funds]}
        }))

        if not existing_funds:
            self.database[settings.MONGO_COLLECTION_FUND].insert_many(funds)
            print("[INFO] Funds data inserted")
        else:
            print("[INFO] Funds already exist in the database")

        existing_user = individual_user(self.database[settings.MONGO_COLLECTION_USER].find_one({
            "name": user["name"]
        }))

        if not existing_user:
            self.database[settings.MONGO_COLLECTION_USER].insert_one(user)
            print("[INFO] User data inserted")
        else:
            print("[INFO] User already exists in the database")

if __name__ == "__main__":
    run_seed = RunSeed()
    run_seed.seed()
