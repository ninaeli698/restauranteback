import requests
import time
import os

def ping_app():
    url = os.environ.get('RENDER_APP_URL', 'https://tu-app.onrender.com')
    try:
        response = requests.get(url, timeout=10)
        print(f"Ping exitoso: {response.status_code}")
    except Exception as e:
        print(f"Error en ping: {e}")

if __name__ == "__backendR__":
    # Ejecutar cada 10 minutos
    while True:
        ping_app()
        time.sleep(600)  # 10 minutos