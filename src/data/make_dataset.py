#making the dataset and things like that
import pandas as pd
from bs4 import BeautifulSoup

def read_local_xml(fp):
    '''
    Reads in an XML file and returns content as a list and a soup object
	:param fp: input filepath
	:return: tuple containing a list of lines and a soup object
    '''
    content = []
    # Read the XML file
    with open(fp, encoding='utf8') as file:
        # Read each line in the file, readlines() returns a list of lines
        content = file.readlines()
        # Combine the lines in the list into a string
        content_string = "".join(content)
        soup = BeautifulSoup(content_string, 'xml')
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

def xml_to_dfs(fp):
    '''
    Reads in an XML file and writes the data into DataFrames
    :param fp: input filepath
    :return: list of article titles, list of corresponding article lightdump data as DataFrame
    '''
    with open(fp, encoding='utf8') as file:
        contents = file.read()
        soup = BeautifulSoup(contents,'xml')
        
    titles = []
    dfs = []
    
    for x in soup.findAll('page'):
        page_text = x.findAll('text', string = True)
        text_hash = list(map(hash, page_text))
        count = 1

        contributor_list = x.findAll('contributor')

        timestamps = x.findAll('timestamp')

        df = pd.DataFrame(columns = ['timestamp', 'revert', 'editNumber', 'contributor', 'hash'])

        for i in range(len(text_hash)):
            rowInfo = pd.Series(index = ['timestamp', 'revert', 'editNumber', 'contributor', 'hash'],
                               dtype = 'object')

            rowInfo['timestamp'] = timestamps[i].text
            rowInfo['hash'] = text_hash[i]

            if text_hash[i] in text_hash[:i]:
                rowInfo['revert'] = 1
                rowInfo['editNumber'] = df[df['hash'] == text_hash[i]]['editNumber'].iloc[0]

            else:
                rowInfo['revert'] = 0
                rowInfo['editNumber'] = count
                count += 1

            try:
                rowInfo['contributor'] = contributor_list[i].find('username').text
            except:
                rowInfo['contributor'] = contributor_list[i].find('ip').text

            df = df.append(rowInfo, ignore_index = True)

        title = x.find('title').text.replace(' ', '_')
        
        titles.append(title)
        
        df = df.drop('hash', axis = 1)
        dfs.append(df)
        
    return titles, dfs

def create_line(row):
    '''
    Helper function to convert DataFrame into string values for lightdump conversion
    '''
    line = "^^^_"

    line = line + str(row['timestamp']) + " "
    line = line + str(row['revert']) + " "
    line = line + str(row['editNumber']) + " "
    line = line + str(row['contributor'])

    return line

def write_lightdump(titles, dfs, fp):
    '''
    Reads in a list of titles and corresponding DataFrames
    and writes the data into lightdump txt format
    :param titles: list of titles
    :param dfs: list of corresponding DataFrames
    :param fp: output txt file path
    '''
    for i in range(len(titles)):

        with open(fp, 'a') as file:
            starting_line = titles[i] + '\n'
            
            file.write(starting_line)
        
        with open(fp, 'a') as file:
            df = dfs[i].iloc[::-1].apply(create_line, axis = 1)

            df.to_csv(fp, mode = 'a', header = False, index = False)  
            
            file.write('\n')
        
#         print("Writing page completed.")

            
def lightdump_read_n(fp, n = 100):
    '''
	Reads in n lightdump pages and returns a list of all titles 
    read and their corresponding data as a DataFrame
	:param fp: input filepath
	:param n: number of articles to read
	:return: list of article titles, list of corresponding article lightdump data as DataFrame
	'''
    titles = []
    dataframes = []

    with open(fp) as file:
        df = pd.DataFrame(columns = ['timestamp', 'revert', 'revision_id', 'user'])
        page = 0
        for line in file:
            if '^^^_' not in line:
                title = line.strip('\n').strip()
                titles.append(title)

                if title != titles[page]:
                    page += 1
                    
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    
                    dataframes.append(df)
                    
                    df = pd.DataFrame(columns = ['timestamp', 'revert', 'revision_id', 'user'])

                    if page == n:
                        break
            else:
                data = line.strip("^^^_").strip('\n').split()
                row = pd.Series(dtype = 'object')

                row['timestamp'] = data[0]
                row['revert'] = int(data[1])
                row['revision_id'] = int(data[2])
                row['user'] = data[3]

                df = df.append(row, ignore_index = True)
    
    return titles, dataframes
