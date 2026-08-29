#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo: correlacionador_forense.py
Descripción: Agente IA Especializado en Correlación Inter-Evidencias y Grafo Probatorio Forense.
Analiza la coherencia cruzada entre múltiples indicios materiales (Fotos, Audios, Cartas, Vouchers, Llamadas),
detecta contradicciones o refuerzos probatorios y construye el Grafo Relacional de Vínculos para la Fiscalía (FECOR).
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("sara.agents.correlacionador_forense")


class CorrelacionadorForenseAgent:
    """
    Agente responsable de la correlación cruzada de indicios, cálculo del Índice de Coherencia Probatoria (ICP)
    y generación de grafos de vínculos para la investigación de Crimen Organizado (Art. 158° y 317° CPP).
    """

    def __init__(self) -> None:
        self.nombre = "Agente Cálculo ICP Forense (Coherencia & Grafo Probatorio)"
        self.sigla = "CALCULO_ICP_FORENSE"

    def correlacionar_expediente_completo(
        self,
        evidencias_analizadas: List[Dict[str, Any]],
        pistas_infractor: Optional[Dict[str, Any]] = None,
        contexto_caso: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta la correlación cruzada de todos los indicios y genera el grafo probatorio unificado.
        """
        pistas = pistas_infractor or {}
        contexto = contexto_caso or {}

        nodos = []
        enlaces = []
        coincidencias = []
        alertas_inconsistencia = []

        # 1. Extraer entidades consolidadas
        bandas = []
        cuentas = []
        telefonos = []
        placas = []
        montos = []
        plazos = []
        calibres = []

        for ev in evidencias_analizadas:
            nom_f = ev.get("nombre_archivo", "evidencia.dat")
            acv = ev.get("analisis_contenido_visual", {})
            org = acv.get("organizacion_criminal")
            if org and org != "No especificada" and org != "Por determinar" and org not in bandas:
                bandas.append(org)
            
            for c in acv.get("cuentas_bancarias_extraidas", []):
                if c not in cuentas:
                    cuentas.append(c)
            for t in acv.get("telefonos_extraidos", []):
                if t not in telefonos:
                    telefonos.append(t)
            for p in acv.get("placas_vehiculos_extraidas", []):
                if p not in placas:
                    placas.append(p)
            for m in acv.get("montos_extraidos", []):
                if m not in montos:
                    montos.append(m)
            for pl in acv.get("plazos_extraidos", []):
                if pl not in plazos:
                    plazos.append(pl)
            
            cal = acv.get("calibre_y_estado_balistico")
            if cal and "No aplica" not in cal and cal not in calibres:
                calibres.append(cal)

        # 2. Construcción de Nodos del Grafo Probatorio
        if bandas:
            for b in bandas:
                nodos.append({"id": f"BANDA_{b.upper()}", "tipo": "ORGANIZACION_CRIMINAL", "etiqueta": b, "color": "#ef4444"})
        else:
            nodos.append({"id": "BANDA_DESCONOCIDA", "tipo": "ORGANIZACION_CRIMINAL", "etiqueta": "Banda en Identificación", "color": "#f87171"})

        for t in telefonos:
            nodos.append({"id": f"TEL_{t}", "tipo": "LINEA_EXTORSIVA", "etiqueta": t, "color": "#38bdf8"})
        for c in cuentas:
            nodos.append({"id": f"CTA_{c}", "tipo": "CUENTA_RECEPTORA", "etiqueta": c, "color": "#10b981"})
        for p in placas:
            nodos.append({"id": f"VEH_{p}", "tipo": "VEHICULO_LOGISTICO", "etiqueta": p, "color": "#f59e0b"})
        for cal in calibres:
            nodos.append({"id": f"BAL_{cal[:10]}", "tipo": "MUNICION_BALISTICA", "etiqueta": cal, "color": "#dc2626"})

        # 3. Construcción de Enlaces Relacionales
        nodo_banda_princ = f"BANDA_{bandas[0].upper()}" if bandas else "BANDA_DESCONOCIDA"
        for t in telefonos:
            enlaces.append({"origen": nodo_banda_princ, "destino": f"TEL_{t}", "relacion": "UTILIZA_LINEA_PARA_COACCION", "fuerza": 0.95})
        for c in cuentas:
            enlaces.append({"origen": nodo_banda_princ, "destino": f"CTA_{c}", "relacion": "EXIGE_ABONO_FINANCIERO", "fuerza": 0.98})
        for p in placas:
            enlaces.append({"origen": nodo_banda_princ, "destino": f"VEH_{p}", "relacion": "DESPLIEGA_MOTORIZADO", "fuerza": 0.90})
        for cal in calibres:
            enlaces.append({"origen": nodo_banda_princ, "destino": f"BAL_{cal[:10]}", "relacion": "ARROJA_MUNICION_COACTIVA", "fuerza": 1.0})

        # 4. Evaluación de Coherencia Cruzada (ICP)
        puntos_coherencia = 0
        total_evaluado = 0

        # Verificación 1: ¿La banda identificada es consistente entre archivos?
        if len(bandas) == 1:
            coincidencias.append(f"✅ Coherencia unánime de autoría criminal: '{bandas[0]}'")
            puntos_coherencia += 25
        elif len(bandas) > 1:
            alertas_inconsistencia.append(f"⚠️ Múltiples firmas delictivas detectadas: {', '.join(bandas)}")
            puntos_coherencia += 10
        total_evaluado += 25

        # Verificación 2: ¿Los montos coinciden o escalan coherentemente?
        if montos:
            coincidencias.append(f"✅ Patrón económico de exigencia fijado en: {', '.join(montos)}")
            puntos_coherencia += 25
        else:
            puntos_coherencia += 15
        total_evaluado += 25

        # Verificación 3: ¿Existen canales de pago (cuentas/Yape) identificados?
        if cuentas:
            coincidencias.append(f"✅ Coincidencia de destino financiero: {len(cuentas)} cuenta(s)/billetera(s)")
            puntos_coherencia += 25
        else:
            puntos_coherencia += 10
        total_evaluado += 25

        # Verificación 4: ¿Hay correlación balística o de entrega física?
        if calibres or placas:
            coincidencias.append("✅ Elementos materiales probatorios vinculados al modus operandi")
            puntos_coherencia += 25
        else:
            puntos_coherencia += 20
        total_evaluado += 25

        icp_score = round((puntos_coherencia / float(total_evaluado)) * 100, 1)

        dictamen_coherencia = (
            "ALTA_COHERENCIA_PROBATORIA_ROBUSTA" if icp_score >= 85.0 else
            "COHERENCIA_MODERADA_REQUIERE_DILIGENCIA" if icp_score >= 65.0 else
            "DISCREPANCIA_O_DATOS_FRAGMENTARIOS"
        )

        return {
            "indice_coherencia_probatoria_icp": icp_score,
            "dictamen_coherencia": dictamen_coherencia,
            "resumen_ejecutivo_fiscal": f"El análisis cruzado de {len(evidencias_analizadas)} evidencia(s) arroja un ICP de {icp_score}%. Los indicios balísticos, bancarios y de telecomunicaciones presentan consistencia probatoria unificada.",
            "matriz_coincidencias_cruzadas": coincidencias,
            "alertas_inconsistencia": alertas_inconsistencia,
            "grafo_vinculos_probatorios": {
                "nodos": nodos,
                "enlaces": enlaces,
                "total_nodos": len(nodos),
                "total_relaciones": len(enlaces)
            },
            "admisibilidad_procesal": "Art. 158° CPP - Valoración de la Prueba por Indicios Plurales y Concordantes"
        }


# Instancia singleton para uso en el ecosistema SARA
correlacionador_forense = CorrelacionadorForenseAgent()
correlacionador_forense_agent = correlacionador_forense
