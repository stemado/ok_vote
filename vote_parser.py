import re
import pandas as pd
from Classes.VoteDetail import VoteDetail, extract_section_by_keyword
from file_writer import write_to_file
from ok_legislature_config import ok_file_sections
from word_doc_helper import doc_to_docx, get_word_document_text

def convert_to_dataframe(vote_details):
    # Convert each VoteDetail object into a dictionary and add it to a list
    data = [vars(vote_detail) for vote_detail in vote_details]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    return df

def split_text_by_all_caps_lines(text):
    # Split text by lines
    lines = text.split('\n')

    # Initialize a list to hold chunks of text
    chunks = []
    # Initialize a temporary string to hold the current chunk of text
    chunk = ""

    for line in lines:
        # If the line contains only capital letters (and possibly spaces)
        if line.isupper():
            # Add the current chunk to the chunks list
            chunks.append(chunk.strip())
            # Start new chunk with the all-caps line
            chunk = line + "\n"
        else:
            # Add the line to the chunk
            chunk += line + "\n"

    # Don't forget to add the last chunk
    chunks.append(chunk.strip())

    # Return the list of chunks, excluding any that are empty
    return [c for c in chunks if c]

# Option 2: Word Document
# Requires converting the doc to docx
# assumes we are iterating through all the links we've already stored
bill_url = '2023 HLeg Day61'
# doc_file_path = r"C:\Users\sdoherty.ANTFARMLLC\Downloads\2023 HLeg Day61.doc"
doc_file_path = r"/home/stephen/PycharmProjects/ok_vote/Journals/2023 HLeg Day16.docx"

# docx_file = doc_to_docx(doc_file_path)
text = get_word_document_text(doc_file_path)

# Split our text - we can use all caps as our section delimitter
split_text = split_text_by_all_caps_lines(text)
for t in split_text:
    print('------------NEW SECTION-------------------')
    print(t)
    print('------------END SECTION-------------------')

for section in split_text:

    result = extract_section_by_keyword(text, section)
    print('-------[NEW SECTION]: ' + section)
    print(result)
    print('-------[END SECTION]: ' + section)
    print('')




