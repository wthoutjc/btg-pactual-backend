from fastapi import HTTPException, Depends, Body
from src.schemas.transaction import TransactionCreate
from src.services.transaction import TransactionService
from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionOut
from typing import Union, List
from src.api.dependencies.database import get_mongodb_repo

def get_extraction_service() -> TransactionService:
    repository = get_mongodb_repo(TransactionRepository)
    return TransactionService(repository)

async def create_transaction(
    transaction_create: TransactionCreate = Body(...),
    transaction_service: TransactionService = Depends(get_extraction_service)
) -> Union[TransactionOut, HTTPException]:
    try:
        transaction = await transaction_service.create_transaction(transaction_create.fund_id, transaction_create.amount, "subscribe")
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_user_transactions(transaction_service: TransactionService = Depends(get_extraction_service)) -> List[TransactionOut]:
    return await transaction_service.get_user_transactions()
