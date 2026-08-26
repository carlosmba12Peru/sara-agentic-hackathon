"""Pruebas Unitarias para el Agente Vigía Normativo y Gobernanza Legal HITL Oficial (El Peruano & GOB.PE)."""

import unittest
from agents.vigia_normativo import vigia_normativo_agent
from agents.asesor_juridico import asesor_juridico_agent


class TestVigiaNormativoOficial(unittest.TestCase):

    def test_escanear_fuentes_oficiales_el_peruano_gob_pe(self):
        """Verifica que el escaneo regulatorio audite exclusivamente fuentes oficiales: El Peruano y GOB.PE."""
        res = vigia_normativo_agent.escanear_fuentes_normativas_tripartitas()
        self.assertIn("timestamp_utc", res)
        self.assertIn("fuentes_oficiales_exclusivas", res)
        fuentes_str = " ".join(res["fuentes_oficiales_exclusivas"])
        self.assertIn("elperuano.pe", fuentes_str)
        self.assertIn("gob.pe", fuentes_str)

    def test_modelos_oficiales_integrados_nl_2384225_3_y_nl_2530996_5(self):
        """Verifica que los modelos de fuentes oficiales (D.S. 007-2025-JUS y Ley 32684) estén presentes con sus NL."""
        propuestas = vigia_normativo_agent.obtener_propuestas_pendientes()
        nombres_normas = [p.get("norma") for p in propuestas]
        dispositivos = [p.get("dispositivo_oficial_el_peruano") for p in propuestas]

        # Verificar D.S. 007-2025-JUS (NL/2384225-3)
        self.assertTrue(any("007-2025-JUS" in n for n in nombres_normas))
        self.assertIn("NL/2384225-3", dispositivos)

        # Verificar Ley Nº 32684 (NL/2530996-5)
        self.assertTrue(any("32684" in n for n in nombres_normas))
        self.assertIn("NL/2530996-5", dispositivos)

    def test_aprobacion_hitl_asocia_fuente_oficial_y_no_doctrinal(self):
        """Verifica que al dictaminar y aprobar una norma, se asocie el enlace oficial de El Peruano y GOB.PE."""
        propuesta = vigia_normativo_agent.crear_propuesta_manual(
            norma="Ley N° 32700",
            titulo="Ley de Fortalecimiento de la Bóveda Zero-PII en Sistemas de Denuncia Policial",
            organo="Congreso de la República",
            poder_estado="Poder Legislativo",
            materia="INTELIGENCIA_ARTIFICIAL_Y_DERECHO_DIGITAL",
            impacto="Exige que las plataformas de auxilio ciudadano garanticen disociación de identidad por diseño.",
            fuente_el_peruano_url="https://busquedas.elperuano.pe/dispositivo/NL/2599999-1",
            dispositivo_nl="NL/2599999-1",
            fuente_gob_pe_url="https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/ley-32700"
        )
        p_id = propuesta["id_propuesta"]

        # El abogado colegiado aprueba
        res_aprob = vigia_normativo_agent.dictaminar_propuesta_humana(
            id_propuesta=p_id,
            decision="APROBAR",
            experto_id="Dra. Milagros Paredes Cárdenas",
            dictamen_juridico="Cumple con los estándares oficiales de la Ley N° 31814 y la Constitución.",
            rol_experto="Especialista en IA y Derecho Penal (CAL 58492)"
        )
        self.assertEqual(res_aprob["status"], "APROBADO_E_INTEGRADO")
        self.assertIn("HITL", res_aprob.get("sello_aprobacion", ""))

        # Verificar que el Asesor Jurídico guardó la referencia oficial
        normas_asesor = [m for m in asesor_juridico_agent.matriz_cumplimiento if "32700" in m.get("norma", "")]
        self.assertTrue(len(normas_asesor) > 0)
        self.assertIn("NL/2599999-1", normas_asesor[0].get("dispositivo_nl", ""))

    def test_veredicto_legal_exclusividad_fuentes_oficiales(self):
        """Verifica que el veredicto del Asesor Jurídico certifique 100% de cumplimiento oficial."""
        veredicto = asesor_juridico_agent.emitir_veredicto_conformidad_legal(
            cup="CUP-TEST-OFICIAL-001",
            modus_operandi="Extorsión desde Penal",
            tiene_armas=True,
            tiene_cuentas=True,
            t_index=90.0
        )
        self.assertEqual(veredicto["estado_veredicto"], "CONFORME_100_PORCENTAJE")
        self.assertEqual(veredicto["simbolo_veredicto"], "✅")
        # Verificar que certifique fuentes oficiales
        self.assertIn("Diario Oficial El Peruano", " ".join(veredicto["fuentes_oficiales_exclusivas"]))


if __name__ == "__main__":
    unittest.main()
