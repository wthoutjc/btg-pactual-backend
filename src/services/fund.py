from src.schemas.fund import FundCreate
from src.repositories.fund import FundRepository
from src.repositories.user import UserRepository
from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionOut, TransactionType, Transaction
from bson.objectid import ObjectId

class FundService:
    def __init__(self, fund_repository: FundRepository, user_repository: UserRepository, transaction_repository: TransactionRepository) -> None:
        self.fund_repository = fund_repository
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository

    async def subscribe(self, user_id: str, fund_create: FundCreate) -> TransactionOut:
        fund = await self.fund_repository.get_fund_by_id(fund_create.id)
        if not fund:
            raise ValueError("Fund not found")

        user = await self.user_repository.get_user_by_id(user_id)
        if user["amount"] < fund["minimum_amount"]:
            raise ValueError(f"No tiene saldo disponible para vincularse al fondo {fund['name']}")

        new_amount = user["amount"] - fund["minimum_amount"]
        await self.user_repository.update_user_amount(user_id, new_amount)

        transaction = Transaction(
            user_id=ObjectId(user_id),
            fund_id=ObjectId(fund.id),
            amount=fund["minimum_amount"],
            transaction_type="subscribe"
        )

        return await self.transaction_repository.create_transaction(transaction)

    async def unsubscribe(self, user_id: str, fund_id: str) -> TransactionOut:
        fund = await self.fund_repository.get_fund_by_id(fund_id)
        if not fund:
            raise ValueError("Fund not found")

        user = await self.user_repository.get_user_by_id(user_id)
        new_amount = user["amount"] + fund["minimum_amount"]
        await self.user_repository.update_user_amount(user_id, new_amount)

        transaction = Transaction(
            user_id=ObjectId(user_id),
            fund_id=ObjectId(fund_id),
            amount=fund["minimum_amount"],
            transaction_type=TransactionType.UNSUBSCRIBE
        )
        return await self.transaction_repository.create_transaction(transaction)
