"""Data models for multimodal evidence ingestion and forensic extraction."""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class EvidenceType(str, Enum):
    """Types of multimodal evidence ingested into SARA."""

    VOICE_TRANSCRIPT = "VOICE_TRANSCRIPT"
    AUDIO_RECORDING = "AUDIO_RECORDING"
    MESSAGE_SCREENSHOT = "MESSAGE_SCREENSHOT"
    TEXT_MESSAGE = "TEXT_MESSAGE"
    BANK_ACCOUNT_INFO = "BANK_ACCOUNT_INFO"
    PHONE_NUMBER = "PHONE_NUMBER"
    CRYPTO_WALLET = "CRYPTO_WALLET"
    OTHER = "OTHER"


class ForensicArtifact(BaseModel):
    """Extracted verifiable forensic token."""

    artifact_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    artifact_type: str = Field(
        ...,
        description="Type of artifact: 'IBAN', 'PHONE', 'CRYPTO_ADDRESS', 'ALIAS', 'LOCATION', etc.",
    )
    raw_value: str = Field(
        ...,
        description="Extracted value (e.g. phone number, bank account number).",
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score of the extraction.",
    )
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional context, e.g. bank name, carrier, geolocation tag.",
    )


class EvidenceItem(BaseModel):
    """Container for ingested multimodal piece of evidence."""

    evidence_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    case_id: str = Field(..., description="Associated case identifier.")
    evidence_type: EvidenceType = Field(..., description="Evidence classification.")
    content_raw: Optional[str] = Field(
        default=None,
        description="Raw transcript, text message, or OCR payload.",
    )
    media_url: Optional[str] = Field(
        default=None,
        description="Encrypted Cloud Storage URI if audio/screenshot binary.",
    )
    extracted_artifacts: List[ForensicArtifact] = Field(
        default_factory=list,
        description="List of structured artifacts extracted by Forensic Agent.",
    )
    threat_indicators: List[str] = Field(
        default_factory=list,
        description="Detected threat keywords, coercion signals, or extortion demands.",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when evidence was ingested.",
    )
