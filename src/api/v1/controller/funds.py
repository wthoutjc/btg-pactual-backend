from fastapi import APIRouter, HTTPException
from src.schemas.fund import FundCreate
from src.services import fund as fund_service
from src.schemas.transaction import TransactionOut

router = APIRouter()

@router.post("/subscribe", response_model=TransactionOut)
async def subscribe_to_fund(fund_create: FundCreate, user: User = Depends(get_current_user)):
    try:
        transaction = await fund_service.subscribe_to_fund(user.id, fund_create)
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
