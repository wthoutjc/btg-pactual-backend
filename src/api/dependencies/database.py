from typing import AsyncGenerator, Callable, Type
from fastapi import Depends
from pymongo import MongoClient
from starlette.requests import Request
from src.database.base import PyMongoBaseRepo

def _get_mongo_client(request: Request) -> MongoClient:
    print(request.app)
    return request.app.state.mongo_client

def get_mongodb_repo(repo_type: Type[PyMongoBaseRepo]) -> Callable:
    async def _get_repo(
        mongo_client: MongoClient = Depends(_get_mongo_client),
    ) -> AsyncGenerator[PyMongoBaseRepo, None]:
        yield repo_type(mongo_client)

    return _get_repo