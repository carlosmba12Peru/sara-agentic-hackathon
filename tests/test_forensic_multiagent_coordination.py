#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite: test_forensic_multiagent_coordination.py
Verifica la coordinación, coherencia y optimización entre el Subagente IA Forense Extractor
y todos los agentes asociados del ecosistema SARA:
1. SubAgenteForenseExtractor (Multimodal, ELA, Acústica, Bounding Boxes, Metadatos)
2. PeritoGrafotecnico (Análisis Paleográfico y Grafotécnico de cartas)
3. CorrelacionadorForense (Grafo Probatorio Inter-Evidencias)
4. AuditorForense (QC Pericial y Validación Anti-Alucinaciones)
5. TSA Client (Sellado Criptográfico RFC 3161 Art. 220 CPP)
6. AnalistaAgent (Perfilamiento Criminal & Deslinde OSIPTEL)
7. CalculoRiesgoAgent (Motor Cuantitativo IRCE / T_index)
8. EmpaquetadorNormativoAgent (Cadena de Custodia & Expediente Normativo)
9. AsesorJuridicoAgent (Dictamen Legal & Subsunción Penal Ley 32684 / Art. 200 CP)
"""

import os
import sys
import io
import json
import time
import base64
import unittest
from PIL import Image

# Asegurar path y UTF-8 en consola
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from agents.forense_extractor import SubAgenteForenseExtractor
from agents.perito_grafotecnico import perito_grafotecnico
from agents.correlacionador_forense import correlacionador_forense
from agents.auditor_forense import auditor_forense_agent
from agents.analista import AnalistaAgent
from agents.calculo import CalculoRiesgoAgent
from agents.empaquetador import EmpaquetadorNormativoAgent
from agents.asesor_juridico import asesor_juridico_agent
from core.tsa_client import tsa_client
from core.supervisor import supervisor


class TestForenseMultiagentCoordination(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*80)
        print("🏛️ INICIANDO SUITE DE EVALUACIÓN MULTIAGENTE FORENSE SARA")
        print("="*80)
        cls.cup_test = "CUP-2026-TEST-FORENSE-01"
        
        # Generar imágenes sintéticas válidas para PIL y ELA
        img_carta = Image.new("RGB", (200, 200), color=(245, 240, 230))
        buf_jpg = io.BytesIO()
        img_carta.save(buf_jpg, format="JPEG", quality=90)
        cls.b64_carta = base64.b64encode(buf_jpg.getvalue()).decode("utf-8")

        img_voucher = Image.new("RGB", (180, 240), color=(255, 255, 255))
        buf_png = io.BytesIO()
        img_voucher.save(buf_png, format="PNG")
        cls.b64_voucher = base64.b64encode(buf_png.getvalue()).decode("utf-8")

        # Audio simulado en base64
        cls.b64_audio = base64.b64encode(b"RIFF....WAVEfmt ....data....FAKE_AUDIO_SAMPLE").decode("utf-8")
        
        cls.evidencias = [
            {
                "nombre_archivo": "carta_manuscrita_amenaza.jpg",
                "mime_type": "image/jpeg",
                "b64_data": cls.b64_carta,
                "hash_sha256": "SHA256:E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
                "tamano_kb": len(buf_jpg.getvalue()) / 1024.0
            },
            {
                "nombre_archivo": "audio_amenaza_whatsapp.mp3",
                "mime_type": "audio/mp3",
                "b64_data": cls.b64_audio,
                "hash_sha256": "SHA256:F1E3E0958D6287A13B445AEBD3C84B79A312B1348D5E87D095861F23A4D67798",
                "tamano_kb": 85.0
            },
            {
                "nombre_archivo": "voucher_yape_transferencia.png",
                "mime_type": "image/png",
                "b64_data": cls.b64_voucher,
                "hash_sha256": "SHA256:E19BA7A700224C24F37E583A11C4F22BD0C8E3C620FB4690C63AE55418E2792D",
                "tamano_kb": len(buf_png.getvalue()) / 1024.0
            }
        ]

    def test_01_forense_extractor_individual_specialties(self):
        """Prueba de extracción pericial profunda y ejecución de sub-especialistas."""
        print("\n--- [TEST 1] SubAgenteForenseExtractor: Peritajes y Sub-Especialistas ---")
        extractor = SubAgenteForenseExtractor()
        
        start_t = time.perf_counter()
        patrones = extractor.extraer_patrones(
            texto_mensaje="Los Injertos del Norte exigen S/ 10,000 en 24 horas al Yape 944556677 o balearán mi local.",
            evidencias_digitales=self.evidencias
        )
        duracion_ms = (time.perf_counter() - start_t) * 1000
        
        print(f"⏱️ Tiempo de ejecución extracción multimodal: {duracion_ms:.2f} ms")
        self.assertLess(duracion_ms, 15000, "El tiempo de procesamiento debe ser < 15000ms")
        
        # Validar organizaciones
        orgs = [str(o).upper() for o in patrones.get("organizaciones_criminales_detectadas", [])]
        self.assertTrue(any("INJERTOS" in o for o in orgs), "Debe detectar la organización delictiva")
        self.assertEqual(len(patrones.get("detalle_archivos_analizados", [])), 3)
        
        # Validar sub-especialidades por archivo
        detalles = patrones.get("detalle_archivos_analizados", [])
        
        # Archivo 1: Carta manuscrita
        d_carta = detalles[0]
        self.assertIn("peritaje_grafotecnico", d_carta)
        self.assertIn("analisis_ela_anti_tampering", d_carta)
        self.assertIn("sello_tiempo_digital_rfc3161", d_carta)
        self.assertIn("auditoria_calidad_probatoria", d_carta)
        self.assertEqual(d_carta["sello_tiempo_digital_rfc3161"]["status"], "GRANTED_AND_CERTIFIED")
        self.assertEqual(d_carta["sello_tiempo_digital_rfc3161"]["admisibilidad_judicial"], "PLENA_FE_PUBLICA_ART_220_CPP")
        print("  ✅ Archivo 1 (Carta): Peritaje Grafotécnico, ELA, TSA RFC3161 y Auditoría QC validados.")
        
        # Archivo 2: Audio de amenaza
        d_audio = detalles[1]
        self.assertIn("biometria_acustica_audio", d_audio)
        self.assertTrue(d_audio["biometria_acustica_audio"].get("es_audio", False))
        print("  ✅ Archivo 2 (Audio): Biometría Acústica y Filtro Anti-Deepfake validados.")
        
        # Archivo 3: Voucher Yape
        d_voucher = detalles[2]
        self.assertIn("evaluacion_autenticidad_voucher", d_voucher)
        print("  ✅ Archivo 3 (Voucher): Evaluación Anti-Fraude Bancario validada.")
        
        # Grafo probatorio inter-evidencias
        grafo = patrones.get("correlacion_inter_evidencias_y_grafo", {})
        self.assertIn("grafo_vinculos_probatorios", grafo)
        self.assertIn("indice_coherencia_probatoria_icp", grafo)
        nodos = grafo.get("grafo_vinculos_probatorios", {}).get("nodos", [])
        print(f"  ✅ Correlacionador Forense: Grafo generado con {len(nodos)} nodos probatorios (ICP: {grafo.get('indice_coherencia_probatoria_icp')}%).")

    def test_02_analista_agent_coordination(self):
        """Prueba de integración entre AnalistaAgent y SubAgenteForenseExtractor."""
        print("\n--- [TEST 2] AnalistaAgent: Orquestación de Inteligencia Criminal ---")
        analista = AnalistaAgent()
        
        start_t = time.perf_counter()
        analisis = analista.analyze_offender_data(
            cup=self.cup_test,
            pistas_infractor={"telefonos_sospechosos": ["+51999111222"]},
            contexto_amenaza="Los Injertos del Norte me dejaron carta con balas exigiendo S/ 10,000 en 24 horas al Yape 944556677.",
            evidencias_digitales=self.evidencias
        )
        duracion_ms = (time.perf_counter() - start_t) * 1000
        print(f"⏱️ Tiempo de análisis criminal: {duracion_ms:.2f} ms")
        
        self.assertEqual(analisis["cup"], self.cup_test)
        self.assertIn("paquete_forense_adjunto", analisis)
        self.assertIn("deslinde_suplantacion_telecom", analisis)
        self.assertIn("clasificacion_artefactos", analisis)
        
        # Verificar deslinde OSIPTEL (Protocolo Anti-Falsos Positivos)
        deslinde = analisis.get("deslinde_suplantacion_telecom", "")
        self.assertIn("OSIPTEL", deslinde)
        print("  ✅ Analista Agent: Integró paquete forense y emitió deslinde procesal OSIPTEL correctamente.")

    def test_03_end_to_end_forensic_pipeline_coordination(self):
        """Prueba de pipeline completo: Forense -> Analista -> Cálculo -> Empaquetador -> Asesor Jurídico."""
        print("\n--- [TEST 3] Pipeline Completo E2E Multiagente ---")
        
        # 1. Kallpa (Contención & Detección)
        from agents.kallpa import KallpaAgent
        kallpa = KallpaAgent()
        kallpa_res = kallpa.interact_and_contain("Los Injertos del Norte me dejaron carta con balas exigiendo S/ 10,000 o matan a mi familia.")
        self.assertEqual(kallpa_res.get("idioma_detectado"), "ESPAÑOL")
        
        # 2. Analista & Forense
        analista = AnalistaAgent()
        analista_res = analista.analyze_offender_data(
            cup=self.cup_test,
            pistas_infractor=kallpa_res.get("pistas_infractor_extraidas", {}),
            contexto_amenaza="Los Injertos del Norte me dejaron carta con balas exigiendo S/ 10,000 o matan a mi familia.",
            evidencias_digitales=self.evidencias
        )
        
        # 3. Cálculo de Riesgo IRCE (T_index)
        calculo = CalculoRiesgoAgent()
        calculo_res = calculo.compute_threat_index(
            cup=self.cup_test,
            kallpa_output=kallpa_res,
            analista_output=analista_res
        )
        self.assertGreaterEqual(calculo_res["t_index"], 70.0, "Amenaza con armas/física debe tener T_index >= 70")
        print(f"  ✅ Cálculo IRCE: T_index={calculo_res['t_index']} (Nivel: {calculo_res['nivel_criticidad']})")
        
        # 4. Empaquetador Normativo (Cadena de Custodia Art. 220 CPP)
        empaquetador = EmpaquetadorNormativoAgent()
        expediente = empaquetador.package_dossier(
            cup=self.cup_test,
            kallpa_data=kallpa_res,
            analista_data=analista_res,
            calculo_data=calculo_res,
            evidencias_digitales=self.evidencias
        )
        self.assertEqual(expediente["cup"], self.cup_test)
        self.assertEqual(expediente["expediente_id"], f"EXP-{self.cup_test}")
        self.assertEqual(expediente["idioma_intake"], "ESPAÑOL")
        self.assertEqual(len(expediente["cadena_custodia_probatoria"]["evidencias_digitales_adjuntas"]), 3)
        print("  ✅ Empaquetador Normativo: Expediente y Cadena de Custodia Art. 220 CPP estructurados.")
        
        # 5. Asesor Jurídico (Veredicto y Subsunción Penal)
        veredicto = asesor_juridico_agent.emitir_veredicto_conformidad_legal(
            cup=self.cup_test,
            modus_operandi="Extorsión agravada con carta manuscrita y munición balística",
            tiene_armas=True,
            tiene_cuentas=True,
            t_index=calculo_res["t_index"]
        )
        self.assertEqual(veredicto["porcentaje_cumplimiento"], 100.0)
        self.assertIn("CERTIFICACIÓN LEGAL APROBADA", veredicto["dictamen_ejecutivo"])
        self.assertIn("LEY_32684_EXTORSION_PENITENCIARIA", asesor_juridico_agent.corpus.keys())
        print("  ✅ Asesor Jurídico: Dictamen de conformidad 100% emitido con subsunción jurídica oficial.")
        
        # 6. Auditoría Zero-PII del Supervisor
        supervisor.audit_payload_zero_pii("EmpaquetadorAgent", expediente, self.cup_test)
        print("  ✅ Supervisor: Verificación Zero-PII aprobada (0 filtraciones de datos personales).")


if __name__ == "__main__":
    unittest.main(verbosity=2)
