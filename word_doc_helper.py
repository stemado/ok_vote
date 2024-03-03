from docx import Document
import platform

def get_word_document_text(file):
    """
    Reads a Word document and returns the text content
    """
    doc = Document(file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def get_word_document_headers(file):
    """
    Reads a Word document and returns the headers
    """
    doc = Document(file)
    headers = []
    for para in doc.paragraphs:
        if para.style.name == 'Heading 1':
            headers.append(para.text)
    return headers


def doc_to_docx(doc_path):
    if platform.system() != 'Windows':
        print("This function is only available on Microsoft platforms.")
        return

    import comtypes.client

    if doc_path.endswith('.docx'):
        return

    # Initialize the Word application
    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False

    # create docx from doc
    docx_path = doc_path + "x"
    # Open the .doc file
    doc = word.Documents.Open(doc_path)

    # Save it as a .docx file
    doc.SaveAs(docx_path, FileFormat=16)  # 16 represents the wdFormatXMLDocument constant

    # Close Word
    doc.Close()
    word.Quit()

    return docx_path