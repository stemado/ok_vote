import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from file_writer import write_links_to_file
from link_helper import extract_links
from vote_parser import vote_parser
from web_data_fetcher import get_house_doc_from_link, extract_page_text
from PyQt5.QtWidgets import QApplication, QWidget, QLabel



class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('OK Vote App')
        self.setGeometry(100, 100, 2400, 2400)  # Adjusted size for practicality

        # Layout
        layout = QVBoxLayout()

        # Label for the URL Text Box
        self.urlLabel = QLabel('URL to Doc File:')
        layout.addWidget(self.urlLabel)
        layout.setAlignment(self.urlLabel, Qt.AlignCenter)

        # URL For Doc File Text Box
        self.textBox = QLineEdit(self)
        self.textBox.setText('http://webserver1.lsb.state.ok.us/cf/2023-24%20JOURNAL/House/2023%20HLeg%20Day%201.doc')
        self.textBox.setFixedHeight(50)
        self.textBox.setFixedWidth(1800)
        layout.addWidget(self.textBox)
        layout.setAlignment(self.textBox, Qt.AlignCenter)

        # Get Single Doc Url Button
        self.single_doc_button = QPushButton('Get Doc', self)
        self.single_doc_button.setFixedHeight(180)
        self.single_doc_button.setFixedWidth(360)
        self.single_doc_button.clicked.connect(self.on_get_url_click)
        layout.addWidget(self.single_doc_button)
        layout.setAlignment(self.single_doc_button, Qt.AlignCenter)

        # Get All Doc Urls Button
        # self.button = QPushButton('Update All Doc Urls', self)
        # self.button.setFixedHeight(40)
        # self.button.clicked.connect(self.on_click)
        # layout.addWidget(self.button)
        # layout.setAlignment(self.button, Qt.AlignCenter)

        self.setLayout(layout)

    def on_click(self):
        # Action to perform when button is clicked
        entered_text = self.textBox.text()
        print(f"Submitted Text: {entered_text}")
        self.return_all_oklahoma_files_locally()

    def on_get_url_click(self):
        # Action to perform when button is clicked
        url = self.textBox.text()
        print(f"Submitted Url: {url}")
        doc_save_path = self.return_oklahoma_file_locally(url)
        vote_parser(doc_save_path)

    def return_oklahoma_file_locally(self, url):
        doc_save_path = get_house_doc_from_link(url)
        return doc_save_path

    def return_all_oklahoma_files_locally(self):
        base_url = get_house_doc_from_link('')
        page_content = extract_page_text(base_url)
        all_links = extract_links(page_content)

        # Skip first link since it is base url
        all_links.pop(0)
        # Write urls
        write_links_to_file(all_links, 'house_vote_doc_urls.txt')

def main():
    app = QApplication(sys.argv)
    ex = SimpleApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# https://chat.openai.com/share/e/b5a728ef-a904-4f82-bd8a-4f59a6465716





