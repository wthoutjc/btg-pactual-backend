from src.repositories import fund as fund_repo
from src.schemas.fund import FundCreate
from src.repositories.transaction import create_transaction

async def subscribe_to_fund(user_id: str, fund_create: FundCreate):
    fund = await fund_repo.get_fund_by_id(fund_create.id)
    if not fund:
        raise ValueError("Fund not found")
    if fund_create.amount < fund["minimum_amount"]:
        raise ValueError("Insufficient amount to subscribe to the fund")
    transaction = {
        "user_id": user_id,
        "fund_id": fund_create.id,
        "amount": fund_create.amount,
        "transaction_type": "subscribe"
    }
    await create_transaction(transaction)
    return transaction
