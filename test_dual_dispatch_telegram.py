import os
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from dotenv import load_dotenv
load_dotenv()

from app.services.notification_service import notification_service
from agents.renitli_agent import renitli_agent

print("1. Despachando mensaje de Denunciante (Awajún)...")
res_ciudadano = notification_service.notificar_solicitud_validacion_biometrica_sync(
    telefono_destino="+51920480154",
    cup="CUP-2026-TESTAWAJUN",
    cpr="CPR-2026-TESTAWAJUN",
    url_validacion="https://sara.gob.pe/verify?token=CPR-2026-TESTAWAJUN",
    canal="TELEGRAM",
    idioma="Awajún (Selva Norte)"
)
print("Respuesta Denunciante:", res_ciudadano.get("estado_entrega"), "Make:", res_ciudadano.get("make_webhook_dispatched"), "TG Direct:", res_ciudadano.get("telegram_direct_dispatched"))

print("\n2. Generando ticket ReNITLI y disparando alerta pericial MINCUL...")
ticket = renitli_agent.disparar_alerta_traductor_renitli(
    cup="CUP-2026-TESTAWAJUN",
    idioma_detectado="AWAJUN",
    transcripcion_ia="Kumpami yatsuch Kallpa, yaimkata. Cenepamanta 977554433 número kuji 1000 soles exigiu lancha peke-peke o namput suwimka mántat.",
    traduccion_ia="Amigo Kallpa, ayúdame. Desde el 977554433 nos exigen 1000 soles por cada lancha peke-peke o si no nos matarán a balazos en el río Cenepa.",
    audio_hash_sha256="SHA256:NATIVE_AUDIO_TEST_AWAJUN"
)

res_perito = notification_service.notificar_traductor_renitli_telegram_sync(ticket)
print("Respuesta Perito ReNITLI:", res_perito.get("estado_entrega"), "Make:", res_perito.get("make_webhook_dispatched"), "TG Direct:", res_perito.get("telegram_direct_dispatched"))

print("\n✅ Prueba completada con éxito.")
