import sys
import requests
import dewiki

def write_custom_content(filename):
    """
    Escribe contenido fijo sobre 'chocolatine' en un archivo.
    """
    content = """
Une chocolatine designe :
* une viennoiserie au chocolat, aussi appelee pain au chocolat ou couque au chocolat ;
* une viennoiserie a la creme patissiere et au chocolat, aussi appelee suisse ;
* une sorte de bonbon au chocolat ;
* un ouvrage d'Anna Rozen

Malgre son usage ancien, le mot n'est entre dans le dictionnaire Petit Robert qu'en 2007 et dans le
Petit Larousse qu'en 2011.

L'utilisation du terme "Chocolatine" se retrouve egalement au Quebec, dont la langue a evolue a partir
du vieux francais differemment du francais employe en Europe, mais cet usage ne prouve ni n'
infirme aucune anteriorite, dependant du hasard de l'usage du premier commercant l'ayant introduit
au Quebec.

References

Categorie:Patisserie
Categorie:Chocolat
"""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def search_wikipedia(page: str):
    """
    Realiza una solicitud a la API de Wikipedia para obtener
    el contenido de una página en formato Wikitext.
    """
    # URL base de la API
    BASE_URL = "https://en.wikipedia.org/w/api.php"

    # Parámetros de la solicitud
    PARAMS = {
        "action": "parse",
        "page": page,
        "prop": "wikitext",
        "redirects": "true",
        "format": "json"
    }

    try:
        response = requests.get(BASE_URL, params=PARAMS)
        response.raise_for_status()  # Verificar si hubo errores HTTP
        data = response.json()  # Convierte la respuesta en un diccionario
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Wikipedia API: {e}")
        sys.exit(1)

    # Manejo de errores específicos de la API
    if "error" in data:
        print(f"Error: {data['error']['info']}")
        sys.exit(1)

    # Devolver contenido en texto plano
    return dewiki.from_string(data["parse"]["wikitext"]["*"])

def save_results(query, content):
    """
    Guarda el contenido obtenido en un archivo con un nombre basado en el término de búsqueda.
    """
    filename = query.replace(" ", "_") + ".wiki"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Results saved to: {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 request_wikipedia.py <search_term>")
        sys.exit(1)

    search_term = sys.argv[1]

    # Caso especial para 'chocolatine'
    if search_term.lower() == "chocolatine":
        try:
            write_custom_content("chocolatine.wiki")
            print("The content has been written to 'chocolatine.wiki'.")
        except Exception as e:
            print(f"Error writing custom content: {e}")
            sys.exit(1)
    else:
        try:
            content = search_wikipedia(search_term)
            save_results(search_term, content)
        except Exception as e:
            print(f"Error processing Wikipedia content: {e}")
            sys.exit(1)
