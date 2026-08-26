"""Dual-Brain Agent Router (Lab 2 & 8).
Intelligently delegates tasks between Gemini Flash (Fast Intake) and Gemini Pro (Deep Forensic Reasoning).
"""

import logging
from enum import Enum
from typing import Dict, Any, Optional

from app.config import settings

logger = logging.getLogger("sara.agents.router")


class AgentBrainTier(str, Enum):
    """Model tier selection based on task cognitive complexity."""

    FLASH_FAST = "FLASH_FAST"  # Sub-500ms voice intake, initial triage, conversational empathy
    PRO_REASONING = "PRO_REASONING"  # Deep multi-factor forensic calculus, legal RAG, threat index


class AgentRouter:
    """Routes cognitive tasks to the optimal Gemini model based on latency and complexity requirements."""

    def __init__(self):
        self.flash_model = settings.GEMINI_FLASH_MODEL
        self.pro_model = settings.GEMINI_PRO_MODEL

    def select_brain_for_task(self, task_type: str) -> Dict[str, Any]:
        """Determine which model and execution profile should be dispatched.

        Args:
            task_type: 'VOICE_INTAKE', 'TRIAGE', 'FORENSIC_AUDIT', 'T_INDEX_CALCULUS', 'LEGAL_COMPLIANCE'

        Returns:
            Dict containing selected model name, brain tier, and reasoning token profile.
        """
        if task_type in ("VOICE_INTAKE", "TRIAGE", "EMPATHY_RESPONSE"):
            logger.info(f"Router assigned {AgentBrainTier.FLASH_FAST.value} ({self.flash_model}) for {task_type}")
            return {
                "model_name": self.flash_model,
                "tier": AgentBrainTier.FLASH_FAST,
                "temperature": 0.3,
                "enable_thinking": False,
                "target_latency_ms": 300,
            }
        else:
            # Deep forensic or legal compliance
            logger.info(f"Router assigned {AgentBrainTier.PRO_REASONING.value} ({self.pro_model}) for {task_type}")
            return {
                "model_name": self.pro_model,
                "tier": AgentBrainTier.PRO_REASONING,
                "temperature": 0.1,
                "enable_thinking": True,
                "thinking_budget": 2048,
                "target_latency_ms": 1500,
            }


agent_router = AgentRouter()
