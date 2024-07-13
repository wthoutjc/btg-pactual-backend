from src.models.user import User
from src.schemas.user import individual_user
from src.database.base import PyMongoBaseRepo
from pymongo import MongoClient
from src.core.config import settings
from bson import ObjectId

class UserRepository(PyMongoBaseRepo):
    def __int__(self, mongo: MongoClient):
        super().__init__(mongo)

    def create_user(self, user: User):
        user_dict = user.model_dump()
        user_dict["_id"] = ObjectId()
        self.database[settings.MONGO_COLLECTION_USER].insert_one(user_dict)
        return user_dict

    def get_user_by_id(self, user_id: str):
        return individual_user(self.database[settings.MONGO_COLLECTION_USER].find_one({"_id": ObjectId(user_id)}))

    def update_user_amount(self, user_id: str, new_amount: float):
        self.database[settings.MONGO_COLLECTION_USER].update_one({"_id": ObjectId(user_id)}, {"$set": {"amount": new_amount}})