"""Script de prueba de conectividad: SARA ➡️ Make.com ➡️ Telegram.

Permite probar el envío automático de la notificación final con Carpeta Fiscal,
CUC y Enlace Seguro de Validación.
"""

import os
import sys
import json
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Cargar variables de entorno locales
load_dotenv()

from app.services.notification_service import notification_service


def test_remision_notification():
    make_url = os.getenv("MAKE_WEBHOOK_URL")
    print("=" * 70)
    print("🧪 SARA - TEST DE NOTIFICACIÓN FINAL (MAKE.COM / TELEGRAM / WHATSAPP)")
    print("=" * 70)

    if make_url:
        print(f"✅ Webhook Make.com configurado: {make_url[:35]}...")
    else:
        print("ℹ️ MAKE_WEBHOOK_URL no está configurado en .env (se ejecutará en Modo Simulación Soberano).")

    # Caso de prueba
    cup_test = "CUP-2026-TEST-MAKE"
    sidpol_test = "SIDPOL-2026-99214"
    carpeta_test = "CF-N°-2026-4821-FECOR-LIMA"
    cuc_test = "CUC-2026-FECOR-LIMA-TEST01"
    fiscalia_test = "3ra Fiscalía Supraprovincial Corporativa FECOR (D.Leg. 1735)"
    telefono_test = "+51984112233"

    print(f"\n📤 Disparando remisión fiscal para caso: {cup_test}")
    print(f"📁 Carpeta Fiscal: {carpeta_test}")
    print(f"🔖 Código CUC: {cuc_test}")
    print(f"📱 Teléfono Destino: {telefono_test}")

    resultado = notification_service.notificar_denunciante_remision_fiscal_sync(
        telefono_destino=telefono_test,
        canal="WHATSAPP",
        cup=cup_test,
        codigo_sidpol=sidpol_test,
        carpeta_fiscal=carpeta_test,
        cuc=cuc_test,
        fiscalia_asignada=fiscalia_test,
        fiscal_responsable="Dra. Elena Alarcón Valverde",
        idioma="es"
    )

    print("\n" + "=" * 70)
    print("📥 RESULTADO DEL DESPACHO DE SARA:")
    print("=" * 70)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    if resultado.get("make_webhook_dispatched"):
        print("\n🎉 ¡ÉXITO! El Webhook de Make.com recibió el evento con código 200/201.")
        print("👉 Revisa tu Telegram o el historial de ejecuciones de Make.com.")
    else:
        print(f"\nℹ️ Estado de entrega: {resultado.get('estado_entrega')}")
        print(f"🏛️ Proveedor: {resultado.get('proveedor_mensajeria')}")
        print(f"🔗 Enlace de validación generado: {resultado.get('enlace_validacion')}")


if __name__ == "__main__":
    test_remision_notification()
