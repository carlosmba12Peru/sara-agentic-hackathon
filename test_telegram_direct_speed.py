import os
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from dotenv import load_dotenv
load_dotenv()

from app.services.notification_service import notification_service

print("Iniciando prueba directa de notificación...")
res = notification_service.notificar_solicitud_validacion_biometrica_sync(
    telefono_destino="+51920480154",
    cup="CUP-2026-TESTSPEED",
    cpr="CPR-2026-TESTSPEED",
    url_validacion="https://sara.gob.pe/verify?token=CPR-2026-TESTSPEED",
    canal="TELEGRAM",
    idioma="Español (Castellano)"
)

print("\nResultado de notificación:")
import pprint
pprint.pprint(res)
