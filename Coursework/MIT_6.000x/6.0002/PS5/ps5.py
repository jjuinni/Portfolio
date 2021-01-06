"""
Problem Set 5: Experimental Analysis
use regression analysis to model the climate of different areas 
in the United States in order to find evidence of global warming. 
 ●First, you will create models to analyze and visualize climate change in terms 
 of temperature, and then consider ways to make the data less noisy and 
 obtain clearer temperature change trends. 
 
 ●You will then test your models to see how well historical data 
 can predict future temperatures. 
 
 ●Lastly, you will investigate a way to model the extremity of temperature, 
 rather than just the increasing temperature.
"""
import pylab
import re
import numpy as np

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    models = []
    for deg in degs: 
        models.append(pylab.polyfit(x, y, deg)) #Least squares polynomial fit
    return models

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    error = ((estimated - y)**2).sum()
    meanError  = error/len(y) 
    return 1 - (meanError/pylab.var(y)) #pylab.var(y): variability in measured data

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for i in range(len(models)):
        est_y = pylab.polyval(models[i], x) #estimated y by a linear regression
        r2 = r_squared(y, est_y)
        degree = np.polynomial.Polynomial.degree(models[i])
        pylab.figure() #plot multiple figures according  to quantity of models
        pylab.plot(x, y, 'bo', label = 'Data Points')
        pylab.plot(x, est_y, 'r-', label = 'Model')
        if degree == 1:
            pylab.title('Fit of degree ' + str(degree) + '\n'
                        + 'R2 = '  + str(round(r2, 5)) + '\n'
                        + 'SE ratio = ' + str(round(se_over_slope(x, y, est_y, models[i]), 5))) #ratio of the std error
        else:
            pylab.title('Fit of degree ' + str(degree) + '\n'
                        + 'R2 = '  + str(round(r2, 5)))
        pylab.legend(loc = 'best')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature in Celsius')

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    avg_temp = []
    for year in years:
        year_temp = []
        for city in multi_cities:
            year_temp.append(climate.get_yearly_temp(city, year))
        year_temp = pylab.array(year_temp)
        avg_temp.append(year_temp.mean())
    avg_temp = pylab.array(avg_temp)
    return pylab.array(avg_temp)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO    
    #Moving averages: allows to emphasize the general/global trend over local/yearly fluctuaction.
    mov_avg_y = [0 for i in range(len(y))] #initially, all 0 list
    for i in range(len(y)):
        num = 0
        if i >= window_length - 1:
            cut = y[(i-window_length+1):(i+1)] #cutted list
            num  = sum(cut)  #numerator 
            mov_avg_y[i] = num/window_length
        else:
            cut = y[:(i+1)]
            num = sum(cut)
            mov_avg_y[i] = num/len(cut)
    return pylab.array(mov_avg_y)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    num =  ((y - estimated)**2).sum()
    den = len(y)
    rmse = pylab.sqrt(num/den)
    return rmse

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO    
    all_std_dev = []
    for year in years:
        year_temp = [] #considering all cities
        for city in multi_cities:
            year_temp.append(climate.get_yearly_temp(city, year))
        year_temp = pylab.array(year_temp)
        daily_mean = year_temp.mean(axis=0) #mean of same day from all cities in the same year
        std_dev = pylab.std(daily_mean)
        all_std_dev.append(std_dev)
    all_std_dev = pylab.array(all_std_dev)
    return all_std_dev

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for i in range(len(models)):
        est_y = pylab.polyval(models[i], x) #estimated y by a linear regression
        rmse_value = rmse(y, est_y)
        degree = np.polynomial.Polynomial.degree(models[i])
        pylab.figure()
        pylab.plot(x, y, 'bo', label = 'Data Points')
        pylab.plot(x, est_y, 'r-', label = 'Model')
        pylab.title('Fit of degree ' + str(degree) + '\n'
                    + 'RMSE = '  + str(round(rmse_value, 5)))
        pylab.legend(loc = 'best')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature in Celsius')

if __name__ == '__main__':

#    pass 

    # Part A.4 Investigatingg the trend
    # TODO: replace this line with your code
##    P.4.I - Temperature on January 10th for New York City in that year
##    1. Generate sample data
#    file = Climate('data.csv')
#    x, y = [], [] #years, temperatures
#    for year in TRAINING_INTERVAL:
#        x.append(year)
#        y.append(file.get_daily_temp('NEW YORK', 1, 10, year))
#    x = pylab.array(x) 
#    y = pylab.array(y) 
##    2. Generate model: Fit data to a degree-one polynomial
#    models = generate_models(x, y, [1])
##    3. Plot regression results
#    evaluate_models_on_training(x, y, models)    
    
    # TODO: replace this line with your code
#     P.4.II - Annual Temperature
#    1. Generate sample data
#    file = Climate('data.csv')
#    x, y = [], [] #years, average_temperatures
#    for year in TRAINING_INTERVAL:
#        x.append(year)
#        y.append(file.get_yearly_temp('NEW YORK', year).mean()) 
#    x = pylab.array(x) 
#    y = pylab.array(y) # 1d array of mean temperatures
##    2. Generate model: fit data to a degree-one polynomial
#    models = generate_models(x, y, [1])
##    3. Plot regression results
#    evaluate_models_on_training(x, y, models)
    
    # Part B - Incorporating Mode Data
    # TODO: replace this line with your code
#    file = Climate('data.csv')
#    x = pylab.array(TRAINING_INTERVAL)
#    y = gen_cities_avg(file, CITIES, TRAINING_INTERVAL)
#    models = generate_models(x,  y, [1])
#    evaluate_models_on_training(x, y, models)
    # Part C
    # TODO: replace this line with your code
#    
#    Part C: 5 years Moving Average
    # TODO: replace this line with your code
#    file = Climate('data.csv')
#    x = pylab.array(TRAINING_INTERVAL)
#    y = gen_cities_avg(file, CITIES, TRAINING_INTERVAL)
#    mov_avg = moving_average(y, window_length=5)
#    models = generate_models(x, mov_avg, [1])
#    evaluate_models_on_training(x, mov_avg, models)

    # Part D.2 - Predicting the  future
    # TODO: replace this line with your code  
#    file = Climate('data.csv')
#    x = pylab.array(TRAINING_INTERVAL)
#    y = gen_cities_avg(file, CITIES, TRAINING_INTERVAL)
#    mov_avg = moving_average(y, window_length=5)
#    models = generate_models(x, mov_avg, [1, 2, 20])
#    evaluate_models_on_training(x, mov_avg, models)
#    
#    test_x = pylab.array(TESTING_INTERVAL)
#    test_y = gen_cities_avg(file, CITIES, TESTING_INTERVAL)
#    test_mov_avg = moving_average(test_y, window_length=5)
#    evaluate_models_on_testing(test_x, test_mov_avg, models)

    # Part E: Modelling Extreme Temperatures
    # TODO: replace this line with your code    
#    file = Climate('data.csv')
#    x = pylab.array(TRAINING_INTERVAL)
#    std_dev = gen_std_devs(file, CITIES, TRAINING_INTERVAL)
#    mov_avg = moving_average(std_dev, window_length=5)
#    models = generate_models(x, mov_avg, [1])
#    evaluate_models_on_training(x, mov_avg, models)