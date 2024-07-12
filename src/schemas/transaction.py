from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    fund_id: str
    amount: float

class TransactionOut(BaseModel):
    id: str
    user_id: str
    fund_id: str
    amount: float
    transaction_type: str
    created_at: datetime
