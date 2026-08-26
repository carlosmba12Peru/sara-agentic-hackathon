"""
GLOSARIO FORENSE Y DICCIONARIO CRIMINALÍSTICO OFICIAL DE SARA
Fuentes Oficiales Integradas:
1. INTERNACIONAL: AICEF (Academia Iberoamericana de Criminalística y Estudios Forenses)
   URL: https://www.aicef.info/glosario-balistica-forense/
2. NACIONAL (PERÚ): INCRIS (Instituto de Criminalística y Ciencias Forenses del Perú)
   URL: https://incris.edu.pe/sitio/diccionario-criminalistico.html
3. NORMATIVA PERUANA: Art. 220° del Código Procesal Penal (CPP) y Ley N° 30299 (SUCAMEC)
"""

from typing import Dict, Any, List

# ==============================================================================
# 1. GLOSARIO INTERNACIONAL DE BALÍSTICA FORENSE (AICEF)
# ==============================================================================
GLOSARIO_BALISTICA_AICEF: Dict[str, Dict[str, str]] = {
    "ANIMA": {
        "termino": "Ánima (Bore)",
        "definicion": "Superficie interior del cañón de un arma de fuego, que puede ser lisa o rayada/estriada.",
        "fuente": "AICEF Internacional"
    },
    "CALIBRE_NOMINAL": {
        "termino": "Calibre Nominal",
        "definicion": "Denominación comercial o convencional dada a un cartucho o arma (ej. 9mm Parabellum, .38 Special, 7.62x51mm).",
        "fuente": "AICEF Internacional"
    },
    "CALIBRE_REAL": {
        "termino": "Calibre Real",
        "definicion": "Diámetro medido entre los campos o fondos opuestos del estriado del cañón.",
        "fuente": "AICEF Internacional"
    },
    "CASQUILLO_O_VAINA": {
        "termino": "Casquillo / Vaina (Cartridge Case)",
        "definicion": "Recipiente cilíndrico metálico (generalmente de latón) que aloja la carga de proyección, la cápsula fulminante y sujeta el proyectil.",
        "fuente": "AICEF Internacional"
    },
    "CAPSULA_FULMINANTE": {
        "termino": "Cápsula Fulminante / Iniciador (Primer)",
        "definicion": "Dispositivo ubicado en el culote que contiene la mezcla explosiva sensible a la percusión mecánica para encender la pólvora.",
        "fuente": "AICEF Internacional"
    },
    "CULOTE": {
        "termino": "Culote (Base / Head)",
        "definicion": "Base del casquillo donde se localiza la cápsula fulminante y los grabados de fábrica (headstamp con lote, marca y año).",
        "fuente": "AICEF Internacional"
    },
    "ESTRIAS_Y_CAMPOS": {
        "termino": "Estrías y Campos (Grooves & Lands)",
        "definicion": "Ranuras helicoidales talladas en el ánima que imprimen al proyectil el movimiento de rotación estabilizador.",
        "fuente": "AICEF Internacional"
    },
    "OJIVA_ENCAMISADA": {
        "termino": "Ojiva Encamisada (Full Metal Jacket - FMJ)",
        "definicion": "Proyectil con núcleo blando de plomo recubierto por una camisa metálica exterior de cobre o aleación latón/tumbaga.",
        "fuente": "AICEF Internacional"
    },
    "PROYECTIL_SIN_PERCUTAR": {
        "termino": "Cartucho Completo sin Percutar",
        "definicion": "Munición balística íntegra que conserva intacta su cápsula fulminante, pólvora y ojiva. Utilizado en extorsión como amenaza letal directa.",
        "fuente": "AICEF Internacional & SARA Forensics"
    },
    "BALISTICA_DE_EFECTOS": {
        "termino": "Balística de Efectos / Terminal",
        "definicion": "Rama pericial que estudia el comportamiento, poder de penetración y daño lesivo del proyectil al impactar sobre el blanco.",
        "fuente": "AICEF Internacional"
    },
    "BALISTICA_IDENTIFICATIVA": {
        "termino": "Balística Identificativa / Comparativa",
        "definicion": "Cotejo macro y microscópico de las huellas de percusión, extracción, eyección y rayado estriado en casquillos y proyectiles.",
        "fuente": "AICEF Internacional"
    }
}

