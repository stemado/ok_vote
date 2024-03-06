import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from Services.Files.file_writer import write_links_to_file
from Helpers.link_helper import extract_links
from Services.VoteDetails.vote_parser import vote_parser
from Helpers.web_data_helper import get_house_doc_from_link, extract_page_text

from UI.ok_vote_ui import OkVoteUi


def main():
    app = QApplication(sys.argv)
    ex = OkVoteUi()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

