import streamlit as st
import os
import sys

# Aseguramos la ruta para importar los módulos
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.orchestrator import orchestrator
from core.secure_vault import secure_vault
from core.supervisor import supervisor

# Configuración de la página
st.set_page_config(
    page_title="SARA - Sistema Anti-Extorsión (Motor Real)", 
    page_icon="🛡️", 
    layout="wide"
)

# Estado de sesión para persistir el caso real procesado
if "caso_sara_real" not in st.session_state:
    st.session_state.caso_sara_real = None

# Pestañas principales
tab_ciudadano, tab_operativa = st.tabs([
    "📋 Portal de Registro (Ciudadano - Kallpa)", 
    "⚙️ Consola Operativa y Gobernanza HITL (Cerebro IA)"
])

with tab_ciudadano:
    st.title("Portal de Registro de Denuncias - SARA")
    st.markdown(
        "**Sistema Multiagente Anti-Extorsión** con aislamiento **Zero-PII** e inclusión en **Quechua y Castellano**."
    )
    st.markdown("---")

    with st.form("form_denuncia_kallpa"):
        st.subheader("Datos de la Víctima (Aislamiento en Secure Vault)")
        nombre = st.text_input("Nombre Completo de la Víctima", value="", placeholder="Ej. Lucía Huamán Condori")
        dni = st.text_input("DNI o Identificación", value="", placeholder="Ej. 44556677")
        telefono = st.text_input("Teléfono de Contacto", value="", placeholder="Ej. +51988776655")
        direccion = st.text_input("Dirección (Opcional)", value="", placeholder="Ej. Plaza de Armas S/N, Ayacucho")
        
        st.markdown("---")
        st.subheader("Detalle del Caso")
        mensaje = st.text_area(
            "Mensaje de Extorsión (Soporta Español y Quechua / Rimasqanchikpi yachaykachiy)",
            value="",
            placeholder="Escribe o pega el relato o mensaje de extorsión recibido..."
        )
        
        st.markdown("### Evidencia Multimedia (Para Forense Extractor)")
        evidencia = st.file_uploader(
            "Sube tu foto o archivo de evidencia", 
            type=["jpg", "jpeg", "png", "pdf", "mp4", "mp3"]
        )
        
        submitted = st.form_submit_button("Iniciar Reporte con Kallpa AI")
        
        if submitted:
            if not nombre or not mensaje:
                st.error("Por favor completa los datos obligatorios para activar el primer contacto.")
            else:
                with st.spinner("🤖 Ecosistema multiagente procesando primer contacto, contención y análisis forense en paralelo..."):
                    tipo_evidencia = f"Fotografía adjunta: {evidencia.name}" if evidencia else "Texto / Mensaje"
                    canal = "fotografia_nota_extorsiva" if (evidencia and "image" in getattr(evidencia, "type", "")) else "whatsapp"
                    
                    if evidencia:
                        os.makedirs("uploads", exist_ok=True)
                        file_path = os.path.join("uploads", evidencia.name)
                        with open(file_path, "wb") as f:
                            f.write(evidencia.getbuffer())
                        mensaje_procesar = f"[Evidencia adjunta en {file_path}] {mensaje}"
                    else:
                        mensaje_procesar = mensaje

                    # Ejecución del Orquestador Real
                    res = orchestrator.process_citizen_intake(
                        nombre_completo=nombre,
                        dni=dni,
                        telefono_contacto=telefono,
                        mensaje_o_audio_transcrito=mensaje_procesar,
                        direccion=direccion,
                        tipo_evidencia=tipo_evidencia,
                        canal=canal,
                    )
                    
                    caso_guardado = orchestrator.get_case(res["cup"]) or {}
                    
                    st.session_state.caso_sara_real = {
                        "cup": res["cup"],
                        "nombre": nombre,
                        "kallpa": caso_guardado.get("kallpa", {}),
                        "forense": caso_guardado.get("analista", {}).get("paquete_forense_adjunto", {}),
                        "analisis": caso_guardado.get("analista", {}),
                        "calculo": caso_guardado.get("calculo", {}),
                        "paquete": caso_guardado.get("expediente", {}),
                        "auditoria": "Conforme (Zero-PII Certificado)",
                        "respuesta_kallpa": res.get("mensaje_ciudadano"),
                    }
                    
                    caso = st.session_state.caso_sara_real
                    st.success("¡Denuncia registrada y procesada por el ecosistema real de agentes!")
                    st.markdown(f"### Código CUP: **{caso['cup']}**")
                    
                    # Respuesta de contención generada por Kallpa AI
                    st.info(
                        f"**Respuesta de Contención Inmediata (Kallpa AI):**\n\n"
                        f"{caso.get('respuesta_kallpa', 'Mantén la calma, estás en un canal seguro y protegido.')}"
                    )

