from bs4 import BeautifulSoup
from services.services_config.serv_config import WIKI_URL, WIKI_DOGS_URL
from urllib.request import HTTPError, urlopen


def parser_breeds():
    """
    Open the link and gets
    structured code page. Searches
    for all tags <tr>, gets titles and links all dog breeds.
    """
    response = urlopen(WIKI_DOGS_URL)
    html_doc = response.read()
    breeds = []
    breeds_links = []
    soup = BeautifulSoup(html_doc, 'lxml')
    table = soup.find('table')
    for rows in table.find_all('tr')[1:-1]:
        column = rows.a.get('title')
        breeds.append(column)
        href = rows.a.get('href')
        links = (WIKI_URL + href)
        breeds_links.append(links)
    return breeds, breeds_links


def breeds_links_read(links):
    """
    Open all links of dog breeds. Reads the pages
    and searches all id='mw-content-text'. Gets
    text with this id.
    :return: list description of dog breeds
    """
    description_breeds = []
    for link in links:
        try:
            response = urlopen(link).read()
        except HTTPError:
            description_breeds.append('Not information')
        soup = BeautifulSoup(response, 'lxml')
        content_text = soup.find(id="mw-content-text")
        for content in content_text.find_all('p')[:1]:
            p = content.get_text()
            description_breeds.append(p)
    return description_breeds


def main():
    breeds, links = parser_breeds()
    description = breeds_links_read(links)
    print(breeds, description)

if __name__ == '__main__':
     main()
