from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.schemas.general import PyObjectId
from pydantic import BaseModel, Field
from bson import ObjectId

class Transaction(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    fund_id: str
    amount: float
    transaction_type: str
    created_at: datetime = datetime.now()

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = { ObjectId: str }
