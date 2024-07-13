from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK
from src.schemas.transaction import TransactionOut
from src.api.dependencies.dependency_fund import subscribe, unsubscribe

fund_router = APIRouter()

@fund_router.post(
    "/subscribe",
    status_code=HTTP_200_OK,
    response_description="init a subscribe",
    response_model=TransactionOut
)
async def subscribe(
    transaction_out: TransactionOut = Depends(subscribe)
):
    return transaction_out


@fund_router.post(
    "/unsubscribe/{fund_id}",
    status_code=HTTP_200_OK,
    response_description="init a unsubscribe",
    response_model=TransactionOut
)
async def unsubscribe(
    transaction_out: TransactionOut = Depends(unsubscribe)
):
    return transaction_out