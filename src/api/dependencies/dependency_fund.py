from fastapi import HTTPException, Depends, Body, Path
from src.services.fund import FundService
from src.repositories.fund import FundRepository
from src.repositories.user import UserRepository
from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionOut, TransactionCreate
from typing import Union
from src.api.dependencies.database import get_mongodb_repo
from typing import List
from src.schemas.fund import FundOut
from src.services.email import EmailService
from src.services.whatsapp import WhatsappService

def get_fund_service(
    fund_repository = Depends(get_mongodb_repo(FundRepository)),
    user_repository = Depends(get_mongodb_repo(UserRepository)),
    transaction_repository = Depends(get_mongodb_repo(TransactionRepository))
) -> FundService:
    email_service = EmailService()
    whatsapp_service = WhatsappService()
    return FundService(fund_repository, user_repository, transaction_repository, email_service, whatsapp_service)

def get_funds(
    fund_service: FundService = Depends(get_fund_service)
) -> List[FundOut]:
    try:
        return fund_service.get_funds()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def subscribe(
    transaction_create: TransactionCreate = Body(...),
    fund_service: FundService = Depends(get_fund_service)
) -> Union[TransactionOut, HTTPException]:
    try:
        transaction = fund_service.subscribe(transaction_create)
        if transaction:
            return transaction.model_dump()
        raise HTTPException(status_code=400, detail="An error occurred creating the transaction")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def unsubscribe(
        fund_id: str = Path(...),
        fund_service: FundService = Depends(get_fund_service)
) -> Union[TransactionOut, HTTPException]:
    try:
        transaction = fund_service.unsubscribe(fund_id)
        if transaction:
            return transaction.model_dump()
        raise HTTPException(status_code=400, detail="An error occurred creating the transaction")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))