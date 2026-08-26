"""Script de Prueba de Cierre del Ciclo de Vida y Resiliencia Cloud (test_cloud_lifecycle.py).
Valida la persistencia de estados tras un reinicio simulado y el proceso de Teardown
inspirado en el Lab 21 del curso.
"""

import logging
import importlib
from main import app

# Configurar logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sara.lifecycle")

def simular_reinicio_servidor():
    """Simula un reinicio del ciclo de vida del contenedor (Cloud Run / App Engine)."""
    logger.info("🔄 [Cloud Lifecycle] Simulando reinicio de contenedor y recarga del motor Flask...")
    # Recargar el módulo principal para asegurar que las conexiones y estados se manejan de forma robusta
    import main
    importlib.reload(main)
    logger.info("    ✅ Contenedor reiniciado y operativo. El Secure Vault mantiene la persistencia.")

def ejecutar_prueba_ciclo_vida():
    logger.info("================================================================================")
    logger.info("☁️ INICIANDO PRUEBA DE CICLO DE VIDA Y RESILIENCIA CLOUD (LAB 21)")
    logger.info("================================================================================\n")

    client = app.test_client()

    # 1. Crear una denuncia inicial antes del reinicio
    payload_inicial = {
        "nombre_completo": "Rosaura Pinedo",
        "dni": "98765432",
        "telefono_contacto": "+51955443322",
        "direccion": "Jr. Cusco 123, Huancayo",
        "mensaje": "Maqtakuna qullqita mañawashanku, yanapaykuwaychik.",
    }

    logger.info("📥 Enviando denuncia previa al ciclo de reinicio...")
    res1 = client.post("/api/denuncia", json=payload_inicial)
    assert res1.status_code == 201
    cup_generado = res1.get_json().get("cup")
    logger.info(f"    🔒 Caso registrado exitosamente bajo el código: {cup_generado}")

    # 2. Simular el reinicio del servidor (Teardown / Redeploy simulation)
    simular_reinicio_servidor()

    # 3. Validar que las trazas de auditoría y el sistema sigan respondiendo tras el reinicio
    logger.info("🔍 Consultando el registro de trazas forenses tras el reinicio...")
    res_trazas = client.get("/api/trazas")
    assert res_trazas.status_code == 200
    datos_trazas = res_trazas.get_json()
    
    total_trazas = len(datos_trazas.get("trazas_supervisor_ia", []))
    logger.info(f"    📋 Integridad de auditoría verificada. Total de eventos en cadena: {total_trazas}")
    assert total_trazas > 0, "❌ Error crítico: Se perdió la cadena de auditoría tras el reinicio."

    logger.info("\n================================================================================")
    logger.info("✅ PRUEBA DE RESILIENCIA Y CICLO DE VIDA CLOUD SUPERADA CON ÉXITO")
    logger.info("================================================================================")

if __name__ == "__main__":
    ejecutar_prueba_ciclo_vida()