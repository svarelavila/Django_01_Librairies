#!/bin/bash

# Verificar si virtualenv está instalado, si no, instalarlo en el directorio de usuario
if ! python3 -m virtualenv --version &> /dev/null; then
    echo "Virtualenv no está instalado. Instalándolo en el directorio de usuario..."
    pip install --user virtualenv
    export PATH=$PATH:~/.local/bin
fi

# Crear el entorno virtual con virtualenv y nombrarlo "django_venv"
python3 -m virtualenv django_venv

# Verificar si el entorno virtual se creó correctamente
if [ ! -d "django_venv" ]; then
    echo "The virtual environment was not created correctly"
    exit 1
fi

# Activar el entorno virtual
source django_venv/bin/activate

# Instalar las dependencias de requirement.txt
pip install -r requirement.txt

# Mantener el entorno virtual activado al salir del script
exec "$SHELL"