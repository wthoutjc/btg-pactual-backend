from src.database.session import db
from src.models.fund import Fund

async def get_fund_by_id(fund_id: str):
    return await db.funds.find_one({"_id": fund_id})

async def create_fund(fund: Fund):
    await db.funds.insert_one(fund.model_dump())
    return fund
