# -*- coding: utf-8 -*-
"""
PART C: FINDING THE RIGHT AMOUNT TO SAVE AWAY
Suppose you want to set a particular goal, 
e.g. to be able to afford the down payment in three years. 
How much should you save each month to achieve this?

Assume:
    1.Your semiannual raise is .07 (7%) 
    2.Your investments have an annual return of 0.04 (4%) 
    3.The down payment is 0.25 (25%) of the cost of the house 
    4.The cost of the house that you are saving for is $1M.
    
Calculate the best savings rate, as a function of your starting salary(annual_salary).
"""
#user input
annual_salary = float(input("Enter the starting salary: "))

#given static variables
total_cost = 1000000.0
semi_annual_raise = .07
portion_down_payment = 0.25
current_savings = 0.
r = 0.04

#monthly_salary = annual_salary/12
needed_savings = total_cost*portion_down_payment

#bisectional method variables   
epsilon = 100.0
num_guesses = 0
low = 0 #low searching boundry
high = 10000 #high searching boundry.

savings_rate = (high + low)//2 #halfway point. Integer division  
    
while abs(current_savings - needed_savings) >= epsilon:
    #initial conditions/resets
    monthly_salary = annual_salary/12
    current_savings = 0.
    
    # convert savings_rate into a float type with two decimals of accuracy
    rate = savings_rate/10000
    
    #for every new guess 
    for months in range (36):
        if months%6 == 0 and months != 0:
            monthly_salary *= 1 + semi_annual_raise
        current_savings += current_savings*r/12
        current_savings += monthly_salary*rate  
    
    if current_savings < needed_savings:
        low = savings_rate
    else:
        high = savings_rate
    savings_rate = (high + low)//2
    num_guesses += 1 
    
    #guess converges on the order of log base 2.
    #for log(10000) base 2 == 13.29
    #Therefore, on the 14th guess it needs to break out of the while loop.
    if num_guesses > 13:
        #Note: without this if statement in case starting_salary == 10000
        #code won't output.
        break
    
    
#Outputs
if num_guesses <= 13: 
    print("Best savings rate: ", rate)
    print("Steps in bisection search: ", num_guesses)
else: 
    print('It is not possible to pay the down payment in three years.')
    
        
        
