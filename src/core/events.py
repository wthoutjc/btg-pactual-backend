from typing import Callable
from fastapi import FastAPI
from loguru import logger
from src.database.events import (close_mongo_connection, connect_to_mongo)

def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        connect_to_mongo(app)
    return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    def stop_app() -> None:
        close_mongo_connection(app)
    return stop_app
