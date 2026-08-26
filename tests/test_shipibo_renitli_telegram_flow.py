"""
Pruebas automatizadas del flujo integral de Lenguas Originarias (Shipibo-Konibo):
1. Ingesta ciudadana en Shipibo-Konibo.
2. Contención y traducción táctica preliminar de Kallpa IA.
3. Despacho de mensaje de validación biométrica a la víctima en Shipibo.
4. Despacho de alerta pericial al Perito Oficial ReNITLI-MINCUL vía Telegram con token y enlace.
5. Convalidación humana con Fe Pública (Art. 220 CPP / Ley 29735) y generación de adenda fiscal.
"""

import pytest
from core.i18n import normalize_language_code, detect_language_heuristic
from agents.kallpa import KallpaAgent
from agents.renitli_agent import ReNITLIAgent, PADRON_OFICIAL_RENITLI
from app.services.notification_service import notification_service
from core.orchestrator import MultiAgentParallelOrchestrator, orchestrator


def test_shipibo_normalization_and_detection():
    """Verifica detección y normalización precisa de Shipibo-Konibo."""
    assert normalize_language_code("Shipibo-Konibo (Ucayali / Pucallpa)") == "shipibo"
    assert normalize_language_code("shipibo") == "shipibo"
    assert normalize_language_code("shp") == "shipibo"

    texto_shipibo = "Jakon nete nokon wetsá, Pucallpamanta nokon artesania xobo 966112233 telefononin koríki 800 soles mañakana o xobo menoti ráke."
    assert detect_language_heuristic(texto_shipibo) == "SHIPIBO"


def test_kallpa_shipibo_containment_and_translation():
    """Verifica contención y generación de traducción preliminar al español en Kallpa."""
    kallpa = KallpaAgent()
    texto_shipibo = "Jakon nete nokon wetsá, Pucallpamanta nokon artesania xobo 966112233 telefononin koríki 800 soles mañakana o xobo menoti ráke."
    res = kallpa.interact_and_contain(texto_shipibo)

    assert res["idioma_detectado"] == "SHIPIBO"
    assert "Jakon nete" in res["mensaje_contencion"]
    assert "traduccion_espanol" in res
    assert len(res["traduccion_espanol"]) > 15
    assert "denuncio" in res["traduccion_espanol"].lower() or "artesanal" in res["traduccion_espanol"].lower() or "extorsivo" in res["traduccion_espanol"].lower() or "protección" in res["traduccion_espanol"].lower()


def test_victim_biometric_validation_message_in_shipibo():
    """Verifica que el mensaje de validación biométrica enviado a la víctima esté en Shipibo."""
    cpr = "CPR-2026-SHP001"
    url_val = f"https://sara.gob.pe/verify?token={cpr}"
    cuerpo, tg = notification_service.redactar_mensaje_validacion_biometrica(
        cpr=cpr,
        url_validacion=url_val,
        idioma="Shipibo-Konibo (Ucayali / Pucallpa)"
    )

    assert "Jakon nete" in cuerpo
    assert "RENIEC" in cuerpo
    assert cpr in cuerpo
    assert url_val in cuerpo
    assert "CUP" in cuerpo

    # Disparo simulado
    dispatch_res = notification_service.notificar_solicitud_validacion_biometrica_sync(
        telefono_destino="+51961112233",
        cup="CUP-2026-SHP001",
        cpr=cpr,
        url_validacion=url_val,
        canal="TELEGRAM",
        idioma="Shipibo-Konibo (Ucayali / Pucallpa)"
    )
    assert dispatch_res["cpr"] == cpr
    assert "Jakon nete" in dispatch_res["cuerpo_mensaje"]
    assert dispatch_res["estado_entrega"] in ["ENVIADO_EXITOSO", "ENVIADO_SIMULADO"]


