#!/bin/bash

# Nombre del entorno virtual y archivo de dependencias
VENV_NAME="django_venv"
REQUIREMENTS_FILE="requirement.txt"

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado. Por favor, instálalo e inténtalo de nuevo."
    exit 1
fi

# Crear el entorno virtual con venv (incluido en Python 3)
echo "Creando el entorno virtual '$VENV_NAME'..."
python3 -m venv $VENV_NAME || exit 1

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


# Mensaje de confirmación
echo "Configuración completada con éxito."
echo "El entorno virtual '$VENV_NAME' está ahora activo."
echo "Usa 'deactivate' para salir del entorno virtual."
