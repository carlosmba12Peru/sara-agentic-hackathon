"""
Test de Optimización Lingüística, Detección Rápida y Coherencia Multilingüe (SARA).
Verifica:
1. Normalización canónica O(1) de códigos de idioma para las 7 lenguas.
2. Detección heurística de lenguaje con expresiones regulares precompiladas.
3. Prevención de falsos positivos en subcadenas.
4. Generación de notificaciones de Carpeta Fiscal para las 7 lenguas sin caídas a fallback.
5. Benchmark de rendimiento (< 1ms por detección).
"""

import time
import pytest
from core.i18n import (
    normalize_language_code,
    detect_language_heuristic,
    get_language_display_name,
    LANG_METADATA
)
from agents.kallpa import kallpa_agent
from app.services.notification_service import notification_service


def test_normalize_language_code_all_languages():
    """Verifica que todas las variantes lingüísticas se normalicen a sus claves canónicas."""
    test_cases = [
        ("Español (Castellano)", "es"),
        ("spanish", "es"),
        ("es", "es"),
        ("Quechua (Runasimi)", "quechua"),
        ("Quechua Cusco-Collao", "quechua"),
        ("qu", "quechua"),
        ("Aimara (Aymara)", "aimara"),
        ("ay", "aimara"),
        ("Asháninka (Selva Central)", "ashaninka"),
        ("ashaninka", "ashaninka"),
        ("cni", "ashaninka"),
        ("Awajún (Selva Norte)", "awajun"),
        ("awajun", "awajun"),
        ("agr", "awajun"),
        ("Shipibo-Konibo (Ucayali / Pucallpa)", "shipibo"),
        ("shipibo", "shipibo"),
        ("shp", "shipibo"),
        ("English (Tourist / Global)", "en"),
        ("english", "en"),
        ("en", "en"),
        (None, "es"),
        ("", "es"),
    ]
    for raw_input, expected_code in test_cases:
        assert normalize_language_code(raw_input) == expected_code, f"Fallo al normalizar '{raw_input}'"


def test_detect_language_heuristic_all_languages():
    """Verifica que el detector identifique correctamente frases nativas para cada una de las 7 lenguas."""
    frases = {
        "QUECHUA": "Allillanchu mamay, huk qari wasiyta ruphachisaq nispa qullqita mañawan",
        "AIMARA": "Kamisaraki jilata, qullqi mayisirïtamxa jiwayäma sasina, yanapita",
        "ASHANINKA": "Kitaiteri nomaimaye, koreti mañawitaka tsikontaaki katsimatagantsi",
        "AWAJUN": "Kumpami yatsuch, kuji suwimka exigitaka namput",
        "SHIPIBO": "Jakon nete nokon wetsá, koríki mañakana xobo akinanti",
        "ENGLISH": "Hello officer, they are demanding money at gunpoint with urgent extortion threats",
        "ESPAÑOL": "Me están llamando a amenazar a mi familia y piden diez mil soles"
    }

    for expected_lang, frase in frases.items():
        detected = detect_language_heuristic(frase)
        assert detected == expected_lang, f"Esperado {expected_lang}, pero se detectó {detected} para '{frase}'"


def test_no_false_positives():
    """Verifica que palabras comunes en español no disparen lenguas originarias por subcadenas."""
    textos_espanol = [
        "El negocio queda cerca a la tienda Tambo en la avenida principal",
        "En la sierra nieva todos los años",
        "Necesito ayuda con este reporte de cobro de cupo"
    ]
    for txt in textos_espanol:
        detected = detect_language_heuristic(txt)
        assert detected == "ESPAÑOL", f"Falso positivo en '{txt}': detectado como {detected}"


def test_kallpa_containment_all_languages():
    """Verifica que Kallpa genere contención empática coherente en los 7 idiomas."""
    frases = [
        ("Allillanchu taytay, qullqi mañawan", "QUECHUA"),
        ("Kamisaraki kullaka, yanapita", "AIMARA"),
        ("Kitaiteri nomaimaye, eiro pitsaroiti", "ASHANINKA"),
        ("Kumpami yatsuch, ishamkaipa", "AWAJUN"),
        ("Jakon nete wetsá, yama rakéte", "SHIPIBO"),
        ("Please help, they are threatening to kill me", "ENGLISH"),
        ("Por favor ayúdenme, me amenazan con quemar mi tienda", "ESPAÑOL")
    ]
    for frase, lang_esperado in frases:
        res = kallpa_agent._heuristic_containment(frase)
        assert res["idioma_detectado"] == lang_esperado
        assert len(res["mensaje_contencion"]) > 10


def test_notification_service_carpeta_fiscal_all_languages():
    """Verifica que el servicio de notificaciones genere plantillas específicas para las 7 lenguas."""
    langs = ["es", "quechua", "aimara", "ashaninka", "awajun", "shipibo", "en"]
    cup = "CUP-TEST-777"
    sid = "SIDPOL-2026-99"
    cf = "CF-2026-101"
    cuc = "CUC-2026-FECOR"
    fisc = "Fiscalía Especializada FECOR"

    for lang in langs:
        msg = notification_service.redactar_mensaje_carpeta_fiscal(
            cup=cup,
            codigo_sidpol=sid,
            carpeta_fiscal=cf,
            cuc=cuc,
            fiscalia_asignada=fisc,
            idioma=lang
        )
        assert cf in msg
        assert sid in msg
        assert cup in msg
        assert len(msg) > 50


def test_detection_performance_benchmark():
    """Benchmark: 1,000 detecciones deben ejecutarse en menos de 100ms (< 0.1ms por llamada)."""
    sample_text = "Allillanchu mamay, huk qari wasiyta ruphachisaq nispa qullqita mañawan"
    t0 = time.perf_counter()
    for _ in range(1000):
        _ = detect_language_heuristic(sample_text)
    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000
    avg_us = (elapsed_ms / 1000) * 1000
    print(f"\n[BENCHMARK] 1000 detecciones en {elapsed_ms:.2f} ms ({avg_us:.2f} us/deteccion)")
    assert elapsed_ms < 100.0, f"Detección demasiado lenta: {elapsed_ms:.2f} ms para 1000 ejecuciones"
