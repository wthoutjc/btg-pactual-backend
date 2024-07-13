from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_200_OK
from src.schemas.transaction import TransactionOut
from src.api.dependencies.dependency_transaction import create_transaction, get_user_transactions
from typing import List, Union

transaction_router = APIRouter()

@transaction_router.post(
    "/",
    status_code=HTTP_200_OK,
    response_description="create a transaction",
    response_model=TransactionOut
)
def create_transaction(
    create_transaction: Union[TransactionOut, HTTPException] = Depends(create_transaction)
):
    return create_transaction

@transaction_router.get(
    "/",
    status_code=HTTP_200_OK,
    response_description="get all transactions",
    response_model=List[TransactionOut]
)
def get_user_transactions(
    transactions: List[TransactionOut] = Depends(get_user_transactions)
):
    return transactions
