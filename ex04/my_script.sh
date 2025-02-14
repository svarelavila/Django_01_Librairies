#!/bin/bash

# Nombre del entorno virtual y archivo de dependencias
VENV_NAME="django_venv"
REQUIREMENTS_FILE="requirement.txt"

# Verificar si virtualenv está instalado, si no, instalarlo en el directorio de usuario
if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv no está instalado. Instalándolo en el directorio de usuario..."
    pip install --user virtualenv
    export PATH=$PATH:~/.local/bin
    if ! command -v virtualenv &> /dev/null; then
        echo "Error: La instalación de virtualenv falló. Intenta instalarlo manualmente con 'pip install virtualenv'."
        exit 1
    fi
fi

# Crear el entorno virtual con virtualenv
echo "Creando el entorno virtual '$VENV_NAME'..."
virtualenv $VENV_NAME || exit 1

# Verificar si el entorno virtual se creó correctamente
if [ ! -d "$VENV_NAME" ]; then
    echo "Error: No se pudo crear el entorno virtual '$VENV_NAME'."
    exit 1
fi

# Activar el entorno virtual
echo "Activando el entorno virtual '$VENV_NAME'..."
source $VENV_NAME/bin/activate || exit 1

# Verificar si requirement.txt existe antes de instalar dependencias
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Instalando dependencias desde '$REQUIREMENTS_FILE'..."
    pip install --upgrade pip
    pip install -r $REQUIREMENTS_FILE || exit 1
else
    echo "Error: No se encontró el archivo '$REQUIREMENTS_FILE'."
    deactivate
    exit 1
fi
