from pydantic import BaseModel
from datetime import datetime
from src.models.transaction import Transaction
from typing import List
from enum import Enum as PyEnum

class TransactionType(PyEnum):
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"

class TransactionCreate(BaseModel):
    fund_id: str
    amount: float

class TransactionOut(BaseModel):
    id: str
    user_id: str
    fund_id: str
    amount: float
    transaction_type: TransactionType
    created_at: datetime

def individual_transaction(transaction: Transaction) -> dict:
    return {
        "id": str(transaction["_id"]),
        "user_id": transaction["user_id"],
        "fund_id": transaction["fund_id"],
        "amount": transaction["amount"],
        "transaction_type": transaction["transaction_type"],
        "created_at": transaction["created_at"]
    }

def list_transaction(funds: List[Transaction]):
    return [individual_transaction(transaction) for transaction in funds]