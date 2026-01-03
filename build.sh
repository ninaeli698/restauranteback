#!/usr/bin/env bash
# build.sh
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate --noinput

# Crear superusuario por defecto (solo si no existe)
# Esto es opcional, pero si quieres un superusuario por defecto, puedes hacerlo aquí.
# Nota: No es seguro dejar la contraseña en el código, pero para desarrollo puedes hacerlo.
# En producción, deberías usar variables de entorno para el superusuario.
# Si no quieres crear un superusuario automáticamente, omite este paso.

# Recolectar archivos estáticos
python manage.py collectstatic --noinput