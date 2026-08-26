"""Human-in-the-Loop (HITL) Safety Gate and Operational Authorization (Lab 15).
Ensures high-stakes irreversible interventions (police tactical dispatch, bank freeze) require human confirmation.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.config import settings
from app.models.case import ExtortionCase, AuditEntry
from app.models.threat_index import RiskTier

logger = logging.getLogger("sara.hitl")


class HumanInTheLoopGate:
    """Safety guardrail that intercepts and enforces human confirmation on critical actions."""

    def evaluate_intervention_approval(
        self, case: ExtortionCase
    ) -> Dict[str, Any]:
        """Check if the case requires human operator sign-off before tactical dispatch."""
        if not settings.REQUIRE_HITL_FOR_HIGH_RISK:
            return {"requires_approval": False, "status": "AUTO_AUTHORIZED"}

        is_high_risk = bool(
            case.threat_assessment and case.threat_assessment.tier == RiskTier.HIGH
        )

        if is_high_risk:
            logger.info(
                f"HITL Safety Gate activated: Case {case.case_id} classified as HIGH RISK. Awaiting operator confirmation."
            )
            return {
                "requires_approval": True,
                "status": "PENDING_OPERATOR_APPROVAL",
                "reason": "Tactical police escalation requires Human-in-the-Loop confirmation.",
                "pending_actions": [
                    "Despacho táctico de unidad especializada PNP/Fiscalía",
                    "Emisión de orden de alerta bancaria a SBS/Unidad de Inteligencia Financiera",
                ],
            }

        return {"requires_approval": False, "status": "APPROVED_AUTOMATICALLY"}

    def confirm_operator_approval(
        self, case: ExtortionCase, operator_id: str, secret_key: str, decision: str = "APPROVED"
    ) -> bool:
        """Process human operator decision to approve or reject high-risk actions."""
        if secret_key != settings.HITL_SECRET_KEY:
            logger.warning(f"Invalid secret key provided by operator {operator_id}")
            return False

        now = datetime.now(timezone.utc)
        case.audit_trail.append(
            AuditEntry(
                agent_name="HITL_SafetyGate",
                action=f"OPERATOR_{decision.upper()}",
                details={
                    "operator_id": operator_id,
                    "timestamp": now.isoformat(),
                    "decision": decision,
                },
            )
        )
        logger.info(f"Operator {operator_id} confirmed {decision} for Case {case.case_id}")
        return True


hitl_gate = HumanInTheLoopGate()
