"""Agente Analista Técnico (Rama 1) - Inteligencia del Infractor.
Opera exclusivamente con el CUP (Código Único de Protección) sin conocer jamás datos personales de la víctima.
"""

import os
import re
import json
import logging
from typing import Dict, Any, Optional, List

# Importamos el Subagente Forense Extractor
from agents.forense_extractor import SubAgenteForenseExtractor

logger = logging.getLogger("sara.agents.analista")

ANALISTA_SYSTEM_INSTRUCTION = """
Eres el Agente Analista Técnico de SARA, especializado en inteligencia criminal y trazabilidad de infractores.
PRINCIPIO OBLIGATORIO DE PRIVACIDAD: Operas 100% a ciegas de los datos de la víctima. Tu único identificador de caso es el CUP.

Tus tareas:
1. Analizar la persistencia y modus operandi del infractor (ej. Gota a gota, cobro de cupos, sextorsión, secuestro virtual).
2. Clasificar los artefactos del infractor (números emisores de extorsión, cuentas receptoras de rescates/pagos).
3. Evaluar patrones de ingeniería social y amenazas tecnológicas basados en la pre-extracción forense.
4. PROTOCOLO ANTI-FALSOS POSITIVOS OSIPTEL (4,000 Celulares Robados/Día y Mercado Negro Las Malvinas):
   - El número telefónico reportado se clasifica estrictamente como VECTOR DE COMUNICACIÓN (altamente vulnerable a suplantación o terminal hurtado).
   - NUNCA imputar autoría delictiva penal al titular nominal de la línea telefónica sin cruce biométrico o coincidencia con el VECTOR FINANCIERO (cuenta bancaria / billetera digital receptora de los fondos).
   - Requerir automáticamente el bloqueo preventivo del código IMEI en <= 3 horas (Ley N° 32303).

Salida estrictamente en JSON:
{
    "cup": "string",
    "modus_operandi_tecnico": "string",
    "clasificacion_artefactos": {
        "telefonos_validados": ["string"],
        "cuentas_y_billeteras": ["string"],
        "geolocalizacion_aproximada_origen": "string"
    },
    "nivel_persistencia_infractor": "BAJA" | "MEDIA" | "ALTA" | "CRITICA",
    "indicadores_riesgo_digital": ["string"],
    "deslinde_suplantacion_telecom": "string",
    "paquete_forense_adjunto": {}
}
"""


