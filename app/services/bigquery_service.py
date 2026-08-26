"""BigQuery Analytics & Threat Intelligence Streamer (Lab 10 & 18).
Streams threat indicators, geospatial coordinates, and T_index assessments for macro-level crime mapping.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timezone

from app.config import settings
from app.models.case import ExtortionCase

logger = logging.getLogger("sara.bigquery")


class BigQueryIntelligenceService:
    """Streams case analytics and threat telemetry into Google BigQuery."""

    def __init__(self):
        self.dataset_id = settings.BIGQUERY_DATASET
        self.table_id = settings.BIGQUERY_TABLE
        self._analytical_buffer: List[Dict[str, Any]] = []

    async def stream_threat_event(self, case: ExtortionCase) -> bool:
        """Stream real-time extortion case metrics into analytical storage."""
        if not case.threat_assessment:
            return False

        record = {
            "case_id": case.case_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "t_index": case.threat_assessment.t_index,
            "tier": case.threat_assessment.tier.value,
            "jurisdiction": case.citizen.location_jurisdiction or "DESCONOCIDO",
            "source_channel": case.source_channel,
            "artifacts_count": len(case.evidences[0].extracted_artifacts) if case.evidences else 0,
            "coercion_score": case.threat_assessment.factor_scores.coercion,
            "persistence_score": case.threat_assessment.factor_scores.persistence,
            "artifacts_score": case.threat_assessment.factor_scores.artifacts,
            "vulnerability_score": case.threat_assessment.factor_scores.vulnerability,
            "confidence": case.threat_assessment.confidence_score,
        }

        # If BigQuery client is available via google-cloud-bigquery in production:
        try:
            from google.cloud import bigquery
            if settings.GCP_PROJECT_ID:
                client = bigquery.Client(project=settings.GCP_PROJECT_ID)
                table_ref = f"{settings.GCP_PROJECT_ID}.{self.dataset_id}.{self.table_id}"
                errors = client.insert_rows_json(table_ref, [record])
                if not errors:
                    logger.info(f"Streamed case {case.case_id} to BigQuery table {table_ref}")
                    return True
                else:
                    logger.error(f"BigQuery stream insert errors: {errors}")
        except Exception as e:
            logger.debug(f"BigQuery live client not configured ({e}). Buffered in analytical memory.")

        self._analytical_buffer.append(record)
        return True

    def get_aggregated_heatmap_data(self) -> List[Dict[str, Any]]:
        """Return analytics for real-time dashboard heatmaps."""
        return self._analytical_buffer[-100:]


bigquery_service = BigQueryIntelligenceService()
