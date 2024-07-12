from fastapi import APIRouter, HTTPException, Depends
from src.schemas.transaction import TransactionCreate, TransactionOut
from src.services import transaction as transaction_service
from src.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=TransactionOut)
async def create_transaction(transaction_create: TransactionCreate, user: User = Depends(get_current_user)):
    try:
        transaction = await transaction_service.create_transaction(user.id, transaction_create.fund_id, transaction_create.amount, "subscribe")
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TransactionOut])
async def get_user_transactions(user: User = Depends(get_current_user)):
    return await transaction_service.get_user_transactions(user.id)
