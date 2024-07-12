from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Fund(BaseModel):
    id: Optional[ObjectId]
    name: str
    minimum_amount: float
