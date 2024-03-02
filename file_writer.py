def write_links_to_file(links, filename):
    with open(filename, 'w') as f:
        for link in links:
            f.write(link + '\n')


def write_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
        f.write('\n')
