"""Webhook endpoints for Vapi voice agents and Make.com automation loops."""

import logging
from typing import Dict, Any
from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field

from app.models.case import ExtortionCase, CitizenProfile
from app.models.evidence import EvidenceItem, EvidenceType
from app.agents.orchestrator import orchestrator

logger = logging.getLogger("sara.api.webhooks")
router = APIRouter(prefix="/webhooks", tags=["Webhooks & Ingestion Streams"])


class VapiPostCallPayload(BaseModel):
    """Payload sent by Vapi when an extortion emergency call finishes."""

    call_id: Optional[str] = Field(default=None)
    transcript: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    caller_phone: Optional[str] = Field(default=None)
    duration: Optional[float] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)


@router.post(
    "/vapi",
    status_code=status.HTTP_200_OK,
    summary="Webhook receiver for Vapi real-time voice call transcripts",
)
async def handle_vapi_post_call(request: Request):
    """Processes post-call voice stream transcripts from Vapi, initializing SARA's cognitive response pipeline."""
    data = await request.json()
    logger.info(f"Received Vapi post-call webhook payload: {data.keys()}")

    # Extract transcript
    message = data.get("message", {})
    transcript = (
        data.get("transcript")
        or message.get("transcript")
        or data.get("summary")
        or str(data)
    )
    caller_number = (
        data.get("customer", {}).get("number")
        or data.get("caller_phone")
        or "ANONYMOUS_VOICE_CALLER"
    )

    # Initialize case
    citizen = CitizenProfile(
        phone_number=caller_number,
        anonymous=True if caller_number == "ANONYMOUS_VOICE_CALLER" else False,
    )
    case = ExtortionCase(
        citizen=citizen,
        source_channel="VAPI_VOICE_CALL",
    )

    # Attach transcript evidence
    evidence = EvidenceItem(
        case_id=case.case_id,
        evidence_type=EvidenceType.VOICE_TRANSCRIPT,
        content_raw=transcript,
    )
    case.evidences.append(evidence)

    # Trigger SARA Multi-Agent processing
    processed_case = await orchestrator.run_full_pipeline(case, primary_evidence_text=transcript)

    return {
        "status": "PROCESSED",
        "case_id": processed_case.case_id,
        "t_index": processed_case.threat_assessment.t_index if processed_case.threat_assessment else None,
        "tier": processed_case.threat_assessment.tier.value if processed_case.threat_assessment else None,
    }


@router.post(
    "/make",
    status_code=status.HTTP_200_OK,
    summary="Webhook receiver for Make.com / n8n event triggers",
)
async def handle_make_event(request: Request):
    """Handles external triggers from automation platforms like Make.com."""
    payload = await request.json()
    logger.info(f"Received Make.com event trigger: {payload}")
    return {"status": "RECEIVED", "payload_keys": list(payload.keys())}
