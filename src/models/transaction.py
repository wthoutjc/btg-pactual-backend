from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Transaction(BaseModel):
    id: Optional[ObjectId]
    user_id: ObjectId
    fund_id: ObjectId
    amount: float
    transaction_type: str
    created_at: datetime = datetime.utcnow()
