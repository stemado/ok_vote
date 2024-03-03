import re
import pandas as pd
from Classes.VoteDetail import VoteDetail, extract_section_by_keyword
from file_writer import write_to_file, split_text_by_all_caps_lines
from word_doc_helper import doc_to_docx, get_word_document_text

# Word Document
# Requires converting the doc to docx
# assumes we are iterating through all the links we've already stored
# doc_file_path = r"C:\Users\sdoherty.ANTFARMLLC\Downloads\2023 HLeg Day61.doc"
doc_file_path = r"/home/stephen/PycharmProjects/ok_vote/Journals/2023 HLeg Day16.docx"

# docx_file = doc_to_docx(doc_file_path)
text = get_word_document_text(doc_file_path)

# Split our text - we can use all caps as our section delimiter

split_text = split_text_by_all_caps_lines(text)
for t in split_text:
    print('------------NEW SECTION-------------------')
    print(t)
    print('------------END SECTION-------------------')
    print(' ')

for section in split_text:

    result = extract_section_by_keyword(text, section)
    print('-------[NEW SECTION]: ' + section)
    print(result)
    print('-------[END SECTION]: ' + section)
    print(' ')




