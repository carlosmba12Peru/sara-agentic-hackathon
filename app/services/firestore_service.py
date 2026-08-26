"""Google Cloud Firestore Service for persistent case and audit trail storage."""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timezone

from app.config import settings
from app.models.case import ExtortionCase, AuditEntry

logger = logging.getLogger("sara.firestore")

try:
    from google.cloud import firestore
    _HAS_FIRESTORE_SDK = True
except ImportError:
    _HAS_FIRESTORE_SDK = False
    logger.warning("google-cloud-firestore package not available. Using in-memory fallback.")


class FirestoreService:
    """Repository handling persistence of extortion cases in Firestore or memory fallback."""

    def __init__(self):
        self.client = None
        self._in_memory_db: Dict[str, dict] = {}
        self.collection_name = "extortion_cases"

        if _HAS_FIRESTORE_SDK:
            try:
                # Initialize Firestore client
                if settings.GCP_PROJECT_ID:
                    self.client = firestore.AsyncClient(
                        project=settings.GCP_PROJECT_ID,
                        database=settings.FIRESTORE_DATABASE,
                    )
                else:
                    self.client = firestore.AsyncClient()
                logger.info("Firestore AsyncClient initialized successfully.")
            except Exception as e:
                logger.warning(
                    f"Could not connect to Google Cloud Firestore ({e}). Using in-memory store."
                )
                self.client = None

    async def save_case(self, case: ExtortionCase) -> ExtortionCase:
        """Persist or update an extortion case document."""
        case.updated_at = datetime.now(timezone.utc)
        case_dict = case.model_dump(mode="json")

        if self.client:
            try:
                doc_ref = self.client.collection(self.collection_name).document(case.case_id)
                await doc_ref.set(case_dict)
                logger.info(f"Case {case.case_id} saved to Firestore.")
                return case
            except Exception as e:
                logger.error(f"Failed to save to Firestore ({e}). Falling back to memory.")

        self._in_memory_db[case.case_id] = case_dict
        logger.info(f"Case {case.case_id} saved in memory fallback.")
        return case

    async def get_case(self, case_id: str) -> Optional[ExtortionCase]:
        """Retrieve a case by its ID."""
        if self.client:
            try:
                doc_ref = self.client.collection(self.collection_name).document(case_id)
                doc = await doc_ref.get()
                if doc.exists:
                    return ExtortionCase(**doc.to_dict())
            except Exception as e:
                logger.error(f"Failed to query Firestore ({e}). Searching in-memory.")

        data = self._in_memory_db.get(case_id)
        if data:
            return ExtortionCase(**data)
        return None

    async def list_cases(self, limit: int = 50) -> List[ExtortionCase]:
        """List recent cases."""
        cases: List[ExtortionCase] = []
        if self.client:
            try:
                query = self.client.collection(self.collection_name).order_by(
                    "created_at", direction=firestore.Query.DESCENDING
                ).limit(limit)
                async for doc in query.stream():
                    cases.append(ExtortionCase(**doc.to_dict()))
                return cases
            except Exception as e:
                logger.error(f"Failed to list from Firestore ({e}). Using in-memory.")

        for item in list(self._in_memory_db.values())[:limit]:
            cases.append(ExtortionCase(**item))
        return cases

    async def append_audit_entry(self, case_id: str, entry: AuditEntry) -> None:
        """Append an audit log entry to a case."""
        case = await self.get_case(case_id)
        if case:
            case.audit_trail.append(entry)
            await self.save_case(case)


firestore_service = FirestoreService()
