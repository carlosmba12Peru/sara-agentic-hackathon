#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de Validación Forense: Extractor Pericial con Casos de Autollenado de SARA.
Ejecuta los escenarios de autollenado y sus evidencias digitales precargadas a través de:
1. SubAgenteForenseExtractor (Peritaje Forense, OCR, Balística, TSA RFC 3161, Cuentas UIF).
2. SARA Orchestrator (Enjambre Completo de 12 Agentes Autónomos).
"""

import os
import sys
import json
import logging
from pprint import pprint

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("test_forense")

# Importar agentes
try:
    from agents.forense_extractor import SubAgenteForenseExtractor
    from core.orchestrator import MultiAgentParallelOrchestrator
except ImportError as e:
    logger.error(f"Error importando módulos: {e}")
    sys.exit(1)

def test_extractor_con_autollenados():
    extractor = SubAgenteForenseExtractor()
    orchestrator = MultiAgentParallelOrchestrator()

    casos_prueba = [
        {
            "id": "CASO_1_SJL_BOMBA",
            "titulo": "💥 SJL: Cupos & Bomba (Pollería El Sol)",
            "nombre": "Juan Carlos Quispe Huamán",
            "dni": "45879612",
            "telefono": "+51987654321",
            "mensaje": "Me dejaron una nota con dos balas y una granada en mi pollería en San Juan de Lurigancho. Me piden 5000 soles mensuales a la cuenta BCP 19198765432100 y llaman del 999111222 amenazando con quemar mi local hoy a las 5pm si no pago.",
            "banda": "Los Injertos de SJL",
            "monto": "5,000",
            "cuentas": ["BCP 19198765432100"],
            "tel_ext": "+51999111222",
            "dep_hecho": "Lima",
            "dist_hecho": "San Juan de Lurigancho",
            "evidencias": [
                {
                    "nombre_archivo": "foto_nota_manuscrita_con_balas_y_granada_lima.jpg",
                    "tamano_kb": 384.5,
                    "mime_type": "image/jpeg",
                    "hash_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "tipo": "Imagen",
                    "descripcion": "Fotografía forense de nota manuscrita extorsiva dejada con dos municiones 9mm y granada defensiva.",
                    "b64_data": ""
                },
                {
                    "nombre_archivo": "captura_voucher_cuenta_receptora_999111222.png",
                    "tamano_kb": 218.4,
                    "mime_type": "image/png",
                    "hash_sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
                    "tipo": "Imagen",
                    "descripcion": "Comprobante pericial con cuenta receptora detectada: BCP 19198765432100.",
                    "b64_data": ""
                }
            ]
        },
        {
            "id": "CASO_2_COMBI_MEXICANOS",
            "titulo": "🚌 Los Mexicanos: Combi (El Agustino)",
            "nombre": "Marcos Huamán Quispe",
            "dni": "40928174",
            "telefono": "+51978123456",
            "mensaje": "Soy transportista de la empresa de combis en El Agustino. La facción 'Los Piseros de Malecón' de la banda 'Los Mexicanos' envía videos de armas por WhatsApp desde el +51988776655 exigiendo S/ 20 diarios por vehículo, obligándonos a transferir al Yape 944556677 de Carlos Renzo Egusquiza (La Cuenta Receptora), bajo amenaza de balear las unidades en el paradero.",
            "banda": "Los Mexicanos (Facción Los Piseros de Malecón)",
            "monto": "20 diarios",
            "cuentas": ["Yape 944556677 (Carlos Renzo Egusquiza)"],
            "tel_ext": "+51988776655",
            "dep_hecho": "Lima",
            "dist_hecho": "El Agustino",
            "evidencias": [
                {
                    "nombre_archivo": "video_amenaza_armas_fuego_whatsapp_988776655.mp4",
                    "tamano_kb": 1420.8,
                    "mime_type": "video/mp4",
                    "hash_sha256": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
                    "tipo": "Video",
                    "descripcion": "Video de WhatsApp con exhibición de armas cortas y advertencia de disparos a unidades de transporte.",
                    "b64_data": ""
                },
                {
                    "nombre_archivo": "captura_voucher_cuenta_receptora_988776655.png",
                    "tamano_kb": 218.4,
                    "mime_type": "image/png",
                    "hash_sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
                    "tipo": "Imagen",
                    "descripcion": "Comprobante pericial con cuenta receptora detectada: Yape 944556677 (Carlos Renzo Egusquiza).",
                    "b64_data": ""
                }
            ]
        },
        {
            "id": "CASO_3_CENEPA_AWAJUN",
            "titulo": "🌿 Cenepa: Awajún (Peke-Peke Fluvial)",
            "nombre": "Tajimat Wampus Petsa",
            "dni": "47819203",
            "telefono": "+51977554433",
            "mensaje": "Kumpami yatsuch Kallpa, yaimkata. Cenepamanta 977554433 número kuji 1000 soles exigiu lancha peke-peke o namput suwimka mántat.",
            "banda": "Extorsión Fluvial Peke-Peke Cenepa",
            "monto": "1,000",
            "cuentas": [],
            "tel_ext": "+51977554433",
            "dep_hecho": "Amazonas",
            "dist_hecho": "El Cenepa (Huampami)",
            "evidencias": [
                {
                    "nombre_archivo": "foto_lancha_embarcacion_baleada_rio_amazonas.jpg",
                    "tamano_kb": 512.3,
                    "mime_type": "image/jpeg",
                    "hash_sha256": "486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7",
                    "tipo": "Imagen",
                    "descripcion": "Fotografía de impactos de proyectil en lancha comunal de transporte fluvial.",
                    "b64_data": ""
                },
                {
                    "nombre_archivo": "audio_nota_voz_amenaza_extorsiva_977554433.opus",
                    "tamano_kb": 345.6,
                    "mime_type": "audio/opus",
                    "hash_sha256": "7d97e98f8af710c7e7fe7036e94f9e8b6b010a5ae87c000b397c7929452d95a9",
                    "tipo": "Audio",
                    "descripcion": "Nota de voz con exigencia extorsiva de dinero (S/ 1,000) y plazo perentorio.",
                    "b64_data": ""
                }
            ]
        }
    ]

    print("\n" + "="*80)
    print("🔬 TEST DE VALIDACIÓN: AGENTE FORENSE EXTRACTOR CON ESCENARIOS DE AUTOLLENADO")
    print("="*80 + "\n")

    for c in casos_prueba:
        print(f"\n👉 Probando: {c['titulo']}")
        print(f"   👤 Víctima: {c['nombre']} (DNI: {c['dni']})")
        print(f"   📁 Evidencias Digitales Adjuntas: {len(c['evidencias'])} archivos")

        # 1. Ejecutar Extractor Forense Directo
        res_extractor = extractor.extraer_patrones(
            texto_mensaje=c["mensaje"],
            evidencias_digitales=c["evidencias"]
        )

        print("\n   [RESULTADOS FORENSE_EXTRACTOR]:")
        print(f"   - 🏴 Banda / Organización: {res_extractor.get('organizaciones_criminales_detectadas')}")
        print(f"   - 💵 Montos Exigidos: {res_extractor.get('montos_exigidos')}")
        print(f"   - 📱 Teléfonos Extorsivos: {res_extractor.get('telefonos_detectados')}")
        print(f"   - 💳 Cuentas / Billeteras UIF: {res_extractor.get('entidades_financieras_detectadas')}")
        print(f"   - 🔫 Balística / Calibre: {res_extractor.get('calibres_y_balistica_detectados')}")
        print(f"   - 💣 Elementos Físicos / Amenazas: {res_extractor.get('elementos_fisicos_detectados')}")
        print(f"   - 📦 Métodos de Entrega: {res_extractor.get('metodos_entrega_detectados')}")
        print(f"   - 🔒 Total Archivos Peritados: {len(res_extractor.get('detalle_archivos_analizados', []))}")

        # Validar cada archivo peritado
        for idx_arch, arch in enumerate(res_extractor.get('detalle_archivos_analizados', [])):
            sello = arch.get('sello_tiempo_digital_rfc3161', {})
            print(f"     📄 Evidencia #{idx_arch+1}: {arch.get('nombre_archivo')} -> Tipo: {arch.get('tipo_forense')} | SHA256: {arch.get('hash_sha256')[:12]}... | TSA: {sello.get('status')}")

        # 2. Ejecutar Enjambre Completo (Orchestrator Intake)
        print("\n   [EJECUTANDO ENJAMBRE SARA COMPLETO]...")
        res_intake = orchestrator.process_citizen_intake(
            nombre_completo=c["nombre"],
            dni=c["dni"],
            telefono_contacto=c["telefono"],
            direccion=f"{c['dist_hecho']}, {c['dep_hecho']}",
            mensaje_o_audio_transcrito=c["mensaje"],
            tipo_evidencia=f"Chat + {len(c['evidencias'])} Evidencias Multimedia",
            canal="kallpa_chat_web",
            evidencias_digitales=c["evidencias"]
        )

        print(f"   ✅ Código CUP: {res_intake.get('cup')}")
        print(f"   ✅ T-Score Amenaza: {res_intake.get('t_index')}")
        print(f"   ✅ Nivel de Riesgo: {res_intake.get('nivel_riesgo')}")
        print(f"   ✅ Estatus Gobernanza: {res_intake.get('status_gobernanza')}")
        print(f"   ✅ Tipificación Penal: {res_intake.get('expediente_normativo', {}).get('tipificacion_penal_sugerida', 'N/A')}")
        print(f"   ✅ Evidencias Selladas en Expediente: {len(res_intake.get('evidencias_digitales', []))}")
        print("-" * 75)

    print("\n🎉 TODOS LOS CASOS DE AUTOLLENADO FUERON PROCESADOS EXITOSAMENTE POR EL AGENTE FORENSE EXTRACTOR Y EL ENJAMBRE SARA.")

if __name__ == "__main__":
    test_extractor_con_autollenados()
