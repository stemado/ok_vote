import csv
import os

from Classes.vote_detail import VoteDetail
from Services.Files.file_writer import split_text_by_general_order, write_to_csv
from Helpers.word_doc_helper import doc_to_docx, get_word_document_text

# Word Document
# Requires converting the doc to docx


def vote_parser_local(docx_file):
    vote_details = list()
    text = get_word_document_text(docx_file)
    location = parse_journal_location(text.split('\n'))

    general_orders = split_text_by_general_order(text)

    # if general_orders is empty return
    if not general_orders:
        return

    unique_id = 1
    for general_order in general_orders:
        vote_detail = VoteDetail(unique_id, None, None, None, None, None, None, None, None, location)

        parsed_text = general_order.split('\n')
        vote_detail.parse(parsed_text)
        vote_details.append(vote_detail)
        unique_id = unique_id + 1

    try:
        # store the records to a database for easier future use
        write_vote_details_to_csv(vote_details)

        # for vote_detail in vote_details:
        #     if vote_detail.bill_number is not None and vote_detail.bill_number.startswith('[') and vote_detail.bill_number.endswith(']'):
        #         continue

    except Exception as error:
        print(f"An exception occurred save vote detail to the database {str(vote_detail)}:", error)  #

def vote_parser(doc_file):
    vote_details = list()
    docx_file = doc_to_docx(doc_file)
    text = get_word_document_text(docx_file)
    location = parse_journal_location(text.split('\n'))

    general_orders = split_text_by_general_order(text)

    # if general_orders is empty return
    if not general_orders:
        return

    unique_id = 1
    for general_order in general_orders:
        vote_detail = VoteDetail(unique_id, None, None, None, None, None, None, None, None, location)

        parsed_text = general_order.split('\n')
        vote_detail.parse(parsed_text)
        vote_details.append(vote_detail)
        unique_id = unique_id + 1

    try:
        # store the records to a database for easier future use
        write_vote_details_to_csv(vote_details)

        # for vote_detail in vote_details:
        #     if vote_detail.bill_number is not None and vote_detail.bill_number.startswith('[') and vote_detail.bill_number.endswith(']'):
        #         continue

    except Exception as error:
        print(f"An exception occurred save vote detail to the database {str(vote_detail)}:", error)  #

@staticmethod
def write_vote_details_to_csv(vote_details_records):
    """
    Append vote detail data to a CSV file. If the file doesn't exist, it creates it.

    :param vote_details: List of VoteDetail objects.
    :param filename: Name of the CSV file.
    """
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    vote_details_path = os.path.join(downloads_folder, "vote_details.csv")
    try:
        # Check if the file already exists to determine if we need to write headers
        file_exists = os.path.isfile(vote_details_path)

        with open(vote_details_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header only if the file didn't exist
            if not file_exists:
                writer.writerow(['Unique Index', 'Bill Number', 'Vote Type', 'Yea', 'Nay', 'CP', 'Excused', 'Vacant', 'Result', 'Location', 'Date', 'Time'])

            # Append vote detail data
            for detail in vote_details_records:
                writer.writerow([detail.unique_index, detail.bill_number, detail.vote_type, detail.yea, detail.nay, detail.cp, detail.excused, detail.vacant, detail.result, detail.location, detail.date, detail.time])

        print(f"Vote detail data successfully appended to {vote_details_path}")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

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
