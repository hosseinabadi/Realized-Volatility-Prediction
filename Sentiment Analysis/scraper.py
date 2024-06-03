"""
    code which was run on EPFL's GPU
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import bs4


# From Wikipedia, download S&P500 stock data: tickers, stock name, GISC sector 
def get_sp500_indexes():
    
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    stocks = []
    tickers = []
    gisc_sectors = []

    # Import stock tickers
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        stock = row.findAll('td')[1].text
        gisc_sector = row.findAll('td')[2].text
        gisc_sectors.append(gisc_sector)
        tickers.append(ticker)
        stocks.append(stock)

    # Store stock tickers into a list
    tickers = [s.replace('\n', '') for s in tickers]
    stocks = [s.replace('\n', '') for s in stocks]
    gisc_sectors = [s.replace('\n', '') for s in gisc_sectors]
    
    # Lowercase
    lowercase_tickers = [ticker.lower() for ticker in tickers]
    
    # return lowercase_tickers, stocks, gisc_sectors
    return pd.DataFrame(data = {'ticker':lowercase_tickers, 'stock':stocks, 'gisc_sectors':gisc_sectors})


# dataframe with tickers, stock name, GISC sector
df_sp500 = get_sp500_indexes()


# create pandas DataFrame to store all data regarding stock
col = ['ticker', 'stock', 'gisc_sectors', 'date', 'title', 'source', 'link_source']
df = pd.DataFrame(columns=col)


number_pages = 1000


# list with all tickers
tickers = list( df_sp500['ticker'] )


for ticker in tickers:
    
    stock = df_sp500.loc[df_sp500['ticker']==ticker]['stock'].values[0]
    gisc_sector = df_sp500.loc[df_sp500['ticker']==ticker]['gisc_sectors'].values[0]
    print(stock)
    
    for i in range(1, number_pages+1):
        # define the url of the i-th page
        url = f'https://markets.businessinsider.com/news/{ticker}-stock?p={i}'

        # use BeautifulSoup
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        # get the articles from 
        articles = soup.find_all('div', class_='latest-news__story')

        # break after the last page
        if not articles:
            break

        for article in articles:
            title = article.find('a', class_='news-link').text
            date = article.find('time', class_='latest-news__date').get('datetime')
            link = article.find('a', class_ = 'news-link').get('href')
            source = article.find('span', class_= 'latest-news__source').text

            # complete link of the website
            if link[0] == '/':
                link = 'https://markets.businessinsider.com' + link
         

            df = pd.concat([pd.DataFrame([[ticker, stock, gisc_sector, date, title, source, link]], columns=col), df], ignore_index=True)



df.to_csv('/home/aolarite/SCRAPER/sp500_news.csv')