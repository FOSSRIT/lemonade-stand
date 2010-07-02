#!/usr/env python
# -*- coding: cp1252 -*-

import random
from counting import play_money
from game import *

# Generalize the names of supplies to make it easily editable
# [0] = name of the stand, [1] = the object that is being sold
variables = ['Lemonade Stand','cups']

# [0] = first supply, [1] = second supply, [2] = third supply
food_items = ['cups','lemons','sugar']
price =      [25,     100,     5]

# Default values
weather = 0
product_price = 150

frontend = None

def weather_change():
    global weather
    
    #Randomly change the weather, but not more than one unit away
    weather += random.randint( -1, 1 )
    
    if weather <= -1:
        weather = -1
        frontend.output( "It looks like its going to rain tomorrow" )
    elif weather == 0:
        frontend.output(  "Its a normal day tomorrow" )
    elif weather >= 1:
        weather = 1
        frontend.output(  "Tomorrow looks to be very hot" )
    
def take_input(text, default = 0):
    in_text = frontend.keypress(text+" ["+`default`+"]: ")
    if not in_text:
        return default
    else:
        try:
            in_text = int(in_text)
            if in_text < 0:
            	frontend.output("Entered number must be positive.  Please try again.")
            	return take_input(text, default)
        except ValueError:
            frontend.output("Entered text is not a number.  Please try again.")
            return take_input(text, default)
        else:
            return in_text

def random_event():
    event = random.randint(0, 10)   
    
    if event == 0:
        if game.resources[0] > 10:
            frontend.modify_supply(2, -10)
        else:
            frontend.update_supply(2, 0)
        
        frontend.output('Ants steal your supplies!')
            
    elif event == 1:
        frontend.modify_supply(1, 10)
        
        frontend.output('A lemon truck crashes in front of your stand!')
        
    elif event == 2:
        frontend.modify_supply(0, 10)

        frontend.output('It starts raining cups!')

    frontend.output()

def supply_decay():
    """Decreases currently the supplies by 10% each day"""
    # Let's assume that resource 0 is not perisahble
    if game.resources[1] > 0:
        game.resources[1] -= 10 % game.resources[1]
    if game.resources[2] > 0:
        game.resources[2] -= 10% game.resources[2]
    frontend.output()
    
    
def main():
    global frontend

    frontend = game()
    
    frontend.output( 'Welcome to ' + variables[0] )
     
    # take in input
    num_days = take_input("How many days would you like to play for?", 30)
    
    for day in range(1, num_days + 1):
    
        frontend.output( "" )
        frontend.output( "____________________" )
        frontend.output( "     Day number {0}".format(day) )
        frontend.output( "____________________" )
        frontend.output( "" )
    
        random_event()
    
        frontend.output( "{0} price: ${1:.2f}      {2} price: ${3:.2f}      {4} price: ${5:.2f}".format(food_items[0], price[0] / 100.0, food_items[1], price[1] / 100.0, food_items[2], price[2] / 100.0) )
    
        #Checks to make sure you dont go over your bank amount while buying.
        expenses = 0
        cost_over = 1
        for num, name in enumerate(food_items):
		    while cost_over == 1:
		        potential_expense = 0
		        in_num = take_input("How many " + name)
		        potential_expense = expenses + (in_num * price[num])
		
		        if potential_expense < frontend.resources[3]:
		            cost_over = -1
		            expenses += in_num * price[num]
		            game.resources[num] += in_num
		        else:
		            frontend.output("You can not afford that many " + name)
		
		    cost_over = 1
    
    
        sales = max(min(game.resources[0], game.resources[1], game.resources[2]),0)
        
        if sales != 0:
            if weather == 0:
                sales -= 10 % sales
            elif weather == -1:
                sales -= 20 % sales
    
        game.resources[0] -= sales
        game.resources[1] -= sales
        game.resources[2] -= sales
        
        
        profit = sales * product_price
        frontend.output("{0} {1} were made today for ${2:.2f}".format(sales, variables[1], expenses / 100.0) )
        frontend.output("{0} {1} were sold today for ${2:.2f}".format(sales, variables[1], profit / 100.0) )
        frontend.output( "You made ${0:.2f} today".format( (profit - expenses) / 100.0) )
        
        
        
        if (profit - expenses) < 0:
            frontend.output( "You lost money today" )
        elif (profit - expenses) == 0:
            frontend.output( "You broke even today" )
        else:
            frontend.output( "You go to put profits away" )
                      
            if play_money(profit - expenses, frontend):
                frontend.output( "You put the money away correctly" )
            else:
                frontend.output( "You lost the money when putting it away" )
                profit = 0
        
        frontend.modify_supply(3, profit - expenses)
        frontend.output()
    
        supply_decay()
        weather_change()
        
        frontend.output() 
        
    "Would you like to continue?"
    "Would you like to play again?"
    frontend.output("Done!")
    take_input("")

if __name__ == "__main__":
    main()   
