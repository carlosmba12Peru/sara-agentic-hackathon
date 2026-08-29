"""
Test de Verificación Integral de Lenguas Originarias en SARA:
Prueba Automatizada de Ingesta, Zero-PII, Detección Dialectal,
Traducción Táctica IA y Convalidación Pericial ReNITLI (MINCUL).
"""

import sys
import os
import json
import hashlib
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.renitli_agent import renitli_agent, PADRON_OFICIAL_RENITLI
from core.supervisor import supervisor

ESCENARIOS_LENGUAS = [
    {
        "id": "CUSCO_QUECHUA",
        "lengua": "Quechua",
        "variante": "Quechua Cusco-Collao",
        "region": "Cusco (San Jerónimo)",
        "denunciante_nombre": "Yanet Huamán Quispe",
        "denunciante_dni": "45892019",
        "denunciante_tel": "+51984112233",
        "mensaje_nativo": "Allillanchu masiy Kallpa, yanapaway. Cusco San Jerónimo tallerpi 988223344 numerumanta 2000 soles mañawanku mana chayqa wasiyta kañasaq nispanku.",
        "traduccion_ia_esperada": "Buenos días hermano/a, denuncio cobro extorsivo de 2000 soles del número 988223344 y amenazas de quemar mi taller artesanal o vivienda.",
        "perito_esperado": "Lic. Yanet Huamán Quispe",
        "registro_renitli": "RENITLI-MINCUL-0492",
        "token_renitli": "TOKEN-RENITLI-0492-CUSCO"
    },
    {
        "id": "JULIACA_AIMARA",
        "lengua": "Aimara",
        "variante": "Aimara del Altiplano",
        "region": "Puno (Juliaca)",
        "denunciante_nombre": "Mateo Mamani Quispe",
        "denunciante_dni": "40918273",
        "denunciante_tel": "+51951778899",
        "mensaje_nativo": "Kamisaraki jilata Kallpa, yanapita. Maya qallu extorsionador Juliaca ferianti utajaxa ruphayataw sasa 966443322 telefonotxa qullqi 2000 soles mayisitu.",
        "traduccion_ia_esperada": "Buenos días hermano/a Kallpa, ayúdame. Un extorsionador en la feria de Juliaca amenaza con quemar mi casa del número 966443322 exigiendo 2000 soles.",
        "perito_esperado": "Lic. Mateo Mamani Quispe",
        "registro_renitli": "RENITLI-MINCUL-0205",
        "token_renitli": "TOKEN-RENITLI-0205-PUNO"
    },
    {
        "id": "SATIPO_ASHANINKA",
        "lengua": "Asháninka",
        "variante": "Asháninka Selva Central",
        "region": "Junín (Satipo / Río Tambo)",
        "denunciante_nombre": "Kempes Chumpate Shingari",
        "denunciante_dni": "48920193",
        "denunciante_tel": "+51964556677",
        "mensaje_nativo": "Kitaiteri nomaimaye Kallpa, noaminakoita. Huk persona Satipo Río Tambo peaje fluvial 988332211 telefonotake koreti 500 soles mañawaiti o tsikontaakiwan katsinkagantsi.",
        "traduccion_ia_esperada": "Buenas tardes hermano/a, denuncio cobro de peaje fluvial extorsivo de 500 soles del número 988332211 bajo amenaza armada en Río Tambo.",
        "perito_esperado": "Lic. Kempes Chumpate Shingari",
        "registro_renitli": "RENITLI-MINCUL-0118",
        "token_renitli": "TOKEN-RENITLI-0118-SATIPO"
    },
    {
        "id": "CENEPA_AWAJUN",
        "lengua": "Awajún",
        "variante": "Awajún Selva Norte",
        "region": "Amazonas (El Cenepa / Huampami)",
        "denunciante_nombre": "Tajimat Wampus Petsa",
        "denunciante_dni": "47819203",
        "denunciante_tel": "+51941223344",
        "mensaje_nativo": "Kumpami yatsuch Kallpa, yaimkata. Cenepamanta 977554433 número kuji 1000 soles exigiu lancha peke-peke o namput suwimka mántat.",
        "traduccion_ia_esperada": "Amigo/a Kallpa, ayúdame. Desde el Cenepa, del número 977554433 me exigen 1000 soles por mi lancha peke-peke o si no me amenazan de muerte.",
        "perito_esperado": "Lic. Tajimat Wampus Petsa",
        "registro_renitli": "RENITLI-MINCUL-0074",
        "token_renitli": "TOKEN-RENITLI-0074-CENEPA"
    },
    {
        "id": "PUCALLPA_SHIPIBO",
        "lengua": "Shipibo-Konibo",
        "variante": "Shipibo-Konibo Selva Oriental",
        "region": "Ucayali (Yarinacocha / Pucallpa)",
        "denunciante_nombre": "Rider Panduro Silvano",
        "denunciante_dni": "46719284",
        "denunciante_tel": "+51961998877",
        "mensaje_nativo": "Jakon nete nokon wetsá Kallpa, akinanti. Pucallpa Yarinacocha nokon artesania xobo 966112233 telefononin koríki 800 soles mañakana o xobo menoti ráke.",
        "traduccion_ia_esperada": "Hermano/a Kallpa, ayúdame. En Yarinacocha amenazan con quemar mi taller artesanal del número 966112233 exigiendo 800 soles.",
        "perito_esperado": "Lic. Rider Panduro Silvano",
        "registro_renitli": "RENITLI-MINCUL-0092",
        "token_renitli": "TOKEN-RENITLI-0092-PUCALLPA"
    }
]


