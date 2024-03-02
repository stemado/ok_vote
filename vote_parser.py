from file_writer import write_to_file


from web_data_fetcher import get_all_page_content
from word_doc_helper import doc_to_docx, get_word_document_text

# Option 1: Text from Html
# bill_url = 'HB4327_votes.htm'
#
# context = get_all_page_content(bill_url)
#
# write_to_file('bill_' + bill_url + '.txt', context)
#
# print(context)

# Option 2: Word Document
# Requires converting the doc to docx
bill_url = '2023 HLeg Day61'
doc_file_path = r"C:\Users\sdoherty.ANTFARMLLC\Downloads\2023 HLeg Day61.doc"
docx_file = r"C:\Users\sdoherty.ANTFARMLLC\Downloads\2023 HLeg Day61.docx"

doc_to_docx(doc_file_path, docx_file)
text = get_word_document_text(docx_file)

print(text)

write_to_file('bill_' + bill_url + '.txt', text)