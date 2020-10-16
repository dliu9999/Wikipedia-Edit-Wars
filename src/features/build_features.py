from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

def soup_to_df(soup):
	'''Converts a soup object to a dataframe'''
	pages = soup.findAll('page')
	lst = []
	for page in pages:
	    title = page.title.text
	    for revision in page.findAll('revision'):
	        try:
	            timestamp = revision.timestamp.text
	        except:
	            timestamp = np.NaN
	        try:
	            username = revision.username.text
	        except:
	            username = np.NaN
	        try:    
	            comment = revision.comment.text
	        except:
	            comment = np.NaN
	        try:
	            text_byte = revision.format.next_sibling.next_sibling.text
	        except:
	            text_byte = np.NaN
	        lst.append([title, timestamp, username, comment, text_byte])
	df = pd.DataFrame(lst, columns=['title', 'timestamp', 'username', 'comment', 'text byte'])
	df['timestamp'] = pd.to_datetime(df['timestamp'])
	return df