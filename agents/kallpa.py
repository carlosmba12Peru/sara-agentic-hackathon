"""
Agente Amparo / Kallpa (Rama 0) - Módulo de compatibilidad.
Importa y reexporta el Agente Amparo (A.M.P.A.R.O. - Contención y Protección Ciudadana Línea 111).
"""

from agents.amparo import (
    AmparoAgent,
    KallpaAgent,
    amparo_agent,
    kallpa_agent,
    AMPARO_SYSTEM_INSTRUCTION,
    KALLPA_SYSTEM_INSTRUCTION
)

__all__ = [
    "AmparoAgent",
    "KallpaAgent",
    "amparo_agent",
    "kallpa_agent",
    "AMPARO_SYSTEM_INSTRUCTION",
    "KALLPA_SYSTEM_INSTRUCTION"
]
