#creating explanatory and results oriented visualizations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def counts_vs_m_distribution_plots(articles_df, outdir):
    '''
    Creates violin plots cross-checking top 20 edit counts versus high m
    :param articles_df: dataframe of articles from sql database
    :param outdir: output directory for plots
    :param N: number of edits and Ms to study
    '''
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    #top 20 edited articles
    top_20_edited = articles_df.sort_values('num_edits', ascending = False).head(20)

    #top 20 m-scores
    top_20_m = articles_df.sort_values('m', ascending = False).head(20)
    
    top_20_m['top 20 edited'] = top_20_m['article_name'].isin(top_20_edited['article_name'].tolist())
    sns.violinplot(data = top_20_m, x = 'top 20 edited', y = 'm', ax=axes[0])
    sns.violinplot(data = top_20_m, x = 'top 20 edited', y = 'num_edits', ax=axes[1])
    
    fig.savefig(os.path.join(outdir, 'counts_vs_m_violin.png'))
    
def nonzero_distribution_plots(articles_df, outdir):
    '''
    Creates a histogram and violin plots of the distributions of log(m) for articles with nonzero M
    :param articles_df: dataframe of articles from sql database
    :param outdir: output directory for plots
    '''
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # nonzero M
    nonzero = articles_df.copy().loc[articles_df['m'] > 0]
    nonzero['log_m'] = np.log(nonzero['m'])
    
    # plot histogram
    sns.distplot(nonzero['log_m'], ax=axes[0])
    
    # plot violin
    sns.violinplot(nonzero['log_m'], ax=axes[1])
    
    fig.savefig(os.path.join(outdir, 'nonzero_distribution.png'))
    
def m_div_counts_distribution_plots(articles_df, outdir):
    '''
    Creates a histogram and violin plots of the distributions of (log(m) / edit counts) for articles with nonzero M
    :param articles_df: dataframe of articles from sql database
    :param outdir: output directory for plots
    '''
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # nonzero M and edit counts
    articles_df = articles_df.copy()
    articles_df['log_m'] = np.log(articles_df['m'])
    non_x2 = articles_df.copy().loc[(articles_df['m'] > 0) & (articles_df['num_edits'] > 0)]
    non_x2['log_m/edits'] = non_x2['log_m']/non_x2['num_edits']
    
    # plot histogram
    sns.distplot(non_x2['log_m/edits'], ax=axes[0])
    
    # plot violin
    sns.violinplot(non_x2['log_m/edits'], ax=axes[1])
    
    fig.savefig(os.path.join(outdir, 'log_m_div_counts_distribution.png'))
    
def counts_vs_m_scatter_plot(articles_df, outdir):
    '''
    Creates a scatterplot comparing edit counts to M-stat for articles with nonzero M
    :param articles_df: dataframe of articles from sql database
    :param outdir: output directory for plot
    '''
    nonzero = articles_df.copy().loc[articles_df['m'] > 0]
    fig = sns.regplot(data = nonzero, x = 'num_edits', y = 'm').get_figure()
    fig.savefig(os.path.join(outdir, 'counts_vs_m_scatter.png'))
    
def descriptive_stats(articles_df, outdir):
    '''
    Descriptive statistic tables for top 20 and top 100 highest M-stat articles
    :param articles_df: dataframe of articles from sql database
    :param outdir: output directory for plot
    '''
    sorted_df = articles_df.sort_values('m', ascending = False)
    sorted_df.head(20).describe().to_csv(os.path.join(outdir, 'top_20_stats.csv'))
    sorted_df.head(100).describe().to_csv(os.path.join(outdir, 'top_100_stats.csv'))

    
def generate_stats(articles_df, outdir):
    '''
    Generates all EDA plots
    :param articles_df: dataframe of articles from sql database
    :param outdir: output directory for plot
    '''
    counts_vs_m_distribution_plots(articles_df, outdir)
    nonzero_distribution_plots(articles_df, outdir)
    m_div_counts_distribution_plots(articles_df, outdir)
    counts_vs_m_scatter_plot(articles_df, outdir)
    descriptive_stats(articles_df, outdir)
    return