class AnalistaAgent:
    """Agente de análisis forense enfocado exclusivamente en los datos del infractor."""

    def __init__(self):
        self.nombre = "Agente Analista (Perfilamiento Criminal)"
        self.sigla = "ANALISTA"
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-flash")
        # Instanciamos al subagente forense como dependencia directa con API Key
        self.forense_extractor = SubAgenteForenseExtractor(api_key=self.api_key)

    def analyze_offender_data(
        self, 
        cup: str, 
        pistas_infractor: Optional[Dict[str, Any]] = None,
        contexto_amenaza: str = "",
        tipo_evidencia: str = "Texto / Mensaje", 
        canal: str = "whatsapp", 
        origen_contacto: str = "Desconocido", 
        modalidad_masiva: bool = False,
        evidencias_digitales: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Orquesta la extracción forense inicial a través del subagente y 
        realiza el perfilamiento técnico del infractor vinculado al CUP.
        Soporta tanto firmas directas como la llamada del orquestador paralelo.
        """
        logger.info(f"🔍 [Analista] Ejecutando subagente forense para extracción del caso {cup}...")

        # Si no se pasó un origen explícito pero hay pistas de Kallpa, intentamos rescatarlo
        if pistas_infractor and (not origen_contacto or origen_contacto == "Desconocido"):
            telefonos = pistas_infractor.get("telefonos_sospechosos", [])
            origen_contacto = telefonos[0] if telefonos else "Desconocido"

        # 1. Delegar la ingesta multimedia al subagente forense
        json_forense_str = self.forense_extractor.procesar_evidencia(
            cup=cup,
            tipo_evidencia=tipo_evidencia,
            canal=canal,
            contenido=contexto_amenaza,
            origen_contacto=origen_contacto,
            modalidad_masiva=modalidad_masiva,
            evidencias_digitales=evidencias_digitales
        )
        paquete_forense = json.loads(json_forense_str)

        # 2. Consolidar pistas extraídas de evidencias y texto
        patrones_forenses = paquete_forense.get("metadatos_contacto", {}).get("patrones_exigencia", {})
        tels_forenses = patrones_forenses.get("telefonos_detectados", [])
        entidades_fin_forenses = patrones_forenses.get("entidades_financieras_detectadas", [])
        cuentas_forenses = [e.get("identificador") for e in entidades_fin_forenses if e.get("identificador")]
        
        pistas_base = pistas_infractor or {}
        tels_consolidados = list(dict.fromkeys((pistas_base.get("telefonos_sospechosos") or []) + tels_forenses + ([origen_contacto] if origen_contacto and origen_contacto != "Desconocido" else [])))
        cuentas_consolidadas = list(dict.fromkeys((pistas_base.get("cuentas_bancarias_mencionadas") or []) + cuentas_forenses))

        pistas_consolidadas = {
            "telefonos_sospechosos": tels_consolidados,
            "cuentas_bancarias_mencionadas": cuentas_consolidadas,
            "montos_exigidos": patrones_forenses.get("montos_exigidos", pistas_base.get("montos_exigidos", ["No especificado"]))
        }
        
        texto_analisis = contexto_amenaza or f"Canal: {canal}. Evidencia procesada."

        logger.info(f"🔍 [Analista] Analizando datos técnicos del infractor para caso {cup}...")

        api_key = (self.api_key or os.getenv("GEMINI_API_KEY", "")).strip()
        from core.llm_circuit_breaker import is_llm_available, report_quota_exhausted
        if is_llm_available() and api_key and len(api_key) > 20 and not api_key.startswith("your_"):
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                prompt = (
                    f"Caso ID (CUP): {cup}\n"
                    f"Resultado del Subagente Forense: {json.dumps(paquete_forense, ensure_ascii=False)}\n"
                    f"Pistas del infractor extraídas: {json.dumps(pistas_consolidadas, ensure_ascii=False)}\n"
                    f"Contexto de la amenaza: \"{texto_analisis}\"\n\n"
                    f"Genera el análisis técnico del infractor bajo Zero-PII estricto, integrando el paquete forense."
                )
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        "system_instruction": ANALISTA_SYSTEM_INSTRUCTION,
                        "response_mime_type": "application/json",
                    },
                )
                resultado_ia = json.loads(response.text)
                resultado_ia["paquete_forense_adjunto"] = paquete_forense
                
                # Integrar cruce PIDE autónomo si se detectaron artefactos
                try:
                    from agents.pide_agent import pide_agent
                    resultado_ia["perfil_inteligencia_pide"] = pide_agent.investigar_infractor_pide(
                        cup=cup,
                        telefonos_infractor=tels_consolidados,
                        cuentas_infractor=cuentas_consolidadas
                    )
                except Exception:
                    pass

                return resultado_ia
            except Exception as e:
                report_quota_exhausted(str(e))
                logger.error(f"Error en Analista ({e}). Usando análisis técnico heurístico.")

        return self._heuristic_analysis(cup, pistas_consolidadas, texto_analisis, paquete_forense)

    def _heuristic_analysis(self, cup: str, pistas: Dict[str, Any], contexto: str, paquete_forense: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis técnico determinista integrando la salida del subagente."""
        # Extraer entidades y patrones detectados por el subagente forense
        patrones_forenses = paquete_forense.get("metadatos_contacto", {}).get("patrones_exigencia", {})
        entidades_fin_raw = list(patrones_forenses.get("entidades_financieras_detectadas", []))
        plazos = patrones_forenses.get("plazos_temporales", ["No especificado"])
        armas = patrones_forenses.get("elementos_fisicos_detectados", [])

        # Deduplicación canónica de entidades financieras
        entidades_fin = []
        ids_ent_vistos = set()
        for e in entidades_fin_raw:
            id_c = re.sub(r"\D", "", str(e.get("identificador", "")))
            if id_c and id_c not in ids_ent_vistos:
                ids_ent_vistos.add(id_c)
                entidades_fin.append(e)

        # Normalización canónica de teléfonos
        def _norm_tel(t: str) -> Optional[str]:
            if not t:
                return None
            digs = re.sub(r"\D", "", str(t))
            if len(digs) == 11 and digs.startswith("519"):
                digs = digs[2:]
            if len(digs) == 9 and digs.startswith("9"):
                return f"+51 {digs[:3]} {digs[3:6]} {digs[6:]}"
            return None

        telefonos_raw = pistas.get("telefonos_sospechosos", []) + patrones_forenses.get("telefonos_detectados", [])
        telefonos_dict = {}
        for tel_item in telefonos_raw:
            tel_norm = _norm_tel(tel_item)
            if tel_norm:
                # Evitar que subcadenas de cuentas bancarias se cuelen como teléfonos
                digs_tel = re.sub(r"\D", "", tel_norm)[2:]
                if not any(digs_tel in e_id for e_id in ids_ent_vistos if len(e_id) >= 10):
                    telefonos_dict[tel_norm] = True
        telefonos = list(telefonos_dict.keys())

        cuentas_raw = list(ids_ent_vistos)

        lower = contexto.lower()
        modus = "Extorsión telefónica digital"
        if any(w in lower for w in ["transporte", "transportista", "chofer", "bus", "combi", "colectivo", "mexicanos", "piseros", "cuenta receptora", "paradero"]):
            modus = "Extorsión Celular Bifurcada a Transporte Público (WhatsApp + Cobro Yape/Billetera)"
        elif "gota" in lower or "préstamo" in lower:
            modus = "Esquema Usurero Coercitivo (Gota a Gota)"
        elif "cupo" in lower or "negocio" in lower or "local" in lower or "pollería" in lower:
            modus = "Cobro Sistemático de Cupos a Comercio"
        elif "foto" in lower or "video" in lower or "redes" in lower or "íntima" in lower:
            modus = "Chantaje Digital / Sextorsión"

        persistencia = "CRITICA" if (len(armas) > 0 or "transporte" in lower or "mexicanos" in lower) else "ALTA" if (len(telefonos) > 0 or len(cuentas_raw) > 0) else "MEDIA"

        clasificacion_medio = "NO_FISICO"
        try:
            clasificacion_medio = paquete_forense.get("evaluacion_multimedia", {}).get("clasificacion_medio", "NO_FISICO")
        except Exception:
            pass

        # Generar recomendaciones de actos de investigación para la Policía y Fiscalía
        diligencias_sugeridas = [
            "Solicitar a OSIPTEL levantamiento de titularidad y reporte de celdas/IMEI para los números extorsivos."
        ]
        if entidades_fin:
            for ent in entidades_fin:
                diligencias_sugeridas.append(
                    f"Requerir a la SBS y al {ent.get('entidad')} el congelamiento preventivo y levantamiento del secreto bancario de {ent.get('identificador')} (Ley N° 32209)."
                )
        if armas:
            diligencias_sugeridas.append(
                "Disponer inspección técnica criminalística y recojo balístico/explosivos en el predio agraviado."
            )

        # 3. Invocar autónomamente el cruce de inteligencia PIDE si hay pistas del infractor
        perfil_pide = None
        try:
            from agents.pide_agent import pide_agent
            perfil_pide = pide_agent.investigar_infractor_pide(
                pistas_infractor={
                    "telefonos_validados": telefonos,
                    "cuentas_y_billeteras": cuentas_raw,
                },
                cup=cup
            )
        except Exception as e:
            logger.warning(f"No se pudo completar el cruce PIDE en Analista ({e}). Continuando con análisis local.")

        calibres = patrones_forenses.get("calibres_y_balistica_detectados", [])
        metodos_ent = patrones_forenses.get("metodos_entrega_detectados", [])
        placas = patrones_forenses.get("placas_vehiculos_detectadas", [])
        jergas = patrones_forenses.get("jergas_hampa_detectadas", [])
        titulares = patrones_forenses.get("titulares_cuentas_detectados", [])

        return {
            "cup": cup,
            "modus_operandi_tecnico": modus,
            "clasificacion_artefactos": {
                "telefonos_validados": telefonos,
                "cuentas_y_billeteras": cuentas_raw,
                "titulares_cuentas": titulares,
                "entidades_financieras_identificadas": entidades_fin,
                "armas_o_elementos_fisicos": armas,
                "calibres_y_balistica": calibres,
                "metodos_entrega": metodos_ent,
                "placas_vehiculos": placas,
                "jergas_hampa": jergas,
                "plazos_y_ultimatums": plazos,
                "geolocalizacion_aproximada_origen": "Triangulación BTS Celular / Mensajería OTT" if telefonos else "Llamada celular / Mensajería OTT",
            },
            "nivel_persistencia_infractor": persistencia,
            "indicadores_riesgo_digital": [
                f"Canal de amenaza clasificado como: {clasificacion_medio} (Mininter 87% Digital / 13% Físico)",
                f"Exigencia económica activa: {pistas.get('montos_exigidos', ['No especificado'])}",
                f"Ultimátum temporal: {', '.join(plazos)}",
            ],
            "deslinde_suplantacion_telecom": (
                "PROTOCOLO OSIPTEL & POLICIAL (Ley N° 32303): Ante la tasa de 4,000 celulares robados al día en el mercado negro (Las Malvinas), "
                "el número telefónico se califica estrictamente como VECTOR DE COMUNICACIÓN pasible de suplantación. "
                "No se imputa autoría penal a la titularidad de la línea sin correlación pericial con el VECTOR FINANCIERO receptor."
            ),
            "diligencias_policiales_recomendadas": diligencias_sugeridas,
            "perfil_inteligencia_pide": perfil_pide,
            "paquete_forense_adjunto": paquete_forense
        }


analista_agent = AnalistaAgent()

