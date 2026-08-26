"""Forensic Audit Agent for SARA with Self-Correction Loop and Grounding (Lab 3, 5, 6, 7, 13).
Performs multimodal evidence inspection, forensic artifact extraction, and threat factor quantification.
"""

import json
import logging
import re
from typing import Dict, Any, List

from app.config import settings
from app.models.case import ExtortionCase
from app.models.evidence import EvidenceItem, ForensicArtifact
from app.core.rag_knowledge import forensic_rag
from app.core.forensic_tools import validate_e164_phone_number, validate_bank_account_format, calculate_distress_sentiment_index
from app.services.grounding_service import grounding_service

logger = logging.getLogger("sara.agents.forensic")

FORENSIC_SYSTEM_INSTRUCTION = """
You are SARA's Forensic Audit Agent, an expert AI investigator specialized in cybercrime and extortion analytics.
Your objective is to inspect multimodal evidence (voice transcripts, screenshots, OCR data, payment messages),
extract actionable forensic artifacts, correlate with criminal typologies, and quantify the 4 threat factor scores.

Required Output Schema (strictly JSON):
{
    "artifacts": [
        {
            "artifact_type": "PHONE" | "IBAN" | "CRYPTO_ADDRESS" | "ALIAS" | "DEMAND_AMOUNT" | "LOCATION",
            "raw_value": "string",
            "confidence": number (0.0 to 1.0),
            "metadata": {"key": "value"}
        }
    ],
    "threat_indicators": ["string"],
    "coercion_score": number (0.0 to 100.0),
    "persistence_score": number (0.0 to 100.0),
    "artifacts_score": number (0.0 to 100.0),
    "vulnerability_score": number (0.0 to 100.0),
    "forensic_notes": "string in Spanish",
    "thought_trace": "step-by-step reasoning steps (Lab 13)"
}
"""


