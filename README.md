# Wikipedia-Edit-Wars

Library code for computing controversiality statistics on Wikipedia articles. Replicating results of:

[Robert Sumi, Taha Yasseri, András Rung, András Kornai, and János Kertész. “Edit Wars in Wikipedia.” 2011 IEEE Third International Conference on Privacy, Security, Risk and Trust and 2011 IEEE Third International Conference on Social Computing.](https://arxiv.org/abs/1107.3689)

## Installation

- Install dependencies (Navigate to the directory you cloned to)
`pip install -r requirements.txt`

- Download data:
Download English light dump from http://wwm.phy.bme.hu/; save it in `data/raw` as `en-wiki.txt`

- Run (all) script:
`python run.py all` Calculates statistics on all Wikipedia articles, puts every statistic and edit into SQL database tables, then outputs EDA plots into `data/eda`

- Run (test) script:
`python run.py test` Runs the (all) script on test data found in `test/testdata`

## Usage
```python
import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/visualization')

from make_dataset import *
from build_features import *
from visualize import *
```
### XML Processing

`read_local_xml(xml_fp)` Read in an XML file and returns content as a list and a soup object

```python
read_local_xml(xml_fp) #returns tuple containing a list of lines and a soup object
```

`xml_to_dfs(xml_fp)` Read in an XML file and write the data into DataFrames

```python
xml_to_dfs(xml_fp) #returns tuple containing list of article titles and list of corresponding article lightdump data as DataFrame
```

`write_lightdump(titles, dfs, fp)` Read in a list of titles and corresponding DataFrames and write the data into lightdump txt format

```python
write_lightdump(titles, dfs, fp) #writes the data into lightdump txt file to filepath
```

### Light Dump Processing

`lightdump_read_n(ld_fp, n=n)` Read in n lightdump pages and returns a list of all titles read and their corresponding data as a DataFrame

```python
lightdump_read_n(ld_fp, n=n) #returns tuple containing a list of article titles and a list of corresponding article lightdump data as DataFrames
```

`lightdump_one_article(fp, article_name)` Reads in lightdump data and returns a list of all the lines of a single article

```python
lightdump_one_article(fp, article_name) #returns a list of the lines of the corresponding article
```

### M-Stat and Database Building

`mstat(article)` Read in article and calculate the M-statistic for a list of edits from an article

```python
mstat(article) #returns M-statistic for the article
```

`ld_to_sql(ld_fp, db_fp, chunksize=5000000` Converts light dump from text file to tables in a SQLite database

```python
ld_to_sql(ld_fp, db_fp, chunksize=5000000) #Writes light dump data to SQLite database
```

`query_articles(db_fp, N=None)` Queries articles from the SQLite database

```python
query_articles(db_fp, N=None) #SQLite database data as DataFrame
```

### Visualization

`counts_vs_m_distribution_plots(articles_df, outdir)` Creates violin plots cross-checking top 20 edit counts versus high m

```python
counts_vs_m_distribution_plots(articles_df, outdir) #creates and saves violin plot, as described above, as figure
```

`nonzero_distribution_plots(articles_df, outdir)` Creates a histogram and violin plots of the distributions of log(m) for articles with nonzero M

```python
onzero_distribution_plots(articles_df, outdir) #creates and saves histogram and violin plots, as described above, as figure
```

`m_div_counts_distribution_plots(articles_df, outdir)` Creates a histogram and violin plots of the distributions of (log(m) / edit counts) for articles with nonzero M

```python
m_div_counts_distribution_plots(articles_df, outdir) #creates and saves histogram and violin plots, as described above, as figure
```

`counts_vs_m_scatter_plot(articles_df, outdir)` Creates a scatterplot comparing edit counts to M-stat for articles with nonzero M

```python
counts_vs_m_scatter_plot(articles_df, outdir) #creates and saves scatterplot, as described above, as figure
```

`descriptive_stats(articles_df, outdir)` Descriptive statistic tables for top 20 and top 100 highest M-stat articles

```python
descriptive_stats(articles_df, outdir) #creates descriptive statistic tables, as described above, as csv
```

`generate_stats(articles_df, outdir)` Generates all EDA plots

```python
generate_stats(articles_df, outdir) #plots and saves all plots in visualize.py 
```

## Contributors

Casey Duong (ck-duong), Darren Liu (dliu9999)
