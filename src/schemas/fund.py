from pydantic import BaseModel
from src.models.fund import Fund
from typing import List
from enum import Enum as PyEnum

class FundCategory(PyEnum):
    FPV = "FPV"
    FIC = "FIC"

class FundCreate(BaseModel):
    name: str
    minimum_amount: float
    category: FundCategory

def individual_fund(fund: Fund) -> dict:
    return {
        "id": str(fund["_id"]),
        "name": fund["name"],
        "minimum_amount": fund["minimum_amount"]
    }

def list_fund(funds: List[Fund]):
    return [individual_fund(fund) for fund in funds]