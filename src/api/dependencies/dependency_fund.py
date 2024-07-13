from fastapi import HTTPException, Depends, Body, Path
from src.schemas.fund import FundCreate
from src.services.fund import FundService
from src.repositories.fund import FundRepository
from src.repositories.user import UserRepository
from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionOut
from typing import Union
from src.api.dependencies.database import get_mongodb_repo

def get_fund_service() -> FundService:
    fund_repository = get_mongodb_repo(FundRepository)
    user_repository = get_mongodb_repo(UserRepository)
    transaction_repository = get_mongodb_repo(TransactionRepository)
    return FundService(fund_repository, user_repository, transaction_repository)

async def subscribe(
    fund_create: FundCreate = Body(...),
    fund_service: FundService = Depends(get_fund_service)
) -> Union[TransactionOut, HTTPException]:
    try:
        return await fund_service.subscribe(fund_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def unsubscribe(
        fund_id: str = Path(...),
        fund_service: FundService = Depends(get_fund_service)
) -> Union[TransactionOut, HTTPException]:
    try:
        return await fund_service.unsubscribe(fund_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))