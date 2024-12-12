import sys
import requests
from bs4 import BeautifulSoup

def get_wikipedia_url(search_term):
    base_url = "https://en.wikipedia.org/wiki/"
    search_term = search_term.replace(" ", "_")
    return base_url + search_term

def get_first_link(url, visited):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Unable to fetch the page.")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the main title
    title = soup.find('h1', {'id': 'firstHeading'}).text
    if title in visited:
        print("It leads to an infinite loop!")
        sys.exit(1)
    visited.add(title)

    # Find the first link in the introduction paragraph
    intro_paragraph = soup.find('p')
    if not intro_paragraph:
        print("It leads to a dead end!")
        sys.exit(1)

    links = intro_paragraph.find_all('a')
    for link in links:
        href = link.get('href')
        if href and href.startswith('/wiki/') and not href.startswith('/wiki/Help:') and not href.startswith('/wiki/Wikipedia:'):
            full_url = "https://en.wikipedia.org" + href
            return full_url

    # If no valid link is found in the first paragraph, try the next paragraphs
    for paragraph in soup.find_all('p'):
        links = paragraph.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith('/wiki/') and not href.startswith('/wiki/Help:') and not href.startswith('/wiki/Wikipedia:'):
                full_url = "https://en.wikipedia.org" + href
                return full_url

    print("It leads to a dead end!")
    sys.exit(1)

def main(search_term):
    url = get_wikipedia_url(search_term)
    visited = set()
    roads = []

    while True:
        url = get_first_link(url, visited)
        if "Philosophy" in url:
            roads.append("Philosophy")
            break
        roads.append(url.split('/')[-1].replace('_', ' '))

    print(f"{len(roads)} roads from {search_term} to philosophy!")
    for road in roads:
        print(road)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python roads_to_philosophy.py <search_term>")
        sys.exit(1)

    search_term = sys.argv[1]
    main(search_term)