# ==============================================================================
# 2. DICCIONARIO CRIMINALÍSTICO DEL PERÚ (INCRIS & MANUAL DIRINCRI PNP)
# ==============================================================================
DICCIONARIO_CRIMINALISTICO_INCRIS: Dict[str, Dict[str, str]] = {
    "CADENA_DE_CUSTODIA": {
        "termino": "Cadena de Custodia (Art. 220° CPP)",
        "definicion": "Procedimiento riguroso de registro, sellado, autenticación y trazabilidad inmutable que garantiza la integridad de los indicios y evidencias desde su recolección hasta el juicio oral.",
        "fuente": "INCRIS & CPP Perú"
    },
    "ELEMENTO_MATERIAL_PROBATORIO": {
        "termino": "Elemento Material Probatorio (EMP)",
        "definicion": "Cualquier objeto, sustancia, arma, documento o soporte digital recogido en la escena o aportado por la víctima que posee relevancia procesal.",
        "fuente": "INCRIS Perú"
    },
    "PERITAJE_GRAFOTECNICO": {
        "termino": "Peritaje Grafotécnico / Paleográfico",
        "definicion": "Examen científico de textos y cartas manuscritas, soporte de papel, tintas, espontaneidad del trazo y pliegues para establecer autoría e intimidación.",
        "fuente": "INCRIS & DIRINCRI PNP"
    },
    "INSPECCION_CRIMINALISTICA": {
        "termino": "Inspección Criminalística en la Escena",
        "definicion": "Conjunto de diligencias técnico-científicas que practica el perito en el lugar de los hechos para descubrir, proteger y peritar indicios.",
        "fuente": "INCRIS Perú"
    },
    "INDICIOS_BALISTICOS_COACTIVOS": {
        "termino": "Indicios Balísticos de Coerción Extorsiva",
        "definicion": "Proyectiles, mechas lentas, cartuchos de dinamita o granadas arrojados a locales comerciales con el propósito de doblegar la voluntad patrimonial de la víctima.",
        "fuente": "INCRIS & DIRINCRI PNP"
    },
    "FIJACION_DIGITAL_FORENSE": {
        "termino": "Fijación Digital Forense (Hash SHA-256)",
        "definicion": "Extracción y sellado matemático de evidencias multimedia (audios, fotos, videos) garantizando que no han sufrido alteración ni borrado.",
        "fuente": "INCRIS & Estándar SARA"
    },
    "FIRMA_CRIMINAL_EXTORSIVA": {
        "termino": "Firma y Apercibimiento de Banda Criminal",
        "definicion": "Sello distintivo, seudónimo o logotipo empleado por organizaciones delictivas peruanas ('Los Pulpos', 'Los Injertos', 'Tren de Aragua') para infundir zozobra.",
        "fuente": "INCRIS & Policía Nacional del Perú"
    }
}

