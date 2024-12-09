import sys

# Asegurar que el módulo path se importa desde el directorio local_lib
sys.path.insert(0, "local_lib")
from local_lib.path import Path

def main():
    # Crear el directorio my_folder
    folder = Path("my_folder")
    folder.mkdir_p() # Crear carpeta, incluso si ya existe

    # Crear un archivo dentro de my_folder
    file = folder / "my_file.txt"
    file.write_text("Hello, World!!!!!!!!!")

    # Leer el contenido del archivo y mostrarlo
    content = file.read_text()
    print(f"File content: {content}")

if __name__ == "__main__":
    main()