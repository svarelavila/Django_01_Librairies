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
    Encuentra el primer enlace válido en el párrafo introductorio.
    """
    content_div = soup.find(id="mw-content-text")
    if not content_div:
        print("No content found in the article.")
        return None

    # Seleccionamos solo el primer párrafo
    first_paragraph = content_div.find("p", recursive=True)
    if not first_paragraph:
        print("No introductory paragraph found.")
        return None

    for link in first_paragraph.find_all("a", href=True):
        href_value = link.get("href", "")
        if href_value.startswith("/wiki/") and not (
            href_value.startswith("/wiki/Help:") or href_value.startswith("/wiki/Wikipedia:")
        ):
            # Ignorar enlaces en cursiva o entre paréntesis
            if link.find_parent("i") or link.find_parent("em"):
                continue
            parent_text = link.find_parent().text
            if "(" in parent_text and ")" in parent_text:
                continue
            return href_value.split("/")[-1]

    print("No valid links found in the introductory paragraph.")
    return None

def road_to_philosophy(page_title):
    """
    Itera a través de enlaces de Wikipedia hasta encontrar "Philosophy".
    """
    visited_pages = []
    while True:
        if page_title in visited_pages:
            print("It leads to an infinite loop!")
            break
        visited_pages.append(page_title)

        soup = fetch_html(page_title)
        current_title = soup.find("title").text.split(" - ")[0]
        print(current_title)

        if current_title == "Philosophy":
            print(f"{len(visited_pages)} roads from {visited_pages[0]} to Philosophy!")
            break

        next_link = find_first_link(soup)
        if not next_link:
            print("It leads to a dead end!")
            break

        page_title = next_link

def main():
    """
    Procesa los argumentos y ejecuta la lógica principal.
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 roads_to_philosophy.py <search_term>")

    search_term = sys.argv[1].replace(" ", "_")
    road_to_philosophy(search_term)

if __name__ == "__main__":
    main()
