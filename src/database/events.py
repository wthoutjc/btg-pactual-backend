from fastapi import FastAPI
from pymongo import MongoClient
from loguru import logger
from src.core.config import settings
import certifi
ca = certifi.where()

class MongoDB:
    client: MongoClient = None

mongo_db = MongoDB()

def connect_to_mongo(app: FastAPI) -> None:
    logger.info("[INFO] Connecting to MongoDB...")
    print(f"[DEBUG] MongoDB URL: {settings.MONGODB_URL}")
    mongo_client = MongoClient(settings.MONGODB_URL, tlsCAFile=ca)
    mongo_db.client = mongo_client
    app.state.mongo_client = mongo_client
    logger.info("[INFO] MongoDB connection succeeded")


def close_mongo_connection(app: FastAPI) -> None:
    logger.info("[INFO] Closing the mongodb connection..")
    app.state.mongo_client.close()
    logger.info("[INFO] MongoDB connection closed")
