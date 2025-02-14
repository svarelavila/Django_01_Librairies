import sys
import requests
from bs4 import BeautifulSoup

# URL base de Wikipedia para construir enlaces de artículos
WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/wiki/"


def road_to_philosophy(article_title, visited_articles):
    """
    Recursive function that navigates through Wikipedia links starting from
    a given article title to find the path to the 'Philosophy' article.

    Args:
    - article_title (str): The initial Wikipedia article title to start the search from.
    - visited_articles (list): A list to keep track of previously visited articles.

    Returns:
    - None: The function prints the path to 'Philosophy' in the terminal.

    Raises:
    - Prints error messages for dead ends, infinite loops, or network issues.
    """
    # Construir la URL del artículo a partir del título
    article_url = WIKIPEDIA_BASE_URL + article_title

    try:
        # Hacer una solicitud HTTP para obtener la página
        response = requests.get(article_url, allow_redirects=True)
        response.raise_for_status()  # Genera un error si la solicitud no es exitosa

        # Analizar el contenido de la página con BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extraer el título real del artículo (puede ser diferente al ingresado)
        article_title = soup.find(name="title").text.split(" - ")[0]

        # Obtener todos los enlaces dentro del contenido principal de la página
        links_in_content = soup.find(id="mw-content-text").select("p > a")

        # Si no hay enlaces en el contenido, es un callejón sin salida
        if len(links_in_content) == 0:
            sys.exit("It leads to a dead end!")

        # Si el artículo ya ha sido visitado antes, significa que estamos en un bucle infinito
        if article_title in visited_articles:
            sys.exit("It leads to an infinite loop!")

        # Imprimir el título del artículo actual en la terminal
        print(article_title)
        visited_articles.append(article_title)  # Agregar el artículo a la lista de visitados

        # Verificar si hemos llegado a la página "Philosophy"
        if article_title == "Philosophy":
            print(f"{len(visited_articles)} roads from {visited_articles[0]} to Philosophy!")
            return

        # Buscar el primer enlace válido dentro del contenido
        first_valid_link = None
        for link in links_in_content:
            link_href = link.get('href', '')  # Obtener la URL del enlace
            # Verificar que sea un enlace válido dentro de Wikipedia
            if link_href.startswith('/wiki/') and not (link_href.startswith('/wiki/Help:') or link_href.startswith('/wiki/Wikipedia:')):
                first_valid_link = link_href  # Guardar el primer enlace válido y salir del bucle
                break

        # Si no se encontró un enlace válido, terminamos la ejecución
        if not first_valid_link:
            sys.exit("It leads to a dead end!")

        # Extraer el título del siguiente artículo a visitar
        next_article = first_valid_link.split('/')[-1]

        # Llamar recursivamente a la función para continuar la navegación
        road_to_philosophy(next_article, visited_articles)

    except requests.exceptions.RequestException:
        # Manejo de errores en caso de problemas con la conexión a Wikipedia
        sys.exit("It leads to a dead end!")


def main():
    """
    Main function that processes the command-line argument and initiates
    the search for the path to 'Philosophy'.
    """
    # Verificar que el usuario ha ingresado exactamente un argumento
    if len(sys.argv) != 2:
        sys.exit("Pass in only one argument, use double quotes if necessary")

    # Reemplazar espacios en el término de búsqueda por guiones bajos (formato de Wikipedia)
    search_query = sys.argv[1].replace(' ', '_')

    # Lista para almacenar los artículos visitados
    visited_articles = []

    # Iniciar la navegación desde el artículo ingresado por el usuario
    road_to_philosophy(search_query, visited_articles)


# Punto de entrada del programa
if __name__ == "__main__":
    main()
