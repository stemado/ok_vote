import requests
import html5lib
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_url(url):
    full_url = urljoin(base_url, url)
    response = requests.get(full_url)
    response.raise_for_status()

    return response.text

def extract_text(text):

    soup = BeautifulSoup(text, 'html5lib')

    return soup

def get_links(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        full_url = urljoin(base_url,href)
        links.append(full_url)
    return links



base_url = 'http://webserver1.lsb.state.ok.us/cf/2021-22%20SUPPORT%20DOCUMENTS/votes/House/'

base_page = fetch_url('')
base_text = extract_text(base_page)
all_links = get_links(base_text)

with(open('house_vote_urls.txt', 'w')) as f:
    for link in all_links:
        f.write(link + '\n')
    f.close()

for link in all_links:
    page_text = fetch_url(link)
    page_soup = extract_text(page_text)
    all_links += get_links(page_soup)

with open('votes.txt', 'w') as f:
    for link in all_links:
        f.write(link + '\n')
    f.close()

