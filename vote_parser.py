import re
import pandas as pd
from Classes.VoteDetail import VoteDetail
from file_writer import write_to_file, split_text_by_all_caps_lines, split_text_by_general_order
from word_doc_helper import doc_to_docx, get_word_document_text

# Word Document
# Requires converting the doc to docx
# assumes we are iterating through all the links we've already stored
# doc_file_path = r"C:\Users\sdoherty.ANTFARMLLC\Downloads\2023 HLeg Day61.doc"
doc_file_path = r"/home/stephen/PycharmProjects/ok_vote/Journals/2023 HLeg Day16.docx"

# docx_file = doc_to_docx(doc_file_path)
text = get_word_document_text(doc_file_path)

# Split our text - we can use all caps as our section delimiter

# split_text = split_text_by_all_caps_lines(text)

# define vote_detail object here
vote_detail = VoteDetail('', '', '', 0, 0, '', '', '', '', '', None, None)

# then we can extract the Date,Time and Location fromthe beginning of the document
# which will be the same for all bills that we parse from the given journal

# ToDo: Implement
vote_detail.date = parse_journal_date(text.split('\n'))
vote_detail.time = parse_journal_time(text.split('\n'))
vote_detail.location = parse_journal_location(text.split('\n'))

general_orders = split_text_by_general_order(text)

for general_order in general_orders:
    parsed_text = general_order.split('\n')
    vote_detail.parse(parsed_text)

# for t in general_orders:
#     print('------------NEW SECTION-------------------')
#     print(t)
#     print('------------END SECTION-------------------')
#     print(' ')





