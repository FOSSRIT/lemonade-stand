"""Logic for the money counting game"""

dollar = 100
quarter = 25
dime = 10
nickel = 5
penny = 1


def play_money(money_find, frontend):
    global quarter, dime, nickel, penny
    total = 0

    #Takes the amount of money
    total += dollar * frontend.take_input("How many dollars? ")
    total += quarter * frontend.take_input("How many quarters? ")
    total += dime * frontend.take_input("How many dimes? ")
    total += nickel * frontend.take_input("How many nickels? ")
    total += penny * frontend.take_input("How many pennies? ")

    if total == money_find:
        return True
    else:
        return False
