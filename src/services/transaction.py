from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionOut
from typing import List

class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self.transaction_repository = transaction_repository

    def get_user_transactions(self, user_id: str) -> List[TransactionOut]:
        return self.transaction_repository.get_transactions_by_user_id(user_id)
