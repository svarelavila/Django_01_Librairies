#!/bin/bash

# Nombre del entorno virtual
VENV_NAME="django_venv"
REQUIREMENTS_FILE="requirement.txt"

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Crear el entorno virtuao
echo "Creating virtual environment '$VENV_NAME'..."
python3 -m venv $VENV_NAME || exit 1

# Activar el entorno virtual
echo "Activating virtual environment '$VENV_NAME'..."
source $VENV_NAME/bin/activate || exit 1

# Instalar dependencias
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --upgrade pip
    pip install -r $REQUIREMENTS_FILE || exit 1
else
    echo "Error: $REQUIREMENTS_FILE not found. Please create it and try again."
    deactivate
    exit 1
fi

# Confirmar la activación
echo "Setup completed successfully."
echo "Virtual environment '$VENV_NAME' is now active."
echo "Use 'deactivate' to exit the virtual environment."
