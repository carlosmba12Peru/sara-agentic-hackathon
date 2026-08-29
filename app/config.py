"""Application configuration module using Pydantic Settings."""

import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseModel
    class BaseSettings(BaseModel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
    SettingsConfigDict = dict


class Settings(BaseSettings):
    """SARA application settings loaded from environment or .env file."""

    # Application settings
    APP_NAME: str = "SARA - Cognitive Extortion Response Agent"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))

    # Google Gemini Models (Dual-Brain Architecture - Lab 2 & 8)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_FLASH_MODEL: str = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.7-flash")
    GEMINI_PRO_MODEL: str = os.getenv("GEMINI_PRO_MODEL", "gemini-3.7-pro")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")

    # Google Cloud Platform & Vertex AI
    GCP_PROJECT_ID: Optional[str] = os.getenv("GCP_PROJECT_ID")
    GCP_REGION: str = os.getenv("GCP_REGION", "us-central1")
    USE_VERTEX: bool = os.getenv("USE_VERTEX", "false").lower() == "true"

    # Firestore Configuration (Lab 10)
    FIRESTORE_DATABASE: str = os.getenv("FIRESTORE_DATABASE", "(default)")
    FIRESTORE_EMULATOR_HOST: Optional[str] = os.getenv("FIRESTORE_EMULATOR_HOST")

    # BigQuery Intelligence Configuration (Lab 18)
    BIGQUERY_DATASET: str = os.getenv("BIGQUERY_DATASET", "sara_intelligence")
    BIGQUERY_TABLE: str = os.getenv("BIGQUERY_TABLE", "extortion_threat_events")

    # Human-in-the-Loop (HITL) Safety Gate (Lab 15)
    REQUIRE_HITL_FOR_HIGH_RISK: bool = True
    HITL_SECRET_KEY: str = os.getenv("HITL_SECRET_KEY", "sara-operator-secret-key")

    # Multi-channel integrations & Voice (Vapi / Telegram / Make)
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_FROM_NUMBER: Optional[str] = os.getenv("TWILIO_FROM_NUMBER")
    MAKE_WEBHOOK_URL: Optional[str] = os.getenv("MAKE_WEBHOOK_URL")
    MAKE_WEBHOOK_VALIDACION_URL: Optional[str] = os.getenv("MAKE_WEBHOOK_VALIDACION_URL")
    VAPI_PUBLIC_KEY: Optional[str] = os.getenv("VAPI_PUBLIC_KEY")
    VAPI_ASSISTANT_ID: Optional[str] = os.getenv("VAPI_ASSISTANT_ID")
    DEMO_NOTIFICATION_TARGET: Optional[str] = os.getenv("DEMO_NOTIFICATION_TARGET")

    # T_index Risk Weights (Configurable per jurisdiction)
    WEIGHT_COERCION: float = 0.35
    WEIGHT_PERSISTENCE: float = 0.25
    WEIGHT_ARTIFACTS: float = 0.25
    WEIGHT_VULNERABILITY: float = 0.15


settings = Settings()