class ForensicAgent:
    """Agent that audits evidence for forensic artifacts and computes factor scores with self-correction."""

    def __init__(self):
        self.model_name = settings.GEMINI_PRO_MODEL

    async def audit_evidence(
        self, case: ExtortionCase, evidence: EvidenceItem
    ) -> Dict[str, Any]:
        """Perform deep forensic evaluation on an ingested piece of evidence."""
        logger.info(f"ForensicAgent auditing evidence {evidence.evidence_id} for case {case.case_id}...")

        raw_text = evidence.content_raw or ""

        # 1. RAG Enrichment (Lab 7)
        matched_typology = forensic_rag.retrieve_relevant_typology(raw_text)
        typology_context = ""
        if matched_typology:
            typology_context = (
                f"\n[RAG Forensic Knowledge Base Match]\n"
                f"Typology: {matched_typology.name} ({matched_typology.legal_code_reference})\n"
                f"Modus Operandi: {matched_typology.modus_operandi_description}\n"
                f"Immediate Mitigation: {matched_typology.immediate_mitigation_advice}\n"
            )

        # 2. AI Model Execution (Gemini Pro with Thinking / Reasoning)
        result: Dict[str, Any] = {}
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                prompt = (
                    f"Evidence Type: {evidence.evidence_type.value}\n"
                    f"Content / Transcript / OCR:\n\"\"\"{raw_text}\"\"\"\n"
                    f"{typology_context}\n"
                    f"Perform deep forensic audit, artifact extraction, and quantitative scoring."
                )
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        "system_instruction": FORENSIC_SYSTEM_INSTRUCTION,
                        "response_mime_type": "application/json",
                    },
                )
                result = json.loads(response.text)
            except Exception as e:
                logger.error(f"Gemini forensic audit failed ({e}). Using deterministic forensic parser.")

        if not result:
            result = self._heuristic_forensic_audit(raw_text, matched_typology)

        # 3. Quality & Self-Correction Loop (Lab 5 - LoopAgent Pattern)
        validated_result = await self._run_self_correction_loop(result, raw_text)
        return validated_result

    async def _run_self_correction_loop(
        self, raw_result: Dict[str, Any], source_text: str
    ) -> Dict[str, Any]:
        """Self-correction loop validating and normalizing extracted artifacts (Lab 5)."""
        corrected_artifacts: List[Dict[str, Any]] = []

        for art in raw_result.get("artifacts", []):
            atype = art.get("artifact_type")
            aval = str(art.get("raw_value", ""))

            # Normalize and validate phone numbers
            if atype == "PHONE":
                val_res = validate_e164_phone_number(aval)
                if val_res["valid"]:
                    art["raw_value"] = val_res["formatted"]
                    art["metadata"]["e164_validated"] = "true"
                    # Grounding check (Lab 6)
                    ground_res = await grounding_service.check_artifact_reputation("PHONE", val_res["formatted"])
                    art["metadata"]["threat_intelligence"] = ground_res.get("summary", "")
                    corrected_artifacts.append(art)
            # Normalize and validate bank accounts
            elif atype in ("IBAN", "BANK_ACCOUNT"):
                acc_res = validate_bank_account_format(aval)
                if acc_res["valid"]:
                    art["raw_value"] = acc_res["sanitized"]
                    art["metadata"]["bank_entity"] = acc_res["bank_detected"]
                    art["metadata"]["account_type"] = acc_res["account_type"]
                    # Grounding check (Lab 6)
                    ground_res = await grounding_service.check_artifact_reputation("IBAN", acc_res["sanitized"])
                    art["metadata"]["threat_intelligence"] = ground_res.get("summary", "")
                    corrected_artifacts.append(art)
            else:
                corrected_artifacts.append(art)

        raw_result["artifacts"] = corrected_artifacts
        return raw_result

    def _heuristic_forensic_audit(self, text: str, typology: Any = None) -> Dict[str, Any]:
        """Regex-based forensic token extractor and factor quantizer."""
        artifacts: List[Dict[str, Any]] = []
        indicators: List[str] = []

        # Phone numbers regex
        phone_matches = re.findall(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}", text)
        for p in set(phone_matches):
            clean_p = p.strip()
            if len(clean_p) >= 7:
                artifacts.append({
                    "artifact_type": "PHONE",
                    "raw_value": clean_p,
                    "confidence": 0.95,
                    "metadata": {"source": "regex_extractor"},
                })

        # Bank accounts / IBAN / CCI regex
        bank_matches = re.findall(r"\b\d{10,24}\b", text)
        for b in set(bank_matches):
            artifacts.append({
                "artifact_type": "IBAN",
                "raw_value": b,
                "confidence": 0.90,
                "metadata": {"pattern": "numerical_account"},
            })

        # Currency / Demands
        money_matches = re.findall(r"(?:\$|S\/\.?|USD|EUR)\s?[\d,.]+|\b\d+\s?(?:dólares|soles|pesos|euros)\b", text, re.IGNORECASE)
        for m in set(money_matches):
            artifacts.append({
                "artifact_type": "DEMAND_AMOUNT",
                "raw_value": m,
                "confidence": 0.90,
                "metadata": {"type": "ransom_or_extortion_fee"},
            })

        # Calculate scores
        lower = text.lower()
        coercion = typology.default_coercion_baseline if typology else 50.0
        if any(w in lower for w in ["matar", "muerte", "balazo", "quemar", "familia", "hijos", "hoy", "bomba"]):
            coercion = 85.0
            indicators.append("Amenaza explícita de violencia física letal")

        persistence = 30.0
        if any(w in lower for w in ["insiste", "llamadas", "mensajes", "diario", "todos los días", "ya van"]):
            persistence = 75.0
            indicators.append("Patrón de contacto recurrente y hostigamiento")

        artifacts_score = min(100.0, max(20.0, float(len(artifacts) * 30.0)))
        vulnerability = calculate_distress_sentiment_index(text)

        notes = f"Se extrajeron {len(artifacts)} artefactos forenses verificables."
        if typology:
            notes += f" Tipología detectada: {typology.name}."

        return {
            "artifacts": artifacts,
            "threat_indicators": indicators,
            "coercion_score": coercion,
            "persistence_score": persistence,
            "artifacts_score": artifacts_score,
            "vulnerability_score": vulnerability,
            "forensic_notes": notes,
            "thought_trace": "1. Ingest evidence -> 2. Match RAG Typology -> 3. Extract tokens -> 4. Compute factors",
        }


forensic_agent = ForensicAgent()
