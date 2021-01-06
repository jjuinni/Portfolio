# -*- coding: utf-8 -*-
"""
Parse webpages from finviz.com 
"""
import pandas as pd
import re
from bs4 import BeautifulSoup as soup
import requests
import sys

METRICS = ['Market Cap', 'Price', 'P/B', 'P/E', 'Forward P/E', 'P/S', 'PEG', 'P/FCF', 'Debt/Eq', 
           'EPS (ttm)', 'EPS next 5Y', 'Dividend %', 'Insider Own', 'ROE', 
           'ROI', 'ROA', 'Profit Margin', 'Shs Outstand', '52W Range', 'RSI (14)', 'Beta']

'''Finviz ticker quote page and screener page parser'''
class Parser(object):
    def __init__(self):
        self.base_url  = 'https://finviz.com/'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
    '''return: filter selected - sector or industry'''
    def get_filter(self):
        return self.filtere
'''
Ticker quote page parser (https://finviz.com/quote.ashx?t=)
'''    
class TickerParser(Parser):
    def __init__(self, ticker, filtere):
        Parser.__init__(self)
        self.ticker = ticker.lower()
        self.filtere = filtere.lower()
        self.serviceurl = self.base_url + 'quote.ashx?t=' + self.ticker
        self.screener_url = None
    '''
    Parse ticker quote page and get correspondent screener page according to filter selection
    return: screener_url
    '''
    def parse(self):
        try:
            html = requests.get(self.serviceurl, headers=self.headers).content
            initial_soup = soup(html, 'html.parser')
        except Exception:
            print(self.ticker.upper(), 'Ticker not found.')
            sys.exit()
        tags = initial_soup.find_all('a', {'class':'tab-link'})
        urls = []
        for tag in tags:
            urls.append(tag.get('href', None))
        screener_tag = None
        if self.filtere == 'sector':
            for url in urls:
                if re.match('.*=sec_(\S+)',  url) is not None:
                    idx = urls.index(url)
                    screener_tag = tags[idx]
            self.screener_url = self.base_url + screener_tag.get('href', None)
        elif self.filtere == 'industry':
            for url in urls:
                if re.match('.*=ind_(\S+)',  url) is not None:
                    idx = urls.index(url)
                    screener_tag = tags[idx]
            self.screener_url = self.base_url + screener_tag.get('href', None)
        return self.screener_url

''' 
Parse all pages from finviz screener (https://finviz.com/screener.ashx?v=111&f=)
'''
class ScreenerParser(Parser):
    def __init__(self, screener_url):
        Parser.__init__(self)
        self.screener_url = screener_url
        self.tickers_url = []
        self.tickers = [] # Will store all ticker symbols
        self.data = None
    '''
    Parse screener pages and store all tickers url.
    return: tickers_url: url of tickers
            tickers: name of tickers
    '''
    def parse(self):
        try:
            screener_html = requests.get(self.screener_url, headers=self.headers).content
            screener_soup = soup(screener_html, 'html.parser')
            print('Retrieving:', self.screener_url)
        except Exception:
            print ('Retrieving', self.screener_url , 'failed.')
        tags = screener_soup.find_all('a', {'class':'screener-link-primary'})
        for tag in tags:
            self.tickers_url.append(self.base_url + tag.get('href', None)) 
        #Store the tag of the next page to be parsed, if there is no other page nextpage_tage = None
        nextpage_tags = screener_soup.find_all('a', {'class':'tab-link'})
        nextpage_tag = None
        for tag in nextpage_tags:
            if tag.text == 'next':
                nextpage_tag = tag
                break
        screenerpage_tags = screener_soup.find_all('a', {'class':'screener-pages'})
        screener_pages = len(screenerpage_tags)
        #Count how many times to go inside loop 
        if screenerpage_tags == []:
            counter = 0 #there in only a single page on screener page
        else:
            counter = int(screenerpage_tags[-1].text)    
        nextpage_url = None
        e_count = 0 # Counter to break loop in case fails page retrieval often.
        
        #loop thru all screener pages to store tickers url 
        while(screener_pages != 0 and counter > 1):
            nextpage_url = self.base_url + nextpage_tag.get('href', None).replace(';','&')
            #Parse screener second to end page
            try: 
                nextpage_html = requests.get(nextpage_url, headers=self.headers).content
                nextpage_soup = soup(nextpage_html, 'html.parser')
                print('Retrieving:', nextpage_url)
            except Exception:
                print ('Retrieving', nextpage_url , 'failed.')
                e_count = e_count + 1
                if e_count > 4 : 
                    print('Try again with a good internet connection. Retrieval is incomplete.')
                    sys.exit()
           
            tags = nextpage_soup.find_all('a', {'class':'screener-link-primary'})
            #store tickers from current page
            for tag in tags:
                self.tickers_url.append(self.base_url + tag.get('href', None))
                self.tickers.append(tag.text)
            #update nextpage_tag so it refers to next screener page to be retrieved
            nextpage_tags = nextpage_soup.find_all('a', {'class':'tab-link'})
            for tag in nextpage_tags:
                if tag.text == 'next':
                    nextpage_tag = tag
            counter = counter - 1
        
        return self.tickers, self.tickers_url
    '''
    Parse tickers pages and stores financial ratios in a dataframe
    '''  
    def get_ratios(self):
        self.data = pd.DataFrame(index=self.tickers, columns=METRICS)
        e_count=0
        ticker_name = ''
        for url in self.tickers_url:
            #retrieve 
            try:
                ticker_html = requests.get(url, headers=self.headers).content
                ticker_soup = soup(ticker_html, 'html.parser')
                ticker_name = re.match('.*t=(\S+)&ty.*',  url).group(1)
                print('Retrieving:', url, '|| Ticker:', ticker_name)
            except Exception:
                print (ticker_name, 'not found.') 
                e_count = e_count + 1
                if e_count > 4 : 
                    print('Try again with a good internet connection. Retrieval is incomplete.')
                    sys.exit()
            for metric in METRICS:
                value = ticker_soup.find(text=metric).find_next('td',{'class':'snapshot-td2'}).text
                self.data.loc[ticker_name, metric] = value
        return self.data

