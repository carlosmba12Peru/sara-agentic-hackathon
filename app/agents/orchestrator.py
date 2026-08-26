"""SARA Master Multi-Agent Cognitive Orchestrator (Labs 2, 4, 8, 9, 10, 13, 15, 18).
Coordinates Triage, Forensic Audit, T_index Risk Computation, HITL Safety Gates, and BigQuery streaming.
"""

import logging
from typing import Optional

from app.models.case import ExtortionCase, CaseStatus, AuditEntry
from app.models.evidence import EvidenceItem, ForensicArtifact
from app.models.threat_index import ThreatFactorScores
from app.core.threat_calculator import threat_calculator
from app.core.hitl import hitl_gate
from app.agents.triage_agent import triage_agent
from app.agents.forensic_agent import forensic_agent
from app.agents.dispatch_agent import dispatch_agent
from app.agents.router import agent_router
from app.services.firestore_service import firestore_service
from app.services.bigquery_service import bigquery_service

logger = logging.getLogger("sara.agents.orchestrator")


class SARAOrchestrator:
    """Master Orchestrator managing end-to-end cognitive extortion response pipeline."""

    async def run_full_pipeline(
        self,
        case: ExtortionCase,
        primary_evidence_text: Optional[str] = None,
    ) -> ExtortionCase:
        """Run the complete multi-agent reasoning, self-correction, safety, and dispatch loop."""
        logger.info(f"--- Starting SARA Cognitive Pipeline for Case {case.case_id} ---")

        # 1. Determine raw text content from evidence or param
        content_to_analyze = primary_evidence_text
        if not content_to_analyze and case.evidences:
            content_to_analyze = case.evidences[0].content_raw or ""

        content_to_analyze = content_to_analyze or "Llamada de extorsión reportada sin texto detallado."

        # 2. Stage 1: Router & Triage Agent Intake (Flash Brain - Lab 2 & 8)
        triage_routing = agent_router.select_brain_for_task("TRIAGE")
        triage_result = await triage_agent.evaluate_intake(case, content_to_analyze)
        case.triage_summary = triage_result.get("summary", "")
        case.status = CaseStatus.TRIAGED
        case.audit_trail.append(
            AuditEntry(
                agent_name="TriageAgent",
                action="TRIAGE_INTAKE",
                details={
                    "model": triage_routing["model_name"],
                    "distress_level": triage_result.get("distress_level", "MODERATE"),
                    "modus_operandi": triage_result.get("modus_operandi", ""),
                },
            )
        )

        # 3. Stage 2: Forensic Agent Audit (Pro Brain + RAG + LoopAgent - Labs 3, 5, 7, 13)
        if not case.evidences:
            from app.models.evidence import EvidenceType
            case.evidences.append(
                EvidenceItem(
                    case_id=case.case_id,
                    evidence_type=EvidenceType.VOICE_TRANSCRIPT,
                    content_raw=content_to_analyze,
                )
            )

        forensic_routing = agent_router.select_brain_for_task("FORENSIC_AUDIT")
        forensic_result = await forensic_agent.audit_evidence(case, case.evidences[0])
        
        # Populate extracted artifacts
        case.evidences[0].extracted_artifacts = []
        for art in forensic_result.get("artifacts", []):
            case.evidences[0].extracted_artifacts.append(
                ForensicArtifact(
                    artifact_type=art.get("artifact_type", "OTHER"),
                    raw_value=art.get("raw_value", ""),
                    confidence=art.get("confidence", 1.0),
                    metadata=art.get("metadata", {}),
                )
            )
        case.evidences[0].threat_indicators = forensic_result.get("threat_indicators", [])
        case.status = CaseStatus.FORENSIC_AUDITED
        case.audit_trail.append(
            AuditEntry(
                agent_name="ForensicAgent",
                action="FORENSIC_AUDIT_WITH_GROUNDING",
                details={
                    "model": forensic_routing["model_name"],
                    "artifacts_count": str(len(case.evidences[0].extracted_artifacts)),
                    "thought_trace": forensic_result.get("thought_trace", "CoT Executed"),
                },
            )
        )

        # 4. Stage 3: Risk Engine & T_index Quantization
        scores = ThreatFactorScores(
            coercion=float(forensic_result.get("coercion_score", 50.0)),
            persistence=float(forensic_result.get("persistence_score", 40.0)),
            artifacts=float(forensic_result.get("artifacts_score", 30.0)),
            vulnerability=float(forensic_result.get("vulnerability_score", 50.0)),
        )

        threat_assessment = threat_calculator.calculate(
            scores=scores,
            reasoning=forensic_result.get("forensic_notes", ""),
            confidence=0.95,
        )
        case.threat_assessment = threat_assessment
        case.status = CaseStatus.RISK_EVALUATED
        case.audit_trail.append(
            AuditEntry(
                agent_name="RiskEngine",
                action="T_INDEX_CALCULATION",
                details={
                    "t_index": str(threat_assessment.t_index),
                    "tier": threat_assessment.tier.value,
                },
            )
        )

        # 5. Stage 4: Human-in-the-Loop Safety Gate (Lab 15)
        hitl_check = hitl_gate.evaluate_intervention_approval(case)
        if hitl_check["requires_approval"]:
            case.audit_trail.append(
                AuditEntry(
                    agent_name="HITL_SafetyGate",
                    action="HOLD_FOR_OPERATOR_APPROVAL",
                    details=hitl_check,
                )
            )

        # 6. Stage 5: Dispatch & Operational Coordination (Lab 11)
        await dispatch_agent.execute_dispatch(case)
        case.audit_trail.append(
            AuditEntry(
                agent_name="DispatchAgent",
                action="OPERATIONAL_DISPATCH",
                details={
                    "verification_token": case.verification_token or "",
                    "alerts_sent": ",".join(case.dispatch_alerts_sent),
                },
            )
        )

        # 7. Stage 6: Persistence in Firestore (Hot Ops) & BigQuery (Cold Analytics) (Labs 10, 18)
        await firestore_service.save_case(case)
        await bigquery_service.stream_threat_event(case)

        logger.info(
            f"--- SARA Pipeline Completed for Case {case.case_id} (T_index: {threat_assessment.t_index}, Tier: {threat_assessment.tier.value}) ---"
        )
        return case


orchestrator = SARAOrchestrator()