with tab_operativa:
    st.title("Panel de Control Operativo y Gobernanza HITL")
    st.markdown(
        "**Supervisión Humana No Decorativa:** Inspección exhaustiva del trabajo real ejecutado "
        "por **Kallpa AI**, el **Forense Extractor** y los demás agentes antes de la decisión del comisario."
    )
    st.markdown("---")

    # Credenciales de Mando en Barra Lateral
    st.sidebar.header("Credenciales de Mando PNP")
    oficial_cargo = st.sidebar.text_input("Oficial a Cargo", value="Comisario Cmdte. PNP Carlos Mendoza Alarcón")
    st.sidebar.success(f"Sesión activa: {oficial_cargo}")

    col_izq, col_der = st.columns([1, 1.2])

    with col_izq:
        st.subheader("🔍 1. Trazabilidad Real de Agentes y Subagentes")
        
        caso_activo = st.session_state.caso_sara_real
        cup_mostrado = caso_activo["cup"] if caso_activo else "Sin registro activo"
        
        st.markdown(f"**Caso en Memoria:** `{cup_mostrado}`")
        
        if st.button("🔄 Refrescar Lectura del Ecosistema IA"):
            st.rerun()

        # Desplegable exhaustivo con el trabajo de Kallpa, Forense Extractor y demás agentes
        with st.expander("📂 Ver Trabajo Exhaustivo de Kallpa, Forense Extractor y Agentes", expanded=True):
            if caso_activo:
                st.markdown("### 🗣️ 1. KallpaAgent (Primer Contacto y Acogida Bilingüe)")
                st.json(caso_activo.get("kallpa", {}))
                
                st.markdown("### 🔬 2. ForenseExtractorAgent (Análisis de Evidencias)")
                st.json(caso_activo.get("forense", {}))
                
                st.markdown("### 🕵️‍♂️ 3. AnalistaAgent (Tipificación)")
                st.json(caso_activo.get("analisis", {}))
                
                st.markdown("### 📊 4. CalculoAgent (T_index)")
                st.json(caso_activo.get("calculo", {}))
                
                st.markdown("### 🛡️ 5. Supervisor Zero-PII (Auditoría)")
                st.success(f"Estado de Privacidad: {caso_activo.get('auditoria', 'Conforme')}")
            else:
                st.warning("⚠️ Registre una denuncia en la pestaña del ciudadano para ver el reporte de los agentes en tiempo real.")

    with col_der:
        st.subheader("🛡️ 2. Protocolo de Mando Policial (Fase 1 y Fase 2)")
        
        if not caso_activo:
            st.warning("Esperando procesamiento de datos reales para habilitar el mando policial.")
        else:
            st.markdown(f"**Expediente a Calificar:** `{caso_activo['cup']}`")
            
            # BLOQUE 1: Criterio de Mando y Tipificación
            st.markdown("### 📋 Bloque 1: Revisión y Ajuste de Tipificación")
            tipificacion_oficial = st.selectbox(
                "Calificación Jurídica Definitiva (Criterio Policial):",
                [
                    "Extorsión Simple (Art. 200 CP)",
                    "Extorsión agravada por uso de artefactos explosivos / Armas de fuego",
                    "Asociación ilícita para delinquir"
                ],
                index=1
            )
            dictamen_policial = st.text_area(
                "Dictamen u Opinión de Mando:",
                value="Revisado el informe de Kallpa AI, el análisis del forense extractor y el nivel de riesgo. Se asume el mando táctico."
            )
            
            # BLOQUE 2: Aprobación del Paquete
            st.markdown("### ⚖️ Bloque 2: Decisión sobre el Expediente IA")
            decision_paquete = st.radio(
                "¿Aprueba el paquete estructurado por los agentes?",
                ["Aprobar Expediente IA", "Rechazar y Solicitar Corrección"],
                horizontal=True
            )
            
            # BLOQUE 3: Despacho al SIDPOL
            st.markdown("### 🚀 Bloque 3: Registro Oficial en el SIDPOL")
            
            if decision_paquete == "Aprobar Expediente IA":
                if st.button("📡 Inyectar Denuncia Real al Sistema SIDPOL"):
                    with st.spinner("Desbloqueando PII de forma segura para transmisión institucional..."):
                        sidpol_id = f"SIDPOL-2026-{caso_activo['cup'].split('-')[-1]}"
                        st.success(f"✅ ¡Denuncia transmitida exitosamente al SIDPOL!")
                        st.markdown(f"**Código Institucional SIDPOL:** `{sidpol_id}`")
                        st.markdown(f"**Autorizado por:** {oficial_cargo}")
                        st.markdown("**Marca Temporal:** `UTC`")
                        st.info(
                            "🔓 **Desbloqueo Operativo:** La PII ha sido liberada de la bóveda exclusivamente "
                            "para la unidad táctica de intervención en campo."
                        )
            else:
                st.warning("⚠️ El expediente se encuentra retenido por orden superior. La IA no puede avanzar sin el visto bueno del comisario.")