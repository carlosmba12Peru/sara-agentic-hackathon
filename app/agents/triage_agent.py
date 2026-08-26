"""Triage Agent for SARA.
Handles initial distress intake, empathy-guided communication, and cognitive situation summarization.
"""

import json
import logging
from typing import Dict, Any, Optional

from app.config import settings
from app.models.case import ExtortionCase, AuditEntry

logger = logging.getLogger("sara.agents.triage")

TRIAGE_SYSTEM_INSTRUCTION = """
You are SARA's Cognitive Triage Agent, a specialized AI for emergency extortion intake and public safety.
Your primary role is to evaluate distress transcripts or messages from citizens facing extortion threats.

Key responsibilities:
1. Extract the core extortion modus operandi (e.g., gota a gota, sextortion, kidnapping hoax, business cartel threat).
2. Assess immediate citizen distress level (MILD, MODERATE, CRITICAL).
3. Identify urgency indicators (active deadline, physical surveillance, immediate threat to family).
4. Provide a structured concise cognitive summary in Spanish for public safety operators.

Output strictly valid JSON with this schema:
{
    "modus_operandi": "string",
    "distress_level": "MILD" | "MODERATE" | "CRITICAL",
    "urgency_indicators": ["string"],
    "summary": "string in Spanish",
    "preliminary_coercion_score": number (0-100),
    "caller_vulnerability_notes": "string"
}
"""


class TriageAgent:
    """Agent that performs cognitive triage on raw citizen statements and distress signals."""

    def __init__(self):
        self.model_name = settings.GEMINI_MODEL

    async def evaluate_intake(self, case: ExtortionCase, raw_content: str) -> Dict[str, Any]:
        """Perform triage analysis on the raw evidence or call transcript."""
        logger.info(f"TriageAgent analyzing case {case.case_id}...")

        # If Gemini API Key is available, use Gemini model
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                prompt = (
                    f"Citizen Statement / Call Transcript:\n"
                    f"\"\"\"{raw_content}\"\"\"\n\n"
                    f"Citizen Context: Anonymous={case.citizen.anonymous}, "
                    f"Jurisdiction={case.citizen.location_jurisdiction or 'Unspecified'}\n"
                    f"Perform cognitive extortion triage according to instructions."
                )
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        "system_instruction": TRIAGE_SYSTEM_INSTRUCTION,
                        "response_mime_type": "application/json",
                    },
                )
                result = json.loads(response.text)
                return result
            except Exception as e:
                logger.error(f"Gemini triage evaluation failed ({e}). Using deterministic heuristics.")

        # Deterministic cognitive fallback if offline or no key
        return self._heuristic_triage(raw_content)

    def _heuristic_triage(self, text: str) -> Dict[str, Any]:
        """Rule-based heuristic triage analyzer."""
        lower_text = text.lower()
        distress = "MODERATE"
        coercion = 50.0
        urgency = []
        modus = "Extorsión telefónica / amenaza digital"

        if any(w in lower_text for w in ["matar", "muerte", "familia", "hijos", "arma", "disparo", "bomba", "hoy mismo", "ahora"]):
            distress = "CRITICAL"
            coercion = 85.0
            urgency.append("Amenaza inminente contra la vida o integridad física.")

        if any(w in lower_text for w in ["plata", "dinero", "cuenta", "banco", "yape", "transferencia", "dólares", "soles", "pago"]):
            urgency.append("Exigencia económica activa con solicitud de pago.")

        if any(w in lower_text for w in ["gota a gota", "préstamo", "cobro"]):
            modus = "Extorsión por esquema de micro-préstamo (Gota a Gota)"
        elif any(w in lower_text for w in ["foto", "video", "íntimo", "desnudo", "facebook", "redes"]):
            modus = "Sextorsión / Amenaza de difusión de material privado"
        elif any(w in lower_text for w in ["negocio", "local", "tienda", "cupo", "vacuna"]):
            modus = "Cobro de cupos a negocio / comercio"

        summary = (
            f"El denunciante reporta {modus.lower()}. "
            f"Se detecta nivel de coerción preliminar de {coercion}/100. "
            f"Nivel de angustia del ciudadano: {distress}."
        )

        return {
            "modus_operandi": modus,
            "distress_level": distress,
            "urgency_indicators": urgency,
            "summary": summary,
            "preliminary_coercion_score": coercion,
            "caller_vulnerability_notes": "Ciudadano en situación de estrés agudo.",
        }


triage_agent = TriageAgent()
