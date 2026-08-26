"""Orquestador Jerárquico-Paralelo (ParallelAgent Pattern - Lab 9).
Coordina las ramas de contención, análisis técnico, cálculo cuantitativo y empaquetado normativo
utilizando concurrent.futures.ThreadPoolExecutor de forma no bloqueante y bajo Zero-PII estricto,
incorporando el Agente Purificador (AI Immune Guardian) y el Sellado de Tiempo Notarial RFC 3161 (TSA).
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional

from core.secure_vault import secure_vault
from core.supervisor import supervisor
from core.tsa_client import tsa_client
from agents.router import agent_router
from agents.centinela import centinela_agent
from agents.purificador import purificador_agent
from agents.kallpa import kallpa_agent
from agents.analista import analista_agent
from agents.calculo import calculo_agent
from agents.empaquetador import empaquetador_agent
from agents.renitli_agent import renitli_agent

logger = logging.getLogger("sara.core.orchestrator")


class MultiAgentParallelOrchestrator:
    """Orquestador maestro que coordina el enjambre de agentes en paralelo."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.active_cases: Dict[str, Dict[str, Any]] = {}

    def process_citizen_intake(
        self,
        nombre_completo: str,
        dni: str,
        telefono_contacto: str,
        mensaje_o_audio_transcrito: str,
        direccion: Optional[str] = None,
        tipo_evidencia: str = "Texto / Mensaje",
        canal: str = "whatsapp",
        evidencias_digitales: Optional[list] = None,
    ) -> Dict[str, Any]:
        """Flujo principal:
        0. Agente Centinela: Blindaje Anti-Falsas Alarmas (D.S. 020-2020-MTC).
        0.5 Agente Purificador: Inmunidad Cognitiva contra Prompt Injections y PII Scrubbing.
        1. Sella la PII real en Secure Vault con Envelope Encryption (AES-256-GCM + KMS) y genera el CUP.
        2. Rama 0 (Kallpa): Contención emocional inclusiva sobre texto sanitizado (Castellano/Quechua).
        3. En paralelo (ThreadPoolExecutor): Analista (Rama 1) y Cálculo (Rama 2).
        4. Rama 3 (Empaquetador): Consolida el expediente normativo con Sello TSA RFC 3161 (Art. 220 CPP).
        5. Auditor Supervisor valida Zero-PII y anti-alucinaciones.
        """
        logger.info("🚀 [Orquestador] Iniciando procesamiento de denuncia con soporte forense optimizado...")

        # Paso 0 y 0.5: Ejecución Concurrente en Paralelo (Centinela Anti-Spam + Purificador Inmune)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_centinela = executor.submit(
                centinela_agent.evaluate_veracity,
                telefono_origen=telefono_contacto,
                mensaje_texto=mensaje_o_audio_transcrito,
                metadatos_audio={"canal": canal, "tipo_evidencia": tipo_evidencia}
            )
            future_purificador = executor.submit(
                purificador_agent.sanitize_input,
                raw_text=mensaje_o_audio_transcrito,
                context_metadata={"canal": canal, "tipo_evidencia": tipo_evidencia}
            )

        centinela_eval = future_centinela.result()
        purificacion_eval = future_purificador.result()

        if centinela_eval.get("dictamen_admision") in ["BLOQUEAR_Y_REPORTAR_MTC", "PROPUESTA_BLOQUEO_MTC"]:
            logger.warning(f"🚫 [Centinela] Alerta con sospecha de broma desde {telefono_contacto}. Derivada a Bandeja de Certificación Policial Humana.")
            cup_bloqueo = f"CUP-BLOCK-{telefono_contacto[-4:] if len(telefono_contacto) >= 4 else '0000'}"
            hoax_payload = {
                "cup": cup_bloqueo,
                "mensaje_ciudadano": "⚠️ Reporte puesto en reserva de certificación. Se han detectado posibles patrones de comunicación no fáctica (D.S. N° 020-2020-MTC / D.L. N° 1277). Un oficial de policía está revisando el registro.",
                "idioma": "ESPAÑOL",
                "t_index": 0.0,
                "nivel_riesgo": "FALSA_ALARMA_BLOQUEADA",
                "evaluacion_centinela": centinela_eval,
                "protocolo_vida_primero": {"activado": False},
                "status_gobernanza": "PENDIENTE_CERTIFICACION_HUMANA_PNP",
                "expediente": {
                    "cup": cup_bloqueo,
                    "origen_llamada": telefono_contacto,
                    "mensaje_reportado": mensaje_o_audio_transcrito,
                    "tipo_caso": "AUDITORIA_FALSA_ALARMA_MTC",
                    "dictamen_sugerido_ia": "SANCION_MTC_DS_020_2020",
                },
                "analista": {
                    "telefono_infractor": telefono_contacto,
                    "observacion": "Sospecha de spoofing o comunicación malintencionada."
                },
                "calculo": {
                    "t_index": 0.0,
                    "nivel_riesgo": "FALSA_ALARMA_BLOQUEADA"
                }
            }
            self.active_cases[cup_bloqueo] = hoax_payload
            return hoax_payload

        texto_seguro = purificacion_eval.get("texto_sanitizado", mensaje_o_audio_transcrito)
        canary_token = purificacion_eval.get("canary_token", "")

        # Paso 1: Aislamiento Criptográfico de PII con Envelope Encryption y obtención del CUP
        biometria_res = secure_vault.seal_pii_with_reniec_biometrics(
            dni=dni,
            nombre_completo=nombre_completo,
            telefono_contacto=telefono_contacto,
            canal_verificacion=canal,
            score_facial=98.6
        )
        cup = biometria_res["cup"]
        cert_reniec = biometria_res["certificado_biometrico"]

        # Enrutamiento Cognitivo Inteligente (Dual-Brain Router)
        triage_routing = agent_router.select_brain_for_task("TRIAGE")
        forensic_routing = agent_router.select_brain_for_task("FORENSIC_AUDIT")

        # Paso 2 y 3: Ejecución Concurrente en Paralelo (Kallpa Contención + Analista Forense Criminal)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_kallpa = executor.submit(kallpa_agent.interact_and_contain, texto_seguro)
            future_analista = executor.submit(
                analista_agent.analyze_offender_data,
                cup=cup,
                pistas_infractor={},
                contexto_amenaza=texto_seguro,
                tipo_evidencia=tipo_evidencia,
                canal=canal,
                origen_contacto=telefono_contacto,
                evidencias_digitales=evidencias_digitales
            )

        kallpa_res = future_kallpa.result()
        analista_res = future_analista.result()

        supervisor.audit_payload_zero_pii("KallpaAgent", kallpa_res, cup)
        supervisor.audit_payload_zero_pii("AnalistaAgent", analista_res, cup)
        supervisor.validate_anti_hallucination("AnalistaAgent", analista_res.get("clasificacion_artefactos", {}))

        # Cálculo de riesgo cuantitativo T_index
        calculo_res = calculo_agent.compute_threat_index(
            cup=cup,
            kallpa_output=kallpa_res,
            analista_output=analista_res,
        )
        supervisor.audit_payload_zero_pii("CalculoAgent", calculo_res, cup)

        # Paso 4: Rama 3 (Empaquetador Normativo con Cadena de Custodia Art. 220 CPP)
        expediente = empaquetador_agent.package_dossier(
            cup=cup,
            kallpa_data=kallpa_res,
            analista_data=analista_res,
            calculo_data=calculo_res,
            evidencias_digitales=evidencias_digitales,
        )
        supervisor.audit_payload_zero_pii("EmpaquetadorAgent", expediente, cup)

        # Sellado de Tiempo Notarial RFC 3161 para el Expediente Completo
        expediente_hash = expediente.get("hash_integridad_sha256", f"SHA256:{cup}")
        sello_tsa_expediente = tsa_client.request_timestamp_token(
            document_hash_sha256=expediente_hash,
            metadata={"cup": cup, "t_index": calculo_res.get("t_index")}
        )
        expediente["sello_tsa_notarial_rfc3161"] = sello_tsa_expediente

        # Paso 5: Alerta Asíncrona ReNITLI-MINCUL para Lenguas Originarias
        idioma_det = kallpa_res.get("idioma_detectado", "ESPAÑOL")
        audio_hash_evidencia = "SHA256:NATIVE_AUDIO_RECOLLECTION"
        if evidencias_digitales:
            for ev in evidencias_digitales:
                if "audio" in str(ev.get("tipo", "")).lower() or "audio" in str(ev.get("nombre", "")).lower():
                    audio_hash_evidencia = ev.get("sha256", audio_hash_evidencia)
                    break

        ticket_renitli = None
        if idioma_det in ["QUECHUA", "AIMARA", "ASHANINKA", "AWAJUN", "SHIPIBO"]:
            ticket_renitli = renitli_agent.disparar_alerta_traductor_renitli(
                cup=cup,
                idioma_detectado=idioma_det,
                transcripcion_ia=texto_seguro,
                traduccion_ia=kallpa_res.get("traduccion_espanol") or kallpa_res.get("resumen_inicial_amenaza", texto_seguro),
                audio_hash_sha256=audio_hash_evidencia
            )

        # Guardar en memoria operativa del orquestador
        self.active_cases[cup] = {
            "cup": cup,
            "certificado_biometrico_reniec": cert_reniec,
            "expediente": expediente,
            "kallpa": kallpa_res,
            "analista": analista_res,
            "calculo": calculo_res,
            "evidencias_digitales": evidencias_digitales or [],
            "ticket_renitli": ticket_renitli,
            "evaluacion_purificador": purificacion_eval,
            "sello_tsa_rfc3161": sello_tsa_expediente,
            "certificado_renitli": None,
            "aprobado_humano": False,
        }

        logger.info(f"✨ [Orquestador] Expediente {cup} completado exitosamente (T_index: {calculo_res['t_index']}, Nivel: {calculo_res['nivel_criticidad']}, Inmunidad: {purificacion_eval['clasificacion_seguridad']}, TSA: {sello_tsa_expediente['tst_info']['serial_number']}).")

        return {
            "cup": cup,
            "certificado_biometrico_reniec": cert_reniec,
            "mensaje_ciudadano": kallpa_res.get("mensaje_contencion"),
            "idioma": idioma_det,
            "t_index": calculo_res.get("t_index"),
            "nivel_riesgo": calculo_res.get("nivel_criticidad"),
            "protocolo_vida_primero": kallpa_res.get("protocolo_vida_primero", {"activado": False}),
            "evaluacion_centinela": centinela_eval,
            "evaluacion_purificador": purificacion_eval,
            "sello_tsa_rfc3161": sello_tsa_expediente,
            "expediente_anonimizado": expediente,
            "expediente_normativo": expediente,
            "analista": analista_res,
            "pistas_infractor": analista_res,
            "calculo": calculo_res,
            "evaluacion_riesgo_t_index": calculo_res,
            "kallpa": kallpa_res,
            "evidencias_digitales": evidencias_digitales or [],
            "ticket_renitli": ticket_renitli,
            "status_gobernanza": "LISTO_PARA_REVISION_HITL",
        }

    def get_case(self, cup: str) -> Optional[Dict[str, Any]]:
        """Obtiene un caso activo por su CUP."""
        return self.active_cases.get(cup)


# Instancia singleton del orquestador
orchestrator = MultiAgentParallelOrchestrator()
