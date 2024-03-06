import os

import requests
from urllib.parse import urljoin
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import urllib.parse
from Configuration.ok_legislative_config import base_house_doc_url


def get_house_txt_from_link(url):
    if url is None:
        full_url = urljoin(base_house_doc_url, url)
    else:
        full_url = url
    response = requests.get(full_url)
    response.raise_for_status()

    return response.text


def get_house_doc_from_link(url):
    # Get the user's home directory
    home_directory = os.path.expanduser('~')

    # Path to the Downloads directory (common for most OS)
    downloads_directory = os.path.join(home_directory, 'Downloads')

    # Extract file name from URL and decode it
    file_name = urllib.parse.unquote(url.split('/')[-1])

    # Full path where the file will be saved
    save_path = os.path.join(downloads_directory, file_name)
    # Download the file and save it
    try:
        urllib.request.urlretrieve(url, save_path)
        return save_path
    except Exception as e:
        return f"An error occurred: {e}"

def get_default_filename_from_url(url):
    # Extracting the last part of the URL
    file_name = url.split('/')[-1]
    # Decoding URL-encoded characters
    decoded_file_name = urllib.parse.unquote(file_name)
    return decoded_file_name

def extract_page_text(text, parser='html5lib'):
    soup = BeautifulSoup(text, parser)
    return soup



