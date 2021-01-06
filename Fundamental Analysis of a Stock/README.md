# Fundamental Analysis of a Stock
For an overview, have a look on this [article](https://medium.com/@juin_48458/scraping-finviz-getting-financial-ratios-with-python-and-applying-valuation-methods-655710a024fe) I wrote about this project.

## Folder Content

<details><summary><strong>Scraping financial ratios</strong></summary> 

- [Finviz Scraper](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/Scraping%20financial%20ratios/finviz_scraper_run.py) : Scrapes financial ratios from website, calculates fair values and store in database
- [Data Cleaning and Intrinsic Value Calculation](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/Scraping%20financial%20ratios/finviz_scraper_intrinsicvalue.py) : Contains scraped data cleaning method and intrinsic value calculation methodology
- [Finviz Parser](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/Scraping%20financial%20ratios/finviz_scraper.py) : Contains scraper code
- [Analysis Visualization](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/Scraping%20financial%20ratios/data_viz.py) : Contains graph functions and method used on [stock analysis](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/fundamental_analysis_of_apple.ipynb).
- Database used: .sqlite files
</details>

<details><summary><strong>EDA on the Tech Sector with focus on Apple</strong></summary> 

- [Fundamental Analysis of Apple stock](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/fundamental_analysis_of_apple.ipynb)
</details>

## Motivation
I'm very interested in making educated investment decisions. For that I'm constantly thinking on tools I can use to assist me evaluate securities.  
**_Disclaimer: I'm not an expert and this is not a suggestion of investment!_**

## What this project involves?
This projects explores the power of web scraping to evaluate a hand picked stock and its sector using financial ratios.
It can be divided in two parts:
1. [Scraping Finviz.com](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/Scraping%20financial%20ratios/finviz_scraper_run.py) : Data gathering according to hand picked stock and pre-defined financial metrics including calculation of intrinsic value with a Simple DCF and Sticker Price valuation methods.
2. [Fundamental Analysis of Apple stock](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/fundamental_analysis_of_apple.ipynb) : Analysis of technology stocks focusing on Apple Inc. including visualization of stock fair value and growth projection.

	_Tools: Web Scraping, BeautifulSoup, Html, Sql, Re, EDA, Pandas, Seaborn, Matplotlib_

## About the data source
Finviz is one of the most widely used US stock screener website. It offers a large range of information mostly for free, which you can use to make a analytical decision on buying/selling certain securities.

## Brief explanation of valuation methodology
- Sticker Price method: Estimate the value of an investment today based on its projected future earnings.
- Discounted Cash Flow method: Estimate the value of an investment today based on its projected future cash flows. 
- To understand better the calculation applied have a look in this script, [Intrinsic Value Calculation](https://github.com/jjuinni/Portfolio/blob/master/Fundamental%20Analysis%20of%20a%20Stock/Scraping%20financial%20ratios/finviz_scraper_intrinsicvalue.py).


## Future considerations
Currently the project's scope is restricted to what we can gather from Finviz. But, there are no limits on how extensively this project could grow. <br>
After tweaking and expanding the data gather my thoughts are that I could upgrade this project to a ranking system scoring stocks according to current buy/sell opportunity. Also, could consider metrics historical data and financial statements for a better analysis of the security evolution. With that, apply more sophisticated valuation methods to calculate its intrinsic value.