def test_renitli_telegram_alert_dispatch_for_shipibo():
    """Verifica la asignación del perito oficial de Shipibo y el despacho del mensaje por Telegram."""
    renitli = ReNITLIAgent()
    cup = "CUP-2026-8D9E1A2B"
    texto_original_shipibo = "Jakon nete nokon wetsá, koríki mañakana xobo akinanti 966112233"
    traduccion_kallpa = "Buenos días hermano/a, denuncio cobro extorsivo de dinero y solicito auxilio policial para mi vivienda."
    hash_audio = "SHA256:7B8F9A1C2D3E4F5A6B7C8D9E0F1A2B3C4D5E6F7A"

    ticket = renitli.disparar_alerta_traductor_renitli(
        cup=cup,
        idioma_detectado="SHIPIBO",
        transcripcion_ia=texto_original_shipibo,
        traduccion_ia=traduccion_kallpa,
        audio_hash_sha256=hash_audio
    )

    assert ticket is not None
    assert ticket["cup"] == cup
    assert ticket["lengua_originaria"] == "SHIPIBO"
    assert "Rider Panduro" in ticket["traductor_titular"]
    assert ticket["registro_renitli"] == "RENITLI-MINCUL-0092"
    assert "TOKEN-RENITLI-0092-PUCALLPA" in ticket["token_acceso"]
    assert "token=" in ticket["url_consola_mincul"]
    assert ticket["transcripcion_original_ia"] == texto_original_shipibo
    assert ticket["traduccion_preliminar_ia"] == traduccion_kallpa

    # Verificar que el mensaje a Telegram fue formateado y procesado
    tg_dispatch = notification_service.notificar_traductor_renitli_telegram_sync(ticket)
    assert tg_dispatch["evento"] == "ALERTA_PERICIAL_TRADUCTOR_RENITLI"
    assert tg_dispatch["ticket_id"] == ticket["ticket_id"]
    assert "Rider Panduro" in tg_dispatch["mensaje_telegram_formateado"]
    assert "Jakon nete" in tg_dispatch["mensaje_telegram_formateado"]
    assert traduccion_kallpa in tg_dispatch["mensaje_telegram_formateado"]
    assert ticket["token_acceso"] in tg_dispatch["mensaje_telegram_formateado"]
    assert tg_dispatch["estado_entrega"] in ["ENVIADO_EXITOSO", "ENVIADO_SIMULADO"]


def test_orchestrator_end_to_end_shipibo_workflow():
    """Verifica que el Orquestador genere el caso en Shipibo y active automáticamente el ticket ReNITLI."""
    orch = MultiAgentParallelOrchestrator()
    texto_shipibo = "Jakon nete nokon wetsá, Pucallpamanta nokon artesania xobo 966112233 telefononin koríki 800 soles mañakana o xobo menoti ráke."

    resultado = orch.process_citizen_intake(
        nombre_completo="Segundo Silvano Cauper",
        dni="45891234",
        telefono_contacto="+51961998811",
        direccion="Comunidad Nativa San Francisco de Yarinacocha, Pucallpa",
        mensaje_o_audio_transcrito=texto_shipibo,
        tipo_evidencia="kallpa_chat_web",
        canal="kallpa_chat_web"
    )

    cup = resultado["cup"]
    assert cup.startswith("CUP-")
    assert resultado["idioma"] == "SHIPIBO"
    assert resultado["ticket_renitli"] is not None
    assert resultado["ticket_renitli"]["registro_renitli"] == "RENITLI-MINCUL-0092"
    assert "Rider Panduro" in resultado["ticket_renitli"]["traductor_titular"]
    assert resultado["ticket_renitli"]["token_acceso"] == "TOKEN-RENITLI-0092-PUCALLPA"


def test_renitli_human_convalidation_and_fe_publica():
    """Verifica la convalidación humana pericial con token, firma digital y certificación de Fe Pública."""
    renitli = ReNITLIAgent()
    cup = "CUP-2026-SHIPIBO-TEST"
    ticket_id = "TICKET-RENITLI-SHIPIBO-0092"
    token = "TOKEN-RENITLI-0092-PUCALLPA"

    cert = renitli.convalidar_fe_publica_renitli(
        cup=cup,
        ticket_id=ticket_id,
        traductor_nombre="Lic. Rider Panduro Silvano",
        registro_renitli="RENITLI-MINCUL-0092",
        token_ingresado=token,
        transcripcion_final="Jakon nete, Pucallpamanta nokon artesania xobo 966112233 telefononin koríki 800 soles mañakana o xobo menoti ráke.",
        traduccion_juridica_final="Buenos días, denuncio que desde el número 966112233 me exigen el pago extorsivo de 800 soles bajo amenaza de quemar mi taller artesanal en Pucallpa.",
        observaciones_dialectales="Traducción jurídica oficial y fehaciente según la variante Shipibo-Konibo Selva Oriental."
    )

    assert cert["estado_procesal"] == "CONVALIDADA_CON_FE_PUBLICA_MINCUL"
    assert cert["token_validado"] is True
    assert cert["registro_oficial_renitli"] == "RENITLI-MINCUL-0092"
    assert cert["nro_certificado_oficial"].startswith("CERT-RENITLI-2026-")
    assert cert["sello_digital_verificacion"].startswith("SHA256:")
    assert "Dirección de Lenguas Indígenas" in cert["entidad_emisora"]
