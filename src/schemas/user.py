from pydantic import BaseModel
from src.models.user import User
from typing import List, Union
from enum import Enum as PyEnum

class NotifyType(PyEnum):
    SMS = "sms"
    EMAIL = "email"

class Notify(BaseModel):
    type: NotifyType = NotifyType.EMAIL
    value: str

class UserCreate(BaseModel):
    name: str
    amount: float = 500000.0
    notify: Notify

def individual_user(user: Union[User, None]) -> dict:
    if user:
        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "amount": user["amount"],
            "notify": Notify(**user["notify"]).model_dump()
        }
    return user

def list_users(users: List[User]):
    return [individual_user(user) for user in users]