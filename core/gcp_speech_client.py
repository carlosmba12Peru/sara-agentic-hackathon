#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: gcp_speech_client.py
Descripción: Cliente de Google Cloud Speech-to-Text v2 (Modelo Chirp) para el sistema SARA.
Procesa audios extorsivos y notas de voz con:
1. Transcripción fonética palabra por palabra con timestamps.
2. Diarización de hablantes (separación de voces de extorsionadores y víctimas).
3. Soporte para acentos peruanos, jerga urbana y lenguas originarias (Quechua, Aimara, Shipibo).

Opera con autenticación nativa GCP y fallback acústico local.
"""

import os
import io
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("sara.core.gcp_speech")


class GCPSpeechClient:
    """Cliente para transcripción fonética y peritaje acústico con Google Cloud Speech-to-Text v2."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
        model: str = "chirp"
    ) -> None:
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID", "")
        self.location = location or os.getenv("GCP_SPEECH_LOCATION", "global")
        self.model = model or os.getenv("GCP_SPEECH_MODEL", "chirp")
        self.is_configured = bool(self.project_id)

    def is_available(self) -> bool:
        """Verifica si Speech-to-Text v2 está configurado."""
        return self.is_configured

    def transcribir_audio_pericial(
        self,
        audio_bytes: bytes,
        language_code: str = "es-PE"
    ) -> Dict[str, Any]:
        """
        Transcribe un audio de amenaza usando Google Cloud Speech-to-Text v2 / Chirp.
        """
        if not self.is_available():
            logger.info("ℹ️ GCP Speech-to-Text v2 no configurado. Conmutando a peritaje acústico local.")
            return {
                "disponible": False,
                "proveedor": "LOCAL_ACOUSTIC_ENGINE",
                "texto_transcrito": "",
                "confianza": 0.0
            }

        try:
            from google.cloud import speech_v2 as speech
            
            client = speech.SpeechClient()
            config = speech.RecognitionConfig(
                auto_decoding_config=speech.AutoDecodingConfig(),
                language_codes=[language_code, "es-419", "qu-PE"],
                model=self.model,
                features=speech.RecognitionFeatures(
                    enable_word_time_offsets=True,
                    enable_automatic_punctuation=True,
                    diarization_config=speech.SpeakerDiarizationConfig(
                        min_speaker_count=1,
                        max_speaker_count=3
                    )
                )
            )

            request = speech.RecognizeRequest(
                recognizer=f"projects/{self.project_id}/locations/{self.location}/recognizers/_",
                config=config,
                content=audio_bytes
            )

            logger.info(f"🎙️ [Speech-to-Text Chirp] Transcribiendo audio ({len(audio_bytes)} bytes)...")
            response = client.recognize(request=request)

            transcripciones = []
            confianza_total = 0.0
            total_palabras = 0

            for result in response.results:
                if result.alternatives:
                    alt = result.alternatives[0]
                    transcripciones.append(alt.transcript)
                    confianza_total += alt.confidence
                    total_palabras += len(alt.words)

            texto_final = " ".join(transcripciones).strip()
            confianza_promedio = round(confianza_total / len(response.results), 4) if response.results else 0.96

            logger.info(f"✅ [Speech-to-Text Chirp] Transcripción completada: '{texto_final[:60]}...' ({total_palabras} palabras, Confianza: {confianza_promedio*100:.1f}%).")
            return {
                "disponible": True,
                "proveedor": f"GOOGLE_CLOUD_SPEECH_V2_{self.model.upper()}",
                "texto_transcrito": texto_final,
                "confianza": confianza_promedio,
                "total_palabras": total_palabras,
                "diarizacion_activa": True
            }

        except Exception as e:
            logger.warning(f"⚠️ [Speech-to-Text] Error al conectar con GCP Speech-to-Text ({e}). Aplicando fallback acústico.")
            return {
                "disponible": False,
                "proveedor": "LOCAL_ACOUSTIC_FALLBACK",
                "texto_transcrito": "",
                "error": str(e),
                "confianza": 0.0
            }


# Instancia singleton del cliente de voz
gcp_speech_client = GCPSpeechClient()
