import re
import pandas as pd
from Classes.VoteDetail import VoteDetail
from vote_detail_repo import insert_vote_detail
from file_writer import write_to_file, split_text_by_all_caps_lines, split_text_by_general_order
from web_data_fetcher import get_house_doc_from_link
from word_doc_helper import doc_to_docx, get_word_document_text

# Word Document
# Requires converting the doc to docx

def vote_parser(doc_file):
    vote_details = list()
    docx_file = doc_to_docx(doc_file)
    text = get_word_document_text(docx_file)
    vote_detail = VoteDetail('', '', '', 0, 0, '', '', '', '', '')
    vote_detail.location = parse_journal_location(text.split('\n'))

    general_orders = split_text_by_general_order(text)

    for general_order in general_orders:
        parsed_text = general_order.split('\n')
        vote_detail.parse(parsed_text)
        vote_details.append(vote_detail)

    current_vote = None
    try:
        for vote_detail in vote_details:
            insert_vote_detail(vote_details)

    except Exception as error:
        print(f"An exception occurred save vote detail to the database {str(vote_detail)}:", error)  #



# https://chat.openai.com/share/e/9aec4b9b-5b41-4341-b5ff-db84a949b090
def parse_journal_location(journal: [str]):
    for row in journal:
        first_row = row.strip()  # Remove leading and trailing whitespace
        if first_row:  # Check if the row is not empty
            first_row_upper = first_row.upper()  # Convert to lowercase for case-insensitive comparison

            if "HOUSE" in first_row_upper:
                return "House Floor"
            elif "SENATE" in first_row_upper:
                return "Senate Floor"
            else:
                return first_row  # Return the full first line as default

    return "No non-empty row found in the journal."

# define vote_detail object here






# for t in general_orders:
#     print('------------NEW SECTION-------------------')
#     print(t)
#     print('------------END SECTION-------------------')
#     print(' ')
