import sys
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org/wiki/"

def fetch_html(page_title):
    """
    Obtiene el contenido HTML de una página de Wikipedia.
    """
    url = BASE_URL + page_title
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as e:
        sys.exit(f"Error fetching page '{page_title}': {e}")

def find_first_link(soup):
    """
    Encuentra el primer enlace válido en los párrafos directamente.
    """
    content_div = soup.find(id="mw-content-text")
    if not content_div:
        return None

    # Usar select para obtener enlaces en párrafos directamente
    links = content_div.select("p > a")
    for link in links:
        href_value = link.get("href", "")
        if href_value.startswith("/wiki/") and not (
            href_value.startswith("/wiki/Help:") or href_value.startswith("/wiki/Wikipedia:")
        ):
            return href_value.split("/")[-1]
    return None

def road_to_philosophy(page_title, pages_visited):
    """
    Navega recursivamente a través de enlaces hasta encontrar "Philosophy".
    """
    soup = fetch_html(page_title)
    current_title = soup.find(name="title").text.split(" - ")[0]

    # Verificar condiciones de finalización
    if current_title in pages_visited:
        sys.exit("It leads to an infinite loop!")
    if not soup.find(id="mw-content-text"):
        sys.exit("It leads to a dead end!")
    if current_title == "Philosophy":
        print(current_title)
        return

    # Imprimir el título actual y registrar
    print(current_title)
    pages_visited.append(current_title)

    # Encontrar el siguiente enlace
    next_link = find_first_link(soup)
    if not next_link:
        sys.exit("It leads to a dead end!")

    # Continuar con la siguiente página
    road_to_philosophy(next_link, pages_visited)

def main():
    """
    Procesa los argumentos y ejecuta la lógica principal.
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 roads_to_philosophy.py <search_term>")

    search_term = sys.argv[1].replace(" ", "_")
    pages_visited = []

    road_to_philosophy(search_term, pages_visited)
    print(f"{len(pages_visited)} roads from {search_term} to Philosophy")

if __name__ == "__main__":
    main()
