# -*- coding: utf-8 -*-
"""
PART B: SAVING, WITH A RAISE
Build on your solution to Part A by factoring in a raise every six months.

Considering PART A include the following: 
    1.Have the user input a semi-annual salary raise semi_annual_raise (as a decimal percentage) 
    2.After the 6th month, increase your salary by that percentage. 
        Do the same after the 12th th month, the 18 month, and so on. 
        
Calculate how many months it will take you save up enough money for a down payment. 
"""
annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

portion_down_payment = 0.25
current_savings = 0.
r = 0.04
monthly_salary = annual_salary/12
needed_savings = total_cost*portion_down_payment

months = 0
while(current_savings < needed_savings):
    if months%6 == 0 and months != 0:
        monthly_salary *= 1 + semi_annual_raise
    current_savings += current_savings*r/12
    current_savings += monthly_salary*portion_saved
    months += 1
    
 
print("Number of months: ", months)
