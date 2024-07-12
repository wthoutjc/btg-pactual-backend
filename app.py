# uvicorn app:app --host 0.0.0.0 --port 5000 --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.controller.funds import router
from src.core.config import settings
import logging
from mangum import Mangum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ETL Extraction Microservice")
handler = Mangum(app)

app.include_router(router, prefix=settings.API_V1_STR)
app.include_router(funds.router, prefix="/api/v1/funds", tags=["funds"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)