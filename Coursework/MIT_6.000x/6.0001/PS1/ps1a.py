# -*- coding: utf-8 -*-
"""
PART A: HOUSE HUNTING
Determine how long it will take you to save enough money to make the down payment 

given the following assumptions: 
    1.Call the cost of your dream home total_cost . 
    2.Call the portion of the cost needed for a down payment portion_down_payment . 
        For simplicity, assume that portion_down_payment = 0.25 (25%). 
    3.Call the amount that you have saved thus far current_savings . 
        You start with a current savings of $0. 
    4.Assume that you invest your current savings wisely, with an annual return of r 
        (in other words, at the end of each month, you receive an additional 
        current_savings*r/12 funds to put into your savings – the 12 is because r is an annual rate).
        Assume that your investments earn a return of r = 0.04 (4%). 
    5.Assume your annual salary is annual_salary . 
    6.Assume you are going to dedicate a certain amount of your salary each month 
        to saving for the down payment. Call that portion_saved . 
        This variable should be in decimal form (i.e. 0.1 for 10%). 
    7.At the end of each month, your savings will be increased by the return on your investment,
        plus a percentage of your monthly salary (annual salary / 12).
        
Calculate how many months it will take you to save up enough money for a down payment. 
"""
annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

portion_down_payment = 0.25
current_savings = 0.
r = 0.04
monthly_salary = annual_salary/12
needed_savings = total_cost*portion_down_payment

months = 0
while(current_savings < needed_savings):
    current_savings += current_savings*r/12 #NO investment savings in the 1st month
    current_savings += monthly_salary*portion_saved
    months += 1
 
print("Number of months: ", months)
