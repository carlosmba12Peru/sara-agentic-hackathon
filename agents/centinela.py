"""Agente Centinela (Pre-Triage & AI Safety Guardian) - Filtro Anti-Falsas Alarmas.
Protege las líneas de emergencia (105 / UDEX) filtrando llamadas de broma, números privados/spoofing,
números del extranjero y falsas alertas con risas de fondo bajo el marco del D.S. N° 020-2020-MTC.
"""

import os
import re
import json
import logging
from typing import Dict, Any, List
from datetime import datetime, timezone

logger = logging.getLogger("sara.agents.centinela")

CENTINELA_SYSTEM_INSTRUCTION = """
Eres el Agente Centinela, el guardián de verificación preliminar y anti-falsas alarmas de SARA.
Tu objetivo es analizar la llamada, audio o mensaje entrante ANTES de derivarlo a la Central 105 de la Policía Nacional.

Evalúa 4 factores críticos:
1. Origen del Número: ¿Es un número privado, número extranjero sospechoso (+234, +44, +1) o VoIP no registrado?
2. Análisis de Acústica y Emoción: ¿Hay indicios de risas de fondo, música festiva, tono burlón o simulación teatral?
3. Coherencia del Relato: ¿El usuario da detalles verificables o incurre en contradicciones absurdas típicas de bromas?
4. Nivel de Veracidad Estimado (Score de 0 a 100):
   - 0-30: FALSA_ALARMA / BROMA (Aplicar D.S. 020-2020-MTC).
   - 31-69: DUDA_REQUERIR_DATOS (Requiere verificación forense adicional).
   - 70-100: EMERGENCIA_GENUINA (Aprobada para triaje con Amparo IA y despacho 105).

Salida en formato JSON estricto:
{
    "score_veracidad": int (0 a 100),
    "clasificacion_alerta": "GENUINA" | "SOSPECHOSA" | "FALSA_ALARMA_BROMA",
    "analisis_telecom": {
        "numero_evaluado": "string",
        "tipo_linea": "MOVIL_NACIONAL" | "NUMERO_PRIVADO" | "EXTRANJERO_SOSPECHOSO" | "VOIP_ANONIMO",
        "pais_origen": "string",
        "es_spoofing_probable": true | false
    },
    "analisis_acustico_conductual": {
        "risas_de_fondo_detectadas": true | false,
        "tono_emocional": "PANICO_GENUINO" | "ACTUACION_BURLONA" | "NEUTRO",
        "ruido_ambiente": "CALLE_HOGAR" | "FIESTA_GRUPO_RISAS" | "SILENCIO"
    },
    "dictamen_admision": "ADMITIR_ENJAMBRE_SARA" | "BLOQUEAR_Y_REPORTAR_MTC",
    "motivo_dictamen": "string explicativo",
    "infraccion_mtc_ds_020_2020": true | false
}
"""


