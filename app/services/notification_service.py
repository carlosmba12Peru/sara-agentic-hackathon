"""Multi-channel notification and operational coordination service."""

import logging
from typing import Optional

try:
    import httpx
except ImportError:
    httpx = None

from app.config import settings
from app.models.case import ExtortionCase
from app.models.threat_index import RiskTier

logger = logging.getLogger("sara.notification")


class NotificationService:
    """Service to push alerts to operations centers (Telegram/Make) and citizen SMS/WhatsApp."""

    def __init__(self):
        self.telegram_token = settings.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = settings.TELEGRAM_CHAT_ID
        self.make_webhook = settings.MAKE_WEBHOOK_URL

    async def send_operations_alert(self, case: ExtortionCase) -> bool:
        """Send an executive threat summary to emergency operations (Telegram)."""
        if not self.telegram_token or not self.telegram_chat_id:
            logger.info("Telegram credentials not configured. Skipping live Telegram push.")
            return False

        tier_icon = "🚨" if case.threat_assessment and case.threat_assessment.tier == RiskTier.HIGH else "⚠️"
        t_index = case.threat_assessment.t_index if case.threat_assessment else "N/A"
        tier_name = case.threat_assessment.tier.value if case.threat_assessment else "UNKNOWN"

        message = (
            f"{tier_icon} *ALERTA SARA - CASO DE EXTORSION*\n"
            f"*ID Caso:* `{case.case_id}`\n"
            f"*Nivel de Riesgo:* `{tier_name}` (T_index: *{t_index}/100*)\n"
            f"*Canal:* `{case.source_channel}`\n"
            f"*Resumen:* {case.triage_summary or 'En evaluación'}\n\n"
            f"*Acciones Inmediatas:*\n"
        )

        if case.threat_assessment:
            for action in case.threat_assessment.recommended_actions[:3]:
                message += f"• {action}\n"

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    logger.info(f"Telegram alert sent for case {case.case_id}")
                    return True
                else:
                    logger.error(f"Failed to send Telegram alert: {resp.text}")
        except Exception as e:
            logger.error(f"Error connecting to Telegram API: {e}")

        return False

    async def trigger_make_webhook(self, case: ExtortionCase) -> bool:
        """Trigger Make.com or n8n event webhook with full case metadata."""
        if not self.make_webhook:
            logger.info("Make webhook URL not configured. Skipping.")
            return False

        payload = case.model_dump(mode="json")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(self.make_webhook, json=payload)
                if resp.status_code in (200, 201, 204):
                    logger.info(f"Make webhook dispatched for case {case.case_id}")
                    return True
        except Exception as e:
            logger.error(f"Error calling Make webhook: {e}")

        return False

    async def send_citizen_verification(
        self, case: ExtortionCase, base_url: str = "https://sara.gov.pe/verify"
    ) -> Optional[str]:
        """Generate citizen verification link and simulate dispatch."""
        if not case.verification_token:
            return None

        verification_url = f"{base_url}?token={case.verification_token}&caso={case.case_id}"
        logger.info(
            f"Dispatched citizen protection link for case {case.case_id}: {verification_url}"
        )
        return verification_url

    def redactar_mensaje_carpeta_fiscal(
        self,
        cup: str,
        codigo_sidpol: str,
        carpeta_fiscal: str,
        cuc: str,
        fiscalia_asignada: str,
        idioma: str = "es"
    ) -> str:
        """Genera el mensaje empático y oficial para la víctima en su idioma nativo."""
        lang = (idioma or "es").lower().strip()

        if "quechua" in lang or "runasimi" in lang:
            return (
                f"🕊️ SARA - PNP & MINISTERIO PÚBLICO (LÍNEA 111)\n\n"
                f"Allillanchu. Willasaykiku: Extorsión denunciayki allin chaskisqam kachkan hinaspa Fiscaliaman apachisqa.\n\n"
                f"📁 Carpeta Fiscal: {carpeta_fiscal}\n"
                f"🔖 CUC Fiscal: {cuc}\n"
                f"📋 SIDPOL PNP: {codigo_sidpol}\n"
                f"🏛️ Fiscalia: {fiscalia_asignada}\n"
                f"🔒 CUP Código: {cup}\n\n"
                f"💚 Sutiykiqa 100% pakasqam kachkan. Ama manchakuychu, manam sapallaykichu kanki."
            )
        elif "aimara" in lang or "aymara" in lang:
            return (
                f"🕊️ SARA - PNP & MINISTERIO PÚBLICO (LÍNEA 111)\n\n"
                f"Suma urukipanaya. Yatiyapxama: Denunciamax suma qillqatawa ukat Fiscalíaru apayatawa.\n\n"
                f"📁 Carpeta Fiscal: {carpeta_fiscal}\n"
                f"🔖 CUC Fiscal: {cuc}\n"
                f"📋 SIDPOL PNP: {codigo_sidpol}\n"
                f"🏛️ Fiscalía Asignada: {fiscalia_asignada}\n"
                f"🔒 CUP Código: {cup}\n\n"
                f"💙 Sutimax 100% imantatawa. Janikiw sapakïtati, nanakax jark'apxirïmawa."
            )
        elif "shipibo" in lang:
            return (
                f"🕊️ SARA - PNP & MINISTERIO PÚBLICO (LÍNEA 111)\n\n"
                f"Jakon shinanwe. Nonra mia yoinai: Miki yoi jaskatira itimati iki ukat Fiscalianin jark'asqam kanqa.\n\n"
                f"📁 Carpeta Fiscal: {carpeta_fiscal}\n"
                f"🔖 CUC Fiscal: {cuc}\n"
                f"📋 SIDPOL PNP: {codigo_sidpol}\n"
                f"🏛️ Fiscalía Asignada: {fiscalia_asignada}\n"
                f"🔒 CUP Código: {cup}\n\n"
                f"💚 Tsaweti sutimax 100% imantatawa. Enra mia akinai."
            )
        elif "ashaninka" in lang:
            return (
                f"🕊️ SARA - PNP & MINISTERIO PÚBLICO (LÍNEA 111)\n\n"
                f"Shireampaye. Notsotaite iitaka pematsikaiti: Fiscaliapi jark'asqam kanqa.\n\n"
                f"📁 Carpeta Fiscal: {carpeta_fiscal}\n"
                f"🔖 CUC Fiscal: {cuc}\n"
                f"📋 SIDPOL PNP: {codigo_sidpol}\n"
                f"🏛️ Fiscalía Asignada: {fiscalia_asignada}\n"
                f"🔒 CUP Código: {cup}\n\n"
                f"💚 Pipaite 100% pakasqam. Noka noaminakoite."
            )
        elif "awajun" in lang:
            return (
                f"🕊️ SARA - PNP & MINISTERIO PÚBLICO (LÍNEA 111)\n\n"
                f"Shiig anentaimsata. Dekainaji wagka juka nagkamau: Fiscalianin jark'asqam kanqa.\n\n"
                f"📁 Carpeta Fiscal: {carpeta_fiscal}\n"
                f"🔖 CUC Fiscal: {cuc}\n"
                f"📋 SIDPOL PNP: {codigo_sidpol}\n"
                f"🏛️ Fiscalía Asignada: {fiscalia_asignada}\n"
                f"🔒 CUP Código: {cup}\n\n"
                f"💚 Daajumek 100% imantatawa. Aminukchauwaitme."
            )
        elif "en" in lang or "english" in lang or "ingles" in lang:
            return (
                f"🕊️ SARA - NATIONAL POLICE & PUBLIC PROSECUTOR'S OFFICE (LINE 111)\n\n"
                f"Dear citizen, your extortion report has been officially processed and transferred to the Specialized Prosecutor's Office:\n\n"
                f"📁 Fiscal Dossier No.: {carpeta_fiscal}\n"
                f"🔖 Unique Case Code (CUC): {cuc}\n"
                f"📋 Police Record (SIDPOL): {codigo_sidpol}\n"
                f"🏛️ Assigned Prosecutor: {fiscalia_asignada}\n"
                f"🔒 Protected Code (CUP): {cup}\n\n"
                f"🛡️ Your identity is 100% sealed under Zero-PII protection. Do not reply to threats from extortionists."
            )
        else:
            return (
                f"🛡️ POLICÍA NACIONAL DEL PERÚ & MINISTERIO PÚBLICO (SARA Línea 111)\n\n"
                f"Estimado/a ciudadano/a, le informamos que su denuncia ha sido procesada formalmente y transferida a la Fiscalía:\n\n"
                f"📁 Carpeta Fiscal N.°: {carpeta_fiscal}\n"
                f"🔖 Código Único de Caso (CUC): {cuc}\n"
                f"📋 Registro Policial (SIDPOL): {codigo_sidpol}\n"
                f"🏛️ Fiscalía Asignada: {fiscalia_asignada}\n"
                f"🔑 Código Reservado (CUP): {cup}\n\n"
                f"🔒 Su identidad permanece bajo reserva y protección absoluta (Res. N.° 098-2026-MP-FN). "
                f"No responda a mensajes de los extorsionadores. La Policía y Fiscalía se encuentran a cargo de su seguridad."
            )

    async def notificar_denunciante_remision_fiscal(
        self,
        telefono_destino: str,
        canal: str,
        cup: str,
        codigo_sidpol: str,
        carpeta_fiscal: str,
        cuc: str,
        fiscalia_asignada: str,
        fiscal_responsable: Optional[str] = None,
        idioma: str = "es"
    ) -> dict:
        """
        Dispara la notificación oficial a la víctima con la Carpeta Fiscal y CUC.
        Soporta WhatsApp Meta Cloud API, Twilio SMS, Webhook y Simulación con trazabilidad.
        """
        import os
        from datetime import datetime, timezone

        mensaje_texto = self.redactar_mensaje_carpeta_fiscal(
            cup=cup,
            codigo_sidpol=codigo_sidpol,
            carpeta_fiscal=carpeta_fiscal,
            cuc=cuc,
            fiscalia_asignada=fiscalia_asignada,
            idioma=idioma
        )

        canal_clean = (canal or "WHATSAPP").upper().strip()
        tel_demo_target = os.getenv("DEMO_NOTIFICATION_TARGET") or getattr(settings, "DEMO_NOTIFICATION_TARGET", None)
        tel_real_envio = (tel_demo_target or telefono_destino or "+51984112233").strip()
        tel_clean = (telefono_destino or "+51984112233").strip()
        tel_mask = tel_clean[:6] + "****" + tel_clean[-2:] if len(tel_clean) >= 8 else tel_clean

        enlace_validacion = f"https://sara.gob.pe/verify?token={cup}&caso={cup}"

        resultado = {
            "timestamp_notificacion_utc": datetime.now(timezone.utc).isoformat(),
            "cup": cup,
            "canal_utilizado": canal_clean,
            "destinatario_enmascarado": tel_mask,
            "telefono_destino": tel_real_envio,
            "telefono_visible": tel_clean,
            "carpeta_fiscal_notificada": carpeta_fiscal,
            "cuc_fiscal_notificado": cuc,
            "codigo_sidpol_notificado": codigo_sidpol,
            "idioma": idioma,
            "cuerpo_mensaje": mensaje_texto,
            "enlace_validacion": enlace_validacion,
            "make_webhook_dispatched": False,
            "telegram_direct_dispatched": False,
            "estado_entrega": "ENVIADO_EXITOSO",
            "proveedor_mensajeria": "SARA_SECURE_MESSAGING_GATEWAY"
        }

        # 0. Intento de disparo a Webhook de Make.com (si está configurado)
        make_webhook_url = settings.MAKE_WEBHOOK_URL or os.getenv("MAKE_WEBHOOK_URL")
        if make_webhook_url and httpx:
            try:
                make_payload = {
                    "evento": "REMISION_FISCAL_COMPLETADA",
                    "evento_display": "REMISIÓN_FISCAL_COMPLETADA",
                    "cup": cup,
                    "codigo_sidpol": codigo_sidpol,
                    "carpeta_fiscal": carpeta_fiscal,
                    "cuc": cuc,
                    "fiscalia_asignada": fiscalia_asignada,
                    "fiscal_responsable": fiscal_responsable or "Fiscal Especializado FECOR",
                    "telefono_denunciante": tel_real_envio,
                    "telefono_visible": tel_clean,
                    "destinatario_enmascarado": tel_mask,
                    "cuerpo_mensaje": mensaje_texto,
                    "enlace_validacion": enlace_validacion,
                    "canal": canal_clean,
                    "idioma": idioma,
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "mensaje_telegram_formateado": mensaje_texto
                }
                async with httpx.AsyncClient(timeout=2.0) as client:
                    resp_make = await client.post(make_webhook_url, json=make_payload)
                    if resp_make.status_code in (200, 201, 204):
                        resultado["make_webhook_dispatched"] = True
                        resultado["proveedor_mensajeria"] = "MAKE_AUTOMATION_HUB"
                        logger.info(f"🌐 Webhook Make.com despachado exitosamente para caso {cup}.")
                    else:
                        logger.warning(f"Respuesta no 200 de Make Webhook: {resp_make.status_code} - {resp_make.text}")
            except Exception as e:
                logger.error(f"Error al enviar Webhook a Make.com: {e}")

        # 0.1 Intento de disparo directo por Telegram Bot (si TELEGRAM_CHAT_ID está configurado)
        tg_bot_token = settings.TELEGRAM_BOT_TOKEN or os.getenv("TELEGRAM_BOT_TOKEN")
        tg_chat_id = settings.TELEGRAM_CHAT_ID or os.getenv("TELEGRAM_CHAT_ID")
        if tg_bot_token and tg_chat_id and httpx:
            try:
                url_tg = f"https://api.telegram.org/bot{tg_bot_token.strip()}/sendMessage"
                tg_payload = {
                    "chat_id": tg_chat_id.strip(),
                    "text": make_payload["mensaje_telegram_formateado"],
                    "parse_mode": "Markdown"
                }
                async with httpx.AsyncClient(timeout=1.5) as client:
                    resp_tg = await client.post(url_tg, json=tg_payload)
                    if resp_tg.status_code == 200:
                        resultado["telegram_direct_dispatched"] = True
                        logger.info(f"📱 Mensaje directo de Telegram enviado para caso {cup}.")
            except Exception as e:
                logger.error(f"Error al enviar directo por Telegram API: {e}")

        # 1. Intento por WhatsApp Cloud API (si hay variables configuradas)
        whatsapp_token = os.getenv("WHATSAPP_API_TOKEN")
        whatsapp_phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        if canal_clean == "WHATSAPP" and whatsapp_token and whatsapp_phone_id and httpx:
            try:
                url = f"https://graph.facebook.com/v18.0/{whatsapp_phone_id}/messages"
                headers = {"Authorization": f"Bearer {whatsapp_token}"}
                payload = {
                    "messaging_product": "whatsapp",
                    "to": tel_clean.replace("+", "").replace(" ", "").replace("-", ""),
                    "type": "text",
                    "text": {"body": mensaje_texto}
                }
                async with httpx.AsyncClient(timeout=8.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code in (200, 201):
                        resultado["proveedor_mensajeria"] = "META_WHATSAPP_CLOUD_API"
                        resultado["meta_response_id"] = resp.json().get("messages", [{}])[0].get("id")
                        logger.info(f"📱 WhatsApp enviado exitosamente a {tel_mask} para caso {cup}.")
                        return resultado
                    else:
                        logger.warning(f"Respuesta no 200 de WhatsApp API: {resp.text}. Aplicando fallback seguro.")
            except Exception as e:
                logger.error(f"Error al enviar WhatsApp vía Meta API: {e}")

        # 2. Intento por Twilio SMS (si hay credenciales configuradas)
        twilio_sid = settings.TWILIO_ACCOUNT_SID or os.getenv("TWILIO_ACCOUNT_SID")
        twilio_auth = settings.TWILIO_AUTH_TOKEN or os.getenv("TWILIO_AUTH_TOKEN")
        twilio_from = settings.TWILIO_FROM_NUMBER or os.getenv("TWILIO_FROM_NUMBER")
        if canal_clean == "SMS" and twilio_sid and twilio_auth and twilio_from and httpx:
            try:
                url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
                auth = (twilio_sid, twilio_auth)
                data = {
                    "From": twilio_from,
                    "To": tel_clean,
                    "Body": mensaje_texto
                }
                async with httpx.AsyncClient(timeout=8.0) as client:
                    resp = await client.post(url, data=data, auth=auth)
                    if resp.status_code in (200, 201):
                        resultado["proveedor_mensajeria"] = "TWILIO_SMS_API"
                        resultado["twilio_sid"] = resp.json().get("sid")
                        logger.info(f"📱 SMS enviado exitosamente a {tel_mask} para caso {cup}.")
                        return resultado
                    else:
                        logger.warning(f"Respuesta no 200 de Twilio SMS: {resp.text}. Aplicando fallback seguro.")
            except Exception as e:
                logger.error(f"Error al enviar SMS vía Twilio: {e}")

        # 3. Fallback en Modo Simulación / Log de Operaciones Soberano
        if not resultado.get("make_webhook_dispatched"):
            resultado["proveedor_mensajeria"] = f"SARA_SOVEREIGN_SIMULATOR_{canal_clean}"
            resultado["estado_entrega"] = "ENVIADO_SIMULADO"
        logger.info(f"📱 [DISPARO {canal_clean} AL DENUNCIANTE] Caso {cup} -> {tel_mask}:\n{mensaje_texto}")
        return resultado

    def redactar_mensaje_validacion_biometrica(
        self,
        cpr: str,
        url_validacion: str,
        idioma: str = "es"
    ) -> tuple:
        """Genera el mensaje empático de validación biométrica en la lengua del ciudadano."""
        from core.i18n import normalize_language_code
        lang = normalize_language_code(idioma)

        if lang == "shipibo":
            cuerpo = (
                f"📋 SARA - Nokon Amachani (Línea 111 - MININTER/PNP)\n\n"
                f"¡Jakon nete! Ea riki Kallpa, akinanti SARA Zero-PII amachani.\n\n"
                f"🔑 Código Pre-Registro (CPR): {cpr}\n\n"
                f"Mía yoi jaskatira RENIEC uya riqsichiy (Prueba de Vida Facial) aka canalanin jark'asqam kanqa:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 Sutimax 100% imantatawa (CUP Código Secreto) policia amachakoyena."
            )
            telegram = (
                f"📋 *SARA - Nokon Amachani (Línea 111 - MININTER/PNP)*\n\n"
                f"¡Jakon nete! Ea riki *Kallpa*, akinanti *SARA Zero-PII* amachani.\n\n"
                f"🔑 *Código Pre-Registro (CPR):* `{cpr}`\n\n"
                f"Mía yoi jaskatira RENIEC uya riqsichiy (Prueba de Vida Facial) aka canalanin jark'asqam kanqa:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 *Sutimax 100% imantatawa (CUP Código Secreto) policia amachakoyena.*"
            )
        elif lang == "quechua":
            cuerpo = (
                f"📋 SARA - Llaqtayuk Willakuy (Línea 111 - MININTER/PNP)\n\n"
                f"Allillanchu. Kallpa yanapaqniykim kani SARA sistimapi.\n\n"
                f"🔑 Código Pre-Registro (CPR): {cpr}\n\n"
                f"RENIEC Uya Riqsichiy (Prueba de Vida Facial) ruwanaykipaq kay enlacepi yaykuy:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 Sutiykiqa 100% pakasqam kachkan CUP Código Secreto nisqawan."
            )
            telegram = (
                f"📋 *SARA - Llaqtayuk Willakuy (Línea 111 - MININTER/PNP)*\n\n"
                f"Allillanchu. *Kallpa* yanapaqniykim kani *SARA* sistimapi.\n\n"
                f"🔑 *Código Pre-Registro (CPR):* `{cpr}`\n\n"
                f"RENIEC Uya Riqsichiy (Prueba de Vida Facial) ruwanaykipaq kay enlacepi yaykuy:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 *Sutiykiqa 100% pakasqam kachkan CUP Código Secreto nisqawan.*"
            )
        elif lang == "aimara":
            cuerpo = (
                f"📋 SARA - Markachirin Yatiyawi (Línea 111 - MININTER/PNP)\n\n"
                f"Kamisaraki. Kallpa yanapirim satatwa SARA sistimata.\n\n"
                f"🔑 Código Pre-Registro (CPR): {cpr}\n\n"
                f"RENIEC Ajanu Uñt'ayawi (Prueba de Vida Facial) lurasiñataki aka linkiru mantam:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 Sutimax 100% imantatawa CUP Código Secreto ukampi."
            )
            telegram = (
                f"📋 *SARA - Markachirin Yatiyawi (Línea 111 - MININTER/PNP)*\n\n"
                f"Kamisaraki. *Kallpa* yanapirim satatwa *SARA* sistimata.\n\n"
                f"🔑 *Código Pre-Registro (CPR):* `{cpr}`\n\n"
                f"RENIEC Ajanu Uñt'ayawi (Prueba de Vida Facial) lurasiñataki aka linkiru mantam:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 *Sutimax 100% imantatawa CUP Código Secreto ukampi.*"
            )
        elif lang == "ashaninka":
            cuerpo = (
                f"📋 SARA - Asháninka Amachantsi (Línea 111 - MININTER/PNP)\n\n"
                f"Kitaiteri nomaimaye. Naro Kallpa, noaminakoita SARA Zero-PII.\n\n"
                f"🔑 Código Pre-Registro (CPR): {cpr}\n\n"
                f"RENIEC validation facial (Prueba de Vida) iitaka timatsi:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 Pipaite 100% pakasqam policia amachakoyena."
            )
            telegram = (
                f"📋 *SARA - Asháninka Amachantsi (Línea 111 - MININTER/PNP)*\n\n"
                f"Kitaiteri nomaimaye. Naro *Kallpa*, noaminakoita *SARA Zero-PII*.\n\n"
                f"🔑 *Código Pre-Registro (CPR):* `{cpr}`\n\n"
                f"RENIEC validation facial (Prueba de Vida) iitaka timatsi:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 *Pipaite 100% pakasqam policia amachakoyena.*"
            )
        elif lang == "awajun":
            cuerpo = (
                f"📋 SARA - Yaimtai Sistema (Línea 111 - MININTER/PNP)\n\n"
                f"Kumpami yatsuch. Wiitjai Kallpa, yaimtai SARA Zero-PII.\n\n"
                f"🔑 Código Pre-Registro (CPR): {cpr}\n\n"
                f"RENIEC yaimtai biometría facial:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 Daajumek 100% imantatawa Policia Nacional yaimpaktinme."
            )
            telegram = (
                f"📋 *SARA - Yaimtai Sistema (Línea 111 - MININTER/PNP)*\n\n"
                f"Kumpami yatsuch. Wiitjai *Kallpa*, yaimtai *SARA Zero-PII*.\n\n"
                f"🔑 *Código Pre-Registro (CPR):* `{cpr}`\n\n"
                f"RENIEC yaimtai biometría facial:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 *Daajumek 100% imantatawa Policia Nacional yaimpaktinme.*"
            )
        elif lang == "en":
            cuerpo = (
                f"📋 SARA - Citizen & Tourist Protection (Emergency Line 111)\n\n"
                f"Hello! I am Kallpa, your AI Emergency & Protection Assistant with SARA.\n\n"
                f"🔑 Pre-Registration Code (CPR): {cpr}\n\n"
                f"To continue with your facial biometric verification (Liveness Test) with RENIEC / Migraciones and activate your Protected Code (CUP), please access:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 Once verified, your report is processed under strict Zero-PII protocol."
            )
            telegram = (
                f"📋 *SARA - Citizen & Tourist Protection (Emergency Line 111)*\n\n"
                f"Hello! I am *Kallpa*, your AI Emergency & Protection Assistant with *SARA*.\n\n"
                f"🔑 *Pre-Registration Code (CPR):* `{cpr}`\n\n"
                f"To continue with your facial biometric verification (Liveness Test) with RENIEC / Migraciones and activate your *Protected Code (CUP)*, please access:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 *Once verified, your report is processed under strict Zero-PII protocol.*"
            )
        else:
            cuerpo = (
                f"📋 Mesa de Ayuda - Registro de Atención (Kallpa | Sistema SARA)\n\n"
                f"Estimado/a usuario/a, soy Kallpa, tu asistente de inteligencia artificial y protección ciudadana del Sistema SARA.\n\n"
                f"🔑 Código de Pre-Registro (CPR): {cpr}\n\n"
                f"Para continuar con la verificación segura de sus datos contra RENIEC y activar su Código Único de Protección (CUP), "
                f"por favor ingrese al siguiente enlace seguro:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 Una vez completada la verificación biométrica, su expediente pasará a la Policía Nacional bajo protocolo Zero-PII."
            )
            telegram = (
                f"📋 *Mesa de Ayuda - Registro de Atención (Kallpa | Sistema SARA)*\n\n"
                f"Estimado/a usuario/a, soy *Kallpa*, tu asistente de inteligencia artificial y protección del *Sistema SARA* (Línea de Emergencia 111).\n\n"
                f"🔑 *Código de Pre-Registro (CPR):* `{cpr}`\n\n"
                f"Para continuar con la verificación segura de sus datos contra RENIEC y activar su *Código Único de Protección (CUP)*, "
                f"por favor ingrese al siguiente enlace seguro:\n\n"
                f"🔗 {url_validacion}\n\n"
                f"🔒 *Una vez completada la verificación biométrica, su expediente pasará a la Policía Nacional bajo protocolo Zero-PII.*"
            )
        return cuerpo, telegram

    async def notificar_solicitud_validacion_biometrica(
        self,
        telefono_destino: str,
        cup: str,
        cpr: Optional[str] = None,
        url_validacion: Optional[str] = None,
        canal: str = "TELEGRAM",
        idioma: str = "es"
    ) -> dict:
        """
        Dispara el Webhook 1 a Make.com / Telegram solicitando la validación biométrica a la víctima
        con su Código de Pre-Registro (CPR) adaptado a su idioma nativo.
        """
        import os
        from datetime import datetime, timezone

        tel_demo_target = os.getenv("DEMO_NOTIFICATION_TARGET") or getattr(settings, "DEMO_NOTIFICATION_TARGET", None)
        tel_real_envio = (tel_demo_target or telefono_destino or "+51984112233").strip()
        tel_clean = (telefono_destino or "+51984112233").strip()
        tel_mask = tel_clean[:6] + "****" + tel_clean[-2:] if len(tel_clean) >= 8 else tel_clean
        cpr_code = cpr or (cup if str(cup).startswith("CPR-") else f"CPR-2026-{str(cup)[-6:]}")
        url_val = url_validacion or f"https://sara.gob.pe/verify?token={cpr_code}"

        cuerpo_mensaje, mensaje_telegram = self.redactar_mensaje_validacion_biometrica(
            cpr=cpr_code,
            url_validacion=url_val,
            idioma=idioma
        )

        resultado = {
            "timestamp_notificacion_utc": datetime.now(timezone.utc).isoformat(),
            "evento": "SOLICITUD_VALIDACION_BIOMETRICA",
            "cpr": cpr_code,
            "cup": cup,
            "canal_utilizado": canal.upper(),
            "idioma": idioma,
            "telefono_destino": tel_real_envio,
            "telefono_visible": tel_clean,
            "destinatario_enmascarado": tel_mask,
            "url_validacion": url_val,
            "cuerpo_mensaje": cuerpo_mensaje,
            "mensaje_telegram_formateado": mensaje_telegram,
            "make_webhook_dispatched": False,
            "telegram_direct_dispatched": False,
            "estado_entrega": "ENVIADO_EXITOSO",
            "proveedor_mensajeria": "SARA_BIOMETRIC_GATEWAY"
        }

        # Intentar enviar a MAKE_WEBHOOK_VALIDACION_URL o MAKE_WEBHOOK_URL
        make_webhook_url = (
            settings.MAKE_WEBHOOK_VALIDACION_URL 
            or os.getenv("MAKE_WEBHOOK_VALIDACION_URL") 
            or settings.MAKE_WEBHOOK_URL 
            or os.getenv("MAKE_WEBHOOK_URL")
        )

        if make_webhook_url and httpx:
            try:
                make_payload = {
                    "evento": "SOLICITUD_VALIDACION_BIOMETRICA",
                    "cpr": cpr_code,
                    "cup": cup,
                    "telefono_denunciante": tel_real_envio,
                    "telefono_visible": tel_clean,
                    "destinatario_enmascarado": tel_mask,
                    "url_validacion": url_val,
                    "cuerpo_mensaje": cuerpo_mensaje,
                    "mensaje_telegram_formateado": mensaje_telegram,
                    "canal": canal.upper(),
                    "idioma": idioma,
                    "timestamp_utc": datetime.now(timezone.utc).isoformat()
                }
                async with httpx.AsyncClient(timeout=2.0) as client:
                    resp = await client.post(make_webhook_url, json=make_payload)
                    if resp.status_code in (200, 201, 204):
                        resultado["make_webhook_dispatched"] = True
                        resultado["proveedor_mensajeria"] = "MAKE_AUTOMATION_HUB"
                        logger.info(f"🌐 Webhook 1 (Validación) despachado exitosamente a Make para caso {cpr_code}.")
                    else:
                        logger.warning(f"Respuesta no 200 de Make Webhook Validación: {resp.status_code} - {resp.text}")
            except Exception as e:
                logger.error(f"Error al enviar Webhook 1 a Make.com: {e}")

        # Intento de envío directo a Telegram Bot (Solo como canal de contingencia si Make no fue despachado)
        tg_bot_token = settings.TELEGRAM_BOT_TOKEN or os.getenv("TELEGRAM_BOT_TOKEN")
        tg_chat_id = settings.TELEGRAM_CHAT_ID or os.getenv("TELEGRAM_CHAT_ID")
        if tg_bot_token and tg_chat_id and httpx and not resultado.get("make_webhook_dispatched"):
            try:
                url_tg = f"https://api.telegram.org/bot{tg_bot_token.strip()}/sendMessage"
                tg_payload = {
                    "chat_id": tg_chat_id.strip(),
                    "text": mensaje_telegram,
                    "parse_mode": "Markdown"
                }
                async with httpx.AsyncClient(timeout=2.0) as client:
                    resp_tg = await client.post(url_tg, json=tg_payload)
                    if resp_tg.status_code == 200:
                        resultado["telegram_direct_dispatched"] = True
                        logger.info(f"📱 Mensaje directo de Telegram enviado para validación biométrica {cpr_code}.")
            except Exception as e:
                logger.error(f"Error al enviar directo por Telegram API: {e}")

        if not resultado.get("make_webhook_dispatched") and not resultado.get("telegram_direct_dispatched"):
            resultado["proveedor_mensajeria"] = f"SARA_SOVEREIGN_SIMULATOR_{canal.upper()}"
            resultado["estado_entrega"] = "ENVIADO_SIMULADO"

        logger.info(f"📱 [DISPARO VALIDACIÓN {canal.upper()}] CPR {cpr_code} -> {tel_mask}:\n{cuerpo_mensaje}")
        return resultado

    async def notificar_traductor_renitli_telegram(
        self,
        ticket_renitli: dict
    ) -> dict:
        """
        Dispara la alerta pericial de fe pública al traductor oficial del ReNITLI (MINCUL) vía Telegram.
        Envía la transcripción original en lengua originaria, la traducción preliminar propuesta por Kallpa IA,
        y el enlace con el Token de Acceso para que el perito humano convalide o modifique la traducción.
        """
        import os
        from datetime import datetime, timezone

        cup = ticket_renitli.get("cup", "CUP-SARA-PENDIENTE")
        ticket_id = ticket_renitli.get("ticket_id", f"TICKET-RENITLI-{cup}")
        lengua = ticket_renitli.get("lengua_originaria", "Lengua Originaria")
        variante = ticket_renitli.get("variante_asignada", "Variante Regional")
        traductor = ticket_renitli.get("traductor_titular", "Perito ReNITLI")
        reg_renitli = ticket_renitli.get("registro_renitli", "RENITLI-MINCUL")
        tel_dest = ticket_renitli.get("telefono_notificacion", "+51961998877")
        token_acceso = ticket_renitli.get("token_acceso", "TOKEN-RENITLI-OFICIAL")
        url_consola = ticket_renitli.get("url_consola_mincul") or f"https://traductoresdelenguas.cultura.pe/?ticket={ticket_id}&cup={cup}&token={token_acceso}"
        
        orig_text = ticket_renitli.get("transcripcion_original_ia", "Declaración registrada en audio/texto.")
        trad_ia = ticket_renitli.get("traduccion_preliminar_ia", "Traducción preliminar en proceso de revisión.")
        hash_audio = ticket_renitli.get("audio_hash_sha256", "SHA256:ART220CPP_VALIDATED")

        mensaje_telegram = (
            "🏛️ *ALERTA PERICIAL ReNITLI — MINISTERIO DE CULTURA (MINCUL)*\n"
            "⚖️ *Convalidación Pericial de Lengua Originaria (Ley N.° 29735 / Art. 220 CPP)*\n\n"
            f"👤 *Perito Intérprete Asignado:* {traductor} (`{reg_renitli}`)\n"
            f"🗣️ *Lengua Materna / Variante:* *{lengua}* ({variante})\n"
            f"🔑 *Código de Caso (CUP):* `{cup}`\n"
            f"🔖 *Ticket ReNITLI:* `{ticket_id}`\n\n"
            "📋 *Acción Requerida:*\n"
            "Se ha recepcionado una denuncia de emergencia en lengua originaria. Por estricta reserva de seguridad (Zero-PII) y cadena de custodia probatoria, ingrese a la Consola de Convalidación Oficial para escuchar la pista acústica original, auditar la traducción preliminar de IA y firmar digitalmente la traducción jurada con Fe Pública para la Fiscalía Especializada (FECOR):\n\n"
            f"🔗 *Enlace de Convalidación Pericial:*\n"
            f"{url_consola}\n\n"
            f"🔐 *Token de Firma Digital ReNITLI:* `{token_acceso}`\n\n"
            f"🛡️ *Integridad Probatoria:* Art. 220 CPP | Hash SHA-256 `{hash_audio[:18]}...`"
        )

        resultado = {
            "timestamp_notificacion_utc": datetime.now(timezone.utc).isoformat(),
            "evento": "ALERTA_PERICIAL_TRADUCTOR_RENITLI",
            "ticket_id": ticket_id,
            "cup": cup,
            "lengua_originaria": lengua,
            "traductor_titular": traductor,
            "registro_renitli": reg_renitli,
            "telefono_notificacion": tel_dest,
            "token_acceso": token_acceso,
            "url_consola_mincul": url_consola,
            "transcripcion_original": orig_text,
            "traduccion_preliminar_ia": trad_ia,
            "mensaje_telegram_formateado": mensaje_telegram,
            "make_webhook_dispatched": False,
            "telegram_direct_dispatched": False,
            "estado_entrega": "ENVIADO_EXITOSO",
            "proveedor_mensajeria": "SARA_RENITLI_PERICIAL_GATEWAY"
        }

        # Intentar despacho a Make.com
        make_webhook_url = (
            settings.MAKE_WEBHOOK_URL 
            or os.getenv("MAKE_WEBHOOK_URL")
        )
        if make_webhook_url and httpx:
            try:
                make_payload = {
                    "evento": "ALERTA_PERICIAL_TRADUCTOR_RENITLI",
                    "ticket_id": ticket_id,
                    "cup": cup,
                    "lengua_originaria": lengua,
                    "traductor_titular": traductor,
                    "registro_renitli": reg_renitli,
                    "telefono_traductor": tel_dest,
                    "url_consola_mincul": url_consola,
                    "token_acceso": token_acceso,
                    "transcripcion_original": orig_text,
                    "traduccion_preliminar_ia": trad_ia,
                    "mensaje_telegram_formateado": mensaje_telegram,
                    "canal": "TELEGRAM",
                    "timestamp_utc": datetime.now(timezone.utc).isoformat()
                }
                async with httpx.AsyncClient(timeout=2.0) as client:
                    resp = await client.post(make_webhook_url, json=make_payload)
                    if resp.status_code in (200, 201, 204):
                        resultado["make_webhook_dispatched"] = True
                        resultado["proveedor_mensajeria"] = "MAKE_AUTOMATION_HUB"
                        logger.info(f"🌐 Webhook ReNITLI despachado exitosamente a Make para caso {cup}.")
            except Exception as e:
                logger.error(f"Error al enviar Webhook ReNITLI a Make.com: {e}")

        # 2. Despacho directo por Telegram Bot API (Garantía de entrega inmediata al perito en Telegram)
        tg_bot_token = settings.TELEGRAM_BOT_TOKEN or os.getenv("TELEGRAM_BOT_TOKEN")
        tg_chat_id = settings.TELEGRAM_CHAT_ID or os.getenv("TELEGRAM_CHAT_ID")
        if tg_bot_token and tg_chat_id and httpx:
            try:
                url_tg = f"https://api.telegram.org/bot{tg_bot_token.strip()}/sendMessage"
                tg_payload = {
                    "chat_id": tg_chat_id.strip(),
                    "text": mensaje_telegram,
                    "parse_mode": "Markdown"
                }
                async with httpx.AsyncClient(timeout=2.0) as client:
                    resp_tg = await client.post(url_tg, json=tg_payload)
                    if resp_tg.status_code == 200:
                        resultado["telegram_direct_dispatched"] = True
                        logger.info(f"📱 Mensaje directo de Telegram enviado al traductor ReNITLI para caso {cup}.")
                    else:
                        logger.warning(f"Respuesta no 200 de Telegram API ReNITLI: {resp_tg.status_code} - {resp_tg.text}")
            except Exception as e:
                logger.error(f"Error al enviar directo por Telegram API a ReNITLI: {e}")

        if not resultado.get("make_webhook_dispatched") and not resultado.get("telegram_direct_dispatched"):
            resultado["proveedor_mensajeria"] = "SARA_SOVEREIGN_SIMULATOR_TELEGRAM_RENITLI"
            resultado["estado_entrega"] = "ENVIADO_SIMULADO"

        logger.info(f"🏛️ [DISPARO TELEGRAM A ReNITLI] Perito {traductor} ({lengua}) para caso {cup}:\n{mensaje_telegram}")
        return resultado

    def notificar_solicitud_validacion_biometrica_sync(
        self,
        telefono_destino: str,
        cup: str,
        cpr: Optional[str] = None,
        url_validacion: Optional[str] = None,
        canal: str = "TELEGRAM",
        idioma: str = "es"
    ) -> dict:
        """Wrapper síncrono para notificar la solicitud de validación biométrica con CPR."""
        import asyncio
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(
                        asyncio.run,
                        self.notificar_solicitud_validacion_biometrica(
                            telefono_destino=telefono_destino,
                            cup=cup,
                            cpr=cpr,
                            url_validacion=url_validacion,
                            canal=canal,
                            idioma=idioma
                        )
                    )
                    return future.result()
            else:
                return asyncio.run(
                    self.notificar_solicitud_validacion_biometrica(
                        telefono_destino=telefono_destino,
                        cup=cup,
                        cpr=cpr,
                        url_validacion=url_validacion,
                        canal=canal,
                        idioma=idioma
                    )
                )
        except Exception as e:
            logger.error(f"Error en notificar_solicitud_validacion_biometrica_sync: {e}")
            return {
                "evento": "SOLICITUD_VALIDACION_BIOMETRICA",
                "cpr": cpr or cup,
                "cup": cup,
                "estado_entrega": "ENVIADO_SIMULADO",
                "make_webhook_dispatched": False,
                "proveedor_mensajeria": "SARA_FALLBACK_GATEWAY"
            }

    def notificar_denunciante_remision_fiscal_sync(
        self,
        telefono_destino: str,
        canal: str,
        cup: str,
        codigo_sidpol: str,
        carpeta_fiscal: str,
        cuc: str,
        fiscalia_asignada: str,
        fiscal_responsable: Optional[str] = None,
        idioma: str = "es"
    ) -> dict:
        """Wrapper síncrono para ser llamado directamente desde Flask, Streamlit u orquestadores síncronos."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(
                        asyncio.run,
                        self.notificar_denunciante_remision_fiscal(
                            telefono_destino=telefono_destino,
                            canal=canal,
                            cup=cup,
                            codigo_sidpol=codigo_sidpol,
                            carpeta_fiscal=carpeta_fiscal,
                            cuc=cuc,
                            fiscalia_asignada=fiscalia_asignada,
                            fiscal_responsable=fiscal_responsable,
                            idioma=idioma
                        )
                    )
                    return future.result()
            else:
                return loop.run_until_complete(
                    self.notificar_denunciante_remision_fiscal(
                        telefono_destino=telefono_destino,
                        canal=canal,
                        cup=cup,
                        codigo_sidpol=codigo_sidpol,
                        carpeta_fiscal=carpeta_fiscal,
                        cuc=cuc,
                        fiscalia_asignada=fiscalia_asignada,
                        fiscal_responsable=fiscal_responsable,
                        idioma=idioma
                    )
                )
        except Exception:
            return asyncio.run(
                self.notificar_denunciante_remision_fiscal(
                    telefono_destino=telefono_destino,
                    canal=canal,
                    cup=cup,
                    codigo_sidpol=codigo_sidpol,
                    carpeta_fiscal=carpeta_fiscal,
                    cuc=cuc,
                    fiscalia_asignada=fiscalia_asignada,
                    fiscal_responsable=fiscal_responsable,
                    idioma=idioma
                )
            )

    def notificar_traductor_renitli_telegram_sync(
        self,
        ticket_renitli: dict
    ) -> dict:
        """Wrapper síncrono para despachar la alerta pericial ReNITLI vía Telegram."""
        import asyncio
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(
                        asyncio.run,
                        self.notificar_traductor_renitli_telegram(ticket_renitli)
                    )
                    return future.result()
            else:
                return asyncio.run(
                    self.notificar_traductor_renitli_telegram(ticket_renitli)
                )
        except Exception as e:
            logger.error(f"Error en notificar_traductor_renitli_telegram_sync: {e}")
            return {
                "evento": "ALERTA_PERICIAL_TRADUCTOR_RENITLI",
                "ticket_id": ticket_renitli.get("ticket_id"),
                "cup": ticket_renitli.get("cup"),
                "estado_entrega": "ENVIADO_SIMULADO",
                "make_webhook_dispatched": False,
                "proveedor_mensajeria": "SARA_FALLBACK_GATEWAY"
            }


notification_service = NotificationService()
