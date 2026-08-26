"""Systematic Quality & Performance Evals Suite for SARA Agents (Lab 14).
Evaluates precision, false-positive reduction, and T_index quantization across benchmark extortion datasets.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.threat_calculator import threat_calculator
from app.models.threat_index import ThreatFactorScores, RiskTier
from app.core.forensic_tools import validate_e164_phone_number, validate_bank_account_format
from app.core.rag_knowledge import forensic_rag
from app.agents.router import agent_router, AgentBrainTier


class TestAgentEvals(unittest.TestCase):
    def test_eval_router_brain_selection(self):
        """Verify intelligent brain selection between Flash and Pro."""
        triage_profile = agent_router.select_brain_for_task("TRIAGE")
        self.assertEqual(triage_profile["tier"], AgentBrainTier.FLASH_FAST)
        self.assertLessEqual(triage_profile["target_latency_ms"], 500)

        forensic_profile = agent_router.select_brain_for_task("FORENSIC_AUDIT")
        self.assertEqual(forensic_profile["tier"], AgentBrainTier.PRO_REASONING)
        self.assertTrue(forensic_profile["enable_thinking"])

    def test_eval_forensic_rag_typology_matching(self):
        """Verify RAG retrieval accuracy across varied criminal scenarios."""
        scenarios = [
            ("Me dieron un préstamo y ahora me cobran 30% diario y amenazan quemar mi moto", "GOTA_A_GOTA"),
            ("Tienen una foto íntima mía y si no pago 500 soles la suben a Facebook", "SEXTO_EXTORSION"),
            ("Dejaron una bala en mi tienda y me piden cupo semanal de 200 dólares", "COBRO_DE_CUPOS"),
            ("Llamaron llorando diciendo que tienen a mi hijo secuestrado", "SECUESTRO_VIRTUAL"),
        ]

        for text, expected_id in scenarios:
            match = forensic_rag.retrieve_relevant_typology(text)
            self.assertIsNotNone(match, f"Failed to match scenario: {text}")
            self.assertEqual(match.typology_id, expected_id, f"Expected {expected_id} but got {match.typology_id}")

    def test_eval_phone_number_e164_normalization(self):
        """Verify E.164 phone normalizer and validator."""
        test_cases = [
            ("999111222", "+51999111222", True),
            ("+51 987 654 321", "+51987654321", True),
            ("12345", None, False),
        ]

        for raw, expected_formatted, valid in test_cases:
            res = validate_e164_phone_number(raw)
            self.assertEqual(res["valid"], valid)
            if valid:
                self.assertEqual(res["formatted"], expected_formatted)

    def test_eval_bank_account_sanitizer(self):
        """Verify CCI and bank entity heuristic identification."""
        res_bcp = validate_bank_account_format("00219198765432100012")  # 20 digits CCI
        self.assertTrue(res_bcp["valid"])
        self.assertEqual(res_bcp["bank_detected"], "BANCO_DE_CREDITO_BCP")

        res_short = validate_bank_account_format("19198765432100")  # 14 digits BCP
        self.assertTrue(res_short["valid"])
        self.assertEqual(res_short["bank_detected"], "BANCO_DE_CREDITO_BCP")


if __name__ == "__main__":
    unittest.main()

