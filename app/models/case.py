"""Data models for Extortion Case management and lifecycle."""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import uuid

from app.models.evidence import EvidenceItem
from app.models.threat_index import ThreatIndexResult


class CaseStatus(str, Enum):
    """Lifecycle statuses for an extortion case in SARA."""

    INGESTED = "INGESTED"
    TRIAGED = "TRIAGED"
    AUDITED = "AUDITED"
    FORENSIC_AUDITED = "FORENSIC_AUDITED"
    RISK_EVALUATED = "RISK_EVALUATED"
    PENDING_HITL = "PENDING_HITL"
    DISPATCHED = "DISPATCHED"
    RESOLVED = "RESOLVED"
    ARCHIVED = "ARCHIVED"


class CitizenProfile(BaseModel):
    """Citizen / Victim profile data."""

    phone_number: Optional[str] = Field(default=None, description="Contact phone number.")
    anonymous: bool = Field(default=False, description="Whether caller wants to remain anonymous.")
    alias: Optional[str] = Field(default=None, description="Safe citizen pseudonym.")
    location_jurisdiction: Optional[str] = Field(default=None, description="District / City location.")


class AuditEntry(BaseModel):
    """Audit log entry for tracing multi-agent actions and governance decisions."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent_name: str = Field(..., description="Agent or entity performing the action.")
    action: str = Field(..., description="Action identifier.")
    details: Dict[str, Any] = Field(default_factory=dict, description="Metadata or payload details.")


class ExtortionCase(BaseModel):
    """Complete SARA Extortion Case Record."""

    case_id: str = Field(default_factory=lambda: f"SARA-{uuid.uuid4().hex[:8].upper()}")
    citizen: CitizenProfile = Field(..., description="Citizen information.")
    status: CaseStatus = Field(default=CaseStatus.INGESTED, description="Current workflow state.")
    source_channel: str = Field(default="VOICE_CALL", description="Intake channel: VOICE_CALL, WHATSAPP, WEB.")
    
    # Evidence & Analysis
    evidences: List[EvidenceItem] = Field(default_factory=list, description="All collected multimodal evidence.")
    triage_summary: Optional[str] = Field(default=None, description="Natural language summary from Triage Agent.")
    threat_assessment: Optional[ThreatIndexResult] = Field(default=None, description="Calculated T_index result.")
    
    # Gobernanza Legal - Propuesta de IA vs Validación Humana
    tipificacion_penal_propuesta_ia: Optional[str] = Field(
        default="PROPUESTA DE IA: Art. 200 del Código Penal (Sujeto a validación policial)",
        description="Sugerencia analítica preliminar generada por el agente empaquetador."
    )
    tipificacion_penal_definitiva_policial: Optional[str] = Field(
        default="PENDIENTE_VALIDACION_OFICIAL",
        description="Tipificación jurídica exacta definida por el oficial de policía tras la aprobación."
    )
    
    # Operational Coordination
    verification_token: Optional[str] = Field(default=None, description="Cryptographic one-time citizen link token.")
    verification_confirmed: bool = Field(default=False, description="Whether citizen accessed verification link.")
    dispatch_alerts_sent: List[str] = Field(default_factory=list, description="Channels notified (e.g. Telegram, Make).")

    # Timestamps & Audit
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    audit_trail: List[AuditEntry] = Field(default_factory=list, description="Cryptographically verifiable event log.")

