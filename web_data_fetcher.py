import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from ok_legislature_config import base_url


def get_all_page_content(url):
    full_url = urljoin(base_url, url)
    response = requests.get(full_url)
    response.raise_for_status()

    return response.text

def extract_page_text(text, parser='html5lib'):
    soup = BeautifulSoup(text, parser)
    return soup



