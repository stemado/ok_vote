from Classes.vote_detail import VoteDetail
from Database.db_config import DbContext
from Services.Files.file_writer import split_text_by_general_order, write_to_csv
from Helpers.word_doc_helper import doc_to_docx, get_word_document_text

# Word Document
# Requires converting the doc to docx

def vote_parser(doc_file):
    db_context = DbContext()
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
        unique_id += 1

    try:
        # store the records to a database for easier future use
        for vote_detail in vote_details:
            if vote_detail.bill_number is not None and vote_detail.bill_number.startswith('[') and vote_detail.bill_number.endswith(']'):
                continue

            db_context.insert_vote_detail(vote_detail.to_dict())

        # Convert to dict for saving
        dict_content = [item.to_dict() for item in vote_details]


        # Ignoring this section because I am going to pull the records from the table and store as csv from there
        # new_extension = ".csv"
        # new_filename = docx_file.rsplit('.', 1)[0] + new_extension
        # But for now, just write the vote_details to a csv
        # write_to_csv(new_filename, dict_content)

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
