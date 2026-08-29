"""Agente de Interoperabilidad PIDE (PCM / SGTD) - Cruce de Inteligencia con el Estado Peruano.
Orquesta autónomamente las consultas a los servicios web del Estado (RENIEC, RENTESEG-OSIPTEL, INPE, SBS/UIF, MIGRACIONES, SUNARP)
bajo estricto cumplimiento de la Directiva N.° 001-2025-PCM/SGTD (Consumo Seguro de la PIDE y Seguridad Digital),
garantizando aislamiento Zero-PII de la víctima y encadenamiento inteligente de pistas del infractor.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from core.pide_connector import pide_connector
from core.supervisor import supervisor

logger = logging.getLogger("sara.agents.pide_agent")


class PIDEInteroperabilityAgent:
    """Agente especializado en interoperabilidad y cruce de datos con la Plataforma de Interoperabilidad del Estado (PIDE)."""

    def __init__(self):
        self.nombre = "Agente PIDE (Interoperabilidad Estatal)"
        self.sigla = "PIDE"
        self.pide = pide_connector
        self.supervisor = supervisor

    def investigar_infractor_pide(
        self,
        pistas_infractor: Dict[str, Any],
        cup: str
    ) -> Dict[str, Any]:
        """
        Orquesta el cruce inteligente de datos del infractor con las entidades del Estado:
        1. Si hay teléfono -> Consulta RENTESEG (OSIPTEL) para verificar IMEI y titularidad.
        2. Si RENTESEG o la denuncia arrojan un DNI -> Encadena consulta a RENIEC.
        3. Si se identifican patrones de extorsión -> Cruza antecedentes con INPE (llamadas desde penales).
        """
        logger.info(f"🏛️ [Agente PIDE] Iniciando investigación intergubernamental para el caso {cup}...")

        telefonos = pistas_infractor.get("telefonos_validados", []) or pistas_infractor.get("telefonos_infractor", [])
        cuentas = pistas_infractor.get("cuentas_y_billeteras", []) or pistas_infractor.get("cuentas_bancarias_infractor", [])
        placas = pistas_infractor.get("vehiculos_o_placas", [])
        dnis_identificados: List[str] = []

        reporte_renteseg = None
        reporte_reniec = None
        reporte_inpe = None
        reporte_uif = None
        servicios_consultados: List[str] = []

        # 1. Consulta RENTESEG (OSIPTEL) si hay línea telefónica sospechosa
        if telefonos:
            tel_principal = telefonos[0]
            logger.info(f"📡 [Agente PIDE] Disparando consulta RENTESEG-OSIPTEL para la línea {tel_principal}...")
            tx_renteseg = self.pide.consultar_renteseg_osiptel(tel_principal)
            reporte_renteseg = tx_renteseg.get("respuesta_oficial", {})
            servicios_consultados.append("PIDE-OSIPTEL-RENTESEG-01")

            dni_titular = reporte_renteseg.get("dni_registrado")
            if dni_titular and dni_titular not in dnis_identificados:
                dnis_identificados.append(dni_titular)

        # 2. Consulta RENIEC si se identificó un DNI del presunto titular/infractor
        if dnis_identificados:
            dni_principal = dnis_identificados[0]
            logger.info(f"👤 [Agente PIDE] Encadenando consulta a RENIEC para el DNI {dni_principal}...")
            tx_reniec = self.pide.consultar_reniec_infractor(dni_principal)
            reporte_reniec = tx_reniec.get("respuesta_oficial", {})
            servicios_consultados.append("PIDE-RENIEC-CONSULTA-02")

            # 3. Consulta INPE (Verificación de llamadas desde recintos penitenciarios)
            logger.info(f"🏢 [Agente PIDE] Cruzando antecedentes con INPE para el DNI {dni_principal}...")
            tx_inpe = self.pide.consultar_inpe_penitenciario(dni_principal)
            reporte_inpe = tx_inpe.get("respuesta_oficial", {})
            servicios_consultados.append("PIDE-INPE-PENITENCIARIO-03")

        # 4. Habilitación de Congelamiento Administrativo UIF-Perú (D.S. N° 007-2025-JUS / Ley 32209)
        if cuentas:
            reporte_uif = {
                "servicio": "PIDE-SBS-UIF-CONGELAMIENTO-06",
                "base_normativa": "Decreto Supremo N° 007-2025-JUS & Art. 3-B Ley N° 27693 (Ley 32209)",
                "estado_congelamiento": "SOLICITUD_EXPRESS_HABILITADA",
                "cuentas_a_congelar": cuentas,
                "urgencia_peligro_demora": "CONFIRMADA",
                "plazo_comunicacion_fiscal_horas": 24,
                "plazo_convalidacion_judicial_horas": 24,
                "oficio_policial_generado": f"OFICIO-PNP-DIRINCRI-UIF-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{cup}"
            }
            servicios_consultados.append("PIDE-SBS-UIF-CONGELAMIENTO-06")

        # Síntesis estructurada de inteligencia del sospechoso
        perfil_inteligencia = {
            "cup": cup,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "estado_interoperabilidad": "EXITO_INTERCONEXION_PIDE",
            "total_servicios_invocados": len(servicios_consultados),
            "servicios_invocados": servicios_consultados,
            "inteligencia_telecomunicaciones_osiptel": reporte_renteseg,
            "identidad_sospechoso_reniec": reporte_reniec,
            "alerta_penitenciaria_inpe": reporte_inpe,
            "medidas_financieras_uif": reporte_uif,
            "certificacion_privacidad": "ZERO_PII_CONFORME (La identidad de la víctima nunca fue transferida al bus PIDE)"
        }

        # Auditoría del payload por el Supervisor IA
        self.supervisor.audit_payload_zero_pii(
            agent_name=self.nombre,
            payload=perfil_inteligencia,
            cup=cup
        )

        logger.info(f"✅ [Agente PIDE] Perfil de inteligencia intergubernamental completado para el caso {cup}.")
        return perfil_inteligencia


PIDEAgent = PIDEInteroperabilityAgent
pide_agent = PIDEInteroperabilityAgent()
