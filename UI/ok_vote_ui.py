from urllib.parse import urljoin

import mechanicalsoup
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel

from Helpers.link_helper import extract_links
from Helpers.ok_website_helper import get_all_links, base_url
from Helpers.web_data_helper import get_house_doc_from_link, extract_page_text
from Services.Files.file_writer import write_links_to_file
from Services.VoteDetails.vote_parser import vote_parser


# https://chat.openai.com/share/e/b5a728ef-a904-4f82-bd8a-4f59a6465716
# Vardhan helped me with the logic for parsing the data
class OkVoteUi(QWidget):
    def __init__(self):
        super().__init__()
        self.single_doc_button = None
        self.text_box = None
        self.url_link_label = None
        self.url_label = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('OK Vote App')
        self.setGeometry(100, 100, 2400, 2400)  # Adjusted size for practicality

        # Layout
        layout = QVBoxLayout()

        # Label for the URL Text Box
        self.url_label = QLabel('<strong>URL to House Journal Doc File</strong>')
        layout.addWidget(self.url_label)
        layout.setAlignment(self.url_label, Qt.AlignCenter)
        self.url_link_label = QLabel('<strong>Copy and Paste Any .doc File Link From:</strong><br><br>http://webserver1.lsb.state.ok.us/cf/2021-22%20JOURNAL/House/<br><br>The Final File Is Saved To Your Downloads Folder As CSV')
        layout.addWidget(self.url_link_label)
        layout.setAlignment(self.url_link_label, Qt.AlignCenter)
        # URL For Doc File Text Box
        default_doc = 'http://webserver1.lsb.state.ok.us/cf/2021-22%20JOURNAL/House/2022%20HLeg%20Day22.doc'

        self.text_box = QLineEdit(self)
        self.text_box.setText(default_doc)
        self.text_box.setFixedHeight(50)
        self.text_box.setFixedWidth(1800)
        layout.addWidget(self.text_box)
        layout.setAlignment(self.text_box, Qt.AlignCenter)

        # Get Single Doc Url Button
        self.single_doc_button = QPushButton('Get Votes', self)
        self.single_doc_button.setStyleSheet('QPushButton {background-color: #FF0000; color: white;}')
        self.single_doc_button.setFixedHeight(180)
        self.single_doc_button.setFixedWidth(360)
        self.single_doc_button.clicked.connect(self.on_get_url_click)
        layout.addWidget(self.single_doc_button)
        layout.setAlignment(self.single_doc_button, Qt.AlignCenter)


        # Label for the URL Get All URLS Text Box
        self.house_url_label = QLabel('<strong>URL to House Journal Doc File</strong>')
        layout.addWidget(self.house_url_label)
        layout.setAlignment(self.house_url_label, Qt.AlignCenter)
        self.house_url_link_label = QLabel('<strong>Will Extract All .doc files from: http://webserver1.lsb.state.ok.us/cf/2021-22%20JOURNAL/House/<br><br>The Final Files Are Saved To Your Downloads Folder')
        layout.addWidget(self.house_url_link_label)
        layout.setAlignment(self.house_url_link_label, Qt.AlignCenter)

        # Get All Doc Urls Button
        self.process_all_urls_button = QPushButton('Process All House Docs', self)
        self.process_all_urls_button.setFixedHeight(180)
        self.process_all_urls_button.setFixedWidth(360)
        self.process_all_urls_button.clicked.connect(self.on_click)
        layout.addWidget(self.process_all_urls_button)
        layout.setAlignment(self.process_all_urls_button, Qt.AlignCenter)

        self.setLayout(layout)

    def on_click(self):
        # Action to perform when button is clicked
        _url = self.text_box.text()
        print(f"URL: {_url}")
        urls = self.return_all_oklahoma_files_locally(_url)
        urls.pop(0) # skip first because it is base url
        for url in urls:
            full_url = urljoin(base_url, url)
            print('Now parsing: ' + full_url)
            doc_save_path = self.return_oklahoma_file_locally(full_url)
            vote_parser(doc_save_path)

    def on_get_url_click(self):
        # Action to perform when button is clicked
        url = self.text_box.text()
        print(f"URL: {url}")
        doc_save_path = self.return_oklahoma_file_locally(url)
        vote_parser(doc_save_path)

    def return_oklahoma_file_locally(self, url):
        doc_save_path = get_house_doc_from_link(url)
        return doc_save_path

    # https://chat.openai.com/share/e/b1fb4092-15bc-41ec-b176-bc0020322db2
    def return_all_oklahoma_files_locally(self, url):

        # Ensure we are only fetching the root directory of House (or later Senate)
        if "JOURNAL/House" in url:
            url = 'http://webserver1.lsb.state.ok.us/cf/2021-22%20JOURNAL/House/'

        # Create a browser object
        browser = mechanicalsoup.Browser()

        # Fetch the webpage
        page = browser.get(url)

        # Parse the page
        soup = page.soup

        # Extract all <a> links
        all_links = [a.get('href') for a in soup.find_all('a') if a.get('href') is not None]
        print(all_links)
        # Write urls
        return all_links
        # write_links_to_file(all_links, 'tests/SampleOutput/house_vote_doc_urls.txt')
