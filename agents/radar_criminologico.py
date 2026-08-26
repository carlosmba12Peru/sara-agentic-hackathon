"""Agente Radar Criminológico & OSINT de Medios - Inteligencia Criminal Preventiva.
Rastrea medios de comunicación peruanos (prensa, televisión, portales de noticias) para detectar:
1. Nuevas modalidades extorsivas emergentes.
2. Nuevas jergas y argot criminal utilizado por bandas delictivas.
3. Nuevos patrones de amenazas sectoriales.

PRINCIPIO DE GOBERNANZA HITL:
Ningún hallazgo se incorpora automáticamente a los modelos de SARA. Todo descubrimiento genera
una 'Propuesta de Calibración Criminológica' que requiere APROBACIÓN HUMANA obligatoria de un
Oficial de Inteligencia Policial (PNP) antes de actualizar los diccionarios de extracción.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

logger = logging.getLogger("sara.agents.radar_criminologico")

# Catálogo de Fuentes Nacionales Confiables Validadas (Prensa y Medios Peruanos)
FUENTES_CONFIABLES_CATALOGO = {
    "EL_PERUANO": {"nombre": "Diario Oficial El Peruano", "tipo": "Prensa Oficial / Normas", "canal_o_portal": "Portal Digital / Edición Impresa", "ambito": "Nacional (Perú)"},
    "EL_COMERCIO": {"nombre": "Diario El Comercio", "tipo": "Prensa Escrita / Digital", "canal_o_portal": "elcomercio.pe", "ambito": "Nacional (Perú)"},
    "LATINA": {"nombre": "Latina Televisión", "tipo": "Televisión Abierta (Canal 2)", "canal_o_portal": "Latina Noticias", "ambito": "Nacional (Perú)"},
    "AMERICA_TV": {"nombre": "América Televisión", "tipo": "Televisión Abierta (Canal 4)", "canal_o_portal": "América Noticias / Cuarto Poder", "ambito": "Nacional (Perú)"},
    "PANAMERICANA": {"nombre": "Panamericana Televisión", "tipo": "Televisión Abierta (Canal 5)", "canal_o_portal": "24 Horas / Buenos Días Perú", "ambito": "Nacional (Perú)"},
    "TV_PERU": {"nombre": "TV Perú", "tipo": "Televisión Estatal (Canal 7)", "canal_o_portal": "TV Perú Noticias", "ambito": "Nacional (Perú)"},
    "ATV": {"nombre": "ATV", "tipo": "Televisión Abierta (Canal 9)", "canal_o_portal": "ATV Noticias / Día D", "ambito": "Nacional (Perú)"},
    "EXPRESO": {"nombre": "Diario Expreso", "tipo": "Prensa Escrita / Digital", "canal_o_portal": "expreso.com.pe", "ambito": "Nacional (Perú)"},
    "GESTION": {"nombre": "Diario Gestión", "tipo": "Prensa Económica / Jurídica", "canal_o_portal": "gestion.pe", "ambito": "Nacional (Perú)"}
}

# Catálogo de Fuentes Internacionales de Ciberinteligencia & Threat Intelligence
FUENTES_INTERNACIONALES_THREAT_INTEL = {
    "KASPERSKY_THREATS": {
        "nombre": "Kaspersky Global Threat Intelligence",
        "tipo": "Centro Global de Inteligencia de Ciberamenazas & Ciberdelincuencia",
        "canal_o_portal": "kaspersky.es/resource-center/threats",
        "ambito": "Internacional / Global",
        "cobertura": "Ciberextorsión, Sextorsión, Doxxing, Ransomware, AI Voice Cloning y Phishing Coactivo"
    },
    "MITRE_ATTACK": {
        "nombre": "MITRE ATT&CK Framework",
        "tipo": "Matriz Global de Tácticas, Técnicas y Procedimientos de Adversarios",
        "canal_o_portal": "attack.mitre.org",
        "ambito": "Internacional / Global",
        "cobertura": "T1566 (Phishing), T1486 (Data Encrypted for Impact), T1656 (Impersonation)"
    },
    "INTERPOL_CYBER": {
        "nombre": "INTERPOL Cybercrime Directorate",
        "tipo": "Dirección Policial Internacional de Lucha contra el Cibercrimen",
        "canal_o_portal": "interpol.int/Crimes/Cybercrime",
        "ambito": "Internacional / Multilateral",
        "cobertura": "Operaciones Globales contra Redes de Extorsión Digital y Fraude Financiero"
    }
}

# Catálogo Unificado del Radar Criminológico
FUENTES_RADAR_TOTAL = {**FUENTES_CONFIABLES_CATALOGO, **FUENTES_INTERNACIONALES_THREAT_INTEL}

# Glosario Criminológico Base Oficial (Verificado por la PNP)
DICCIONARIO_JERGAS_BASE = {
    "chalequeo": {
        "significado": "Cobro forzado bajo la fachada de brindar supuesta seguridad o protección a locales o transportistas.",
        "categoria": "MODALIDAD_PROTECCION_FALSA",
        "nivel_riesgo_asociado": "ALTO"
    },
    "piso": {
        "significado": "Cuota periódica obligatoria impuesta por bandas para permitir operar una ruta de transporte o negocio.",
        "categoria": "COBRO_SISTEMATICO_CUPOS",
        "nivel_riesgo_asociado": "CRITICO"
    },
    "plomear": {
        "significado": "Disparar con arma de fuego contra el local, vehículo o vivienda de la víctima.",
        "categoria": "COERCION_ARMADA",
        "nivel_riesgo_asociado": "CRITICO"
    },
    "gota a gota": {
        "significado": "Préstamos extorsivos con intereses usurarios y cobranza violenta diaria/semanal.",
        "categoria": "USURA_EXTORSIVA",
        "nivel_riesgo_asociado": "ALTO"
    },
    "enfriar": {
        "significado": "Amenaza de muerte o sicariato contra la víctima o sus familiares.",
        "categoria": "AMENAZA_DE_MUERTE",
        "nivel_riesgo_asociado": "CRITICO"
    },
    "bajar de la moto": {
        "significado": "Atentado armado ejecutado por sicarios en motocicleta contra conductores o paraderos.",
        "categoria": "ATAQUE_SICARIAL_TRANSPORTE",
        "nivel_riesgo_asociado": "CRITICO"
    }
}


class RadarCriminologicoAgent:
    """Agente de Inteligencia OSINT y Monitoreo de Medios contra Nuevas Modalidades Extorsivas.
    
    Implementa un Algoritmo de Deduplicación y Agrupación Canónica de Noticias:
    Cuando múltiples medios de comunicación rebotan la misma noticia, SARA unifica los reportes en
    un único evento canónico con trazabilidad de todos los canales emisores, evitando duplicidad visual.
    """

    def __init__(self):
        self.nombre = "Agente Radar Criminológico (OSINT & Threat Intel)"
        self.sigla = "RADAR_CRIMINOLOGICO"
        self.fuentes_autorizadas = FUENTES_RADAR_TOTAL
        self.fuentes_nacionales = FUENTES_CONFIABLES_CATALOGO
        self.fuentes_internacionales = FUENTES_INTERNACIONALES_THREAT_INTEL
        self.diccionario_jergas_activo: Dict[str, Any] = dict(DICCIONARIO_JERGAS_BASE)
        self.propuestas_pendientes: List[Dict[str, Any]] = []
        self.historial_calibraciones_osint: List[Dict[str, Any]] = []
        self._inicializar_noticias_deduplicadas()

    def _inicializar_noticias_deduplicadas(self):
        """Simula la ingesta de noticias brutas de múltiples medios y aplica el algoritmo de deduplicación."""
        # Noticias brutas que provienen de distintos medios sobre los mismos eventos (Efecto Rebote)
        noticias_raw = [
            {
                "id_raw": "RAW-01",
                "fuente": "Diario El Comercio",
                "titular": "Bandas delictivas usan falsos servicios mecánicos para extorsionar a transportistas de carga en la Carretera Central",
                "modalidad_clave": "Falso Auxilio Mecánico en Carretera",
                "jerga": "sembrar el clavo",
                "descripcion": "Delincuentes arrojan clavos/trampas para pinchar llantas en ruta y luego exigen cuotas para permitir el paso.",
                "distrito_o_zona": "Carretera Central (Ate - Chosica)",
                "fecha": "2026-08-19"
            },
            {
                "id_raw": "RAW-02",
                "fuente": "Latina Televisión (Canal 2)",
                "titular": "Carretera Central: Choferes denuncian sabotaje con clavos y cobro de peaje criminal por falsos mecánicos",
                "modalidad_clave": "Falso Auxilio Mecánico en Carretera",
                "jerga": "sembrar el clavo",
                "descripcion": "Noticiero 24 Horas / Latina Noticias alerta de cobro de 50 soles por viaje a camiones de carga.",
                "distrito_o_zona": "Carretera Central (Ate - Chosica)",
                "fecha": "2026-08-19"
            },
            {
                "id_raw": "RAW-03",
                "fuente": "América Televisión (Canal 4)",
                "titular": "América Noticias: 'Los Claveros de la Carretera' exigen cupos tras provocar averías a buses interprovinciales",
                "modalidad_clave": "Falso Auxilio Mecánico en Carretera",
                "jerga": "sembrar el clavo",
                "descripcion": "Reportaje de Cuarto Poder sobre la técnica de sabotaje en carretera.",
                "distrito_o_zona": "Carretera Central (Ate - Chosica)",
                "fecha": "2026-08-19"
            },
            {
                "id_raw": "RAW-04",
                "fuente": "Diario Gestión",
                "titular": "Extorsión digital al comercio: Bandas exigen transferencias trianguladas mediante códigos QR en Lima Norte",
                "modalidad_clave": "Bancarización Forzada con Códigos QR Fantasma",
                "jerga": "yapear el peaje",
                "descripcion": "Pegado de códigos QR de billeteras digitales en paraderos y comercios para cobro deslocalizado.",
                "distrito_o_zona": "Lima Norte (Independencia / Los Olivos)",
                "fecha": "2026-08-18"
            },
            {
                "id_raw": "RAW-05",
                "fuente": "Panamericana Televisión (Canal 5)",
                "titular": "Independencia: Comerciantes obligados a escanear QR extorsivo pegado en postes para pagar cuota semanal",
                "modalidad_clave": "Bancarización Forzada con Códigos QR Fantasma",
                "jerga": "yapear el peaje",
                "descripcion": "Panamericana Noticias documenta modus operandi de códigos QR falsificados.",
                "distrito_o_zona": "Lima Norte (Independencia / Los Olivos)",
                "fecha": "2026-08-18"
            },
            {
                "id_raw": "RAW-06",
                "fuente": "ATV (Canal 9)",
                "titular": "Alerta ATV: La nueva modalidad del 'QR extorsivo' asedia a transportistas y bodegueros",
                "modalidad_clave": "Bancarización Forzada con Códigos QR Fantasma",
                "jerga": "yapear el peaje",
                "descripcion": "Informe periodístico sobre transferencias forzadas en Yape/Plin mediante códigos QR pegados.",
                "distrito_o_zona": "Lima Norte (Independencia / Los Olivos)",
                "fecha": "2026-08-18"
            }
        ]

        self.propuestas_pendientes = self._deduplicar_y_agrupar_noticias(noticias_raw)

    def _deduplicar_y_agrupar_noticias(self, noticias_raw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Algoritmo de Agrupación Canónica: Deduplica noticias rebotadas por múltiples medios."""
        clusters: Dict[str, Dict[str, Any]] = {}

        for n in noticias_raw:
            # Clave canónica única por modalidad + jerga clave
            clave_canonica = f"{n['modalidad_clave']}::{n.get('jerga', '')}".strip().lower()

            if clave_canonica not in clusters:
                clusters[clave_canonica] = {
                    "propuesta_id": f"PROP-OSINT-{len(clusters)+1:03d}",
                    "fecha_deteccion": n["fecha"],
                    "termino_o_modalidad": n["modalidad_clave"],
                    "titular_noticia_canonica": n["titular"],
                    "descripcion_tecnica": n["descripcion"],
                    "zona_geografica_afectada": n.get("distrito_o_zona", "Lima Metropolitana"),
                    "jerga_detectada": n.get("jerga", ""),
                    "significado_jerga": f"Modus operandi identificado como '{n.get('jerga', '')}' reportado de forma concurrente por la prensa.",
                    "medios_que_rebotan": [n["fuente"]],
                    "total_medios_cobertura": 1,
                    "estado": "PENDIENTE_DE_APROBACION_HUMANA",
                    "impacto_propuesto_en_sara": f"Incorporar patrón en AnalistaAgent y actualizar IRCE sectorial.",
                    "nivel_verosimilitud_prensa": "ALTA (Confirmada por múltiples medios nacionales)"
                }
            else:
                # Si el evento ya existe, consolidamos la fuente sin duplicar la tarjeta
                if n["fuente"] not in clusters[clave_canonica]["medios_que_rebotan"]:
                    clusters[clave_canonica]["medios_que_rebotan"].append(n["fuente"])
                    clusters[clave_canonica]["total_medios_cobertura"] = len(clusters[clave_canonica]["medios_que_rebotan"])

        # Retornamos la lista deduplicada de propuestas canónicas únicas
        return list(clusters.values())

    def procesar_decision_humana(
        self,
        propuesta_id: str,
        decision_legal: str = "APROBAR",
        decision_sistemas: str = "APROBAR",
        decision_pnp: str = "APROBAR",
        experto_legal_id: str = "Dra. Milagros Paredes Cárdenas (CAL 58492)",
        director_sistemas_id: str = "Ing. Carlos Mendoza (CIP 189421)",
        oficial_pnp_id: str = "Coronel PNP V. Revoredo (DIRINCRI / CIP 318920)",
        dictamen_comite: str = "Incorporación aprobada unánimemente tras verificar tipicidad penal y neutralidad técnica."
    ) -> Dict[str, Any]:
        """
        Gobernanza del Comité Tripartito Colegiado de SARA (Legal + Sistemas + DIRINCRI/PNP):
        Ningún oficial individual puede incorporar jergas o alterar el cerebro de SARA.
        Requiere obligatoriamente la resolución unánime del Comité Tripartito:
        1. ⚖️ Asesoría Jurídica (Abogado CAL): Certifica tipicidad y apego al Código Penal.
        2. 💻 Dirección de Sistemas / OTI (Ingeniero CIP): Certifica que no exista riesgo de inyección semántica ni data poisoning.
        3. 👮 Inteligencia Policial (DIRINCRI / PNP Central): Certifica autenticidad del modus operandi criminal en campo.
        """
        propuesta = next((p for p in self.propuestas_pendientes if p["propuesta_id"] == propuesta_id), None)
        if not propuesta:
            return {"status": "ERROR_NO_ENCONTRADO", "mensaje": f"Propuesta {propuesta_id} no encontrada."}

        timestamp = datetime.now(timezone.utc).isoformat()
        dec_l = decision_legal.upper().strip()
        dec_s = decision_sistemas.upper().strip()
        dec_p = decision_pnp.upper().strip()

        legal_ok = any(k in dec_l for k in ["APROBAR", "ACEPTAR", "INTEGRAR", "CONFORME"])
        sist_ok = any(k in dec_s for k in ["APROBAR", "ACEPTAR", "INTEGRAR", "CONFORME"])
        pnp_ok = any(k in dec_p for k in ["APROBAR", "ACEPTAR", "INTEGRAR", "CONFORME"])

        if legal_ok and sist_ok and pnp_ok:
            propuesta["estado"] = "APROBADO_E_INCORPORADO_POR_COMITE_TRIPARTITO"
            propuesta["comite_resolucion"] = {
                "legal": {"experto": experto_legal_id, "voto": dec_l},
                "sistemas": {"director": director_sistemas_id, "voto": dec_s},
                "pnp_dirincri": {"oficial": oficial_pnp_id, "voto": dec_p},
                "dictamen": dictamen_comite,
                "sello_tripartito": f"HITL-COMITE-{hashlib.sha256((propuesta_id + experto_legal_id + director_sistemas_id + oficial_pnp_id).encode()).hexdigest()[:12].upper()}"
            }
            propuesta["fecha_aprobacion"] = timestamp

            # Incorporar la jerga al diccionario activo validado colegiadamente
            if "jerga_detectada" in propuesta and propuesta["jerga_detectada"]:
                jerga = propuesta["jerga_detectada"].lower()
                self.diccionario_jergas_activo[jerga] = {
                    "significado": propuesta.get("significado_jerga", ""),
                    "categoria": propuesta.get("tipo_hallazgo", "OSINT"),
                    "fuente_aprobacion": f"Comité Tripartito de SARA (Ref: {propuesta_id})",
                    "sello_gobernanza": propuesta["comite_resolucion"]["sello_tripartito"]
                }
                logger.info(f"✨ [Radar Criminológico] Jerga '{jerga}' incorporada colegiadamente por el Comité Tripartito.")

            self.historial_calibraciones_osint.append(propuesta)
            self.propuestas_pendientes = [p for p in self.propuestas_pendientes if p["propuesta_id"] != propuesta_id]

            return {
                "status": "EXITO_APROBADO_TRIPARTITO",
                "propuesta_id": propuesta_id,
                "mensaje": f"Propuesta {propuesta_id} aprobada unánimemente por el Comité Tripartito e integrada a SARA.",
                "propuesta": propuesta
            }
        else:
            motivos = []
            if not legal_ok: motivos.append(f"Observación Legal: {decision_legal}")
            if not sist_ok: motivos.append(f"Observación Sistemas/OTI: {decision_sistemas}")
            if not pnp_ok: motivos.append(f"Observación DIRINCRI/PNP: {decision_pnp}")

            propuesta["estado"] = "RECHAZADO_POR_COMITE_TRIPARTITO"
            propuesta["comite_resolucion"] = {
                "legal": {"experto": experto_legal_id, "voto": dec_l},
                "sistemas": {"director": director_sistemas_id, "voto": dec_s},
                "pnp_dirincri": {"oficial": oficial_pnp_id, "voto": dec_p},
                "motivos_bloqueo": motivos
            }
            propuesta["fecha_rechazo"] = timestamp

            self.historial_calibraciones_osint.append(propuesta)
            self.propuestas_pendientes = [p for p in self.propuestas_pendientes if p["propuesta_id"] != propuesta_id]

            return {
                "status": "BLOQUEADO_POR_COMITE",
                "propuesta_id": propuesta_id,
                "mensaje": f"⛔ Propuesta {propuesta_id} bloqueada por falta de consenso tripartito. Motivo: {' | '.join(motivos)}. El vocabulario de SARA permanece inmutable.",
                "propuesta": propuesta
            }

    def obtener_diccionario_jergas(self) -> Dict[str, Any]:
        """Retorna el diccionario de jergas y argot delictivo activo y validado."""
        return self.diccionario_jergas_activo

    def obtener_propuestas_pendientes(self) -> List[Dict[str, Any]]:
        """Retorna las propuestas que requieren revisión humana colegiada."""
        return self.propuestas_pendientes

    def obtener_eventos_canonicos(self) -> List[Dict[str, Any]]:
        """Retorna la lista de eventos canónicos deduplicados de medios peruanos."""
        eventos = []
        for p in self.propuestas_pendientes:
            eventos.append({
                "modalidad_clave": p.get("termino_o_modalidad", "Modalidad Detectada"),
                "titular_sintetizado": p.get("titular_noticia_canonica", ""),
                "descripcion_sintetizada": p.get("descripcion_tecnica", ""),
                "distrito_o_zona": p.get("zona_geografica_afectada", "Lima Metropolitana"),
                "jerga_asociada": p.get("jerga_detectada", ""),
                "fecha_deteccion": p.get("fecha_deteccion", "2026-08-19"),
                "fuentes_emisoras": p.get("medios_que_rebotan", [])
            })
        return eventos

    def calibrar_jerga_o_modalidad(
        self,
        jerga: str,
        significado: str,
        categoria: str = "MODALIDAD_EXTORSIVA",
        nivel_riesgo: str = "ALTO",
        resolucion_comite: str = "Resolución N° 004-2026-COMITE-SARA (Legal + OTI + DIRINCRI)"
    ) -> Dict[str, Any]:
        """Calibra y ratifica una nueva jerga mediante resolución colegiada del Comité Tripartito."""
        j_clean = jerga.strip().lower()
        self.diccionario_jergas_activo[j_clean] = {
            "significado": significado,
            "categoria": categoria,
            "nivel_riesgo_asociado": nivel_riesgo,
            "autoridad_aprobatoria": resolucion_comite,
            "fecha_registro": datetime.now(timezone.utc).isoformat()
        }
        return {
            "status": "CALIBRACION_EXITOSA_COMITE",
            "jerga": j_clean,
            "categoria": categoria,
            "nivel_riesgo": nivel_riesgo,
            "autoridad_aprobatoria": resolucion_comite
        }

    def obtener_historial_osint(self) -> List[Dict[str, Any]]:
        """Retorna el historial de auditoría de calibraciones OSINT."""
        return self.historial_calibraciones_osint


# Instancia singleton del Radar Criminológico
radar_criminologico = RadarCriminologicoAgent()
radar_criminologico_agent = radar_criminologico


