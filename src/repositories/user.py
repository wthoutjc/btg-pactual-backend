from src.models.user import User
from src.schemas.user import individual_user
from src.database.base import PyMongoBaseRepo
from pymongo import MongoClient
from src.core.config import settings
from bson import ObjectId
from typing import Union

class UserRepository(PyMongoBaseRepo):
    def __int__(self, mongo: MongoClient):
        super().__init__(mongo)

    def create_user(self, user: User):
        user_dict = user.model_dump()
        user_dict["_id"] = ObjectId()
        self.database[settings.MONGO_COLLECTION_USER].insert_one(user_dict)
        return user_dict

    def get(self) -> Union[User, None]:
        user = self.database[settings.MONGO_COLLECTION_USER].find_one({})
        print(f"[DEBUG] User: {user}")
        return individual_user(user) if user else None

    def update(self, user_id: str, user_update: User) -> Union[User, None]:
        if "notify" in user_update and "type" in user_update["notify"]:
            user_update["notify"]["type"] = user_update["notify"]["type"].value

        result = self.database[settings.MONGO_COLLECTION_USER].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_update}
        )
        if result.modified_count:
            return self.get()
        return None

    def update_user_amount(self, user_id: str, new_amount: float):
        self.database[settings.MONGO_COLLECTION_USER].update_one({"_id": ObjectId(user_id)}, {"$set": {"amount": new_amount}})