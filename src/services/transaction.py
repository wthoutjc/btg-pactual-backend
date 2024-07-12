from src.repositories import transaction as transaction_repo
from src.schemas.transaction import TransactionCreate
from src.models.transaction import Transaction
from bson import ObjectId

async def create_transaction(user_id: str, fund_id: str, amount: float, transaction_type: str):
    transaction = Transaction(
        user_id=ObjectId(user_id),
        fund_id=ObjectId(fund_id),
        amount=amount,
        transaction_type=transaction_type
    )
    return await transaction_repo.create_transaction(transaction)

async def get_user_transactions(user_id: str):
    return await transaction_repo.get_transactions_by_user_id(user_id)
