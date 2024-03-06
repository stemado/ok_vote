import csv
import os

import pandas as pd


def write_links_to_file(links, filename):
    with open(filename, 'w') as f:
        for link in links:
            f.write(link + '\n')


def write_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
        f.write('\n')

# https://chat.openai.com/share/e/9aec4b9b-5b41-4341-b5ff-db84a949b090
def write_to_csv(filename, content):

    # Convert to DataFrame
    df = pd.DataFrame(content)
    # Write to CSV
    df.to_csv(filename, index=False)



def split_text_by_general_order(text):
    # Split text by lines
    lines = text.split('\n')

    # Initialize a list to hold chunks of text
    chunks = []
    # Initialize a temporary string to hold the current chunk of text
    chunk = ""
    # Flag to indicate if we are inside a GENERAL ORDER section
    inside_general_order = False

    for line in lines:
        # Check if the line is "GENERAL ORDER"
        if line.strip() == "GENERAL ORDER":
            if inside_general_order:
                # Add the current chunk to the chunks list and start a new chunk
                chunks.append(chunk.strip())
                chunk = line + "\n"
            else:
                # Start new chunk with GENERAL ORDER
                chunk = line + "\n"
                inside_general_order = True
        else:
            if inside_general_order:
                # Add the line to the chunk
                chunk += line + "\n"

    # Add the last chunk if it exists
    if inside_general_order:
        chunks.append(chunk.strip())

    return chunks


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

    return [c for c in chunks if c]
