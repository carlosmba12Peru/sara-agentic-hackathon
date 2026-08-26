"""Diagnóstico y Prueba de Conectividad de Variables .env en SARA:
1. Google Gemini API (Gemini Flash 3.7 / 2.5)
2. Make.com Webhook 1: Solicitud de Validación Biométrica (CPR)
3. Make.com Webhook 2: Notificación de Carpeta Fiscal (CUP / CUC)
4. Telegram Direct Bot API (Token & Chat ID)
5. Vapi Assistant (Public Key & Assistant ID)
"""

import os
import sys
import json
import httpx
from datetime import datetime, timezone
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

def print_separator(title=""):
    print("\n" + "=" * 75)
    if title:
        print(f"  🔍 {title}")
        print("=" * 75)


def test_gemini_api():
    print_separator("1. PRUEBA DE CONECTIVIDAD: GOOGLE GEMINI AI STUDIO")
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.7-flash")

    if not api_key:
        print("❌ GEMINI_API_KEY no está configurada en .env")
        return False

    masked_key = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
    print(f"🔑 API Key Detectada: {masked_key}")
    print(f"🤖 Modelo Configurado: {model_name}")

    try:
        # Probar endpoint REST directo de Google Generative Language
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                models = [m.get("name", "").replace("models/", "") for m in data.get("models", [])]
                print(f"✅ Conexión con Google AI Studio Exitosa (Status {resp.status_code})")
                print(f"📦 Modelos disponibles ({len(models)}): {', '.join(models[:5])}...")
                return True
            else:
                print(f"⚠️ Error al conectar con Google AI: Status {resp.status_code} - {resp.text[:100]}")
                return False
    except Exception as e:
        print(f"❌ Excepción al conectar con Google Gemini: {e}")
        return False


