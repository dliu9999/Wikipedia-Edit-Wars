#to turn raw data into features for modeling
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import sqlite3

def mstat(article):
    '''
    Calculates the M-statistic for a list of edits from an article
    :param article: list of edits from an article
    :return: M-statistic for the article
    '''
    revert = 0
    revert_pairs = []

    #the list of mutual reverting pairs
    mutual_revert_pairs = []
    #the list of unique users among reverting pairs
    mutual_revert_users = []

    #a dictionary of user as key, and his number of edits as the value
    user_edits = {}

    #a dictionary with the line number (actual version number) as key, and the line label as value(i.e. line label is either the same as version number if not revert version, or equal to an older version number if it's a revert version)
    lineLabels = []
    #a dictionary with the line number (actual version number) as key, and the author of that line as value
    lineAuthors = []

    ### Helper Function ###
    def getLine(label, lineLabels):
        for line, ll in reversed(list(enumerate(lineLabels))):
            if lineLabels[line] == label:
                return line
    
    ### Read File ###
    for ln in article:
        parts = ln
        if len(parts) < 5:
            continue

        if parts[4] not in user_edits:
            user_edits[parts[4]] = 1
        else:
            user_edits[parts[4]] = user_edits[parts[4]] + 1
        if parts[2] == '1':
            revert += 1
            #the found line is the version i-1 equal to this version j, and the revert is assumed to be between the author of i, and j
            line = getLine(int(parts[3]), lineLabels)
            #ignore cases when i-1, and i are equal (consecutive versions)
            if line >= len(lineLabels)-1:
                continue
            revertedU = lineAuthors[line + 1]
            revertingU = parts[4]
            if revertedU == revertingU:
                continue
            pair = revertedU + "~!~" + revertingU
            if pair not in revert_pairs:
                revert_pairs.append(pair)
        lineLabels.append(int(parts[3]))
        lineAuthors.append(parts[4])

    ### Get Mutual ###
    for pair in revert_pairs:
        parts = pair.split("~!~")
        if parts[1] + "~!~" + parts[0] in revert_pairs:
            sorted_pair = ""
            if parts[0] < parts[1]:
                sorted_pair = parts[0] + "~!~" + parts[1]
            else:
                sorted_pair = parts[1] + "~!~" + parts[0]
                mutual_revert_pairs.append(sorted_pair)
            if parts[1] not in mutual_revert_users:
                mutual_revert_users.append(parts[1])
            if parts[0] not in mutual_revert_users:
                mutual_revert_users.append(parts[0])
        
        
    #calculating the score
    score = 0
    pairs = []
    for pair in list(set(mutual_revert_pairs)):
        parts = pair.split("~!~")
        u1 = parts[0]
        u2 = parts[1]
        if user_edits[u1]<user_edits[u2]:
            edit_min = user_edits[u1]
        else:
            edit_min = user_edits[u2]
        pairs.append(pair + ":" + str(edit_min))
        score += edit_min

    score *= len(mutual_revert_users)    
    
    return score

def ld_to_sql(ld_fp, db_fp, chunksize=5000000):
    '''
    Converts light dump from text file to tables in a SQLite database
    :param ld_fp: input light dump filepath
    :param db_fp: output database filepat
    :param chunksize: chunksize to hold in memory at a time before appending to SQL, default 50000000
    '''
    con = sqlite3.connect(db_fp)
    articles_cols = ['article_id', 'article_name', 'num_edits', 'm']
    edits_cols = ['article_id', 'timestamp', 'revert', 'edit_id', 'username']
    pd.DataFrame(columns=articles_cols).to_sql('articles', con, if_exists='replace', index=False)
    pd.DataFrame(columns=edits_cols).to_sql('edits', con, if_exists='replace', index=False)
    
    with open(ld_fp) as fh:
        articles_data = []  
        edits_data = []
        article_id = 0
        first = True                   # first article
        num_lines = 0                  # number of lines read
        num_edits = 0                  # number of edits in current article
        for line in fh:
            line = line.strip()
            if len(line) == 0:
                continue
            
            # append to sql
            if num_lines % chunksize == 0:
                articles_df = pd.DataFrame(articles_data, columns=articles_cols)
                edits_df = pd.DataFrame(edits_data, columns=edits_cols)
                articles_df.to_sql('articles', con, if_exists='append', index=False)
                edits_df.to_sql('edits', con, if_exists='append', index=False)
                articles_data = []                               # reset variables
                edits_data = []
                
            # article name line    
            if line[0] != '^':
                if first:              # check if first article
                    first = False
                else:                  # append to lists
                    current_article = current_article[::-1]
                    # calculate m
                    if num_edits < 3:
                        m = 0
                    else:
                        m = mstat(current_article)
                    articles_data.append([article_id, article_name, num_edits, m])
                    edits_data += current_article
                    article_id += 1
                # reset variables
                article_name = line
                current_article = []
                num_edits = 0
            
            # add to current article
            else:
                line = line.split(' ')
                current_article.append([article_id] + line)
                num_edits += 1
            num_lines += 1
        # final article
        current_article = current_article[::-1]
        # calculate m
        if num_edits < 3:
            m = 0
        else:
            m = mstat(current_article)
        articles_data.append([article_id, article_name, num_edits, m])
        edits_data += current_article
        
        # to sql
        articles_df = pd.DataFrame(articles_data, columns=articles_cols)
        edits_df = pd.DataFrame(edits_data, columns = edits_cols)
        articles_df.to_sql('articles', con, if_exists='append', index=False)
        edits_df.to_sql('edits', con, if_exists='append', index=False)
        
def query_articles(db_fp, N=None):
    '''
    Queries articles from the SQL database
    :param db_fp: input database filepath
    :param N: Number of articles to query, default all articles
    :return: dataframe of articles read in
    '''
    conn = sqlite3.connect(db_fp)
    if N:
        df =  pd.read_sql('select * from articles limit {0}'.format(N), conn)
    else:
        df =  pd.read_sql('select * from articles', conn)
    df['m'] = df['m'].astype(int)
    df['num_edits'] = df['num_edits'].astype(int)
    return df