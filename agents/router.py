"""Enrutador Agéntico Inteligente de Modelos (Cognitive Dual-Brain Router).
Asigna de forma granular y dinámica los modelos Gemini de Google (Flash vs. Pro Reasoning)
según la complejidad cognitiva, exigencia de latencia y presupuesto de razonamiento (Reasoning Budget) de cada agente.

Arquitectura Dual-Brain (Google Cloud & Gemini 3.7):
1. TIER FLASH_FAST (gemini-3.7-flash):
   - Agentes: Centinela (Pre-Triaje y VAD Anti-Spam), Kallpa (Contención empática en Quechua/Castellano).
   - Perfil: Latencia objetivo <300ms, streaming instantáneo, temperatura 0.3.
2. TIER PRO_REASONING (gemini-3.7-pro):
   - Agentes: Analista Pro (Inteligencia Criminal), SubAgenteForenseExtractor (Visión OCR), Asesor Jurídico.
   - Perfil: Thinking Budget activado (hasta 2048 tokens), temperatura 0.1, razonamiento deductivo multi-salto.
"""

import os
import logging
from enum import Enum
from typing import Dict, Any, Optional

logger = logging.getLogger("sara.agents.router")

DEFAULT_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.7-flash")
DEFAULT_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.7-pro")


class AgentBrainTier(str, Enum):
    """Nivel de capacidad y razonamiento del modelo según la tarea cognitiva."""
    FLASH_FAST = "FLASH_FAST"          # <300ms: Triaje, contención ciudadana, filtrado de ruido
    PRO_REASONING = "PRO_REASONING"    # Inferencia profunda: OCR forense, correlación de bandas, fundamentación legal


class AgentRouter:
    """Enrutador inteligente de modelos Gemini para el Enjambre Multiagente SARA."""

    def __init__(self, flash_model: Optional[str] = None, pro_model: Optional[str] = None):
        self.flash_model = flash_model or DEFAULT_FLASH_MODEL
        self.pro_model = pro_model or DEFAULT_PRO_MODEL
        self.historial_enrutamiento: list = []

    def select_brain_for_task(self, task_type: str, context_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Determina qué modelo y perfil de inferencia despachar para cada agente.

        Args:
            task_type: Tipo de tarea ('TRIAGE', 'VOICE_INTAKE', 'EMPATHY_RESPONSE', 
                                    'FORENSIC_AUDIT', 'CRIMINAL_ANALYSIS', 'LEGAL_COMPLIANCE', 'T_INDEX')
            context_metadata: Metadatos opcionales (ej: tiene imágenes, audios o urgencia extrema)

        Returns:
            Dict con nombre del modelo, tier, temperatura, thinking_budget y latencia objetivo.
        """
        task_normalized = task_type.upper().strip()

        # Tareas de Respuesta Rápida y Baja Latencia (<300ms)
        if task_normalized in ("TRIAGE", "VOICE_INTAKE", "EMPATHY_RESPONSE", "PRE_FILTRADO", "CENTINELA", "KALLPA"):
            perfil = {
                "task_type": task_type,
                "model_name": self.flash_model,
                "tier": AgentBrainTier.FLASH_FAST,
                "temperature": 0.3,
                "enable_thinking": False,
                "thinking_budget": 0,
                "target_latency_ms": 300,
                "justificacion": "Optimizado para contención ciudadana empática y respuesta en tiempo real (<300ms)."
            }
            logger.info(f"Router assigned {AgentBrainTier.FLASH_FAST.value} ({self.flash_model}) for {task_type}")
        
        # Tareas de Análisis Profundo, Visión Forense y Fundamentación Legal
        else:
            perfil = {
                "task_type": task_type,
                "model_name": self.pro_model,
                "tier": AgentBrainTier.PRO_REASONING,
                "temperature": 0.1,
                "enable_thinking": True,
                "thinking_budget": 2048,
                "target_latency_ms": 1500,
                "justificacion": "Razonamiento deductivo multi-paso (Chain-of-Thought) para desarticulación criminal y auditoría legal."
            }
            logger.info(f"Router assigned {AgentBrainTier.PRO_REASONING.value} ({self.pro_model}) for {task_type}")

        self.historial_enrutamiento.append(perfil)
        return perfil

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de distribución de inferencia del enrutador."""
        total = len(self.historial_enrutamiento)
        flash_count = sum(1 for p in self.historial_enrutamiento if p["tier"] == AgentBrainTier.FLASH_FAST)
        pro_count = total - flash_count
        return {
            "total_enrutamientos": total,
            "flash_fast_count": flash_count,
            "pro_reasoning_count": pro_count,
            "proporcion_flash": (flash_count / total * 100) if total > 0 else 0.0,
            "proporcion_pro": (pro_count / total * 100) if total > 0 else 0.0
        }


# Instancias singleton del Enrutador
agent_router = AgentRouter()
router_agent = agent_router
