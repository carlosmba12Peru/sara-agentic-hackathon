"""
Agente Yachaq IA - Especialista en Lingüística Forense y Lenguas Originarias del Perú.
Módulo de acceso directo por identidad (Yachaq IA).
"""

from agents.traductor_originario import (
    AgenteTraductorOriginarias,
    yachaq_agent,
    traductor_originario_agent,
    CORPUS_DIALECTAL_PERUANO
)

# Alias de clase e instancia para máxima claridad
YachaqAgent = AgenteTraductorOriginarias
YachaqAgentClass = AgenteTraductorOriginarias

__all__ = [
    "YachaqAgent",
    "AgenteTraductorOriginarias",
    "yachaq_agent",
    "traductor_originario_agent",
    "CORPUS_DIALECTAL_PERUANO"
]
