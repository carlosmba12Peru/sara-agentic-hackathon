"""REST API Endpoints for Case Intake, Evidence Ingestion, SARA Multi-Agent Triage, and HITL Safety (Labs 11, 15, 18)."""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.models.case import ExtortionCase, CitizenProfile
from app.models.evidence import EvidenceItem, EvidenceType
from app.agents.orchestrator import orchestrator
from app.core.hitl import hitl_gate
from app.core.rag_knowledge import forensic_rag
from app.services.firestore_service import firestore_service
from app.services.bigquery_service import bigquery_service

router = APIRouter(prefix="/cases", tags=["Extortion Cases & Operations"])


class CreateCaseRequest(BaseModel):
    """Payload to initiate an extortion case."""

    citizen_phone: Optional[str] = Field(default=None, description="Citizen contact phone")
    anonymous: bool = Field(default=False, description="Whether caller wants to remain anonymous")
    alias: Optional[str] = Field(default=None, description="Safe citizen pseudonym")
    jurisdiction: Optional[str] = Field(default=None, description="Location / District")
    source_channel: str = Field(default="REST_API", description="Intake source")
    initial_statement: Optional[str] = Field(
        default=None, description="Initial transcript, text message, or report text"
    )


class IngestEvidenceRequest(BaseModel):
    """Payload to add multimodal evidence to an existing case."""

    evidence_type: EvidenceType
    content_raw: Optional[str] = None
    media_url: Optional[str] = None


class HITLConfirmationRequest(BaseModel):
    """Payload for human operator authorization of high-risk actions."""

    operator_id: str = Field(..., description="Unique ID of the police/public safety operator")
    secret_key: str = Field(..., description="Authorization token")
    decision: str = Field(default="APPROVED", description="'APPROVED' or 'REJECTED'")


@router.post(
    "",
    response_model=ExtortionCase,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Extortion Case and run automated SARA multi-agent triage",
)
async def create_case(req: CreateCaseRequest):
    """Initiates a new extortion investigation record and runs automated SARA triage if statement provided."""
    citizen = CitizenProfile(
        phone_number=req.citizen_phone,
        anonymous=req.anonymous,
        alias=req.alias,
        location_jurisdiction=req.jurisdiction,
    )
    case = ExtortionCase(
        citizen=citizen,
        source_channel=req.source_channel,
    )

    if req.initial_statement:
        evidence = EvidenceItem(
            case_id=case.case_id,
            evidence_type=EvidenceType.TEXT_MESSAGE,
            content_raw=req.initial_statement,
        )
        case.evidences.append(evidence)
        case = await orchestrator.run_full_pipeline(case, primary_evidence_text=req.initial_statement)
    else:
        await firestore_service.save_case(case)

    return case


@router.post(
    "/{case_id}/triage",
    response_model=ExtortionCase,
    summary="Execute Multi-Agent Triage & T_index computation on an existing case",
)
async def run_triage_on_case(case_id: str):
    """Executes the full SARA multi-agent pipeline on an existing case."""
    case = await firestore_service.get_case(case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Extortion case '{case_id}' not found.",
        )

    updated_case = await orchestrator.run_full_pipeline(case)
    return updated_case


@router.post(
    "/{case_id}/hitl/confirm",
    summary="Human-in-the-Loop Operator Confirmation for High-Risk Tactical Interventions (Lab 15)",
)
async def confirm_hitl_action(case_id: str, req: HITLConfirmationRequest):
    """Human-in-the-loop operator authorization gate."""
    case = await firestore_service.get_case(case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Extortion case '{case_id}' not found.",
        )

    success = hitl_gate.confirm_operator_approval(
        case=case,
        operator_id=req.operator_id,
        secret_key=req.secret_key,
        decision=req.decision,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid operator credentials or unauthorized signature.",
        )

    await firestore_service.save_case(case)
    return {
        "status": "CONFIRMED",
        "case_id": case.case_id,
        "operator_id": req.operator_id,
        "decision": req.decision,
    }


@router.get(
    "/analytics/heatmap",
    summary="Retrieve BigQuery analytical threat telemetry and geo-intelligence (Lab 18)",
)
async def get_threat_heatmap():
    """Returns aggregated threat records for operations center mapping."""
    return bigquery_service.get_aggregated_heatmap_data()


@router.get(
    "/typologies",
    summary="Retrieve RAG Forensic Knowledge Base criminal typologies (Lab 7)",
)
async def list_extortion_typologies():
    """Lists standard extortion profiles and legal references."""
    return forensic_rag.get_all_typologies()


@router.get(
    "/{case_id}",
    response_model=ExtortionCase,
    summary="Retrieve full case details, forensic artifacts, and T_index risk score",
)
async def get_case_by_id(case_id: str):
    """Fetches full case details including audit trail, evidence items, and calculated T_index."""
    case = await firestore_service.get_case(case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Extortion case '{case_id}' not found.",
        )
    return case


@router.get(
    "",
    response_model=List[ExtortionCase],
    summary="List recent extortion cases",
)
async def list_cases(limit: int = 50):
    """Returns list of recent cases for dashboard monitoring."""
    return await firestore_service.list_cases(limit=limit)
