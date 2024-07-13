from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK
from src.schemas.transaction import TransactionOut
from src.schemas.fund import Fund
from src.api.dependencies.dependency_fund import subscribe, unsubscribe, get_funds
from typing import List

fund_router = APIRouter()

@fund_router.get(
    "/",
    status_code=HTTP_200_OK,
    response_description="get all funds",
    response_model=List[Fund]
)
def get_funds(
    funds: List[Fund] = Depends(get_funds)
):
    return funds

@fund_router.post(
    "/subscribe",
    status_code=HTTP_200_OK,
    response_description="init a subscribe",
    response_model=TransactionOut
)
def subscribe(
    transaction: TransactionOut = Depends(subscribe)
):
    return transaction


@fund_router.put(
    "/unsubscribe/{fund_id}",
    status_code=HTTP_200_OK,
    response_description="init a unsubscribe",
    response_model=TransactionOut
)
def unsubscribe(
    transaction: TransactionOut = Depends(unsubscribe)
):
    return transaction