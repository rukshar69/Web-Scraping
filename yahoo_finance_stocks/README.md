## Yahoo Finance Stock Market Data Mining

### Data Retrieval

- This crawler uses Scrapy to crawl [finance.yahoo.com](finance.yahoo.com), and collects information on stocks in various sectors including healthcare, technology, energy, and more. It collects information such as the ticker, name, price, change in price, etc. of stocks and stores them.     

    - An example [data](https://github.com/rukshar69/Web-Scrapping/blob/main/yahoo_finance_stocks/stocks_info.csv) is added. The data is collected on the 1st August, 2023
    - In order to practise storing data in PostgreSQL and MongoDB in the local machine, [2 pipeline scripts](https://github.com/rukshar69/Web-Scrapping/tree/main/yahoo_finance_stocks/yahoo_finance_stocks/pipelines) are written along with necessary additions in [settings.py](https://github.com/rukshar69/Web-Scrapping/blob/main/yahoo_finance_stocks/yahoo_finance_stocks/settings.py)