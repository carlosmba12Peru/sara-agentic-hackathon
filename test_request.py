import requests

url = "http://127.0.0.1:5000/api/denuncia"

# Datos de texto simulados (con soporte inclusivo/UTF-8)
payload = {
    "nombre_completo": "Eduardo",
    "dni": "12345678",
    "telefono_contacto": "987654321",
    "mensaje": "Prueba de extorsión con evidencia fotográfica desde Antigravity."
}

# Si tienes una imagen de prueba en tu workspace, colócale su ruta aquí:
# (Asegúrate de cambiar 'evidencia.jpg' por el nombre real de tu archivo de imagen)
files = {
    'archivo_evidencia': ('evidencia.jpg', open('evidencia.jpg', 'rb'), 'image/jpeg')
}

try:
    response = requests.post(url, data=payload, files=files)
    print("Código de estado:", response.status_code)
    print("Respuesta JSON:", response.json())
except Exception as e:
    print("Error al conectar con la API:", str(e))