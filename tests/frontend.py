import requests
import streamlit as st

st.title("Portal de Registro de Denuncias - SARA")
st.markdown("Sistema Multiagente Anti-Extorsión con aislamiento **Zero-PII** e inclusión en Quechua y Castellano.")

with st.form("form_denuncia"):
    nombre_completo = st.text_input("Nombre Completo de la Víctima")
    dni = st.text_input("DNI o Identificación")
    telefono = st.text_input("Teléfono de Contacto")
    direccion = st.text_input("Dirección (Opcional)")
    mensaje = st.text_area("Mensaje de Extorsión (Soporta Español y Quechua)")
    
    # Selector de evidencia fotográfica
    archivo_foto = st.file_uploader("Sube tu foto evidencia", type=["jpg", "jpeg", "png"])
    
    enviado = st.form_submit_button("Enviar Denuncia")

    if enviado:
        url = "http://127.0.0.1:5000/api/denuncia"
        
        # Datos en formulario (Form-Data)
        payload = {
            "nombre_completo": nombre_completo,
            "dni": dni,
            "telefono_contacto": telefono,
            "direccion": direccion,
            "mensaje": mensaje
        }
        
        # Archivos adjuntos
        files = {}
        if archivo_foto is not None:
            files = {
                'archivo_evidencia': (archivo_foto.name, archivo_foto.getvalue(), archivo_foto.type)
            }

        try:
            # Envío de datos y archivos multimedia a Flask
            response = requests.post(url, data=payload, files=files if files else None)
            
            if response.status_code == 201:
                res_json = response.json()
                st.success("¡Denuncia registrada con éxito bajo aislamiento Zero-PII!")
                st.info(f"**Código CUP:** {res_json.get('cup')}")
                st.write("**Respuesta de Contención Inmediata:**")
                st.write(res_json.get("respuesta_inmediata_victima"))
            else:
                st.error(f"Error en el servidor: {response.text}")
        except Exception as e:
            st.error(f"Error al conectar con la API: {str(e)}")