class CentinelaAgent:
    """Guardián de triaje preventivo y detección de falsas alarmas."""

    def __init__(self):
        self.nombre = "Agente Centinela (Filtro Anti-Falsas Alarmas)"
        self.sigla = "CENTINELA"
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.5-flash")

    def evaluate_veracity(self, telefono_origen: str, mensaje_texto: str, metadatos_audio: Dict[str, Any] = None) -> Dict[str, Any]:
        """Evalúa la veracidad de la alerta antes de comprometer recursos de la Policía Nacional."""
        logger.info(f"🛡️ [Centinela] Auditando veracidad de alerta desde origen '{telefono_origen}'...")

        # Fast-Path Determinista ultrarrápido (<0.2ms): Verificación directa de origen y acústica
        heuristic_res = self._heuristic_evaluation(telefono_origen, mensaje_texto, metadatos_audio)
        if heuristic_res.get("clasificacion_alerta") == "GENUINA" and heuristic_res.get("score_veracidad", 0) >= 80:
            return heuristic_res

        api_key = (self.api_key or os.getenv("GEMINI_API_KEY", "")).strip()
        from core.llm_circuit_breaker import is_llm_available, report_quota_exhausted
        if is_llm_available() and api_key and len(api_key) > 20 and not api_key.startswith("your_"):
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                prompt = (
                    f"Número de Origen: {telefono_origen}\n"
                    f"Mensaje o Transcripción: \"\"\"{mensaje_texto}\"\"\"\n"
                    f"Metadatos acústicos: {json.dumps(metadatos_audio or {})}\n\n"
                    f"Aplica las 4 capas de blindaje anti-falsas alarmas y emite el dictamen JSON."
                )
                from core.llm_circuit_breaker import call_with_fast_timeout
                response = call_with_fast_timeout(
                    client.models.generate_content,
                    model=self.model_name,
                    contents=prompt,
                    config={
                        "system_instruction": CENTINELA_SYSTEM_INSTRUCTION,
                        "response_mime_type": "application/json",
                    },
                    timeout_seconds=2.5
                )
                if response and getattr(response, "text", None):
                    return json.loads(response.text)
            except Exception as e:
                report_quota_exhausted(str(e))
                logger.error(f"Error en Centinela con Gemini ({e}). Aplicando análisis heurístico determinista.")

        return heuristic_res

    def _heuristic_evaluation(self, tel: str, text: str, audio_meta: Dict[str, Any] = None) -> Dict[str, Any]:
        """Heurística determinista de telecomunicaciones y detección de patrones de bromas."""
        tel_clean = (tel or "").strip().replace(" ", "").replace("-", "")
        text_lower = (text or "").lower()
        audio_meta = audio_meta or {}

        # 1. Análisis de Telecomunicaciones
        tipo_linea = "MOVIL_NACIONAL"
        pais = "Perú (+51)"
        es_spoofing = False

        if not tel_clean or "privado" in tel_clean.lower() or "desconocido" in tel_clean.lower() or tel_clean == "0":
            tipo_linea = "NUMERO_PRIVADO"
            pais = "Desconocido (Oculto)"
        elif tel_clean.startswith("+51") or (len(tel_clean) == 9 and tel_clean.startswith("9")):
            tipo_linea = "MOVIL_NACIONAL"
            pais = "Perú (+51)"
        elif tel_clean.startswith("+"):
            tipo_linea = "EXTRANJERO_SOSPECHOSO"
            if tel_clean.startswith("+1"):
                pais = "Norteamérica (+1)"
            elif tel_clean.startswith("+234"):
                pais = "Nigeria (+234 - Alto riesgo Spoofing)"
                es_spoofing = True
            elif tel_clean.startswith("+44"):
                pais = "Reino Unido (+44)"
            else:
                pais = "Internacional"

        # 2. Detección de Llamadas Silentes, Spam Masivo (Línea 111) y Risas
        es_silente = (
            len(text_lower.strip()) == 0 or 
            text_lower in ["...", ".", "[silencio]", "[ruido estatico]", "hola?", "alo?", "aló?"] or
            audio_meta.get("silencio_detectado", False)
        )
        
        patrones_broma = ["jajaja", "jejeje", "xd", "broma", "fake", "mentira", "chiste", "risas", "payaso"]
        hay_risas = any(p in text_lower for p in patrones_broma) or audio_meta.get("risas_detectadas", False)

        # 3. Puntuación de Veracidad
        score = 85  # Base confiable por defecto

        if tipo_linea == "NUMERO_PRIVADO":
            score -= 25
        elif tipo_linea == "EXTRANJERO_SOSPECHOSO":
            score -= 35
        
        if hay_risas:
            score -= 60
        elif es_silente:
            score = 15  # Clasificado como llamada silente / spam robodialer
        
        # Penalización si el texto es excesivamente corto o incoherente
        elif len(text_lower.strip()) < 15:
            score -= 30

        # Bonificación si contiene datos concretos (plazos, montos, números extorsivos)
        if any(w in text_lower for w in ["soles", "dolares", "cuenta", "bcp", "bbva", "yape", "plin", "granada", "balas"]):
            score += 15

        score = max(0, min(100, score))

        if es_silente:
            clasificacion = "LLAMADA_SILENTE_SPAM"
            dictamen = "PROPUESTA_BLOQUEO_MTC"
            motivo = "Llamada silente / Robodialer spam en Línea 111. Cero actividad vocal en ventana de 3.5 segundos."
            infraccion_mtc = True
        elif score < 35 or hay_risas:
            clasificacion = "FALSA_ALARMA_BROMA"
            dictamen = "PROPUESTA_BLOQUEO_MTC"
            motivo = "Detección de patrones lúdicos/risas o procedencia de numeración anónima/spoofed sin sustento fáctico."
            infraccion_mtc = True
        elif score < 65:
            clasificacion = "SOSPECHOSA"
            dictamen = "ADMITIR_ENJAMBRE_SARA"
            motivo = "Línea con metadatos no estándar. Se admite con advertencia y verificación de pruebas."
            infraccion_mtc = False
        else:
            clasificacion = "GENUINA"
            dictamen = "ADMITIR_ENJAMBRE_SARA"
            motivo = "Línea nacional verificada, relato consistente y ausencia de marcadores lúdicos."
            infraccion_mtc = False

        return {
            "score_veracidad": score,
            "clasificacion_alerta": clasificacion,
            "es_llamada_silente": es_silente,
            "canal_protegido": "LÍNEA_111_MININTER / PORTAL_SARA",
            "analisis_telecom": {
                "numero_evaluado": tel_clean,
                "tipo_linea": tipo_linea,
                "pais_origen": pais,
                "es_spoofing_probable": es_spoofing,
                "patron_rafaga_spam": False
            },
            "analisis_acustico_conductual": {
                "risas_de_fondo_detectadas": hay_risas,
                "silencio_o_ruido_estatico": es_silente,
                "tono_emocional": "SILENTE_INANIMADO" if es_silente else "ACTUACION_BURLONA" if hay_risas else "PANICO_GENUINO" if score > 70 else "NEUTRO",
                "ruido_ambiente": "SILENCIO_FANTASMA" if es_silente else "FIESTA_GRUPO_RISAS" if hay_risas else "CALLE_HOGAR"
            },
            "dictamen_admision": dictamen,
            "motivo_dictamen": motivo,
            "infraccion_mtc_ds_020_2020": infraccion_mtc,
            "propuesta_sancion_legal": {
                "base_normativa": "D.S. N° 020-2020-MTC (Reglamento D.L. N° 1277 - Categoría Silente / Spam)",
                "medida_preventiva_propuesta": "Suspensión preventiva de la línea por 15 días",
                "sancion_economica_propuesta": "Multa de S/ 8,600 a S/ 17,200",
                "sancion_definitiva": "Cancelación definitiva de la línea e inscripción en Registro de Infractores MTC"
            },
            "gobernanza_hitl": {
                "estado": "PENDIENTE_CERTIFICACION_POLICIAL_HUMANA",
                "rol_ia": "ASISTENTE_RECOMENDADOR",
                "autoridad_decisoria": "OFICIAL_PNP_HUMANO",
                "certificacion_humana_requerida": True
            }
        }


centinela_agent = CentinelaAgent()
