'''
This script contains the visualization functions 
used to on the Fundamental Analysis of a stock Notebook
'''
import pandas as pd
import sqlite3 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import numpy as np

cnx = sqlite3.connect('200902_ind_consumer_electronics_db.sqlite')
conn = sqlite3.connect('200902_sec_tech_db.sqlite')
ind = pd.read_sql_query("SELECT * FROM Fundamentals", cnx)
sec = pd.read_sql_query("SELECT * FROM Fundamentals", conn)

'''
Draws a football field chart 
param: ticker(string)
       df(dataframe)
return: bar chart(pyplot) with price tags
'''
def valuation(ticker, db):
    ticker = ticker.upper()
    #values needed to plot footbaal field chart
    db['Range diff'] = db['52W Range High'] - db['52W Range Low']
    db['DCF ms=0.5'] = db['DCF Value (tv=10']*0.5 #lowest DCF value * lowest margin
    db['DCF Value diff'] = db['DCF Value (tv=15)'] - db['DCF ms=0.5']
    db['SP diff'] = db['SP Fair Value'] - db['SP Buy Value (ms=0.5)']
    
    row = db.loc[db['index'] == ticker].iloc[0]
    
    df = pd.DataFrame(columns=['low', 'diff', 'high'], index=['DCF Value', 'SP Value', 'Range 52W H/L'])
    df.iloc[0]['low'] = row['DCF ms=0.5'] #lowest possible buy value
    df.iloc[0]['diff'] = row['DCF Value diff'] #what I want to see
    df.iloc[0]['high'] = row['DCF Value (tv=15)'] #best fair value
    df.iloc[1]['low'] = row['SP Buy Value (ms=0.5)']
    df.iloc[1]['diff'] = row['SP diff']
    df.iloc[1]['high'] = row['SP Fair Value']
    df.iloc[2]['low'] = row['52W Range Low']
    df.iloc[2]['diff'] = row['Range diff']
    df.iloc[2]['high'] = row['52W Range High']
    price= row['Price'] #current price of stock

    fig, ax=plt.subplots()
    df.plot(kind='bar', stacked=True, color=['w','burlywood','w'], legend=False, ax=ax)
    ax.axhline(y=price, color='r', linestyle='dotted')
    plt.title('Valuation summary, Ticker: ' + ticker)
    plt.ylabel('Price ($)')
    plt.xticks(rotation='horizontal')
    plt.ylim(min(df['low'])-30, max(df['high'])+100)

    # current price line labeling
    trans = transforms.blended_transform_factory(ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,price, "{:.0f}".format(price), color="red", transform=trans, ha="right", va="center")
    
    # setting up label position
    #Note: try (del str) in case 'str' is not callable happens
    labels_1 = []
    labels_2 = []
    for j in df.columns:
        for i in df.index:
            label = "$" + str(round(df.loc[i][j], 2))
            labels_1.append(label)
            labels_2.append(label)

    patches = ax.patches
    #lower label position
    for i in range(3, len(labels_1)):
        labels_1[i] = ''
        #example: labels_1 = ['$63.23', '$33.53', '$51.06', '', '', '', '', '', '']
    for label, rect in zip(labels_1, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width/2., y + height/1.1, label, ha='center', va='top')
    #upper label position
    for i in range(len(labels_2)-3):
        labels_2[i] = ''
        #example: labels_2 = ['', '', '', '', '', '', '$78.88', '$44.7', '$134.8']
    for label, rect in zip(labels_2, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width/2., y + height/14, label, ha='center', va='bottom')

    return plt

'''
Graphs constant EPS annual growth for a period of years.
param: start_year  = when to start projection
       period = years of valuation
       df = dataframe with ticker ratios
return: ax = projection plot
        df = Dataframe with EPS growth values
'''
def projection(start_year, period, df):
    growths = df['EPS next 5Y %'].tolist()
    epss = df['EPS (ttm)'].tolist()
    tickers = df['index'].tolist()
    
    #projection 
    proj_10y = []
    proj_10y.append(epss) #first year eps
    for year in range(period-1):
        projection = []
        for eps in epss:
            growth = growths[epss.index(eps)]
            new_eps = eps + eps*growth
            eps = round(new_eps, 2)
            projection.append(eps)
        epss = projection
        proj_10y.append(projection)

    #string manipulation
    start_year = start_year - 1
    start = '1 1 ' + str(start_year)
    
    #plot data
    index = pd.date_range(start, periods=period, freq='A', name='Year')
    data = np.array(proj_10y)
    projection = pd.DataFrame(data, index, tickers)
    ax = sns.lineplot(data=projection)
    
    plt.title('EPS Growth Projection')
    plt.ylabel('EPS')
    
    #store data
    df = pd.DataFrame(data, columns=tickers)
    df.index.name = 'Year'
    
    return ax, df


'''
Create a dataframe with summary of metrics values or ratios
param: ticker(string) = tickers name
       metric(string) = metric that wants to retrieve values
       sec_tickers(dataframe) = selected tickers from sector
       ind_tickers(dataframe) = selected tickers from industry
return: dataframe with summary
'''
def get_resume(ticker, metric, sec_tickers, ind_tickers):
    ticker = ticker.upper()
    ind_mean = round(ind.mean(),2) #mean values of all sector tickers
    sec_mean = round(sec.mean(),2) #mean values of all sector tickers
    sec_eps = sec_mean[metric] 
    ind_eps = ind_mean[metric] 
    ticker_row = sec_tickers.loc[sec_tickers['index'] == ticker]
    current_eps = ticker_row[metric].iloc[0]
    sec_sel_tickers_eps = sec_tickers[metric].mean()
    ind_sel_tickers_eps = ind_tickers[metric].mean()
    
    resume = pd.DataFrame({'Current '+ metric: [current_eps], 
              'Sector '+ metric: [sec_eps], 'Sector_5 '+ metric: [sec_sel_tickers_eps], 
              'Industry '+ metric: [ind_eps], 'Industry_5 '+ metric: [ind_sel_tickers_eps]})
    resume.set_index([[ticker]], inplace=True)

    #output dataframe with resumed EPS values
    return resume
