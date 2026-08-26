"""Dynamic Extortion Threat Indexing (T_index) Calculator Engine.

This module implements the mathematical quantization formula:
    T_index = min(100, max(0, w_c * C + w_p * P + w_a * A + w_v * V))

Where:
    - C: Coercion / Physical Harm Immediacy (0-100)
    - P: Persistence / Frequency / Velocity (0-100)
    - A: Forensic Artifacts / Verifiability (0-100)
    - V: Target Profile Vulnerability (0-100)
"""

from typing import Dict, List, Tuple
from app.config import settings
from app.models.threat_index import ThreatFactorScores, ThreatIndexResult, RiskTier


class ThreatCalculator:
    """Mathematical engine to evaluate extortion severity objectively."""

    def __init__(
        self,
        weight_coercion: float = settings.WEIGHT_COERCION,
        weight_persistence: float = settings.WEIGHT_PERSISTENCE,
        weight_artifacts: float = settings.WEIGHT_ARTIFACTS,
        weight_vulnerability: float = settings.WEIGHT_VULNERABILITY,
    ):
        # Normalize weights if their sum is not exactly 1.0
        total_weight = weight_coercion + weight_persistence + weight_artifacts + weight_vulnerability
        if total_weight <= 0:
            total_weight = 1.0

        self.w_c = weight_coercion / total_weight
        self.w_p = weight_persistence / total_weight
        self.w_a = weight_artifacts / total_weight
        self.w_v = weight_vulnerability / total_weight

    def calculate(
        self,
        scores: ThreatFactorScores,
        reasoning: str = "",
        confidence: float = 0.95,
    ) -> ThreatIndexResult:
        """Compute the weighted T_index and categorize into RiskTier.

        Args:
            scores: Normalized scores for Coercion, Persistence, Artifacts, Vulnerability.
            reasoning: AI explanation of the assessment.
            confidence: Confidence score of the assessment.

        Returns:
            ThreatIndexResult with calculated index, tier, and recommended actions.
        """
        # Weighted sum
        raw_index = (
            self.w_c * scores.coercion
            + self.w_p * scores.persistence
            + self.w_a * scores.artifacts
            + self.w_v * scores.vulnerability
        )

        # Clamping to [0.0, 100.0] and rounding to 2 decimal places
        t_index = round(min(100.0, max(0.0, raw_index)), 2)

        tier, recommended_actions = self._evaluate_tier_and_actions(t_index, scores)

        weights_dict: Dict[str, float] = {
            "weight_coercion": round(self.w_c, 4),
            "weight_persistence": round(self.w_p, 4),
            "weight_artifacts": round(self.w_a, 4),
            "weight_vulnerability": round(self.w_v, 4),
        }

        return ThreatIndexResult(
            t_index=t_index,
            tier=tier,
            factor_scores=scores,
            factor_weights=weights_dict,
            reasoning=reasoning or self._generate_default_reasoning(t_index, tier, scores),
            recommended_actions=recommended_actions,
            confidence_score=confidence,
        )

    def _evaluate_tier_and_actions(
        self, t_index: float, scores: ThreatFactorScores
    ) -> Tuple[RiskTier, List[str]]:
        """Assign risk tier and standard operational playbooks."""
        actions: List[str] = []

        if t_index >= 70.0:
            tier = RiskTier.HIGH
            actions.append("🚨 INMEDIATO: Notificar a la unidad táctica de respuesta contra extorsión.")
            actions.append("🔒 Generar enlace criptográfico de verificación y protección para el ciudadano.")
            actions.append("📱 Bloqueo preventivo y monitoreo en tiempo real de números y cuentas asociadas.")
            if scores.coercion >= 80.0:
                actions.append("🛡️ Ofrecer protocolo de resguardo físico y geolocalización de seguridad.")
        elif t_index >= 40.0:
            tier = RiskTier.MEDIUM
            actions.append("📋 Registrar caso en expediente activo de investigación policial.")
            actions.append("🔍 Cruzar artefactos (cuentas bancarias, teléfonos) con base de datos de extorsión recurrente.")
            actions.append("✉️ Enviar guía preventiva de no-pago y medidas de contención al ciudadano.")
        else:
            tier = RiskTier.LOW
            actions.append("🤖 Clasificado como intento de estafa genérica / llamada automatizada.")
            actions.append("💡 Enviar recomendaciones de seguridad digital y bloqueo de número en dispositivo.")
            actions.append("📊 Archivar en repositorio de inteligencia de bajo impacto.")

        return tier, actions

    def _generate_default_reasoning(
        self, t_index: float, tier: RiskTier, scores: ThreatFactorScores
    ) -> str:
        """Generate structured analytical reasoning text."""
        return (
            f"Evaluación T_index = {t_index}/100 clasificada en nivel {tier.value}. "
            f"Factores clave: Coerción={scores.coercion:.1f} (peso {self.w_c*100:.0f}%), "
            f"Persistencia={scores.persistence:.1f} (peso {self.w_p*100:.0f}%), "
            f"Artefactos={scores.artifacts:.1f} (peso {self.w_a*100:.0f}%), "
            f"Vulnerabilidad={scores.vulnerability:.1f} (peso {self.w_v*100:.0f}%)."
        )


threat_calculator = ThreatCalculator()
