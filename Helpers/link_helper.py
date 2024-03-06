from urllib.parse import urljoin

from Configuration.ok_legislative_config import base_house_support_docs_url
from Helpers.web_data_helper import get_house_doc_from_link, extract_page_text


def process_links(links):
    all_extracted_links = []
    for link in links:
        page_text = get_house_doc_from_link(link)
        page_soup = extract_page_text(page_text)
        extracted_links = extract_links(page_soup)
        all_extracted_links.extend(extracted_links)
    return all_extracted_links

def extract_links(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        full_url = urljoin(base_house_support_docs_url, href)
        links.append(full_url)
    return links
