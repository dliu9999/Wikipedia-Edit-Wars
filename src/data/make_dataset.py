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

def lightdump_one_article(fp, article_name):
	'''
	Reads in lightdump data and returns a list of all the lines of a single article
	:param fp: input filepath
	:param article_name: name of the article to return
	:return: list of the lines of the corresponding article
	'''
	with open(fp) as fh:
	    article = []
	    found = False
	    for line in fh:
	        if found and (line[0] != '^'):
	            break
	        if found:
	            article.append(line.strip())
	        if line.strip() == article_name:
	            found = True
	if found == False:
		return 'Article not found'

	return article[::-1]