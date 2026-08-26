"""Integration tests for SARA API endpoints."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app


class TestSARAAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        """Verify health endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "HEALTHY")
        self.assertEqual(data["service"], "SARA Anti-Extorsion Agentic System")

    def test_create_case_and_triage_flow(self):
        """Verify end-to-end case creation and automated SARA triage flow."""
        payload = {
            "nombre_completo": "Comerciante A. Test",
            "dni": "44556677",
            "telefono_contacto": "+51987654321",
            "direccion": "San Juan de Lurigancho, Lima",
            "mensaje": "Me están pidiendo 5000 soles para no atentar contra mi negocio familiar. Llaman todos los días desde el número +51999111222 a la cuenta BCP 19198765432100.",
        }
        response = self.client.post("/api/denuncia", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        self.assertIn("cup", data)
        self.assertIn("t_index", data)
        self.assertIn("nivel_riesgo", data)
        self.assertIn("mensaje_ciudadano", data)
        self.assertIn("protocolo_vida_primero", data)

    def test_trazas_forenses(self):
        """Verify forensic audit trail endpoint."""
        response = self.client.get("/api/trazas")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("trazas_supervisor_ia", data)
        self.assertIsInstance(data["trazas_supervisor_ia"], list)

    def test_hitl_and_fiscal_remission_flow(self):
        """Verify full HITL approval, SIDPOL dispatch, and remission to Fiscalia under D.Leg. 1735."""
        # 1. Crear denuncia
        payload = {
            "nombre_completo": "Transportista Beta Test",
            "dni": "77889900",
            "telefono_contacto": "+51988776655",
            "direccion": "El Agustino, Lima",
            "mensaje": "Banda Los Mexicanos cobra S/ 30 diarios a las combis. Dejaron carta con proyectil de 9mm.",
        }
        res_den = self.client.post("/api/denuncia", json=payload)
        self.assertEqual(res_den.status_code, 201)
        cup = res_den.get_json()["cup"]

        # 2. Aprobar policialmente con SIDPOL
        payload_hitl = {
            "token_operador": "CIP-PNP-TEST-9988",
            "operador_id": "Capitán PNP Test",
            "tipificacion_definitiva": "Art. 200° Inciso 5 CP - Extorsión Agravada a Transporte",
            "opinion_policial": "Conforme. Disponer bloqueo IMEI en 3h y patrullaje.",
            "medidas_determinadas_policia": ["BLOQUEO_IMEI_3H_LEY_32303", "CONGELAMIENTO_ADMINISTRATIVO_UIF"],
            "accion": "TRANSMISION_SIDPOL"
        }
        res_hitl = self.client.post(f"/api/humano/aprobar/{cup}", json=payload_hitl)
        self.assertEqual(res_hitl.status_code, 200)
        sid_code = res_hitl.get_json().get("codigo_sidpol")
        self.assertIsNotNone(sid_code)

        # 3. Remitir al Ministerio Público (D.Leg. 1735)
        payload_remision = {
            "token_operador": "CIP-PNP-TEST-9988",
            "operador_id": "Capitán PNP Test",
            "codigo_sidpol": sid_code,
            "tipificacion_definitiva": "Art. 200° Inciso 5 CP - Extorsión Agravada a Transporte",
            "medidas_aprobadas": ["BLOQUEO_IMEI_3H_LEY_32303", "CONGELAMIENTO_ADMINISTRATIVO_UIF"],
            "evidencias": [{"nombre": "carta.jpg", "tipo": "Imagen OCR", "sha256": "abc123hash"}]
        }
        res_rem = self.client.post(f"/api/humano/remitir_fiscalia/{cup}", json=payload_remision)
        self.assertEqual(res_rem.status_code, 200)
        rem_json = res_rem.get_json()
        self.assertEqual(rem_json["status"], "EXPEDIENTE_TRANSFERIDO_AL_MINISTERIO_PUBLICO")
        self.assertIn("remision_fiscal", rem_json)
        self.assertTrue(
            "INFORME-POLICIAL" in rem_json["remision_fiscal"]["numero_oficio_pnp"]
            or "OFICIO" in rem_json["remision_fiscal"]["numero_oficio_pnp"]
        )
        self.assertIn("codigo_sidpol", rem_json["remision_fiscal"])
        self.assertIn("respuesta_ministerio_publico", rem_json["remision_fiscal"])
        self.assertIn("codigo_unico_caso_fiscal_cuc", rem_json["remision_fiscal"]["respuesta_ministerio_publico"])
        
        # 4. Validar disparo de notificación SMS/WhatsApp a la denunciante
        self.assertIn("notificacion_denunciante", rem_json)
        notif = rem_json["notificacion_denunciante"]
        self.assertIn("carpeta_fiscal_notificada", notif)
        self.assertIn("cuc_fiscal_notificado", notif)
        self.assertIn("cuerpo_mensaje", notif)
        self.assertIn("estado_entrega", notif)
        self.assertTrue(notif["estado_entrega"] in ["ENVIADO_EXITOSO", "ENVIADO_SIMULADO"])
        self.assertIn(notif["carpeta_fiscal_notificada"], notif["cuerpo_mensaje"])


    def test_renitli_alert_and_convalidation_flow(self):
        """Verify ReNITLI async alert dispatch, token signing, and linguistic calibration audit."""
        from agents.renitli_agent import renitli_agent
        from core.supervisor import supervisor

        cup_test = "CUP-TEST-QUECHUA-01"
        audio_hash = "SHA256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
        transcripcion_quechua = "Allillanchu mamay, yanapaywayku. Huk qari prestamota qowarqan Chinchero Cuscopi, kunantaq 5000 soles mañawan."
        traduccion_ia = "Hola señora, ayúdennos. Un hombre me dio un préstamo en Chinchero Cusco, y ahora me pide 5000 soles."
        traduccion_humana = "Saludos respetada señora, solicitamos auxilio. Un sujeto me entregó un préstamo en el distrito de Chinchero, Cusco, y en este momento me exige coactivamente la suma de 5000 soles."

        # 1. Disparar alerta ReNITLI
        ticket = renitli_agent.disparar_alerta_traductor_renitli(
            cup=cup_test,
            idioma_detectado="QUECHUA",
            transcripcion_ia=transcripcion_quechua,
            traduccion_ia=traduccion_ia,
            audio_hash_sha256=audio_hash
        )
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket["cup"], cup_test)
        self.assertEqual(ticket["registro_renitli"], "RENITLI-MINCUL-0492")

        # 2. Convalidar traducción con Token ReNITLI
        cert = renitli_agent.convalidar_fe_publica_renitli(
            cup=cup_test,
            ticket_id=ticket["ticket_id"],
            traductor_nombre=ticket["traductor_titular"],
            registro_renitli=ticket["registro_renitli"],
            token_ingresado="TOKEN-RENITLI-0492-CUSCO",
            transcripcion_final=transcripcion_quechua,
            traduccion_juridica_final=traduccion_humana,
            observaciones_dialectales="Variante Quechua Cusco-Collao. Traducción conforme."
        )
        self.assertIsNotNone(cert)
        self.assertTrue(cert["nro_certificado_oficial"].startswith("CERT-RENITLI-2026-"))
        self.assertTrue(cert["token_validado"])
        self.assertEqual(cert["estado_procesal"], "CONVALIDADA_CON_FE_PUBLICA_MINCUL")
        self.assertIn("metrica_calibracion_mlops", cert)
        self.assertGreater(cert["metrica_calibracion_mlops"]["similitud_lexica_porcentaje"], 0)

        # 3. Generar Adenda Policial-Fiscal
        adenda = renitli_agent.generar_adenda_pericial_policial_fiscal(
            cup=cup_test,
            sidpol_code="SIDPOL-2026-TEST99",
            carpeta_fiscal="CF-N°-2026-0045-FECOR",
            cuc_fiscal="CUC-2026-009988",
            certificado_renitli=cert,
            oficial_pnp="Mayor PNP Valdivia",
            token_oficial="CIP-PNP-8877"
        )
        self.assertIsNotNone(adenda)
        self.assertTrue(adenda["oficio_remision_adenda"].startswith("OFICIO-ADENDA-PERICIAL-N°-2026-"))
        self.assertEqual(adenda["estado_adenda"], "ANEXADA_A_SIDPOL_Y_CARPETA_FISCAL_MPFN")


if __name__ == "__main__":
    unittest.main()




