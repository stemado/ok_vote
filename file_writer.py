def write_links_to_file(links, filename):
    with open(filename, 'w') as f:
        for link in links:
            f.write(link + '\n')


def write_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
        f.write('\n')


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
