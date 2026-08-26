"""Custom Forensic Tools and Quality Validators (Lab 3 & 5).
Equips agents with deterministic validators to eliminate alucinations and normalize artifacts.
"""

import re
from typing import Dict, Any, Optional


def validate_e164_phone_number(phone_raw: str, default_country_code: str = "+51") -> Dict[str, Any]:
    """Validates and formats a phone number into international E.164 format.

    Args:
        phone_raw: Raw string representing phone number.
        default_country_code: Country dial code fallback.

    Returns:
        Dict with validation status, formatted number, and carrier/country info.
    """
    cleaned = re.sub(r"[^\d+]", "", phone_raw.strip())

    if not cleaned:
        return {"valid": False, "formatted": None, "reason": "Empty number"}

    if cleaned.startswith("+"):
        digits_after_plus = cleaned[1:]
        is_valid = bool(re.match(r"^[1-9]\d{7,14}$", digits_after_plus))
        return {
            "valid": is_valid,
            "formatted": cleaned if is_valid else None,
            "length": len(cleaned),
            "dial_code": cleaned[:3] if is_valid else None,
        }

    if len(cleaned) == 9 and cleaned.startswith("9"):
        formatted = f"{default_country_code}{cleaned}"
        return {
            "valid": True,
            "formatted": formatted,
            "length": len(formatted),
            "dial_code": default_country_code,
        }
    elif len(cleaned) == 11 and cleaned.startswith("51"):
        formatted = f"+{cleaned}"
        return {
            "valid": True,
            "formatted": formatted,
            "length": len(formatted),
            "dial_code": "+51",
        }
    elif 7 <= len(cleaned) <= 8:
        formatted = f"{default_country_code}{cleaned}"
        return {
            "valid": True,
            "formatted": formatted,
            "length": len(formatted),
            "dial_code": default_country_code,
        }
    else:
        return {
            "valid": False,
            "formatted": None,
            "length": len(cleaned),
            "reason": "Invalid length for national/international phone",
        }


def validate_bank_account_format(account_raw: str) -> Dict[str, Any]:
    """Inspects bank account, CCI or IBAN format.

    Args:
        account_raw: Raw account or CCI digits.

    Returns:
        Dict with bank identification heuristic and length validation.
    """
    digits_only = re.sub(r"[^\d]", "", account_raw.strip())
    length = len(digits_only)

    bank_detected = "UNKNOWN_FINANCIAL_ENTITY"
    account_type = "ACCOUNT_NUMBER"

    if length == 20:
        account_type = "CCI_INTERBANCARIA"
        code_bank = digits_only[:3]
        bank_map = {
            "002": "BANCO_DE_CREDITO_BCP",
            "011": "BBVA_PERU",
            "003": "INTERBANK",
            "009": "SCOTIABANK",
            "018": "BANCO_DE_LA_NACION",
            "801": "YAPE_BCP_DIGITAL",
            "802": "PLIN_DIGITAL",
        }
        bank_detected = bank_map.get(code_bank, "FINANCIAL_INSTITUTION_REGISTERED")
    elif 13 <= length <= 14:
        account_type = "BCP_DIRECT_ACCOUNT"
        bank_detected = "BANCO_DE_CREDITO_BCP"
    elif 16 <= length <= 18:
        account_type = "BBVA_OR_INTERBANK_DIRECT"
        bank_detected = "COMMERCIAL_BANK"

    return {
        "valid": length >= 10,
        "sanitized": digits_only,
        "account_type": account_type,
        "bank_detected": bank_detected,
        "length": length,
    }


def calculate_distress_sentiment_index(text: str) -> float:
    """Analyzes text for emergency anxiety and panic indicators (0.0 to 100.0)."""
    if not text:
        return 0.0

    lower = text.lower()
    high_panic_keywords = ["ayuda", "socorro", "matar", "muerte", "hijos", "familia", "bomba", "desesperado", "miedo"]
    medium_stress_keywords = ["plata", "pagar", "amenaza", "extorsión", "denuncia", "policía", "temor", "preocupado"]

    score = 20.0
    for kw in high_panic_keywords:
        if kw in lower:
            score += 15.0

    for kw in medium_stress_keywords:
        if kw in lower:
            score += 8.0

    return min(100.0, max(0.0, score))
