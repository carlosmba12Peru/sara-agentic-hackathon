"""
SARA - Módulo de Internacionalización y Optimización Lingüística (i18n)
Proporciona normalización O(1) de códigos de idioma, resolución de variantes
y utilidades de detección/traducción ultrarrápidas para las 7 lenguas del Perú y el mundo:
- Español (Castellano)
- Quechua (Qusqu-Qullaw, Chanka, Áncash, Wanka)
- Aimara (Altiplano / Puno)
- Asháninka (Selva Central)
- Awajún (Selva Norte)
- Shipibo-Konibo (Ucayali)
- English (Tourist / Global)
"""

import re
from typing import Dict, Any, Optional, List

# Mapeo canónico O(1) de identificadores a códigos estándar
LANG_CANONICAL_MAP = {
    "es": "es",
    "español": "es",
    "espanol": "es",
    "castellano": "es",
    "spanish": "es",
    "español (castellano)": "es",
    "qu": "quechua",
    "quechua": "quechua",
    "runasimi": "quechua",
    "quechua (runasimi)": "quechua",
    "quechua cusco-collao": "quechua",
    "quechua chanka": "quechua",
    "quechua áncash": "quechua",
    "quechua wanka": "quechua",
    "ay": "aimara",
    "aimara": "aimara",
    "aymara": "aimara",
    "aimara (aymara)": "aimara",
    "cni": "ashaninka",
    "ashaninka": "ashaninka",
    "asháninka": "ashaninka",
    "asháninka (selva central)": "ashaninka",
    "agr": "awajun",
    "awajun": "awajun",
    "awajún": "awajun",
    "awajún (selva norte)": "awajun",
    "shp": "shipibo",
    "shipibo": "shipibo",
    "shipibo-konibo": "shipibo",
    "shipibo-konibo (ucayali / pucallpa)": "shipibo",
    "en": "en",
    "english": "en",
    "inglés": "en",
    "ingles": "en",
    "english (tourist / global)": "en",
}

# Metadatos oficiales por lengua
LANG_METADATA: Dict[str, Dict[str, Any]] = {
    "es": {
        "codigo": "es",
        "iso_639_3": "spa",
        "nombre_oficial": "Español (Castellano)",
        "familia": "Indoeuropea",
        "region": "Nacional / Internacional",
        "flag": "🇵🇪"
    },
    "quechua": {
        "codigo": "quechua",
        "iso_639_3": "que",
        "nombre_oficial": "Quechua (Runasimi)",
        "familia": "Quechua",
        "region": "Sierra Sur, Central y Norte",
        "flag": "🗣️"
    },
    "aimara": {
        "codigo": "aimara",
        "iso_639_3": "aym",
        "nombre_oficial": "Aimara (Aymara)",
        "familia": "Aru",
        "region": "Puno / Moquegua / Tacna / Altiplano",
        "flag": "🗣️"
    },
    "ashaninka": {
        "codigo": "ashaninka",
        "iso_639_3": "cni",
        "nombre_oficial": "Asháninka",
        "familia": "Arawak",
        "region": "Selva Central (Satipo / Junín / Pasco / Ucayali)",
        "flag": "🌿"
    },
    "awajun": {
        "codigo": "awajun",
        "iso_639_3": "agr",
        "nombre_oficial": "Awajún",
        "familia": "Jíbaro / Chicham",
        "region": "Selva Norte (Condorcanqui / Amazonas / San Martín / Loreto)",
        "flag": "🌿"
    },
    "shipibo": {
        "codigo": "shipibo",
        "iso_639_3": "shp",
        "nombre_oficial": "Shipibo-Konibo",
        "familia": "Pano",
        "region": "Ucayali / Pucallpa / Yarinacocha / Cantagallo",
        "flag": "🌿"
    },
    "en": {
        "codigo": "en",
        "iso_639_3": "eng",
        "nombre_oficial": "English (Global / Tourist)",
        "familia": "Indoeuropea (Germánica)",
        "region": "Turismo Internacional / Global",
        "flag": "🌐"
    }
}

# Vocabularios altamente específicos y ponderados por lengua
VOCABULARY_SHIPIBO = [
    "jakon", "wetsá", "wetsa", "koríki", "koriki", "mawatanti", "xobo", "akinanti", "tsaweti",
    "yoinamabi", "ráke", "rake", "nokon", "enra", "yoyo", "shipibo", "yarinacocha", "cantagallo",
    "nonra", "jaskatira", "itimati"
]

VOCABULARY_ASHANINKA = [
    "kitaiteri", "nomaimaye", "koreti", "kireki", "katsimatagantsi", "tsikontaaki", "oowa", 
    "katsinkagantsi", "pashitakoyena", "eiro pitsaroiti", "ashaninka", "noaminakoita",
    "kemisantantsi", "shireampaye", "notsotaite", "pipaite", "pematsikaiti"
]

