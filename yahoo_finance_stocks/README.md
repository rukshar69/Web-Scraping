## Yahoo Finance Stock Market Data Mining

### Data Retrieval

- This crawler uses Scrapy to crawl [finance.yahoo.com](finance.yahoo.com), and collects information on stocks in various sectors including healthcare, technology, energy, and more. It collects information such as the ticker, name, price, change in price, etc. of stocks and stores them.     

    - An example [data](https://github.com/rukshar69/Web-Scrapping/blob/main/yahoo_finance_stocks/stocks_info.csv) is added. The data is collected on the 1st August, 2023
    - In order to practise storing data in PostgreSQL and MongoDB in the local machine, [2 pipeline scripts](https://github.com/rukshar69/Web-Scrapping/tree/main/yahoo_finance_stocks/yahoo_finance_stocks/pipelines) are written along with necessary additions in [settings.py](https://github.com/rukshar69/Web-Scrapping/blob/main/yahoo_finance_stocks/yahoo_finance_stocks/settings.py)

### Streamlit App

- A [streamlit app](https://yahoo-finance-aug-1-23.streamlit.app/) is developed to visualize the collected data. The app has following visualizations:
    - Top 10 companies based on selected sector and numerical column('avg_vol_3_month', 'intraday_price', 'market_cap', 'pe_ratio_ttm', 'percent_change', 'price_change', 'volume')
    - Data distribution and boxplot for selected sector and numerical column
    - Donut chart showing % distribution of companies within a sector based on a numerical column divided into 6 ranges. 
    - Scatter plot for Market Cap vs. PE Ratio for a selected sector. The size of a point is determined by average volume
    - Scatter matrix showing pairwise relationships between numerical columns 
    - Violin Plot showing distribution of selected numerical column by sector
    - Bar Chart showing average volume by sector
    - Pie Chart showing distribution of Companies by sector
    - Heatmap representing the correlation matrix between numerical columns