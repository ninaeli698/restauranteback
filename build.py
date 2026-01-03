# build.py
import os
import sys
import subprocess

def run_command(command):
    """Ejecuta un comando y verifica si hubo error"""
    print(f"Ejecutando: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error en: {command}")
        sys.exit(1)

# Comandos para producción
run_command("pip install -r requirements.txt")
run_command("python manage.py collectstatic --noinput")
run_command("python manage.py migrate")

print("✅ Build completado exitosamente")