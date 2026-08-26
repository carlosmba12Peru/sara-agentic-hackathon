"""Pruebas Unitarias para el Agente Enrutador Inteligente (Dual-Brain Router)."""

import unittest
from agents.router import agent_router, AgentBrainTier


class TestAgentRouter(unittest.TestCase):

    def test_router_triage_assignment(self):
        """Verifica que las tareas de triaje y contención se asignen a FLASH_FAST."""
        profile = agent_router.select_brain_for_task("TRIAGE")
        self.assertEqual(profile["tier"], AgentBrainTier.FLASH_FAST)
        self.assertEqual(profile["target_latency_ms"], 300)
        self.assertFalse(profile["enable_thinking"])

    def test_router_voice_intake_assignment(self):
        """Verifica que la recepción de notas de voz en Kallpa use FLASH_FAST."""
        profile = agent_router.select_brain_for_task("VOICE_INTAKE")
        self.assertEqual(profile["tier"], AgentBrainTier.FLASH_FAST)

    def test_router_forensic_audit_assignment(self):
        """Verifica que las tareas de visión OCR y desarticulación criminal usen PRO_REASONING."""
        profile = agent_router.select_brain_for_task("FORENSIC_AUDIT")
        self.assertEqual(profile["tier"], AgentBrainTier.PRO_REASONING)
        self.assertTrue(profile["enable_thinking"])
        self.assertEqual(profile["thinking_budget"], 2048)

    def test_router_legal_compliance_assignment(self):
        """Verifica que la fundamentación del Asesor Jurídico use PRO_REASONING."""
        profile = agent_router.select_brain_for_task("LEGAL_COMPLIANCE")
        self.assertEqual(profile["tier"], AgentBrainTier.PRO_REASONING)

    def test_router_stats(self):
        """Verifica que el enrutador lleve estadísticas de inferencia."""
        stats = agent_router.get_stats()
        self.assertIn("total_enrutamientos", stats)
        self.assertIn("flash_fast_count", stats)
        self.assertIn("pro_reasoning_count", stats)


if __name__ == "__main__":
    unittest.main()
