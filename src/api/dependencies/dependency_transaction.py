from fastapi import Depends,  Path
from src.services.transaction import TransactionService
from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionOut
from typing import List
from src.api.dependencies.database import get_mongodb_repo

def get_extraction_service(
        transaction_repository: TransactionRepository = Depends(get_mongodb_repo(TransactionRepository))
) -> TransactionService:
    return TransactionService(transaction_repository)

def get_user_transactions(
    user_id: str = Path(...),
    transaction_service: TransactionService = Depends(get_extraction_service)
) -> List[TransactionOut]:
    return transaction_service.get_user_transactions(user_id)
