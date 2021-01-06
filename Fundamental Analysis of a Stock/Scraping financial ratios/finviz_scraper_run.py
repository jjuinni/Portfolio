# -*- coding: utf-8 -*-
"""
This script scrapes pre-defined metrics data of a chosen ticker and 
it's sector or industry remaining tickers data.

Website scrapped: Finviz (https://finviz.com/)

After successfully retrieving the web data, the data will be treated 
to an all numerical dataframe which will be used to manipulate data 
and do valuation analysis of a stock to calculate it's fair value 
according to DCF or Sticker Price & Margin of Safety method.

Finally the data is stored in a database from which the data can be explored
in many different ways.
"""
from finviz_scraper import TickerParser, ScreenerParser
from finviz_scraper_data import clean_data, CalculateValue
import pandas as pd
import sqlite3
import sys

#User input
print("Calculate your Stock Fair Value per Share")
ticker = input("Ticker name or press Enter to quit:")   
filtere = input("Filter by 'sector' or 'industry'?")
if len(ticker) < 1 or len(filtere) < 1: sys.exit()

#Parse inputted ticker page
tickerscreen = TickerParser(ticker, filtere)
screener_url = tickerscreen.parse()

#Parse screener page
screener = ScreenerParser(screener_url)
tickers, tickers_url = screener.parse()

#Parse all ticker pages and store data
data = screener.get_ratios()
#All numerical values dataframe
data = clean_data(data)

intrinsic_value = CalculateValue(data)
#'Sticker Price'(Fair Value of a Stock) and 'Margin of Safety' valuation method
fairvalue_1, buyvalue_1 = intrinsic_value.sp_valuation(years=10, rate_return=0.15, margin_safety=0.6666)
fairvalue_2, buyvalue_2 = intrinsic_value.sp_valuation(years=10, rate_return=0.15, margin_safety=0.5)
#Discounted cash flow valuation method
enterprise_value_1, dcf_value_1 = intrinsic_value.simple_dcf_valuation(years=10, rate_discount=0.1, tv_multiplier=10)
enterprise_value_2, dcf_value_2 = intrinsic_value.simple_dcf_valuation(years=10, rate_discount=0.1, tv_multiplier=15)

valuation = pd.DataFrame({'DCF EV(B) (tv=10)': enterprise_value_1, 
                          'DCF Value (tv=10': dcf_value_1,
                          'DCF EV(B) (tv=15)': enterprise_value_2, 
                          'DCF Value (tv=15)': dcf_value_2,
                          'SP Fair Value': fairvalue_1, #same as fairvalue_1, so I'll print just one of them
                          'SP Buy Value (ms=0.66)': buyvalue_1,
                          'SP Buy Value (ms=0.5)': buyvalue_2})
results = pd.concat([valuation, data], axis=1)

#store in database file
conn = sqlite3.connect("stocks_db.sqlite")
cur = conn.cursor() 
results.to_sql("Fundamentals", conn, if_exists='replace', index = True)
conn.commit()
cur.close()
