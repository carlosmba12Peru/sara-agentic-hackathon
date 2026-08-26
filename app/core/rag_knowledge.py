"""Private Forensic RAG Knowledge Base (Lab 7).
Contains structured forensic typologies, legal penal frameworks, and emergency response playbooks.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel


class ExtortionTypology(BaseModel):
    """Forensic profile for a specific extortion criminal typology."""

    typology_id: str
    name: str
    legal_code_reference: str
    modus_operandi_description: str
    typical_threat_patterns: List[str]
    forensic_red_flags: List[str]
    immediate_mitigation_advice: str
    default_coercion_baseline: float


# Curated Knowledge Repository for Criminal Extortion and Public Safety
EXTORTION_KNOWLEDGE_BASE: Dict[str, ExtortionTypology] = {
    "GOTA_A_GOTA": ExtortionTypology(
        typology_id="GOTA_A_GOTA",
        name="Extorsión y Usura por Préstamos Informales (Gota a Gota)",
        legal_code_reference="Art. 200 y Art. 214 del Código Penal (Extorsión y Usura Agravada)",
        modus_operandi_description="Bandas transnacionales que otorgan micropréstamos sin garantías pero con tasas de interés usureras diarias (20-40%). Ante el retraso de un día, inician cobro coercitivo violento.",
        typical_threat_patterns=[
            "Amenazas de quema o destrucción del local comercial",
            "Fotografías de las fachadas o de los familiares de la víctima",
            "Notas extorsivas con balas o dinamita dejadas en la puerta",
        ],
        forensic_red_flags=[
            "Aplicaciones móviles de préstamo maliciosas que roban la libreta de contactos",
            "Múltiples cuentas bancarias de testaferros para micro-depósitos",
            "Mensajes recurrentes por WhatsApp con prefijos internacionales",
        ],
        immediate_mitigation_advice="No realizar pagos adicionales. Bloquear accesos de permisos en aplicaciones móviles. Establecer resguardo policial y preservar todas las capturas de pantalla.",
        default_coercion_baseline=80.0,
    ),
    "SEXTO_EXTORSION": ExtortionTypology(
        typology_id="SEXTO_EXTORSION",
        name="Sextorsión y Chantaje Digital",
        legal_code_reference="Art. 200 y Art. 154-B del Código Penal (Extorsión y Difusión de Imágenes Íntimas)",
        modus_operandi_description="El agresor obtiene material íntimo o privado mediante engaño o hackeo, exigiendo pagos periódicos bajo amenaza de difundirlo a familiares o en redes sociales.",
        typical_threat_patterns=[
            "Capturas de listas de amigos o seguidores en Instagram/Facebook",
            "Amenaza con plazos estrictos de menos de 2 horas para el primer desembolso",
            "Promesa engañosa de borrar el material tras el pago (nunca lo hacen)",
        ],
        forensic_red_flags=[
            "Cuentas de billeteras digitales (Yape/Plin) a nombre de terceros",
            "Perfiles falsos de redes sociales creados recientemente",
        ],
        immediate_mitigation_advice="Bajo ninguna circunstancia pagar (el pago incrementa la persistencia). Desactivar perfiles sociales temporalmente y levantar denuncia forense digital.",
        default_coercion_baseline=65.0,
    ),
    "COBRO_DE_CUPOS": ExtortionTypology(
        typology_id="COBRO_DE_CUPOS",
        name="Cobro de Cupos / Vacunas a Negocios y Obras",
        legal_code_reference="Art. 200 del Código Penal (Extorsión a Obras y Establecimientos Comerciales)",
        modus_operandi_description="Organizaciones criminales exigen pagos semanales o mensuales a transportistas, comerciantes o constructoras a cambio de 'seguridad' o para dejarlos operar.",
        typical_threat_patterns=[
            "Disparos a la fachada o artefactos explosivos (cartuchos de dinamita)",
            "Pegatinas o calcomanías de la banda para marcar los vehículos o locales",
            "Llamadas de cabecillas desde centros penitenciarios",
        ],
        forensic_red_flags=[
            "Stickers distintivos de la organización criminal",
            "Nombres de alias o 'baterías' conocidas en la jurisdicción",
        ],
        immediate_mitigation_advice="Alerta prioritaria a la división de secuestros y extorsiones. Habilitar patrullaje integrado municipal y reserva de identidad de la víctima.",
        default_coercion_baseline=90.0,
    ),
    "SECUESTRO_VIRTUAL": ExtortionTypology(
        typology_id="SECUESTRO_VIRTUAL",
        name="Falso Secuestro / Secuestro Virtual",
        legal_code_reference="Art. 200 del Código Penal (Extorsión mediante Simulación de Autoridad o Privación de Libertad)",
        modus_operandi_description="Llamada de pánico fingiendo tener secuestrado a un hijo o familiar con llantos de fondo, exigiendo un depósito inmediato antes de colgar.",
        typical_threat_patterns=[
            "Impedir que la víctima cuelgue la llamada o se comunique con el familiar",
            "Voz distorsionada o llanto en segundo plano",
            "Exigencia de transferencias inmediatas por agentes bancarios o cripto",
        ],
        forensic_red_flags=[
            "Llamadas provenientes de penales o números desconocidos",
            "Falta de prueba de vida concreta",
        ],
        immediate_mitigation_advice="Mantener la calma, usar otro teléfono para verificar el paradero del familiar en cuestión y cortar la llamada de inmediato.",
        default_coercion_baseline=85.0,
    ),
}


class ForensicRAGKnowledge:
    """RAG Retriever that matches distress statements to legal typologies and mitigation playbooks."""

    def retrieve_relevant_typology(self, text: str) -> Optional[ExtortionTypology]:
        """Search the knowledge base for the closest matching criminal typology."""
        lower_text = text.lower()

        if any(w in lower_text for w in ["préstamo", "gota", "interés", "diario", "cuota", "prestamista"]):
            return EXTORTION_KNOWLEDGE_BASE["GOTA_A_GOTA"]
        elif any(w in lower_text for w in ["foto", "video", "desnudo", "íntimo", "redes", "facebook", "instagram"]):
            return EXTORTION_KNOWLEDGE_BASE["SEXTO_EXTORSION"]
        elif any(w in lower_text for w in ["cupo", "vacuna", "negocio", "local", "tienda", "obra", "construcción", "bala", "dinamita"]):
            return EXTORTION_KNOWLEDGE_BASE["COBRO_DE_CUPOS"]
        elif any(w in lower_text for w in ["secuestrado", "hijo", "hija", "mamá", "llanto", "tienen a mi", "no cuelgues"]):
            return EXTORTION_KNOWLEDGE_BASE["SECUESTRO_VIRTUAL"]

        return None

    def get_all_typologies(self) -> List[ExtortionTypology]:
        """Return the complete set of supported extortion typologies."""
        return list(EXTORTION_KNOWLEDGE_BASE.values())


forensic_rag = ForensicRAGKnowledge()
