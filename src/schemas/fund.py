from pydantic import BaseModel
from typing import Optional

class FundCreate(BaseModel):
    name: str
    minimum_amount: float
