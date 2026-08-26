"""Security and cryptography utilities for citizen protection and link verification."""

import hashlib
import secrets
from datetime import datetime, timezone


def generate_verification_token(case_id: str) -> str:
    """Generate a high-entropy cryptographic token for citizen verification."""
    random_hex = secrets.token_hex(16)
    timestamp = datetime.now(timezone.utc).isoformat()
    raw = f"{case_id}:{timestamp}:{random_hex}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def mask_sensitive_data(text: str) -> str:
    """Mask phone numbers or identification cards for privacy in logs."""
    if not text or len(text) <= 4:
        return "****"
    return f"{text[:2]}{'*' * (len(text) - 4)}{text[-2:]}"
