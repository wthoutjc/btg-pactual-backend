from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.api.errors.http_error import http_error_handler
from src.api.errors.validation_error import http422_error_handler
from src.api.v1.controller import funds, transaction, user
from src.core.config import settings
from src.core.events import create_start_app_handler, create_stop_app_handler
from mangum import Mangum

def get_application() -> FastAPI:
    app = FastAPI(title="BTG Pactual FVP Microservice")

    app.add_event_handler("startup", create_start_app_handler(app))
    app.add_event_handler("shutdown", create_stop_app_handler(app))

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)

    app.include_router(funds.fund_router, prefix=f"{settings.API_V1_STR}/funds", tags=["funds"])
    app.include_router(transaction.transaction_router, prefix=f"{settings.API_V1_STR}/transactions", tags=["transactions"])
    app.include_router(user.user_router, prefix=f"{settings.API_V1_STR}/user", tags=["user"])

    # Health Check
    @app.get("/health")
    async def health():
        return {"status": "ok"}

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    return app

app = get_application()
handler = Mangum(app)