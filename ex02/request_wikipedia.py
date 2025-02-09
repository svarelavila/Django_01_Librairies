import sys
import requests
import json
from dewiki import from_string  # Importar solo la función necesaria

def fetch_wikipedia_page(query):
    """
    Realiza una búsqueda en la API de Wikipedia (en inglés) y devuelve el contenido en texto plano.
    """
    url = "https://en.wikipedia.org/w/api.php"  # URL fija en inglés
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": query,
        "explaintext": True,
        "redirects": 1  # Manejar redirecciones
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta un error si la solicitud falla

        data = response.json()
        pages = data["query"]["pages"]
        page_id = next(iter(pages))  # Obtener el primer ID de página

        if page_id == "-1":
            print(f"Error: No se encontró información para '{query}' en Wikipedia.")
            sys.exit(1)

        return from_string(pages[page_id]["extract"])  # Convertir de Wiki Markup a texto limpio

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con Wikipedia: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Respuesta de Wikipedia no válida.")
        sys.exit(1)
    except KeyError:
        print("Error: No se encontró información relevante.")
        sys.exit(1)

def save_to_file(filename, content):
    """Guarda el contenido en un archivo con el nombre formateado."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Resultado guardado en '{filename}'.")
    except IOError as e:
        print(f"Error al escribir el archivo: {e}")
        sys.exit(1)

def main():
    """
    Función principal del script.
    """
    if len(sys.argv) != 2:
        print("Uso: python3 request_wikipedia.py <término de búsqueda>")
        sys.exit(1)

    query = sys.argv[1]
    filename = f"{query.replace(' ', '_')}.wiki"  # Formatear nombre del archivo

    content = fetch_wikipedia_page(query)
    save_to_file(filename, content)

if __name__ == "__main__":
    main()
