#!/bin/bash

# Mostrar la versión de pip
echo "Using pip version:"
pip --version

# Instalar la biblioteca path.py en local_lib y guardar logs
echo "Installing path.py in local_lib..."
pip install --target=local_lib --force-reinstall git+https://github.com/jaraco/path.git > install.log 2>&1

# Verificar si la instalación fue exitosa
if [ $? -eq 0 ]; then
    echo "Installation successful. Running Python program..."
    python3 my_program.py
else
    echo "Installation failed. Check install.log for details."
    exit 1
fi
