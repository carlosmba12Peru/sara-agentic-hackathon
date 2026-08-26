"""Dispatch and Compliance Agent for SARA.
Coordinates emergency response playbooks, generates verification tokens, and dispatches operational alerts.
"""

import logging
from typing import Dict, Any, List

from app.core.security import generate_verification_token
from app.models.case import ExtortionCase, AuditEntry, CaseStatus
from app.models.threat_index import RiskTier
from app.services.notification_service import notification_service

logger = logging.getLogger("sara.agents.dispatch")


class DispatchAgent:
    """Agent that coordinates institutional dispatch, playbooks, and verification links."""

    async def execute_dispatch(self, case: ExtortionCase) -> Dict[str, Any]:
        """Execute dispatch workflow based on T_index risk tier."""
        logger.info(f"DispatchAgent coordinating response for case {case.case_id}...")

        # 1. Generate cryptographic citizen verification token if missing
        if not case.verification_token:
            case.verification_token = generate_verification_token(case.case_id)

        actions_taken: List[str] = []
        alerts_sent: List[str] = []

        # 2. Dispatch verification link
        citizen_link = await notification_service.send_citizen_verification(case)
        if citizen_link:
            actions_taken.append(f"Enlace de verificación generado: {citizen_link}")

        # 3. If HIGH or MEDIUM tier, trigger Ops Alert (Telegram / Make)
        if case.threat_assessment and case.threat_assessment.tier in (RiskTier.HIGH, RiskTier.MEDIUM):
            telegram_ok = await notification_service.send_operations_alert(case)
            if telegram_ok:
                alerts_sent.append("TELEGRAM_OPS_CHANNEL")
                actions_taken.append("Alerta prioritaria enviada al centro de comando por Telegram.")

            make_ok = await notification_service.trigger_make_webhook(case)
            if make_ok:
                alerts_sent.append("MAKE_AUTOMATION_HUB")
                actions_taken.append("Webhook de orquestación enviado a Make.com.")

        case.dispatch_alerts_sent = alerts_sent
        case.status = CaseStatus.DISPATCHED

        return {
            "status": "DISPATCHED",
            "actions_taken": actions_taken,
            "alerts_sent": alerts_sent,
            "verification_token": case.verification_token,
        }


dispatch_agent = DispatchAgent()
