"""
SARA - Módulo de Gestión de Jurisdicciones Soberanas (GovSaaS Multi-Country Engine)
Permite a SARA operar de forma desacoplada y nativa en múltiples países y marcos penales:
- Perú (D.Leg. 1735, SIDPOL, MPFN, ReNITLI, RENIEC, Art. 220 CPP)
- México (CNPP Art. 227, C5-911, FGR, INALI, RENAPO/CURP)
- Colombia (Ley 599 Art. 244, SIEDCO, FGN, MinCultura Nativas, Registraduría)
- Global / USA (CJIS Title 18, 911/NIBRS, FBI/Interpol, ATA Interpreters)
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("sara.core.jurisdiction_manager")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config", "jurisdictions")

# Estado singleton en memoria para el runtime
_ACTIVE_JURISDICTION_ID = "PER_PNP"
_CACHED_JURISDICTIONS: Dict[str, Dict[str, Any]] = {}


def _load_all_jurisdictions() -> Dict[str, Dict[str, Any]]:
    """Carga y almacena en caché todos los archivos JSON de jurisdicción disponibles."""
    global _CACHED_JURISDICTIONS
    if _CACHED_JURISDICTIONS:
        return _CACHED_JURISDICTIONS

    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

    loaded = {}
    for fname in os.listdir(CONFIG_DIR):
        if fname.endswith(".json"):
            fpath = os.path.join(CONFIG_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    j_id = data.get("id")
                    if j_id:
                        loaded[j_id] = data
            except Exception as e:
                logger.error(f"Error cargando archivo de jurisdicción {fname}: {e}")

    _CACHED_JURISDICTIONS = loaded
    return _CACHED_JURISDICTIONS


def list_jurisdictions() -> List[Dict[str, Any]]:
    """Devuelve la lista de jurisdicciones disponibles ordenadas con metadatos clave."""
    juris_dict = _load_all_jurisdictions()
    result = []
    for j_id, data in juris_dict.items():
        result.append({
            "id": j_id,
            "pais": data.get("pais", "Desconocido"),
            "bandera": data.get("bandera", "🌐"),
            "nombre_completo": data.get("nombre_completo", ""),
            "agencia_sigla": data.get("agencia_policial", {}).get("sigla", ""),
            "sistema_denuncias": data.get("agencia_policial", {}).get("sistema_denuncias", ""),
            "fiscalia_sigla": data.get("entidad_fiscal", {}).get("sigla", ""),
            "ley_principal": data.get("marco_legal", {}).get("decreto_principal", ""),
            "delito_articulo": data.get("marco_legal", {}).get("codigo_penal_delito", ""),
            "cadena_custodia": data.get("marco_legal", {}).get("cadena_custodia", "")
        })
    return sorted(result, key=lambda x: 0 if x["id"] == "PER_PNP" else 1)


def get_jurisdiction(jurisdiction_id: Optional[str] = None) -> Dict[str, Any]:
    """Obtiene el objeto de configuración completo de una jurisdicción (o la activa por defecto)."""
    juris_dict = _load_all_jurisdictions()
    target_id = jurisdiction_id or _ACTIVE_JURISDICTION_ID
    if target_id in juris_dict:
        return juris_dict[target_id]
    
    # Fallback seguro a Perú PNP si no se encuentra
    if "PER_PNP" in juris_dict:
        return juris_dict["PER_PNP"]
    elif juris_dict:
        return next(iter(juris_dict.values()))
    
    return {
        "id": "PER_PNP",
        "pais": "Perú",
        "bandera": "🇵🇪",
        "agencia_policial": {"sigla": "PNP", "sistema_denuncias": "SIDPOL"},
        "entidad_fiscal": {"sigla": "MPFN", "especialidad": "FECOR"},
        "marco_legal": {"decreto_principal": "D.Leg. N.° 1735", "cadena_custodia": "Art. 220 CPP"}
    }


def set_active_jurisdiction(jurisdiction_id: str) -> bool:
    """Cambia la jurisdicción activa en el runtime de SARA."""
    global _ACTIVE_JURISDICTION_ID
    juris_dict = _load_all_jurisdictions()
    if jurisdiction_id in juris_dict:
        _ACTIVE_JURISDICTION_ID = jurisdiction_id
        logger.info(f"🏛️ Jurisdicción activa cambiada a: {juris_dict[jurisdiction_id].get('pais')} ({jurisdiction_id})")
        return True
    logger.warning(f"Jurisdicción desconocida: {jurisdiction_id}. Manteniendo {_ACTIVE_JURISDICTION_ID}")
    return False


def get_active_jurisdiction() -> Dict[str, Any]:
    """Devuelve la configuración de la jurisdicción soberana actualmente activa."""
    return get_jurisdiction(_ACTIVE_JURISDICTION_ID)


def format_police_incident_code(cup: str, jurisdiction_id: Optional[str] = None) -> Dict[str, str]:
    """Genera los códigos de incidente policial y carpeta fiscal según la jurisdicción activa."""
    j = get_jurisdiction(jurisdiction_id)
    j_id = j.get("id", "PER_PNP")
    clean_cup = cup.replace("CUP-", "").replace("DEMO-", "")[:6].upper()

    if j_id == "MEX_SSPC":
        return {
            "tipo_registro": "IPH (Informe Policial Homologado)",
            "codigo_policial": f"IPH-2026-FGR-MEX-{clean_cup}",
            "codigo_fiscal": f"CI-FEMDO-2026-{clean_cup}",
            "sistema_nombre": "C5 / Plataforma México",
            "cadena_custodia_norma": "Art. 227 y 228 CNPP",
            "sigla_policia": "SSPC/GN",
            "sigla_fiscalia": "FGR"
        }
    elif j_id == "COL_PONAL":
        return {
            "tipo_registro": "SIEDCO (Registro Policial de Noticia Criminal)",
            "codigo_policial": f"SIEDCO-2026-GAULA-{clean_cup}",
            "codigo_fiscal": f"NUNC-11001-2026-{clean_cup}",
            "sistema_nombre": "SIEDCO / ¡A Denunciar!",
            "cadena_custodia_norma": "Art. 254 Ley 906 CPP",
            "sigla_policia": "PONAL/GAULA",
            "sigla_fiscalia": "FGN"
        }
    elif j_id == "GLOBAL_INTERPOL":
        return {
            "tipo_registro": "NIBRS (National Incident Incident Report)",
            "codigo_policial": f"NIBRS-2026-FBI-{clean_cup}",
            "codigo_fiscal": f"US-DOJ-CRIM-2026-{clean_cup}",
            "sistema_nombre": "NIBRS / CAD 911",
            "cadena_custodia_norma": "FRE Rule 901 / NIST 800-86",
            "sigla_policia": "FBI/INTERPOL",
            "sigla_fiscalia": "DOJ"
        }
    else:
        # Default Perú PNP
        return {
            "tipo_registro": "SIDPOL (Informe Policial Oficial)",
            "codigo_policial": f"SIDPOL-2026-{clean_cup}",
            "codigo_fiscal": f"CF-N°-2026-0045-FECOR (CUC: 2026-0045-FECOR)",
            "sistema_nombre": "SIDPOL / PNP",
            "cadena_custodia_norma": "Art. 220 CPP",
            "sigla_policia": "PNP/DIVINHOM",
            "sigla_fiscalia": "MPFN/FECOR"
        }


# Inicialización en la importación
_load_all_jurisdictions()
