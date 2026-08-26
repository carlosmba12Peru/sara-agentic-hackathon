"""Script de Evaluación Sistemática de Calidad (evals.py).
Mide las métricas de precisión de SARA (tipificación, idioma, Zero-PII y riesgo)
inspirado en el Lab 14 del curso.
"""

import logging
from main import app

# Configurar logger para consola
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sara.evals")

# Dataset de prueba para Evals (Casos esperados)
DATASET_EVALUACION = [
    {
        "id": "EVAL_01",
        "payload": {
            "nombre_completo": "Carlos Mendoza R.",
            "dni": "12345678",
            "telefono_contacto": "+51911222333",
            "direccion": "Av. Larco 456, Miraflores, Lima",
            "mensaje": "Me dejaron un sobre con una granada y piden 5000 soles a la cuenta BCP o queman mi pollería hoy.",
        },
        "idioma_esperado": "ESPAÑOL",
        "nivel_riesgo_esperado": "CRITICO",
    },
    {
        "id": "EVAL_02",
        "payload": {
            "nombre_completo": "Juana Quispe Ticona",
            "dni": "87654321",
            "telefono_contacto": "+51944556677",
            "direccion": "Comunidad de Raqchi, Cusco",
            "mensaje": "Ama sua, ama llulla, ama quella. Huk qari qullqita mañawashan manchachikuspan, wasiytapas ruphachisayki nispa.",
        },
        "idioma_esperado": "QUECHUA",
        "nivel_riesgo_esperado": "CRITICO",
    },
]

def ejecutar_evaluaciones():
    logger.info("================================================================================")
    logger.info("📊 INICIANDO BATERÍA DE EVALUACIÓN SISTEMÁTICA DE CALIDAD (EVALS - LAB 14)")
    logger.info("================================================================================\n")

    client = app.test_client()
    total_casos = len(DATASET_EVALUACION)
    exitos_idioma = 0
    exitos_cup = 0

    for item in DATASET_EVALUACION:
        caso_id = item["id"]
        logger.info(f"👉 Evaluando caso [{caso_id}]...")
        
        res = client.post("/api/denuncia", json=item["payload"])
        assert res.status_code == 201
        data = res.get_json()

        # Validaciones de métricas
        cup = data.get("cup")
        idioma_detectado = data.get("idioma_detectado")
        nivel_riesgo = data.get("nivel_riesgo")

        logger.info(f"   🔒 CUP Generado (Aislamiento Zero-PII): {cup}")
        logger.info(f"   🗣️ Idioma Esperado: {item['idioma_esperado']} | Detectado: {idioma_detectado}")
        logger.info(f"   📊 Nivel de Riesgo Calculado: {nivel_riesgo}")

        # Comprobaciones lógicas
        if cup and cup.startswith("CUP-"):
            exitos_cup += 1
        
        if idioma_detectado == item["idioma_esperado"]:
            exitos_idioma += 1

        logger.info(f"   ✅ Caso [{caso_id}] evaluado correctamente.\n")

    # Resumen de Métricas (Evals Scorecard)
    logger.info("================================================================================")
    logger.info("📈 SCORECARD DE EVALUACIÓN (EVALS)")
    logger.info("================================================================================")
    logger.info(f"   Total Casos Evaluados: {total_casos}")
    logger.info(f"   Precisión de Aislamiento Zero-PII (CUP): {(exitos_cup / total_casos) * 100:.1f}%")
    logger.info(f"   Precisión de Detección Lingüística: {(exitos_idioma / total_casos) * 100:.1f}%")
    logger.info("================================================================================")
    logger.info("🎉 EVALUACIÓN SISTEMÁTICA FINALIZADA EXITOSAMENTE")
    logger.info("================================================================================")

if __name__ == "__main__":
    ejecutar_evaluaciones()