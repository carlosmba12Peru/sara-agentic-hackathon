"""Unit tests for the Threat Index (T_index) mathematical calculator."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.threat_calculator import ThreatCalculator
from app.models.threat_index import ThreatFactorScores, RiskTier


class TestThreatCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = ThreatCalculator()
        self.sample_scores_high = ThreatFactorScores(
            coercion=85.0,
            persistence=80.0,
            artifacts=75.0,
            vulnerability=90.0,
        )
        self.sample_scores_low = ThreatFactorScores(
            coercion=20.0,
            persistence=15.0,
            artifacts=10.0,
            vulnerability=25.0,
        )

    def test_threat_calculator_high_risk(self):
        """Verify high risk calculation and tier assignment."""
        result = self.calculator.calculate(self.sample_scores_high)
        self.assertGreaterEqual(result.t_index, 70.0)
        self.assertEqual(result.tier, RiskTier.HIGH)
        self.assertGreater(len(result.recommended_actions), 0)
        self.assertTrue(any("INMEDIATO" in action for action in result.recommended_actions))

    def test_threat_calculator_low_risk(self):
        """Verify low risk calculation and tier assignment."""
        result = self.calculator.calculate(self.sample_scores_low)
        self.assertLess(result.t_index, 40.0)
        self.assertEqual(result.tier, RiskTier.LOW)
        self.assertGreater(len(result.recommended_actions), 0)

    def test_threat_calculator_bounds(self):
        """Verify that scores are strictly clamped between 0 and 100."""
        extreme_max = ThreatFactorScores(
            coercion=100.0,
            persistence=100.0,
            artifacts=100.0,
            vulnerability=100.0,
        )
        result_max = self.calculator.calculate(extreme_max)
        self.assertEqual(result_max.t_index, 100.0)
        self.assertEqual(result_max.tier, RiskTier.HIGH)

        extreme_min = ThreatFactorScores(
            coercion=0.0,
            persistence=0.0,
            artifacts=0.0,
            vulnerability=0.0,
        )
        result_min = self.calculator.calculate(extreme_min)
        self.assertEqual(result_min.t_index, 0.0)
        self.assertEqual(result_min.tier, RiskTier.LOW)


if __name__ == "__main__":
    unittest.main()
