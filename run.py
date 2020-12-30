#!/usr/bin/env python

import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/visualization')

from make_dataset import *
from build_features import *
from visualize import *

def main(targets):
    sql_config = json.load(open('config/data-db-params.json'))
    eda_config = json.load(open('config/eda-params.json'))
    all_config = json.load(open('config/all-params.json'))
    test_config = json.load(open('config/test-params.json'))
        
    if 'data-db' in targets:
        wiki_fp = sql_config['wiki_fp']
        db_fp = sql_config['db_outfp']
        ld_to_sql(wiki_fp, db_fp)
        
    if 'eda' in targets:
        outdir = eda_config['outdir']
        db_fp = eda_config['db_infp']
        articles_df = query_articles(db_fp)
        generate_stats(articles_df, outdir)
        
    if 'all' in targets:
        # assumes english wikipedia light dump was downloaded into data/raw as 'en-wiki.txt'
        lightdump_fp = all_config['data_fp']
        db_outfp = all_config['db_outfp']
        outdir = all_config['outdir']
        db_infp = all_config['db_fp']
        
        ld_to_sql(lightdump_fp, db_outfp)
        print('Created database from lightdump')
        
        articles_df = query_articles(db_infp)
        generate_stats(articles_df, outdir)
        print('Generated EDA plots on database')
        
    if 'test' in targets:
        lightdump_fp = test_config['data_fp']
        db_outfp = test_config['db_outfp']
        outdir = test_config['outdir']
        db_infp = test_config['db_fp']
        
        ld_to_sql(lightdump_fp, db_outfp)
        print('Created database from lightdump')
        
        articles_df = query_articles(db_infp)
        generate_stats(articles_df, outdir)
        print('Generated EDA plots on database')
        
    else:
        print('You did not pass in any arguments!')

if __name__ == '__main__':
    # run via:
    # python main.py data model
    targets = sys.argv[1:]
    main(targets)
