import sys
import requests
from bs4 import BeautifulSoup

WIKI_BASE_URL = "https://en.wikipedia.org"
PHILOSOPHY_TITLE = "Philosophy"  # Definimos la constante

def find_first_link(parsed_page):
    """
    Encuentra el primer enlace válido dentro del contenido principal de la página.
    Ignora enlaces de ayuda, referencias y texto en cursiva.
    """
    content = parsed_page.find(id="mw-content-text").find(class_="mw-parser-output")
    
    for paragraph in content.find_all("p", recursive=False):  # Buscar en párrafos principales
        for link in paragraph.find_all("a", recursive=False):
            href = link.get("href")
            if href and href.startswith("/wiki/") and "Help:" not in href:
                # Ignorar enlaces dentro de <i> (cursiva) o <sup> (nota al pie)
                if link.find_parent(["i", "sup"]):
                    continue
                return href

    # Si no hay enlaces en <p>, buscar en listas <ul>
    for unordered_list in content.find_all("ul", recursive=False):
        for list_item in unordered_list.find_all("li", recursive=False):
            for link in list_item.find_all("a", recursive=False):
                href = link.get("href")
                if href and href.startswith("/wiki/") and "Help:" not in href:
                    return href

    return None  # No se encontró ningún enlace válido

def roads_to_philosophy(start_topic):
    """
    Encuentra la ruta desde un artículo de Wikipedia hasta la página de Filosofía.
    """
    session = requests.Session()  # Usar una sesión para optimizar solicitudes
    visited_pages = []
    current_path = f"/wiki/{start_topic.replace(' ', '_')}"
    
    while True:
        current_url = WIKI_BASE_URL + current_path
        try:
            response = session.get(current_url)  # Usar sesión en lugar de requests.get()
            if response.status_code == 404:
                print(f"Error: La página '{start_topic}' no existe en Wikipedia.")
                return
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return
        
        parsed_page = BeautifulSoup(response.text, "html.parser")
        current_title = parsed_page.find(id="firstHeading").text.strip()  # Obtener el título de la página
        print(current_title)

        if current_title in visited_pages:
            print("¡Se detectó un bucle infinito!")
            return
        elif current_title == PHILOSOPHY_TITLE:  # Verificamos si llegamos a "Philosophy"
            print(f"¡Llegamos a Filosofía en {len(visited_pages) + 1} pasos!")
            return
        
        visited_pages.append(current_title)

        current_path = find_first_link(parsed_page)
        if not current_path:
            print("¡Llegamos a un callejón sin salida!")
            return

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 roads_to_philosophy.py '<término de búsqueda>'")
        sys.exit(1)
    
    roads_to_philosophy(sys.argv[1])

if __name__ == "__main__":
    main()
