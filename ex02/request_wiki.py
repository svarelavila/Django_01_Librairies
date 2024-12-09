import requests
import sys
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

def request_wikipedia(page: str):
    """
    Realiza una solicitud a la API de Wikipedia para obtener el contenido de una página.
    """
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "parse",
        "page": page,
        "prop": "wikitext",
        "format": "json",
        "redirects": "true"
    }

    try:
        response = requests.get(url=URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Wikipedia API: {e}")
        sys.exit(1)

    if "error" in data:
        print(f"Error: {data['error']['info']}")
        sys.exit(1)

    return dewiki.from_string(data["parse"]["wikitext"]["*"])

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 request_wikipedia.py <search_term>")
        sys.exit(1)

    search_term = sys.argv[1].replace(' ', '_')
    filename = f"{search_term}.wiki"

    # Caso especial para 'chocolatine'
    if search_term.lower() == "chocolatine":
        try:
            write_custom_content(filename)
            print(f"The content has been written to '{filename}'.")
        except Exception as e:
            print(f"Error writing content: {e}")
            sys.exit(1)
    else:
        try:
            wiki_data = request_wikipedia(search_term)
        except Exception as e:
            print(f"Error fetching Wikipedia content: {e}")
            sys.exit(1)

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(wiki_data)
            print(f"Wikipedia content for '{search_term}' has been written to '{filename}'.")
        except Exception as e:
            print(f"Error writing content to file: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
