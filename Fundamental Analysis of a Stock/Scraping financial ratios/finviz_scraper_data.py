# -*- coding: utf-8 -*-
"""
Script contains functions and class related to financial ratio Dataframe. 
"""
import pandas as pd

'''
Finantial data clearing and transforming dataframe to all numeric values
'''
def clean_data(data):
    #filling empty cells with nan value and treating '52W Range' column
    mymap = {'-': float('nan')}
    range_df = data['52W Range']
    data.drop(columns=['52W Range'], axis=1, inplace=True)
    data.applymap(lambda s: mymap.get(s) if s in mymap else s)
    
    range_df = range_df.apply(lambda x: x.split(' - '))
    data['52W Range Low'] = range_df.apply(lambda x: x[0])
    data['52W Range High'] = range_df.apply(lambda x: x[1])
    #treating % and Million/Billion values to numeric
    mymap = {'%': 0.01, 'M': 1000000, 'B': 1000000000}
    metrics_tonumeric = ['Market Cap', 'EPS next 5Y', 'Dividend %', 'Insider Own', 
                         'ROE', 'ROI', 'ROA', 'Profit Margin', 'Shs Outstand']
    for metric in metrics_tonumeric:
        data.loc[:, metric] = pd.to_numeric(data[metric].str[:-1]) * \
                                    data[metric].str[-1].replace(mymap)
    #transforming whole df to numeric values
    data = data.apply(pd.to_numeric, errors='coerce')
    #adjustments on dataframe to make it more readable
    data['Market Cap'] = data['Market Cap'].apply(lambda x: x/1000000000)
    data['Shs Outstand'] = data['Shs Outstand'].apply(lambda x: x/1000000)
    data.columns = ['Market Cap(B)', 'Price', 'P/B', 'P/E', 'Forward P/E', 'P/S', 'PEG', 
                         'P/FCF', 'Debt/Eq', 'EPS (ttm)', 'EPS next 5Y %', 'Dividend %', 
                         'Insider Own %', 'ROE %', 'ROI %', 'ROA %', 'Profit Margin %', 
                         'Shs Outstand(M)', 'RSI (14)', 'Beta', '52W Range Low', '52W Range High']
    return data
    
'''
Calculation of Intrinsic value of stocks
'''
class CalculateValue(object):
    def __init__(self, data):
        self.data = data
    '''
     Discounted cash flow (DCF) is a valuation method used to estimate the value 
     of an investment based on its future cash flows. DCF analysis attempts to 
     figure out the value of an investment today, based on projections of 
     how much money it will generate in the future.
     param: years = valuation period to be considered
            rate_discount = rate of return that wants to make
            tv_multiplier = terminal value multiplier 
                           (for high quality businesses recommended: 15 and
                            10 for lower quality businesses)
     return: enterprise_value = EV calculated to achieve the set goal
             dcf_value = Stock price calculated to achieve the set goal         
    '''
    def simple_dcf_valuation(self, years, rate_discount, tv_multiplier):
        #free cash flow
        fcf = self.data['Market Cap(B)']/self.data['P/FCF']
          
        growth_1 = self.data['EPS next 5Y %'] #growth of first 5 years
        growth_2 = self.data['EPS next 5Y %']*0.7 #growth of remaining years
          
        compound_list = []
        pv_list = []
        compound_list.append(fcf)
        pv = fcf/(1+rate_discount)
        pv_list.append(pv)
          
        for year in range(2, years//2 + 1):
            new_fcf = fcf + fcf*growth_1
            fcf = new_fcf
            pv = fcf/(1 + rate_discount)**year
            compound_list.append(fcf)
            pv_list.append(pv)
        
        for year in range(years//2 + 1, years + 1):
            new_fcf = fcf + fcf*growth_2
            fcf = new_fcf
            pv = fcf/(1 + rate_discount)**year
            compound_list.append(fcf)
            pv_list.append(pv)
        
        terminal_value = compound_list[-1]*tv_multiplier
        tv_pv = terminal_value/(1 + rate_discount)**years
        pv_list.append(tv_pv)
        enterprise_value = sum(pv_list)
        dcf_value = enterprise_value/self.data['Shs Outstand(M)']*1000 #*1000 because EV(billion)/Shs Outstd(million)
        return enterprise_value, dcf_value
        
    '''
    'Sticker Price'(Fair Value of a Stock) and 'Margin of Safety' valuation method
     param: years = valuation period to be considered
            rate_return = wanted rate of return out of the investment
            margin_safety = is the risk tolerance of the investment. 
                            i.e) a margin of 0.5 means I'll buy the stock
                                 wen priced at 0.5 or less of their 
                                 intrinsic value(fair value)
     return: fairvalue = sticker price or intrinsic value of the stock
             buyvalue = buying price of stock 
    '''
    def sp_valuation(self, years, rate_return, margin_safety):
        eps = self.data['EPS (ttm)']
        growth = self.data['EPS next 5Y %']
        pe = 2*growth*100
        
        compound_list = []
        compound_list.append(eps) #year 1)
        for year in range(years-1):
            new_eps = eps + eps*growth
            eps = new_eps
            compound_list.append(eps)
        values = []
        value = compound_list[-1]*pe
        values.append(value)
        for year in range(years-1):
            value = value/(1 + rate_return)
            values.append(value)
        
        fairvalue = values[-1]
        buyvalue = fairvalue*margin_safety
        return fairvalue, buyvalue