from src.database.session import db
from src.models.transaction import Transaction
from bson import ObjectId

async def create_transaction(transaction: Transaction):
    transaction_dict = transaction.model_dump()
    transaction_dict["_id"] = ObjectId()
    await db.transactions.insert_one(transaction_dict)
    return transaction_dict

async def get_transactions_by_user_id(user_id: str):
    transactions = await db.transactions.find({"user_id": ObjectId(user_id)}).to_list(length=100)
    return transactions