VOCABULARY_AWAJUN = [
    "kumpami", "yatsuch", "kuji", "suwimka", "namput", "mántat", "yaimkata", "yaimtai",
    "ishamkaipa", "awajun", "condorcanqui", "chicham", "shiig", "anentaimsata", "dekainaji",
    "daajumek", "aminukchauwaitme"
]

# Palabras específicas del Aimara (excluyendo palabras compartidas con Quechua)
VOCABULARY_AIMARA = [
    "kamisaraki", "jilata", "kullaka", "waliki", "ch'iqhi", "jiwayäma", "jiwayama",
    "axsartwa", "yanapita", "yanapapxita", "utajaxa", "amuyasipxam", "sarxapxam",
    "kankaña", "aimara", "aymara", "janiw", "axsaramti", "sutimax", "imantatawa",
    "yatiyita", "janikiw", "sapakïtati", "suma urukipanaya", "qhana", "nanakax",
    "jark'apxirïmawa", "qullqita mayisirïtamxa", "mayisirïtamxa"
]

# Palabras específicas del Quechua
VOCABULARY_QUECHUA = [
    "allillanchu", "taytay", "mamay", "wañuchisayki", "wañuchisaq", "manchakuni",
    "manchakuychu", "yanapay", "yanapaywayku", "kashani", "kashayku", "kachkani",
    "wasiypi", "wasiyta", "wasiykitapas", "panillay", "wawqillay", "amachay",
    "cuidamusaykiku", "ayllu", "mamitay", "taytacha", "willasaykiku", "chaskisqam",
    "apachisqa", "pakasqam", "ruphachisayki", "ruphachisaq", "sapa p'unchay",
    "runasimi", "samaykuy", "sunqullaykiwan", "amachasqam", "qullqi", "qollqe",
    "mañawan", "nispa", "qillqay", "huk qari", "tiyanki"
]

VOCABULARY_ENGLISH = [
    "hello", "please help", "extortion", "threat", "threats", "threatening", "kill you",
    "send money", "urgent help", "afraid", "scared", "blackmail", "police department",
    "demanding", "gunpoint", "police officer"
]

def _build_regex_pattern(words: List[str]) -> re.Pattern:
    """Construye un patrón regex precompilado con delimitadores de palabra y flags case-insensitive."""
    sorted_words = sorted(words, key=len, reverse=True)
    pattern = r'\b(?:' + '|'.join(re.escape(w) for w in sorted_words) + r')\b'
    return re.compile(pattern, re.IGNORECASE)

# Patrones regex precompilados a nivel de módulo (Cero reconstrucción en runtime)
COMPILED_LANG_PATTERNS = {
    "shipibo": _build_regex_pattern(VOCABULARY_SHIPIBO),
    "ashaninka": _build_regex_pattern(VOCABULARY_ASHANINKA),
    "awajun": _build_regex_pattern(VOCABULARY_AWAJUN),
    "aimara": _build_regex_pattern(VOCABULARY_AIMARA),
    "quechua": _build_regex_pattern(VOCABULARY_QUECHUA),
    "en": _build_regex_pattern(VOCABULARY_ENGLISH),
}


def normalize_language_code(lang_input: Optional[str]) -> str:
    """
    Normaliza de forma ultra-rápida O(1) cualquier denominación o código a su clave estándar:
    'es', 'quechua', 'aimara', 'ashaninka', 'awajun', 'shipibo', 'en'.
    """
    if not lang_input:
        return "es"
    cleaned = str(lang_input).strip().lower()
    return LANG_CANONICAL_MAP.get(cleaned, "es")


def get_language_display_name(lang_input: Optional[str]) -> str:
    """Devuelve el nombre oficial de la lengua según metadatos."""
    code = normalize_language_code(lang_input)
    return LANG_METADATA.get(code, {}).get("nombre_oficial", "Español (Castellano)")


def detect_language_heuristic(text: str) -> str:
    """
    Detecta de forma determinista, ponderada y ultrarrápida el idioma del texto ingresado
    utilizando conteo de coincidencias sobre expresiones regulares precompiladas.
    Retorna: 'SHIPIBO', 'ASHANINKA', 'AWAJUN', 'AIMARA', 'QUECHUA', 'ENGLISH' o 'ESPAÑOL'.
    """
    if not text or not text.strip():
        return "ESPAÑOL"

    # Conteo ponderado O(1) de coincidencias por lengua
    counts = {
        "SHIPIBO": len(COMPILED_LANG_PATTERNS["shipibo"].findall(text)),
        "ASHANINKA": len(COMPILED_LANG_PATTERNS["ashaninka"].findall(text)),
        "AWAJUN": len(COMPILED_LANG_PATTERNS["awajun"].findall(text)),
        "AIMARA": len(COMPILED_LANG_PATTERNS["aimara"].findall(text)),
        "QUECHUA": len(COMPILED_LANG_PATTERNS["quechua"].findall(text)),
        "ENGLISH": len(COMPILED_LANG_PATTERNS["en"].findall(text)),
    }

    max_lang, max_hits = max(counts.items(), key=lambda x: x[1])
    if max_hits > 0:
        return max_lang

    return "ESPAÑOL"
