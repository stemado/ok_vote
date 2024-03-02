import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

import PyPDF2
import pandas as pd
from bs4 import BeautifulSoup

# Reviewed by Vardhan Moduga

# File Selector using Tkinter
# https://chat.openai.com/share/e/41df872a-a2e0-453a-836e-b3f18eecc166
def select_file():
    filename = filedialog.askopenfilename()
    print(f'Selected file: {filename}')

    # Get the file extension
    _, file_extension = os.path.splitext(filename)

    # Check if the file extension is in the list of allowed extensions
    if file_extension not in ['.txt', '.pdf', '.html']:
        messagebox.showerror("Error", "Only .txt, .pdf, and .html files are allowed. Please select a valid file.")
    else:
        # For .txt files, save as .csv
        if file_extension == '.txt':
            new_filename = os.path.splitext(filename)[0] + '.csv'

            # df = pd.read_csv(filename, delimiter="\t")
            df = pd.read_csv(filename)

            # Use csv.QUOTE_ALL to wrap all fields in double quotes
            df.to_csv(new_filename, index=False, quoting=csv.QUOTE_ALL, sep=',')

            open_file(new_filename)

        # For .html files, remove tags and save as .txt
        elif file_extension == '.html':
            new_filename = os.path.splitext(filename)[0] + '.txt'
            with open(filename, 'r') as f:
                # from_encoding may be static for our OK use case, but ideally it should be dynamic
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text()
            with open(new_filename, 'w') as f:
                f.write(text)
            open_file(new_filename)

        # For .pdf files, save as .txt
        elif file_extension == '.pdf':
            new_filename = os.path.splitext(filename)[0] + '.txt'

            pdf_file_obj = open(filename, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(text)
            open_file(new_filename)


# https://chat.openai.com/share/e/5934fe1f-4eab-4f7f-b47d-f46464dbad1d
def open_file(file_path):
    try:

        # Windows uses backslashes, so we need to replace the forward slashes with backslashes
        # for the file path to be recognized by the operating system vis python os
        os_system_file_path_check = file_path.replace('/', '\\')

        # Check if the file exists
        if not os.path.exists(os_system_file_path_check):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Open the file using the default application
        os.startfile(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        messagebox.showerror("Error: File Not Found", f"The file {file_path} does not exist.")

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred while opening the file {file_path}.")

# Program starts here

root = tk.Tk()
root.geometry("300x300")
label = tk.Label(root, text="File Selector (.txt, .html, .pdf)")
label.pack()
button = tk.Button(root, text="Browse...", command=select_file)
button.pack()

root.mainloop()