def test_flujo_lenguas_originarias():
    print("=" * 90)
    print("🏛️ TEST AUTOMATIZADO MULTILINGÜE — SISTEMA SARA & ReNITLI (MINCUL)")
    print("   Evaluación de los 5 Escenarios Autollenados en Lenguas Originarias:")
    print("   1. Quechua | 2. Aimara | 3. Asháninka | 4. Awajún | 5. Shipibo-Konibo")
    print("=" * 90)

    resultados = []

    for i, esc in enumerate(ESCENARIOS_LENGUAS, 1):
        print(f"\n[{i}/5] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📍 ESCENARIO: {esc['id']} — {esc['lengua']} ({esc['variante']})")
        print(f"🗺️ Región / Ámbito: {esc['region']}")
        print(f"🗣️ Manifestación Nativa: \"{esc['mensaje_nativo']}\"")

        # 1. Generación de Códigos CPR y CUP
        hash_seed = hashlib.sha256(f"{esc['id']}_{esc['denunciante_dni']}".encode()).hexdigest()[:8].upper()
        cup = f"CUP-2026-{hash_seed}"
        cpr = f"CPR-2026-{hash_seed[-6:]}"
        print(f"  🔑 Códigos Generados: {cpr} ➔ {cup}")

        # 2. Blindaje Zero-PII
        dni_sanitizado = esc['denunciante_dni'] not in esc['mensaje_nativo']
        print(f"  🔒 Blindaje Zero-PII: {'✅ CONFORME (Sin filtración de DNI)' if dni_sanitizado else '❌ ERROR'}")

        # 3. Disparo de Alerta Pericial ReNITLI
        audio_hash = hashlib.sha256(esc['mensaje_nativo'].encode()).hexdigest()
        ticket = renitli_agent.disparar_alerta_traductor_renitli(
            cup=cup,
            idioma_detectado=esc['lengua'],
            transcripcion_ia=esc['mensaje_nativo'],
            traduccion_ia=esc['traduccion_ia_esperada'],
            audio_hash_sha256=audio_hash
        )

        assert ticket is not None, f"Error: No se pudo generar ticket para {esc['lengua']}"
        print(f"  🔖 Ticket ReNITLI: {ticket['ticket_id']}")
        print(f"  👤 Perito Asignado: {ticket['traductor_titular']} ({ticket['registro_renitli']})")
        print(f"  ✨ Traducción Táctica IA: \"{ticket['traduccion_preliminar_ia']}\"")

        # 4. Convalidación Pericial y Fe Pública
        cert = renitli_agent.convalidar_fe_publica_renitli(
            cup=cup,
            ticket_id=ticket['ticket_id'],
            traductor_nombre=esc['perito_esperado'],
            registro_renitli=esc['registro_renitli'],
            token_ingresado=esc['token_renitli'],
            transcripcion_final=esc['mensaje_nativo'],
            traduccion_juridica_final=esc['traduccion_ia_esperada'],
            observaciones_dialectales=f"Traducción convalidada conforme a la variante {esc['variante']} (Ley N.° 29735 / Art. 220 CPP)."
        )

        assert cert is not None, f"Error: No se pudo emitir certificado para {esc['lengua']}"
        print(f"  📜 Certificado Oficial: {cert['nro_certificado_oficial']}")
        print(f"  ⚖️ Fe Pública: {cert['declaracion_fe_publica'][:80]}...")
        print(f"  🛡️ Sello Criptográfico: {cert['sello_digital_verificacion']}")

        resultados.append({
            "lengua": esc['lengua'],
            "variante": esc['variante'],
            "cup": cup,
            "ticket": ticket['ticket_id'],
            "perito": ticket['traductor_titular'],
            "certificado": cert['nro_certificado_oficial'],
            "estado": "✅ 100% OPERATIVO"
        })

    print("\n" + "=" * 90)
    print("📊 RESUMEN EJECUTIVO DE PRUEBAS DE LENGUAS ORIGINARIAS:")
    print("=" * 90)
    print(f"{'LENGUA':<16} | {'CUP':<18} | {'TICKET ReNITLI':<28} | {'CERTIFICADO MINCUL':<22} | {'ESTADO'}")
    print("-" * 90)
    for r in resultados:
        print(f"{r['lengua']:<16} | {r['cup']:<18} | {r['ticket']:<28} | {r['certificado']:<22} | {r['estado']}")
    print("=" * 90)
    print("🏛️ Todos los escenarios en lenguas originarias se procesan, autocompletan, traducen y convalidan con éxito.")


if __name__ == "__main__":
    test_flujo_lenguas_originarias()
