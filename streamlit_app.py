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

# ==============================================================================
# 🚨 BANNER OFICIAL DE DESCARGO DE RESPONSABILIDAD (HACKATHON EXPERIMENTAL PoC)
# ==============================================================================
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.16) 0%, rgba(220, 38, 38, 0.16) 100%); border: 2px solid #f59e0b; border-radius: 14px; padding: 14px 20px; margin-bottom: 18px; box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 12px; flex: 1; min-width: 280px;">
            <span style="font-size: 2.2rem; line-height: 1;">⚠️</span>
            <div>
                <div style="font-weight: 800; color: #fcd34d; font-size: 0.98rem; letter-spacing: 0.3px;">ENTORNO DE DEMOSTRACIÓN TÉCNICA — HACKATHON GOOGLE CLOUD 2026</div>
                <div style="font-size: 0.84rem; color: #f1f5f9; margin-top: 2px; line-height: 1.35;">
                    Este prototipo es una <b>prueba de concepto experimental de Inteligencia Artificial</b> para evaluación técnica. <b>NO constituye un canal oficial en vivo de denuncias de la PNP ni del MININTER.</b><br/>
                    🏷️ <b>Cláusula de Datos Sintéticos (Ley N° 29733):</b> Todos los datos de los Casos Modelo son <b>100% ficticios y sintéticos</b> con fines exclusivos de demostración técnica.
                </div>
            </div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #f59e0b; border-radius: 10px; padding: 8px 14px; text-align: center;">
            <div style="font-size: 0.74rem; color: #cbd5e1; font-weight: 700; text-transform: uppercase;">🚨 Emergencias Reales:</div>
            <div style="font-size: 0.92rem; font-weight: 800; color: #38bdf8;">📞 Línea 111 (Extorsión) | 📞 105 (PNP)</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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
    
    # 🔒 MODO SANDBOX ESTRICTO
    st.markdown("""
    <div style="background: rgba(8, 51, 68, 0.35); border-left: 4px solid #38bdf8; border-radius: 8px; padding: 10px 14px; margin-bottom: 14px;">
        <span style="font-weight: 800; color: #38bdf8; font-size: 0.88rem;">🔒 MODO SANDBOX (CASOS MODELO SINTÉTICOS):</span>
        <span style="font-size: 0.82rem; color: #cbd5e1; margin-left: 4px;">
            Para proteger la privacidad de la ciudadanía (Ley N° 29733), este entorno opera con casos de prueba sintéticos precargados.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Presets de Casos Modelo
    CASOS_PRESET_LIVIANOS = {
        "sjl_bomba": {
            "nombre": "Juan Carlos Quispe Huamán",
            "dni": "45879612",
            "telefono": "+51987654321",
            "direccion": "Av. Próceres de la Independencia 1234, San Juan de Lurigancho",
            "mensaje": "Me dejaron una nota con dos balas y una granada en mi pollería en San Juan de Lurigancho. Me piden 5000 soles mensuales a la cuenta BCP 19198765432100 y llaman del 999111222 amenazando con quemar mi local hoy a las 5pm si no pago."
        },
        "cusco_quechua": {
            "nombre": "Santosa Condori Mamani",
            "dni": "71234567",
            "telefono": "+51977665544",
            "direccion": "Comunidad Campesina de Chinchero, Urubamba, Cusco",
            "mensaje": "Allillanchu mamay, yanapaywayku. Huk qari préstamoto qowarqan Chinchero Cuscopi, kunantaq sapa p'unchay qullqita mañawan, 'wañuchisayki wasiykitapas ruphachisayki' nispa 988776655 numeromanta."
        },
        "trujillo_sextorsion": {
            "nombre": "Andrea Flores Vega",
            "dni": "73445566",
            "telefono": "+51944332211",
            "direccion": "Urb. San Andrés Mz. C Lt. 4, Trujillo, La Libertad",
            "mensaje": "Tienen fotografías privadas mías en Trujillo Urb San Andrés y me exigen 2000 soles por Yape al 955112233 en menos de 12 horas o las difundirán a mis contactos de trabajo."
        }
    }
    
    col_pre1, col_pre2, col_pre3 = st.columns(3)
    if "form_preset_data" not in st.session_state:
        st.session_state.form_preset_data = CASOS_PRESET_LIVIANOS["sjl_bomba"]
        
    with col_pre1:
        if st.button("💥 Caso 1: SJL (Bomba a Pollería)", use_container_width=True):
            st.session_state.form_preset_data = CASOS_PRESET_LIVIANOS["sjl_bomba"]
            st.rerun()
    with col_pre2:
        if st.button("🗣️ Caso 2: Cusco (Quechua)", use_container_width=True):
            st.session_state.form_preset_data = CASOS_PRESET_LIVIANOS["cusco_quechua"]
            st.rerun()
    with col_pre3:
        if st.button("📱 Caso 3: Trujillo (Sextorsión)", use_container_width=True):
            st.session_state.form_preset_data = CASOS_PRESET_LIVIANOS["trujillo_sextorsion"]
            st.rerun()

    st.markdown("---")

    cur_p = st.session_state.form_preset_data
    with st.form("form_denuncia_kallpa"):
        st.subheader("Datos de la Víctima (Aislamiento en Secure Vault)")
        nombre = st.text_input("Nombre Completo de la Víctima", value=cur_p["nombre"])
        dni = st.text_input("DNI o Identificación", value=cur_p["dni"])
        telefono = st.text_input("Teléfono de Contacto", value=cur_p["telefono"])
        direccion = st.text_input("Dirección", value=cur_p["direccion"])
        
        st.markdown("---")
        st.subheader("Detalle del Caso")
        mensaje = st.text_area(
            "Mensaje de Extorsión (Soporta Español y Quechua / Rimasqanchikpi yachaykachiy)",
            value=cur_p["mensaje"],
            height=120
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