# ==============================================================================
# 3. GLOSARIO INTERNACIONAL DE CIBEREXTORSIÓN Y CIBERAMENAZAS (KASPERSKY GLOBAL THREATS)
# URL: https://www.kaspersky.es/resource-center/threats/extortion-scams-how-to-avoid-them
# ==============================================================================
GLOSARIO_CIBEREXTORSION_KASPERSKY: Dict[str, Dict[str, str]] = {
    "CIBEREXTORSION": {
        "termino": "Ciberextorsión (Cyber-Extortion)",
        "definicion": "Delito cibernético donde se coacciona a la víctima mediante comunicaciones digitales exigiendo pagos económicos o criptomonedas bajo amenaza de divulgación de datos confidenciales, secuestro de información o daños a la integridad personal.",
        "fuente": "Kaspersky Global Threat Intelligence"
    },
    "SEXTORSION": {
        "termino": "Sextorsión (Sextortion / Digital Blackmail)",
        "definicion": "Chantaje extorsivo invasivo mediante la amenaza de divulgación pública de fotografías, videos íntimos o grabaciones no autorizadas de cámara web (reales o adulteradas mediante Deepfakes).",
        "fuente": "Kaspersky Global Threat Intelligence & NCMEC"
    },
    "DOXXING_EXTORSIVO": {
        "termino": "Doxxing Extorsivo (Extortive Doxxing)",
        "definicion": "Exfiltración, recopilación y amenaza de publicación masiva de datos personales, documentos de identidad (DNI), domicilio y entorno familiar de la víctima en la Dark Web o foros públicos para quebrar su resistencia.",
        "fuente": "Kaspersky Global Threat Intelligence"
    },
    "EXTORSION_FINANCIERA_DIGITAL": {
        "termino": "Extorsión Financiera y Suplantación Bancaria",
        "definicion": "Modalidad donde ciberdelincuentes alegan haber intervenido las cuentas bancarias de la víctima o suplantan a entidades tributarias/financieras exigiendo pagos para no vaciar los fondos o evitar falsas sanciones.",
        "fuente": "Kaspersky Global Threat Intelligence"
    },
    "RANSOMWARE_EXTORSIVO": {
        "termino": "Ransomware & Ataques DDoS Extorsivos",
        "definicion": "Cifrado hostil de bases de datos o amenaza de saturación de servidores de una empresa/comercio con exigencia de pago en criptomonedas dentro de una ventana temporal estricta.",
        "fuente": "Kaspersky Global Threat Intelligence"
    },
    "AI_VOICE_CLONING_SCAM": {
        "termino": "Estafa por Clonación Vocal con IA (Deepfake Audio Vishing)",
        "definicion": "Uso de modelos generativos de voz para clonar el timbre y tono de familiares de la víctima y simular emergencias médicas, secuestros exprés o accidentes con el fin de exigir transferencias inmediatas.",
        "fuente": "Kaspersky Threat Intelligence & SARA Biometrics"
    },
    "PRESION_PSICOLOGICA_PERENTORIA": {
        "termino": "Presión Psicológica Perentoria (Urgent Demands)",
        "definicion": "Táctica de coerción coercitiva basada en imponer plazos breves y arbitrarios (24 a 72 horas) para inducir miedo, pánico y bloquear el raciocinio de la víctima antes de que pueda pedir ayuda policial.",
        "fuente": "Kaspersky Global Threat Intelligence"
    },
    "BLUFFING_EXTORSIVO": {
        "termino": "Bluffing Extorsivo / Amenaza Vacía (Extortion Bluffing)",
        "definicion": "Uso de contraseñas filtradas en brechas antiguas o datos públicos para fingir que el atacante tiene control total del dispositivo y forzar pagos por pánico sin poseer material comprometedor.",
        "fuente": "Kaspersky Global Threat Intelligence"
    },
    "SIM_SWAPPING_EXTORSIVO": {
        "termino": "SIM Swapping / Hijacking de Línea Móvil",
        "definicion": "Clonación o transferencia fraudulenta de la tarjeta SIM para apoderarse de la línea telefónica, interceptar códigos 2FA y utilizar el número de la víctima para coaccionar a sus contactos.",
        "fuente": "Kaspersky Global Threat Intelligence & OSIPTEL"
    }
}

# ==============================================================================
# 4. INTEROPERABILIDAD Y CONSULTA PERICIAL CENTRALIZADA
# ==============================================================================
def consultar_glosario_pericial(termino_clave: str) -> Dict[str, Any]:
    """
    Busca coincidencias en el glosario internacional AICEF (balística), 
    INCRIS (criminalística peruana) y Kaspersky (ciberextorsión)
    para enriquecer los informes policiales y peritajes de SARA.
    """
    key = termino_clave.strip().upper().replace(" ", "_")
    
    if key in GLOSARIO_BALISTICA_AICEF:
        return GLOSARIO_BALISTICA_AICEF[key]
    
    if key in DICCIONARIO_CRIMINALISTICO_INCRIS:
        return DICCIONARIO_CRIMINALISTICO_INCRIS[key]

    if key in GLOSARIO_CIBEREXTORSION_KASPERSKY:
        return GLOSARIO_CIBEREXTORSION_KASPERSKY[key]
    
    glosario_unificado = {
        **GLOSARIO_BALISTICA_AICEF, 
        **DICCIONARIO_CRIMINALISTICO_INCRIS,
        **GLOSARIO_CIBEREXTORSION_KASPERSKY
    }

    for k, v in glosario_unificado.items():
        if termino_clave.lower() in v["termino"].lower() or termino_clave.lower() in v["definicion"].lower():
            return v
            
    return {
        "termino": termino_clave,
        "definicion": "Término pericial bajo evaluación técnica criminalística estándar.",
        "fuente": "AICEF / INCRIS / Kaspersky Threat Intelligence"
    }
