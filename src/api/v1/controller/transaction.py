from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK
from src.schemas.transaction import TransactionOut
from src.api.dependencies.dependency_transaction import get_user_transactions
from typing import List

transaction_router = APIRouter()

@transaction_router.get(
    "/{user_id}",
    status_code=HTTP_200_OK,
    response_description="get all transactions by user",
    response_model=List[TransactionOut]
)
def get_user_transactions(
    transactions: List[TransactionOut] = Depends(get_user_transactions)
):
    return transactions
