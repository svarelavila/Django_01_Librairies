import sys
import requests
import json
from dewiki import from_string  # Para convertir texto limpio


def fetch_wikipedia_page(query):
    """
    Performs a search on the Wikipedia API
    and returns content in plain text.
    """
    url = "https://en.wikipedia.org/w/api.php"  # URL fija en inglés
    params = {
    "action": "query",      # Realiza una consulta a la API de Wikipedia
    "format": "json",       # La respuesta se devolverá en formato JSON
    "prop": "extracts",     # Extrae solo el contenido de la página sin código HTML ni metadatos
    "titles": query,        # Especifica el título de la página a buscar en Wikipedia
    "explaintext": True,    # Devuelve solo texto sin formato, eliminando etiquetas de Wiki Markup
    "redirects": 1          # Sigue automáticamente redirecciones si la página ha cambiado de título
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta un error si la solicitud falla

        data = response.json()
        pages = data["query"]["pages"]
        page_id = next(iter(pages))  # Obtener el primer ID de página

        if page_id == "-1":
            print(f"Error: No information found for '{query}' on Wikipedia.")
            sys.exit(1)

        return from_string(pages[page_id]["extract"])  # Convertir de Wiki Markup a texto limpio

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Wikipedia: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid Wikipedia response.")
        sys.exit(1)
    except KeyError:
        print("Error: No relevant information found.")
        sys.exit(1)


def save_to_file(filename, content):
    """Saves the content to a file with the formatted name."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Result saved in '{filename}")
    except IOError as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 request_wikipedia.py <término de búsqueda>")
        sys.exit(1)

    query = sys.argv[1]
    filename = f"{query.replace(' ', '_')}.wiki"  # Formatear nombre del archivo

    content = fetch_wikipedia_page(query)
    save_to_file(filename, content)


if __name__ == "__main__":
    main()
