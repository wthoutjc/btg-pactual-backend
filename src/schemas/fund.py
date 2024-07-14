from src.models.fund import Fund
from typing import List, Optional
from enum import Enum as PyEnum
from pydantic import BaseModel

class FundCategory(PyEnum):
    FPV = "FPV"
    FIC = "FIC"

class FundOut(BaseModel):
    id: str
    name: str
    minimum_amount: float
    category: FundCategory
    last_transaction: Optional[dict]


def individual_fund(fund: Fund) -> dict:
    return {
        "id": str(fund["_id"]),
        "name": fund["name"],
        "minimum_amount": fund["minimum_amount"],
        "category": fund["category"]
    }

def list_fund(funds: List[Fund]):
    return [individual_fund(fund) for fund in funds]