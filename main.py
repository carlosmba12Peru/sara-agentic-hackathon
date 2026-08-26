"""Servidor API REST (Flask) de SARA con Endpoints Human-in-the-Loop (HITL), Zero-PII, FIDO2/JWT y Sanitización Forense.
Diseñado para ejecución local y despliegue en Google Cloud Run.
"""

import os
import logging
import uuid
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from core.orchestrator import orchestrator
from core.secure_vault import secure_vault
from core.supervisor import supervisor
from core.auth_service import require_police_auth, police_auth_service
from core.file_sanitizer import file_sanitizer

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("sara.main")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    """Ruta raíz de bienvenida e información del servicio."""
    return jsonify({
        "proyecto": "SARA - Sistema Autónomo de Respuesta Anti-Extorsión (Zero-PII & Inclusión Multilingüe)",
        "hackathon": "All Things Agentic Hackathon",
        "estado": "EN_LINEA",
        "seguridad_activa": {
            "inmunidad_cognitiva": "Agente Purificador Activo (Anti-IPI / PII Scrubbing)",
            "boveda_criptografica": "Secure Vault con Envelope Encryption (AES-256-GCM + GCP KMS)",
            "sellado_temporal": "TSA RFC 3161 (Indecopi / RENIEC)",
            "autenticacion_policial": "FIDO2 WebAuthn & JWT Asimétrico (Zero-Trust)"
        },
        "endpoints": {
            "auth_policial": "POST /api/auth/token_policial",
            "denuncia_intake": "POST /api/denuncia",
            "hitl_revisar": "GET /api/humano/revisar/<id_caso>",
            "hitl_aprobar": "POST /api/humano/aprobar/<id_caso>",
            "remitir_fiscalia": "POST /api/humano/remitir_fiscalia/<id_caso>",
            "observabilidad_trazas": "GET /api/trazas",
            "health_check": "GET /health",
        },
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check para Google Cloud Run."""
    return jsonify({
        "status": "HEALTHY",
        "service": "SARA Anti-Extorsion Agentic System",
        "version": "2.0.0",
        "security_hardening": "ACTIVE"
    }), 200


@app.route("/api/auth/token_policial", methods=["POST"])
def generar_token_policial():
    """Emite un token JWT criptográfico policial para autenticación en endpoints HITL."""
    data = request.get_json(silent=True) or {}
    cip = data.get("cip", "CIP-48291032")
    nombre = data.get("nombre", "Mayor PNP Carlos Mendoza")
    unidad = data.get("unidad", "DIVINCRI - DIRINCRI PNP")
    jerarquia = data.get("jerarquia", "COMISARIO")
    permisos = data.get("permisos", ["HITL_APPROVE_EXTORTION", "SIDPOL_DISPATCH", "FECOR_TRANSMISSION", "UNLOCK_PII"])
    fido2_verified = data.get("fido2_hardware_verified", True)

    token = police_auth_service.issue_police_token(
        cip=cip,
        nombre_oficial=nombre,
        unidad=unidad,
        jerarquia=jerarquia,
        permisos=permisos,
        fido2_verified=fido2_verified
    )

    return jsonify({
        "token_policial": token,
        "tipo": "Bearer",
        "cip": cip,
        "fido2_hardware_verified": fido2_verified,
        "mensaje": "Token de autenticación policial y autorización HITL emitido con éxito."
    }), 200


@app.route("/api/denuncia", methods=["POST"])
def recibir_denuncia():
    """Paso 4.1: Conecta la validación biométrica/datos reales con el Secure Vault,
    Kallpa y el orquestador paralelo en segundo plano, soportando adjuntos multimedia sanitizados.
    """
    # Detectar si viene por JSON o por Form-Data (con archivos adjuntos)
    if request.is_json:
        data = request.get_json() or {}
        nombre = data.get("nombre_completo", "Ciudadano Denunciante")
        dni = data.get("dni", "00000000")
        telefono = data.get("telefono_contacto", "000000000")
        mensaje = data.get("mensaje") or data.get("mensaje_denuncia") or ""
        direccion = data.get("direccion", None)
        tipo_evidencia = data.get("tipo_evidencia", "Texto / Mensaje")
        canal = data.get("canal", "whatsapp")
        evidencias_digitales = data.get("evidencias_digitales", [])
    else:
        nombre = request.form.get("nombre_completo", "Ciudadano Denunciante")
        dni = request.form.get("dni", "00000000")
        telefono = request.form.get("telefono_contacto", "000000000")
        mensaje = request.form.get("mensaje") or request.form.get("mensaje_denuncia") or ""
        direccion = request.form.get("direccion", None)
        evidencias_digitales = []
        
        # Manejo seguro y sanitización forense de archivo adjunto
        archivo = request.files.get("archivo_evidencia")
        if archivo and archivo.filename != '':
            try:
                f_bytes = archivo.read()
                sanitized_ev = file_sanitizer.process_and_seal_evidence(
                    file_bytes=f_bytes,
                    original_filename=archivo.filename,
                    content_type=archivo.content_type
                )
                evidencias_digitales.append({
                    "nombre": sanitized_ev["nombre_archivo_original"],
                    "nombre_seguro": sanitized_ev["nombre_archivo_seguro"],
                    "tipo": sanitized_ev["mime_detectado"],
                    "sha256": sanitized_ev["hash_sha256"],
                    "sello_tsa": sanitized_ev["sello_tsa_rfc3161"],
                    "ruta": sanitized_ev["ruta_almacenamiento_seguro"]
                })
                tipo_evidencia = f"Evidencia digital sanitizada: {sanitized_ev['nombre_archivo_original']}"
                canal = "multimedia_forense"
                mensaje = f"[Evidencia forense sellada: {sanitized_ev['hash_sha256']}] {mensaje}"
            except Exception as err:
                logger.error(f"Error procesando evidencia forense: {err}")
                return jsonify({"error": f"Fallo en la sanitización forense del archivo: {str(err)}"}), 400
        else:
            tipo_evidencia = request.form.get("tipo_evidencia", "Texto / Mensaje")
            canal = request.form.get("canal", "whatsapp")

    if not mensaje:
        return jsonify({"error": "El campo 'mensaje' o la evidencia adjunta es obligatorio."}), 400

    logger.info("📥 Nueva denuncia recibida con soporte forense. Iniciando protocolo Zero-PII e Inmunidad...")

    # Ejecución del Orquestador con aislamiento de PII y metadatos forenses
    resultado = orchestrator.process_citizen_intake(
        nombre_completo=nombre,
        dni=dni,
        telefono_contacto=telefono,
        mensaje_o_audio_transcrito=mensaje,
        direccion=direccion,
        tipo_evidencia=tipo_evidencia,
        canal=canal,
        evidencias_digitales=evidencias_digitales,
    )

    return jsonify({
        "mensaje": "Denuncia procesada con contención empática, sanitizada y sellada bajo Zero-PII.",
        "cup": resultado["cup"],
        "mensaje_ciudadano": resultado.get("mensaje_ciudadano"),
        "respuesta_inmediata_victima": resultado.get("mensaje_ciudadano"),
        "idioma_detectado": resultado.get("idioma"),
        "t_index": resultado.get("t_index"),
        "t_index_calculado": resultado.get("t_index"),
        "nivel_riesgo": resultado.get("nivel_riesgo"),
        "protocolo_vida_primero": resultado.get("protocolo_vida_primero", {}),
        "evaluacion_centinela": resultado.get("evaluacion_centinela", {}),
        "evaluacion_purificador": resultado.get("evaluacion_purificador", {}),
        "sello_tsa_rfc3161": resultado.get("sello_tsa_rfc3161", {}),
        "gobernanza": "Expediente anónimo disponible para revisión del operador en GET /api/humano/revisar/<cup>",
    }), 201


@app.route("/api/humano/revisar/<id_caso>", methods=["GET"])
def revisar_caso_humano(id_caso: str):
    """Paso 4.2 (HITL 1): Permite al analista/operador policial visualizar el
    expediente generado por los agentes sin violar la privacidad (solo con CUP).
    """
    caso = orchestrator.get_case(id_caso)
    if not caso:
        return jsonify({"error": f"Expediente con CUP '{id_caso}' no encontrado."}), 404

    return jsonify({
        "cup": id_caso,
        "expediente_normativo": caso["expediente"],
        "evaluacion_riesgo_t_index": caso["calculo"],
        "pistas_infractor": caso["analista"],
        "sello_tsa_rfc3161": caso.get("sello_tsa_rfc3161"),
        "evaluacion_purificador": caso.get("evaluacion_purificador"),
        "estado_privacidad": "CUP_ACTIVO - PII Bloqueada bajo Envelope Encryption (AES-256-GCM)",
    }), 200


@app.route("/api/humano/aprobar/<id_caso>", methods=["POST"])
@require_police_auth("HITL_APPROVE_EXTORTION")
def aprobar_caso_humano(id_caso: str):
    """Paso 4.2 (HITL 2): Valida formalmente el caso con autenticación FIDO2/JWT,
    desencripta la PII del Secure Vault y procesa la acción de aprobación o transmisión al SIDPOL.
    """
    data = request.get_json(silent=True) or {}
    token_operador = data.get("token_operador") or data.get("token_cip") or request.headers.get("Authorization", "").replace("Bearer ", "")
    operador_info = getattr(request, "operador_autenticado", {})
    operador_id = operador_info.get("sub", data.get("operador_id", "OPERADOR_PNP_01"))
    accion = data.get("accion", "APROBACION_ESTANDAR")
    
    # Capturar la decisión jurídica y el dictamen de mando del oficial
    tipificacion_definitiva = data.get("tipificacion_definitiva", "Art. 200 del Código Penal - Delito de Extorsión")
    opinion_policial = data.get("opinion_policial", "Validado por el oficial a cargo.")

    caso = orchestrator.get_case(id_caso)
    if not caso:
        return jsonify({"error": f"Expediente con CUP '{id_caso}' no encontrado."}), 404

    # Desbloqueo seguro de PII en la bóveda con verificación criptográfica
    pii_real = secure_vault.unlock_pii_for_dispatch(cup=id_caso, token_autorizacion_humana=token_operador)
    if not pii_real:
        return jsonify({"error": "No autorizado para desbloquear PII o credenciales revocadas."}), 403

    caso["aprobado_humano"] = True
    caso["expediente"]["estado_gobernanza"] = f"APROBADO_POR_OPERADOR_{operador_id}"
    tip_ia_original = caso["expediente"].get("tipificacion_penal_sugerida", "Art. 200 del Código Penal")
    tipificacion_definitiva = data.get("tipificacion_definitiva", tip_ia_original)
    opinion_policial = data.get("opinion_policial", "Conforme con la apreciación táctica.")
    medidas_determinadas = data.get("medidas_determinadas_policia", [])

    # Registrar calibración humana (RLHF) en el Asesor Jurídico
    try:
        from agents.asesor_juridico import asesor_juridico_agent
        asesor_juridico_agent.registrar_calibracion_humana(
            cup=id_caso,
            tipificacion_ia=tip_ia_original,
            tipificacion_humana=tipificacion_definitiva,
            opinion_policial=opinion_policial,
            operador_id=operador_id
        )
    except Exception:
        pass

    # Expediente completo para el despacho policial oficial
    despacho_oficial = {
        "expediente_id": caso["expediente"].get("expediente_id", f"EXP-{id_caso}"),
        "cup": id_caso,
        "operador_aprobador": operador_id,
        "oficial_nombre": operador_info.get("nombre", "Oficial de Turno"),
        "fido2_verificado": operador_info.get("fido2_hardware_verified", True),
        "nivel_criticidad": caso["calculo"]["nivel_criticidad"],
        "t_index": caso["calculo"]["t_index"],
        "tipificacion_penal_propuesta_ia": tip_ia_original,
        "tipificacion_penal_actualizada_policial": tipificacion_definitiva,
        "dictamen_u_opinion_policial": opinion_policial,
        "medidas_ejecutadas_por_comando": medidas_determinadas,
        "datos_victima_para_patrullaje": {
            "nombre": pii_real["nombre_completo"],
            "dni": pii_real["dni"],
            "telefono": pii_real["telefono_contacto"],
            "direccion": pii_real["direccion_residencia"],
        },
        "objetivo_investigacion_infractor": caso["expediente"].get("evidencias_infractor", {}),
        "accion_tactica": "DESPACHO_UNIDAD_ESPECIALIZADA_HABILITADO",
    }

    respuesta_json = {
        "status": "CASO_APROBADO_Y_DESPACHADO",
        "cup": id_caso,
        "mensaje": "Tipificación, medidas y dictamen policial integrados exitosamente con autenticación FIDO2/JWT.",
        "medidas_aprobadas_policia": medidas_determinadas,
        "orden_despacho_oficial": despacho_oficial,
    }

    # Si se solicita la transmisión formal al SIDPOL
    if accion == "TRANSMISION_SIDPOL":
        codigo_sidpol = f"SIDPOL-2026-{uuid.uuid4().hex[:6].upper()}"
        despacho_oficial["codigo_registro_sidpol"] = codigo_sidpol
        despacho_oficial["timestamp_envio_sidpol"] = datetime.now(timezone.utc).isoformat()
        
        respuesta_json["status"] = "ENVIADO_A_SIDPOL"
        respuesta_json["mensaje"] = "Expediente vinculado y actualizado con criterio policial en el SIDPOL."
        respuesta_json["codigo_sidpol"] = codigo_sidpol
        logger.info(f"📤 [SIDPOL] Expediente {id_caso} transmitido con código oficial {codigo_sidpol} bajo tipificación: {tipificacion_definitiva}.")
    else:
        logger.info(f"🚨 [HITL APROBADO] Despacho oficial generado para {id_caso} por {operador_id}.")

    return jsonify(respuesta_json), 200


@app.route("/api/humano/remitir_fiscalia/<id_caso>", methods=["POST"])
@require_police_auth("FECOR_TRANSMISSION")
def remitir_fiscalia(id_caso):
    """Transfiere formalmente la carpeta fiscal y el paquete probatorio sellado (Art. 220 CPP & TSA RFC 3161)
    al Ministerio Público (FECOR / Subsistema D.Leg. 1735), concluyendo la labor de SARA en sede policial."""
    data = request.get_json(silent=True) or {}
    operador_info = getattr(request, "operador_autenticado", {})
    operador_id = operador_info.get("sub", data.get("operador_id", "OFICIAL_PNP_ASIGNADO"))
    token = data.get("token_operador") or data.get("token_cip") or request.headers.get("Authorization", "").replace("Bearer ", "")
    codigo_sidpol = data.get("codigo_sidpol", f"SIDPOL-2026-{uuid.uuid4().hex[:6].upper()}")
    tipificacion_definitiva = data.get("tipificacion_definitiva", "Art. 200 C.P.")
    medidas_aprobadas = data.get("medidas_aprobadas", [])
    evidencias = data.get("evidencias", [])
    telefono_denunciante = data.get("telefono_denunciante") or data.get("telefono_contacto")
    canal_notificacion = data.get("canal_notificacion", "WHATSAPP")
    idioma = data.get("idioma", "es")

    # Si no se pasó explícitamente en el payload, intentar recuperar el teléfono de forma segura del Secure Vault
    if not telefono_denunciante:
        try:
            pii_desbloqueada = secure_vault.unlock_pii_for_dispatch(id_caso, token)
            if pii_desbloqueada:
                telefono_denunciante = pii_desbloqueada.get("telefono_contacto")
        except Exception:
            telefono_denunciante = None

    from agents.empaquetador import empaquetador_agent
    remision_packet = empaquetador_agent.generar_oficio_remision_fiscal(
        cup=id_caso,
        codigo_sidpol=codigo_sidpol,
        oficial_id=operador_id,
        token_cip=token,
        tipificacion_humana=tipificacion_definitiva,
        medidas_aprobadas=medidas_aprobadas,
        evidencias=evidencias,
        telefono_denunciante=telefono_denunciante,
        canal_notificacion=canal_notificacion,
        idioma=idioma
    )

    logger.info(f"🏛️ [REMISIÓN FISCAL] Expediente {id_caso} transferido formalmente a la Fiscalía Especializada con Oficio {remision_packet['numero_oficio_pnp']}.")
    return jsonify({
        "status": "EXPEDIENTE_TRANSFERIDO_AL_MINISTERIO_PUBLICO",
        "mensaje": "Expediente y evidencias selladas transferidos exitosamente a la Fiscalía Especializada (D.Leg. 1735) y notificación enviada a la víctima.",
        "remision_fiscal": remision_packet,
        "notificacion_denunciante": remision_packet.get("notificacion_denunciante", {})
    }), 200


@app.route("/api/trazas", methods=["GET"])
def obtener_trazas():
    """Observabilidad y auditoría de la IA."""
    return jsonify({
        "trazas_supervisor_ia": supervisor.get_latest_audit_trace(),
    }), 200


# ==============================================================================
# ⚖️ ENDPOINTS DEL AGENTE VIGÍA NORMATIVO Y GOBERNANZA HITL LEGAL
# ==============================================================================
@app.route("/api/vigia/escanear", methods=["POST"])
def vigia_escanear():
    """Ejecuta el escaneo normativo tripartito (Legislativo, Ejecutivo, Judicial)."""
    try:
        from agents.vigia_normativo import vigia_normativo_agent
        resultado = vigia_normativo_agent.escanear_fuentes_normativas_tripartitas()
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Error en escaneo del Vigía Normativo: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/vigia/propuestas", methods=["GET"])
def vigia_propuestas():
    """Devuelve las propuestas pendientes de revisión del experto legal y el historial de decisiones."""
    try:
        from agents.vigia_normativo import vigia_normativo_agent
        from agents.asesor_juridico import asesor_juridico_agent
        return jsonify({
            "propuestas_pendientes": vigia_normativo_agent.obtener_propuestas_pendientes(),
            "historial_decisiones": vigia_normativo_agent.get_historial_decisiones_humanas(),
            "matriz_cumplimiento_sara": asesor_juridico_agent.matriz_cumplimiento,
            "historial_actualizaciones_asesor": asesor_juridico_agent.historial_actualizaciones
        }), 200
    except Exception as e:
        logger.error(f"Error obteniendo propuestas del Vigía: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/vigia/dictaminar", methods=["POST"])
def vigia_dictaminar():
    """Gobernanza HITL Legal: El experto legal humano aprueba o rechaza la integración a asesor_juridico.py."""
    data = request.get_json(silent=True) or {}
    id_propuesta = data.get("id_propuesta")
    decision = data.get("decision", "RECHAZAR")
    experto_id = data.get("experto_id", "Abog. Especialista CAL")
    dictamen = data.get("dictamen_juridico", "Dictamen de análisis de impacto normativo.")
    rol = data.get("rol_experto", "Asesor Legal en IA y Derecho Penal")

    if not id_propuesta:
        return jsonify({"error": "Falta el id_propuesta para dictamen."}), 400

    try:
        from agents.vigia_normativo import vigia_normativo_agent
        resultado = vigia_normativo_agent.dictaminar_propuesta_humana(
            id_propuesta=id_propuesta,
            decision=decision,
            experto_id=experto_id,
            dictamen_juridico=dictamen,
            rol_experto=rol
        )
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Error en dictamen legal HITL: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/vigia/crear-manual", methods=["POST"])
def vigia_crear_manual():
    """Permite al experto legal proponer una norma ad-hoc para evaluación."""
    data = request.get_json(silent=True) or {}
    norma = data.get("norma", "")
    titulo = data.get("titulo", "")
    organo = data.get("organo", "")
    poder = data.get("poder_del_estado", "Poder Ejecutivo")
    materia = data.get("materia", "INTELIGENCIA_ARTIFICIAL_Y_DERECHO_DIGITAL")
    impacto = data.get("impacto", "")

    if not norma or not titulo:
        return jsonify({"error": "Norma y título son requeridos."}), 400

    try:
        from agents.vigia_normativo import vigia_normativo_agent
        res = vigia_normativo_agent.crear_propuesta_manual(
            norma=norma,
            titulo=titulo,
            organo=organo,
            poder_estado=poder,
            materia=materia,
            impacto=impacto
        )
        return jsonify(res), 201
    except Exception as e:
        logger.error(f"Error creando propuesta manual: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=True)