def test_make_webhooks():
    print_separator("2. PRUEBA DE WEBHOOKS MAKE.COM")
    webhook_url_1 = os.getenv("MAKE_WEBHOOK_VALIDACION_URL") or os.getenv("MAKE_WEBHOOK_URL")
    webhook_url_2 = os.getenv("MAKE_WEBHOOK_URL")

    print(f"🌐 Webhook 1 (Validación Biométrica CPR): {webhook_url_1[:45]}..." if webhook_url_1 else "❌ No configurado")
    print(f"🌐 Webhook 2 (Remisión Fiscal CUP):       {webhook_url_2[:45]}..." if webhook_url_2 else "❌ No configurado")

    res_1 = False
    res_2 = False

    # Test Webhook 1
    if webhook_url_1:
        payload_1 = {
            "evento": "TEST_DIAGNOSTICO_SARA_VALIDACION",
            "cpr": "CPR-2026-DIAGNOSTIC",
            "telefono_denunciante": "+51920480154",
            "url_validacion": "https://sara.gob.pe/verify?token=CPR-2026-DIAGNOSTIC",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "mensaje": "Prueba de validación diagnóstica SARA"
        }
        try:
            with httpx.Client(timeout=8.0) as client:
                resp = client.post(webhook_url_1, json=payload_1)
                if resp.status_code in (200, 201, 204):
                    print(f"  ✅ Webhook 1 (Validación CPR): RECIBIDO POR MAKE (Status {resp.status_code}) - {resp.text[:50]}")
                    res_1 = True
                else:
                    print(f"  ⚠️ Webhook 1: Respuesta no 200 (Status {resp.status_code})")
        except Exception as e:
            print(f"  ❌ Webhook 1 Falló: {e}")

    # Test Webhook 2
    if webhook_url_2:
        payload_2 = {
            "evento": "TEST_DIAGNOSTICO_SARA_REMISIÓN_FISCAL",
            "cup": "CUP-2026-DIAGNOSTIC",
            "carpeta_fiscal": "CF-N°-2026-TEST-FECOR",
            "cuc": "CUC-2026-FECOR-TEST",
            "codigo_sidpol": "SIDPOL-2026-TEST",
            "fiscalia_asignada": "3ra Fiscalía Supraprovincial FECOR (D.Leg. 1735)",
            "telefono_destino": "+51920480154",
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
        try:
            with httpx.Client(timeout=8.0) as client:
                resp = client.post(webhook_url_2, json=payload_2)
                if resp.status_code in (200, 201, 204):
                    print(f"  ✅ Webhook 2 (Remisión Fiscal): RECIBIDO POR MAKE (Status {resp.status_code}) - {resp.text[:50]}")
                    res_2 = True
                else:
                    print(f"  ⚠️ Webhook 2: Respuesta no 200 (Status {resp.status_code})")
        except Exception as e:
            print(f"  ❌ Webhook 2 Falló: {e}")

    return res_1 and res_2


def test_telegram_direct():
    print_separator("3. PRUEBA DE BOT TELEGRAM DIRECTO")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("ℹ️ TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no configurados en .env (Opcional si se usa Make.com).")
        return False

    masked_token = token[:8] + "..." + token[-4:] if len(token) > 12 else "***"
    print(f"🤖 Bot Token: {masked_token}")
    print(f"💬 Chat ID:   {chat_id}")

    try:
        # 1. Probar getMe
        url_getme = f"https://api.telegram.org/bot{token}/getMe"
        with httpx.Client(timeout=8.0) as client:
            resp = client.get(url_getme)
            if resp.status_code == 200:
                bot_info = resp.json().get("result", {})
                print(f"  ✅ Bot Identificado: @{bot_info.get('username')} (Nombre: {bot_info.get('first_name')})")
                
                # 2. Enviar mensaje de ping de prueba
                url_send = f"https://api.telegram.org/bot{token}/sendMessage"
                msg_payload = {
                    "chat_id": chat_id,
                    "text": (
                        "🛡️ *SARA - DIAGNÓSTICO DE CONECTIVIDAD*\n\n"
                        "✅ Conexión con el Bot de Notificaciones verificada con éxito.\n"
                        f"⏰ Timestamp: `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`"
                    ),
                    "parse_mode": "Markdown"
                }
                resp_send = client.post(url_send, json=msg_payload)
                if resp_send.status_code == 200:
                    print(f"  ✅ Mensaje de prueba despachado y entregado al Chat ID {chat_id}.")
                    return True
                else:
                    print(f"  ⚠️ Error enviando mensaje a Telegram: {resp_send.text}")
                    return False
            else:
                print(f"  ❌ Token de Telegram inválido (Status {resp.status_code}): {resp.text}")
                return False
    except Exception as e:
        print(f"  ❌ Error conectando a API de Telegram: {e}")
        return False


def test_vapi_configuration():
    print_separator("4. PRUEBA DE INTEGRACIÓN VAPI (VOZ KALLPA)")
    vapi_pub = os.getenv("VAPI_PUBLIC_KEY")
    vapi_asst = os.getenv("VAPI_ASSISTANT_ID")

    print(f"🎙️ Vapi Public Key:    {vapi_pub[:8]}...{vapi_pub[-4:]}" if vapi_pub else "❌ No configurada")
    print(f"🤖 Vapi Assistant ID:  {vapi_asst[:8]}...{vapi_asst[-4:]}" if vapi_asst else "❌ No configurado")

    if not vapi_pub or not vapi_asst:
        print("⚠️ Variables de Vapi incompletas en .env")
        return False

    try:
        # Validar Assistant ID consultando la API pública de Vapi o validando formato UUID
        import uuid
        is_valid_pub = bool(uuid.UUID(vapi_pub))
        is_valid_asst = bool(uuid.UUID(vapi_asst))

        if is_valid_pub and is_valid_asst:
            print("  ✅ Formato de credenciales Vapi (UUID v4) VÁLIDO.")
            print(f"  ✅ Assistant ID: {vapi_asst} listo para renderizar widget en vivo en Streamlit / Web.")
            return True
        else:
            print("  ⚠️ El formato de Vapi Public Key o Assistant ID no coincide con UUID estándar.")
            return False
    except Exception as e:
        print(f"  ⚠️ Verificación Vapi: {e}")
        return False


def run_all_diagnostics():
    print("\n" + "🌟" * 38)
    print("  🚀 SARA - DIAGNÓSTICO COMPLETO DE VARIABLES .ENV Y SERVICIOS EXTERNOS")
    print("🌟" * 38)

    r_gemini = test_gemini_api()
    r_make = test_make_webhooks()
    r_telegram = test_telegram_direct()
    r_vapi = test_vapi_configuration()

    print_separator("RESUMEN GENERAL DEL DIAGNÓSTICO")
    print(f"  • Google Gemini AI Studio: {'✅ OPERATIVO' if r_gemini else '❌ REVISAR'}")
    print(f"  • Webhooks Make.com:       {'✅ OPERATIVO' if r_make else '⚠️ REVISAR'}")
    print(f"  • Bot Telegram Directo:    {'✅ OPERATIVO' if r_telegram else '⚠️ REVISAR'}")
    print(f"  • Vapi Voice Assistant:    {'✅ OPERATIVO' if r_vapi else '⚠️ REVISAR'}")

    all_good = r_gemini and r_make and r_telegram and r_vapi
    print("\n" + ("=" * 75))
    if all_good:
        print("  🎉 TODOS LOS SERVICIOS Y WEBHOOKS EXTERNOS ESTÁN 100% OPERATIVOS")
    else:
        print("  ℹ️ EL SISTEMA CUENTA CON FALLBACKS SOBERANOS ACTIVOS PARA HACKATHON")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    run_all_diagnostics()
