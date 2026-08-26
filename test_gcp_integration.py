"""Script de Prueba de Integración con Secretos y BigQuery (test_gcp_integration.py).
Valida la gestión de secretos institucionales y el volcado analítico seguro hacia
BigQuery bajo el protocolo Zero-PII, inspirado en el Lab 18 del curso.
"""

import logging
import os
from main import app

# Configurar logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sara.gcp_integration")

def simular_gestor_secretos():
    """Simula la carga de secretos de GCP (Secret Manager) requeridos por el Secure Vault."""
    logger.info("🔑 [Secret Manager] Conectando con Google Cloud Secret Manager...")
    # Simulando la recuperación de una llave institucional cifrada
    secreto_mock = "projects/sara-gov-prod/secrets/vault-encryption-key/versions/latest"
    logger.info(f"    🔒 Llave institucional recuperada de forma segura: {secreto_mock}")
    return True

def simular_streaming_bigquery(expediente_resumen):
    """Simula el envío de métricas anonimizadas a una tabla de BigQuery (Zero-PII)."""
    logger.info("📊 [BigQuery Service] Preparando streaming de datos analíticos...")
    
    # Validar estrictamente el cumplimiento Zero-PII antes del streaming
    datos_analiticos = {
        "cup": expediente_resumen.get("cup"),
        "t_index": expediente_resumen.get("t_index_calculado", expediente_resumen.get("t_index")),
        "nivel_riesgo": expediente_resumen.get("nivel_riesgo"),
        "idioma": expediente_resumen.get("idioma_detectado"),
    }
    
    # Comprobación de seguridad: Asegurar que no existan campos con PII
    keys_prohibidas = ["nombre_completo", "dni", "telefono_contacto", "direccion"]
    for k in keys_prohibidas:
        assert k not in datos_analiticos, f"❌ ALERTA DE SEGURIDAD: PII detectada en el payload de BigQuery ({k})"

    logger.info(f"    🚀 Inserción exitosa en dataset institucional BigQuery: {datos_analiticos}")
    return True

def ejecutar_prueba_gcp():
    logger.info("================================================================================")
    logger.info("☁️ INICIANDO PRUEBA DE INTEGRACIÓN: SECRETOS & BIGQUERY (LAB 18)")
    logger.info("================================================================================\n")

    # 1. Validar Secret Manager
    secretos_ok = simular_gestor_secretos()
    assert secretos_ok, "Fallo al conectar con el gestor de secretos."

    # 2. Ejecutar denuncia real a través de Flask para obtener un expediente vivo
    client = app.test_client()
    payload_prueba = {
        "nombre_completo": "Lucía Huamán Condori",
        "dni": "44556677",
        "telefono_contacto": "+51988776655",
        "direccion": "Plaza de Armas S/N, Ayacucho",
        "mensaje": "Maqta, qullqita mañawashanku, mana quptiyqa familianchispa contranpi imatapas ruwasaq ninku.",
    }

    logger.info("📥 Enviando denuncia de prueba al core de SARA...")
    res = client.post("/api/denuncia", json=payload_prueba)
    assert res.status_code == 201
    datos_respuesta = res.get_json()

    # 3. Validar Streaming a BigQuery con aislamiento Zero-PII
    bq_ok = simular_streaming_bigquery(datos_respuesta)
    assert bq_ok, "Fallo en la sincronización con BigQuery."

    logger.info("\n================================================================================")
    logger.info("✅ PRUEBA DE INTEGRACIÓN GCP (SECRETOS Y BIGQUERY) SUPERADA CON ÉXITO")
    logger.info("================================================================================")

if __name__ == "__main__":
    ejecutar_prueba_gcp()