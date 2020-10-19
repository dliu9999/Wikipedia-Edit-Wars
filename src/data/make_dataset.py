from bs4 import BeautifulSoup as bs

def read_local_xml(fp):
    '''Reads in an XML file and returns content as a list and a soup object'''
    content = []
    # Read the XML file
    with open(fp, encoding='utf8') as file:
        # Read each line in the file, readlines() returns a list of lines
        content = file.readlines()
        # Combine the lines in the list into a string
        content_string = "".join(content)
        soup = bs(content_string, 'xml')
    return content, soup