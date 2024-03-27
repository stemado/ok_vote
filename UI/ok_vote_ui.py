import csv
import os
from urllib.parse import urljoin

import mechanicalsoup
import requests
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel
from bs4 import BeautifulSoup

from Classes.member import Member
from Helpers.link_helper import extract_links
from Helpers.ok_website_helper import get_all_links, base_url
from Helpers.web_data_helper import get_house_doc_from_link, extract_page_text
from Services.Files.file_writer import write_links_to_file
from Services.VoteDetails.vote_parser import vote_parser, vote_parser_local


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

        # # Label for the URL Text Box
        # self.url_label = QLabel('<strong>URL to House Journal Doc File</strong>')
        # layout.addWidget(self.url_label)
        # layout.setAlignment(self.url_label, Qt.AlignCenter)
        # self.url_link_label = QLabel(
        #     '<strong>Copy and Paste Any .doc File Link From:</strong><br><br>http://webserver1.lsb.state.ok.us/cf/2021-22%20JOURNAL/House/<br><br>The Final File Is Saved To Your Downloads Folder As CSV')
        # layout.addWidget(self.url_link_label)
        # layout.setAlignment(self.url_link_label, Qt.AlignCenter)
        # # URL For Doc File Text Box
        # default_doc = 'http://webserver1.lsb.state.ok.us/cf/2021-22%20JOURNAL/House/2022%20HLeg%20Day22.doc'
        #
        # self.text_box = QLineEdit(self)
        # self.text_box.setText(default_doc)
        # self.text_box.setFixedHeight(50)
        # self.text_box.setFixedWidth(1800)
        # layout.addWidget(self.text_box)
        # layout.setAlignment(self.text_box, Qt.AlignCenter)
        #
        # # Get Single Doc Url Button
        # self.single_doc_button = QPushButton('Get Votes', self)
        # self.single_doc_button.setStyleSheet('QPushButton {background-color: #FF0000; color: white;}')
        # self.single_doc_button.setFixedHeight(180)
        # self.single_doc_button.setFixedWidth(360)
        # self.single_doc_button.clicked.connect(self.on_get_url_click)
        # layout.addWidget(self.single_doc_button)
        # layout.setAlignment(self.single_doc_button, Qt.AlignCenter)

        # Label for the URL Get All URLS Text Box
        # self.house_url_label = QLabel('<strong>URL to House Journal Doc File</strong>')
        # layout.addWidget(self.house_url_label)
        # layout.setAlignment(self.house_url_label, Qt.AlignCenter)
        # self.house_url_link_label = QLabel(
        #     '<strong>Will Extract All .doc files from: http://webserver1.lsb.state.ok.us/cf/2021-22%20JOURNAL/House/<br><br>The Final Files Are Saved To Your Downloads Folder')
        # layout.addWidget(self.house_url_link_label)
        # layout.setAlignment(self.house_url_link_label, Qt.AlignCenter)

        # Refresh House Members Button
        # self.refresh_members_button = QPushButton('Refresh House Members', self)
        # self.refresh_members_button.setFixedHeight(180)
        # self.refresh_members_button.setFixedWidth(360)
        # # Connect the button to the appropriate slot or function
        # self.refresh_members_button.clicked.connect(self.on_refresh_house_members)
        # layout.addWidget(self.refresh_members_button)
        # layout.setAlignment(self.refresh_members_button, Qt.AlignCenter)

        # Get All Doc Urls Button
        self.process_all_urls_button = QPushButton('Process All House Docs', self)
        self.process_all_urls_button.setFixedHeight(180)
        self.process_all_urls_button.setFixedWidth(360)
        self.process_all_urls_button.clicked.connect(self.process_vote_detail_locally)
        layout.addWidget(self.process_all_urls_button)
        layout.setAlignment(self.process_all_urls_button, Qt.AlignCenter)

        self.setLayout(layout)

    def on_click(self):
        QMessageBox.information(self, "Processing", "Processing all 58th and 59th House documents. This may take a while, but click 'OK' to continue")
        self.on_refresh_house_members()
        # store all house members
        # Action to perform when button is clicked
        urls = self.return_all_oklahoma_files_locally()
        urls.pop(0)  # skip first because it is base url
        for url in urls:
            full_url = urljoin(base_url, url)
            print('Now parsing: ' + full_url)
            doc_save_path = self.return_oklahoma_file_locally(full_url)
            vote_parser(doc_save_path)

        QMessageBox.information(self, "Done", "Finished. Check your Downloads Folder For Exported Members, VoteDetails, and VoteRollCall csv riles")

    def on_refresh_house_members(self):
        house_url = "https://www.okhouse.gov/representatives"

        # Parse HTML with BeautifulSoup
        # response = requests.get(house_url)
        # html_content = response.content.decode('utf-8')  # Decode binary response to string

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(house_members_content, 'html.parser')

        # Find all <article> tags
        articles = soup.find_all('article')
        # Extracting Title, Name, and District values
        members = []
        uniqueIdIndex = 1
        for article in articles:

            # Extract the title
            title_tag = article.find("p", class_="utility-font caption mb-1")
            title = title_tag.text.strip() if title_tag else None

            # Extract the name
            name_tag = article.find("p", class_="text-primary cta utility-font mb-1")
            name = name_tag.text.strip() if name_tag else None

            # Extract the district
            district_div = article.find("div", class_="flex flex-nowrap items-center")
            district = district_div['title'] if district_div and 'title' in district_div.attrs else None

            unique_index = uniqueIdIndex  # Placeholder value
            chamber = 'House'  # Placeholder value or logic to determine the chamber

            member = Member(unique_index, chamber, district, name, title)
            members.append(member)
            uniqueIdIndex = uniqueIdIndex + 1

        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        csv_file_path = os.path.join(downloads_folder, "members.csv")
        self.write_members_to_csv(members, csv_file_path)

        return members


    def write_members_to_csv(self, members, filename):
        """
        Write the unique members to a CSV file.

        :param members: List of unique Member objects.
        :param filename: Name of the CSV file.
        """
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write the header
                writer.writerow(['Unique Index', 'Chamber', 'District', 'Member Name', 'Title'])

                # Write member data
                for member in members:
                    writer.writerow([member.unique_index, member.chamber, member.district, member.member_name, member.title])

            print(f"Members data successfully written to {filename}")
        except Exception as e:
            print(f"An error occurred while writing to CSV: {e}")

    def get_unique_members(self, members):
        """
        Return only unique instances of members based on chamber, district, member_name, and title.

        :param members: List of Member objects.
        :return: List of unique Member objects.
        """
        unique_members = []
        seen = set()

        for member in members:
            identifier = (member.chamber, member.district, member.member_name, member.title)
            if identifier not in seen:
                seen.add(identifier)
                unique_members.append(member)

        return unique_members

    def fetch_all_senate_members(self):
        senate_url = "https://oksenate.gov/senators"

        # Fetch HTML content from the URL
        response = requests.get(senate_url)
        html_content = response.text

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all elements with class 'sSen__item'
        senator_items = soup.find_all("div", class_="sSen__item")

        # Extracting 'sSen_Dis' and 'sSen_Name' values
        senator_info = []
        for item in senator_items:
            district = item.find("span", class_="sSen__sDis").text.strip()
            name = item.find("span", class_="sSen__sName").text.strip()
            senator_info.append({"name": name, "district": district})

        return senator_info

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
    def return_all_oklahoma_files_locally(self):
        urls = []
        all_links = []
        # Ensure we are only fetching the root directory of House (or later Senate)
        urls = ['http://webserver1.lsb.state.ok.us/cf/2021-22%20JOURNAL/House/', 'http://webserver1.lsb.state.ok.us/cf/2023-24%20JOURNAL/House/']

        for url in urls:
            # Create a browser object
            browser = mechanicalsoup.Browser()

            # Fetch the webpage
            page = browser.get(url)

            # Parse the page
            soup = page.soup

            # Parse the page
            soup = page.soup

            # Extract all <a> links
            all_links.extend([a.get('href') for a in soup.find_all('a') if a.get('href') is not None])

            print(all_links)
            # Write urls

        return all_links

    def process_vote_detail_locally(self):
        files = get_docx_files(r"C:\Users\sdoherty\Downloads")
        for file in files:
            vote_parser_local(file)

