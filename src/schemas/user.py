from pydantic import BaseModel
from src.models.user import User
from typing import List

class UserCreate(BaseModel):
    name: str
    amount: float = 500000.0

def individual_user(user: User) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "amount": user["amount"]
    }

def list_users(users: List[User]):
    return [individual_user(user) for user in users]