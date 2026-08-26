"""Circuit Breaker para llamadas LLM a Google Gemini.
Previene bloqueos de red cuando la cuota Free-Tier se agota (HTTP 429) o no hay conexión.
"""

import time
import logging
from typing import Optional, Any

logger = logging.getLogger("sara.core.circuit_breaker")

# Estado global del interruptor de cuota
_QUOTA_EXHAUSTED = False
_LAST_CHECK_TIME = 0.0
_COOLDOWN_SECONDS = 25.0  # 25 segundos de descanso antes de reintentar si se agotó cuota


def is_llm_available() -> bool:
    """Retorna True si el canal LLM remoto está disponible y no está bloqueado por cuota."""
    global _QUOTA_EXHAUSTED, _LAST_CHECK_TIME
    if not _QUOTA_EXHAUSTED:
        return True
    if time.time() - _LAST_CHECK_TIME > _COOLDOWN_SECONDS:
        _QUOTA_EXHAUSTED = False
        return True
    return False


def report_quota_exhausted(error_msg: str = ""):
    """Registra que la cuota o conexión de la API remota falló y activa el interruptor anti-bloqueo."""
    global _QUOTA_EXHAUSTED, _LAST_CHECK_TIME
    err_low = str(error_msg).lower()
    trigger_words = [
        "429", "quota", "resource_exhausted", "rate limit", "exceeded",
        "404", "not_found", "not found",
        "aborted", "timeout", "timed out", "connection error", "503", 
        "500", "unavailable", "wsarecv", "connection reset", "broken pipe"
    ]
    if any(k in err_low for k in trigger_words):
        _QUOTA_EXHAUSTED = True
        _LAST_CHECK_TIME = time.time()
        logger.warning(f"⚡ [Circuit Breaker] Canal remoto inaccesible o agotado ({error_msg[:100]}...). Activando inferencia local determinista de alta velocidad.")


def reset_circuit_breaker():
    """Restablece el interruptor manualmente."""
    global _QUOTA_EXHAUSTED
    _QUOTA_EXHAUSTED = False
    logger.info("🔄 [Circuit Breaker] Estado restablecido. Habilitando llamadas remotas.")