def get_docx_files(directory):
    """
    Get all .docx files from the specified directory.

    :param directory: Path to the directory to search for .docx files.
    :return: List of .docx file paths.
    """
    docx_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.docx')]
    return docx_files
house_members_content =  """
    <article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Charles McCall"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Mc_Call_Charles_e33f5959b7.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Mc_Call_Charles_e33f5959b7.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Speaker of the House</p><p class="text-primary cta utility-font mb-1">Charles McCall</p><div class="flex flex-nowrap items-center" title="District 22"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 22</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Kyle Hilbert"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Hilbert_Kyle_1ad857b15c.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Hilbert_Kyle_1ad857b15c.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Speaker Pro Tempore</p><p class="text-primary cta utility-font mb-1">Kyle Hilbert</p><div class="flex flex-nowrap items-center" title="District 29"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 29</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Jon Echols"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Echols_Jon_f30d6d951a.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Echols_Jon_f30d6d951a.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Majority Floor Leader</p><p class="text-primary cta utility-font mb-1">Jon Echols</p><div class="flex flex-nowrap items-center" title="District 90"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 90</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on John Pfeiffer"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Pfeiffer_John_b6d9e128ad.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Pfeiffer_John_b6d9e128ad.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Deputy Floor Leader</p><p class="text-primary cta utility-font mb-1">John Pfeiffer</p><div class="flex flex-nowrap items-center" title="District 38"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 38</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Steve Bashore"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Bashore_Steve_6a8da04622.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Bashore_Steve_6a8da04622.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Deputy Floor Leader</p><p class="text-primary cta utility-font mb-1">Steve Bashore</p><div class="flex flex-nowrap items-center" title="District 7"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 7</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Mark McBride"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Mc_Bride_Mark_8e30415cfc.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Mc_Bride_Mark_8e30415cfc.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Floor Leader</p><p class="text-primary cta utility-font mb-1">Mark McBride</p><div class="flex flex-nowrap items-center" title="District 53"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 53</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Josh West"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_West_Josh_250829de04.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/West_Josh_250829de04.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Floor Leader</p><p class="text-primary cta utility-font mb-1">Josh West</p><div class="flex flex-nowrap items-center" title="District 5"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 5</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Kevin West"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_West_Kevin_fa81932eeb.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/West_Kevin_fa81932eeb.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Floor Leader</p><p class="text-primary cta utility-font mb-1">Kevin West</p><div class="flex flex-nowrap items-center" title="District 54"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 54</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Brian Hill"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Hill_Brian_07205f3747.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Hill_Brian_07205f3747.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Floor Leader</p><p class="text-primary cta utility-font mb-1">Brian Hill</p><div class="flex flex-nowrap items-center" title="District 47"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 47</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Tammy West"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_West_Tammy_fc38ad9d08.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/West_Tammy_fc38ad9d08.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Majority Leader</p><p class="text-primary cta utility-font mb-1">Tammy West</p><div class="flex flex-nowrap items-center" title="District 84"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 84</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Kevin Wallace"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Wallace_Kevin_9d1c5f65cd.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Wallace_Kevin_9d1c5f65cd.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Chair of the House Appropriations and Budget Committee</p><p class="text-primary cta utility-font mb-1">Kevin Wallace</p><div class="flex flex-nowrap items-center" title="District 32"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 32</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Stan May"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_May_Stan_bfa92e0195.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/May_Stan_bfa92e0195.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Majority Caucus Chair</p><p class="text-primary cta utility-font mb-1">Stan May</p><div class="flex flex-nowrap items-center" title="District 80"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 80</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Danny Williams"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Williams_Danny_1e529cde0a.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Williams_Danny_1e529cde0a.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Majority Caucus Vice Chair</p><p class="text-primary cta utility-font mb-1">Danny Williams</p><div class="flex flex-nowrap items-center" title="District 28"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 28</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Sherrie Conley"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Conley_Sherri_e0c9089345.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Conley_Sherri_e0c9089345.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Majority Caucus Secretary</p><p class="text-primary cta utility-font mb-1">Sherrie Conley</p><div class="flex flex-nowrap items-center" title="District 20"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 20</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Terry O'Donnell"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_O_Donnell_Terry_bb64e4877a.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/O_Donnell_Terry_bb64e4877a.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Majority Whip</p><p class="text-primary cta utility-font mb-1">Terry O'Donnell</p><div class="flex flex-nowrap items-center" title="District 23"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 23</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Nicole Miller"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Miller_Nicole_09d0b444e4.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Miller_Nicole_09d0b444e4.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Nicole Miller</p><div class="flex flex-nowrap items-center" title="District 82"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 82</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Mark Vancuren"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Vancuren_Mark_009023a3a7.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Vancuren_Mark_009023a3a7.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Mark Vancuren</p><div class="flex flex-nowrap items-center" title="District 74"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 74</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on David Hardin"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Hardin_David_d9a2de7aff.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Hardin_David_d9a2de7aff.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">David Hardin</p><div class="flex flex-nowrap items-center" title="District 86"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 86</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Jim Grego"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Grego_Jim_f730683998.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Grego_Jim_f730683998.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Jim Grego</p><div class="flex flex-nowrap items-center" title="District 17"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 17</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Rusty Cornwell"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Cornwell_Rusty_bb45545065.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Cornwell_Rusty_bb45545065.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Rusty Cornwell</p><div class="flex flex-nowrap items-center" title="District 6"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 6</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Eddy Dempsey"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Dempsey_Eddy_8f54da1753.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Dempsey_Eddy_8f54da1753.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Eddy Dempsey</p><div class="flex flex-nowrap items-center" title="District 1"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 1</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Mike Dobrinski"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Dobrinski_Mike_c10e4d4d1d.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Dobrinski_Mike_c10e4d4d1d.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Mike Dobrinski</p><div class="flex flex-nowrap items-center" title="District 59"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 59</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Dick Lowe"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Lowe_Dick_6c380e017b.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Lowe_Dick_6c380e017b.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Dick Lowe</p><div class="flex flex-nowrap items-center" title="District 56"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 56</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Preston Stinson"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Stinson_Preston_d0a68ee235.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Stinson_Preston_d0a68ee235.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Preston Stinson</p><div class="flex flex-nowrap items-center" title="District 96"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 96</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Eric Roberts"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Roberts_Eric_e9d78c6ce5.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Roberts_Eric_e9d78c6ce5.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Eric Roberts</p><div class="flex flex-nowrap items-center" title="District 83"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 83</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Denise Crosswhite Hader"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Crosswhite_Hader_Denise_0c73413b62.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Crosswhite_Hader_Denise_0c73413b62.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Denise Crosswhite Hader</p><div class="flex flex-nowrap items-center" title="District 41"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 41</p></div></div></div></article><article class="mt-6 md:px-2 md:w-1/3 lg:w-1/4 xl:w-1/5 w-full cursor-pointer" role="link" tabindex="0" aria-label="see details on Ross Ford"><div class="theme-shape theme-border relative shadow-md w-full h-full flex bg-white flex-row hover:shadow-xl transition-shadow md:flex-col min-w-[200px] overflow-hidden"><div class="relative w-[96px] bg-coolgray-200 md:w-full md:h-[290px]"><div class="bg-cover relative min-h-full min-w-full bg-top block md:hidden" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/thumbnail_Ford_Ross_4e537e5438.jpg&quot;);"></div><div class="bg-cover relative min-h-full min-w-full bg-top hidden md:block" style="background-image: url(&quot;https://dgbf0g52sf9l0.cloudfront.net/Ford_Ross_4e537e5438.jpg&quot;);"></div><div class="hidden md:block h-2.5 absolute inset-x-0 bottom-0 horizontal-gradient"></div></div><div class="flex-1 ig--member-info p-6 md:p-4"><p class="utility-font caption mb-1">Assistant Majority Whip</p><p class="text-primary cta utility-font mb-1">Ross Ford</p><div class="flex flex-nowrap items-center" title="District 76"><span class="rounded-full border-2 h-8 w-8 overflow-hidden flex shadow-md" style="border-color: rgb(143, 1, 27); background-color: rgb(143, 1, 27);"><p class="type-h6 text-white m-auto">R</p></span><p class="ml-2 utility-font label">District 76</p></div></div></div></article>
    """
