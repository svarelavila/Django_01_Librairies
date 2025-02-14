import sys

# Asegurar que el módulo path se importa desde el directorio local_lib
sys.path.insert(0, "local_lib")

from local_lib.path import Path


def main():
    """
    Creates a directory, writes a text file inside it,
     and then reads the file content.

    - Creates a directory named 'my_folder' if it does not exist.
    - Writes a message into 'my_file.txt' inside 'my_folder'.
    - Reads the content of the file and prints it.

    Raises:
        Exception: If there is an issue with file operations.
    """
    try:
        # Crear el directorio my_folder
        folder = Path("my_folder")
        folder.mkdir_p()  # Crear carpeta, incluso si ya existe

        # Crear un archivo dentro de my_folder
        file = folder / "my_file.txt"
        file.write_text("¡Hola, este es un archivo creado con path.py!\n")

        # Leer el contenido del archivo y mostrarlo
        content = file.read_text()
        print(f"File content: {content}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
