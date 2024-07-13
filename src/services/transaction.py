from src.repositories.transaction import TransactionRepository
from src.models.transaction import Transaction
from bson import ObjectId
from typing import List

class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self.transaction_repository = transaction_repository

    async def create_transaction(self, user_id: str, fund_id: str, amount: float, transaction_type: str) -> Transaction:
        transaction = Transaction(
            user_id=ObjectId(user_id),
            fund_id=ObjectId(fund_id),
            amount=amount,
            transaction_type=transaction_type
        )
        return await self.transaction_repository.create_transaction(transaction)

    async def get_user_transactions(self, user_id: str) -> List[Transaction]:
        return await self.transaction_repository.get_transactions_by_user_id(user_id)
