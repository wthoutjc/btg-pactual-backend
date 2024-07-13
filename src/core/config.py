import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    API_V1_STR: str = "/api/v1"

    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/btg_pactual")
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE", "btg_fvp")

    # Collections
    MONGO_COLLECTION_FUND: str = os.getenv("MONGO_COLLECTION_FUND", default="funds")
    MONGO_COLLECTION_TRANSACTION: str = os.getenv("MONGO_COLLECTION_TRANSACTION", default="transactions")
    MONGO_COLLECTION_USER: str = os.getenv("MONGO_COLLECTION_USER", default="users")

    # Whatsapp SMS Service
    WHATSAPP_URL: str = os.getenv("WHATSAPP_URL", default="")
    WHATSAPP_NUMBER_ID: str = os.getenv("WHATSAPP_NUMBER_ID", default="")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", default="")
    WHATSAPP_TEMPLATE_NAME: str = os.getenv("WHATSAPP_TEMPLATE_NAME", default="")
    FIRED_WHATSAPP_NUMBER: str = os.getenv("FIRED_WHATSAPP_NUMBER", default="")

    # Email Service
    MAIL_HOST: str = os.getenv("MAIL_HOST", default="")
    MAIL_PORT: str = os.getenv("MAIL_PORT", default="")
    MAIL_SENDER: str = os.getenv("MAIL_SENDER", default="")
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", default="")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", default="")

settings = Settings()