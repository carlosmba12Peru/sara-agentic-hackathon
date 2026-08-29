"""
Prueba Unitaria y Forense de YachaqAgent (Agente Traductor de Lenguas Originarias).
"""
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.traductor_originario import yachaq_agent

def test_yachaq():
    casos = [
        {
            "cup": "CUP-2026-6FF1",
            "texto": "Allillanchu mamay, yanapaywayku. Huk qari préstamoto qowarqan Chinchero Cuscopi, kunantaq sapa p'unchay qullqita mañawan, 'wañuchisayki wasiykitapas ruphachisayki' nispa 988776655 numeromanta.",
            "lengua_esperada": "Quechua"
        },
        {
            "cup": "CUP-2026-AIM1",
            "texto": "Kamisaraki jilata Kallpa, yanapita. Maya qallu extorsionador Juliaca ferianti utajaxa ruphayataw sasa 966443322 telefonotxa qullqi 2000 soles mayisitu.",
            "lengua_esperada": "Aimara"
        },
        {
            "cup": "CUP-2026-ASH1",
            "texto": "Kitaiteri nomaimaye Kallpa, noaminakoita. Huk persona Satipo Río Tambo peaje fluvial 988332211 telefonotake koreti 500 soles mañawaiti o tsikontaakiwan katsinkagantsi.",
            "lengua_esperada": "Asháninka"
        },
        {
            "cup": "CUP-2026-AWJ1",
            "texto": "Kumpami yatsuch Kallpa, yaimkata. Cenepamanta 977554433 número kuji 1000 soles exigiu lancha peke-peke o namput suwimka mántat.",
            "lengua_esperada": "Awajún"
        },
        {
            "cup": "CUP-2026-SHP1",
            "texto": "Jakon nete nokon wetsá Kallpa, akinanti. Pucallpa Yarinacocha nokon artesania xobo 966112233 telefononin koríki 800 soles mañakana o xobo menoti ráke.",
            "lengua_esperada": "Shipibo-Konibo"
        }
    ]

    print("=" * 80)
    print("🧠 EVALUACIÓN DE YACHAQ IA (AGENTE TRADUCTOR FORENSE ORIGINARIO)")
    print("=" * 80)

    for c in casos:
        res = yachaq_agent.procesar_manifestacion_completa(c["texto"], c["cup"])
        perfil = res["perfil_linguistico"]
        entidades = res["entidades_forenses"]
        trad = res["resultado_traduccion"]

        print(f"\n🔑 Caso: {c['cup']}")
        print(f"  🗣️ Idioma Detectado:  {perfil['idioma']} ({perfil['variante']})")
        print(f"  🗺️ Ámbito Territorial: {perfil.get('ambito')}")
        print(f"  📱 Teléfonos:         {entidades['telefonos_extraidos']}")
        print(f"  💰 Montos:            {entidades['montos_extraidos']}")
        print(f"  🚨 Modalidades:       {entidades['modalidades_detectadas']}")
        print(f"  ✨ Traducción Táctica: {trad['traduccion_tactica_espanol']}")
        print(f"  🔒 SHA-256:           {trad['hash_integridad_sha256'][:24]}...")

        assert perfil["idioma"] == c["lengua_esperada"], f"Error: esperaba {c['lengua_esperada']}, obtuvo {perfil['idioma']}"

    print("\n" + "=" * 80)
    print("✅ TODAS LAS PRUEBAS DE YACHAQ AGENT SUPERADAS CON 100% DE EXACTITUD.")
    print("=" * 80)

if __name__ == "__main__":
    test_yachaq()
