# Lemonade stand is Licensed under the Don't Be A Dick License
# (dbad-license). This license is an extension of the Apache License.
#
# If you do not wish to comply with the restrictions of the Don't Be A Dick
# License, this software is also available under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# The text of the Don't Be A Dick License is available at at
# <http://dbad-license.org/license>, while the GNU General Public License
# is available at <http://www.gnu.org/licenses/>.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Authors:
#     Justin Lewis <jlew.blackout@gmail.com>
#     Nathaniel Case <Qalthos@gmail.com>

from __future__ import unicode_literals
from random import randint
from gettext import gettext as _
import gettext
lang = gettext.translation('Lemonade', '/usr/share/locale/', languages = ['es'])
_ = lang.ugettext
from operator import itemgetter
from constants import STARTING_MONEY, B_EVENTS_DICT, MAX_MSG, ITEMS, \
                      CURRENCY, RECIPES, DIFFICULTY, format_money, \
                      WEATHER, GOOD_ODDS, BAD_ODDS, SCALE, EVENT_KEYS, \
					  STARTING_ITEMS, G_EVENTS_DICT, B_EVENTS_DICT, \
                      SERVING_ITEM, LOCATIONS, REP_VALUES, UPGRADES

class LemonadeMain:
    """
    The main class for the Lemonade Game.
    This class holds all the logic of the game
    """

    def __init__(self, difficulty_level=0):
        self.splash = True
        self.__day = 1
        self.__difficulty = difficulty_level
        self.version = "lemonade"
        self.__resources = {
            'money': 0,
            'day_start_money': 0,
            'last_income': 0,
            'last_profit': 0,
            'last_spent': 0,
            'price': RECIPES[self.version]['basic']['cost'],
            'recipe': RECIPES[self.version]['basic'],
            'upgrades': [0,
                {
                    'name': [],
                    'level': [],
                    'capacity': []
                }
            ]
        }

        # Populate resources with item keys
        for item_key in ITEMS[self.version].keys():
            self.__resources[item_key] = []

        # Populate the upgrade resource
        for i in range(0, len(UPGRADES[self.version])):
            self.__resources['upgrades'][1]['name'].append(\
                UPGRADES[self.version][i]['name'])
            self.__resources['upgrades'][1]['level'].append(0)
            self.__resources['upgrades'][1]['capacity'].append(0)

        self.__weather = 1
        self.__msg_queue = []
        self.challenge_mode = False
        self.challenge_completed = False
        self.__reputation = {
                'neighborhood': 0
        }
        self.location = "neighborhood"

        # run weather
        self.weather_change()

        self.event_messages = []

    @property
    def upgrades(self):
        return self.__resources['upgrades']

    @property
    def reputation(self):
        return self.__reputation

    @property
    def location(self):
        return self.location

    @property
    def version(self):
        return self.version

    @property
    def challenge_completed(self):
        return self.challenge_completed

    @property
    def challenge(self):
        return self.challenge_mode

    @property
    def event_messages(self):
        return self.event_messages

    @property
    def difficulty(self):
        return self.__difficulty

    @property
    def start_money(self):
        return self.__resources['day_start_money']

    @property
    def spent(self):
        return self.__resources['spent']

    @property
    def prices(self):
        return self.__resources['price']
    
    @property
    def price(self):
        return self.__resources['price'][self.difficulty]

    @property
    def income(self):
        return self.__resources['last_income']

    @property
    def current_recipe(self):
        return self.__resources['recipe']

    @property
    def money(self):
        return self.__resources['money']

    @property
    def profit(self):
        return self.__resources['last_profit']

    @property
    def day(self):
        return self.__day

    @property
    def weather(self):
        return self.__weather

    @property
    def weather_name(self):
        return WEATHER[self.weather]

    def get_resource(self, key):
        return self.count_item(key)

    @property
    def resource_list(self):
        resources = {}
        for item_key in ITEMS[self.version].keys():
            resources[item_key] = self.count_item(item_key)
        return resources

    def recipe(self, ingredient):
        return self.__resources['recipe'].get(ingredient, 0)

    @property
    def messages(self):
        return self.__msg_queue

    def process_buy_upgrade(self, info):
        """
        Checks to see if the player can afford a specific upgrade.

        :type info: list
        :param info: A list of information about the upgrade
        """
        name = info[0]
        base_price = info[1]
        base_capacity = info[2]

        upgrade_index = self.upgrades[1]['name'].index(name)
        price = base_price + base_price * 1.5 * \
            self.upgrades[1]['level'][upgrade_index]

        if self.money >= price:
            self.money -= price
            self.upgrades[1]['level'][upgrade_index] += 1
            self.upgrades[1]['capacity'][upgrade_index] += base_capacity
            return True

        return False

    def reset_game(self):
        """
        Resets the game to its beginning game states
        """
        self.day = 1
        self.challenge = False
        self.challenge_completed = False

    def populate_resources(self, difficulty):
        """
        Populates the player's resources depending on the difficulty

        :type difficulty: int
        :param difficulty: The difficulty setting
        """

        # Set the new difficulty
        self.difficulty = difficulty

        # Populate the player's inventory with the starting
        # items for this specific difficulty
        for item_key in ITEMS[self.version].keys():
            self.add_item(item_key,
                STARTING_ITEMS[self.version][item_key][difficulty])

        # Give the player starting money depending on the difficulty
        self.money = STARTING_MONEY[difficulty]
        self.start_money = STARTING_MONEY[difficulty]

    def add_msg(self, mesg):
        self.__msg_queue.append(mesg)
        if len(self.__msg_queue) > MAX_MSG:
            self.__msg_queue.pop(0)

    def clear_queue(self):
        self.__msg_queue = []

    def weather_change(self):
        """
        Randomly change the weather, but not more than one unit away
        """

        self.__weather += randint(-1, 1)

        # It looks like its going to rain tomorrow
        if self.__weather <= 0:
            self.__weather = 0
        # Tomorrow looks to be very hot
        elif self.__weather >= 2:
            self.__weather = 2

    def event_select(self, events):
        """
        Randomly selects an event based on the weight
        """

        # Generate a random value
        rand_num = randint(1,100)

        # Loop through all the weights starting with the lowest
        for key in EVENT_KEYS:

            # Once you found which weight value you are using,
            # return a random event with that weight
            if rand_num <= int(key):
                index = randint(0, len(events[key]) - 1)
                return events[key][index]

    def random_event(self):
        """
        Attempt to run random events
        """

        # Adds a event free buffer for the first few days
        if self.day < 5:
            return

        # Create a message list and a random number for checking
        # if you got a good, bad, or no event
        self.event_messages = []
        event_num = randint(1, 100)

        # Check if you got a bad event
        if event_num <= BAD_ODDS[self.difficulty]:

            # Generate a bad event
            event = self.event_select(B_EVENTS_DICT)

            # Get the amount of the item you have
            itemcount = self.count_item(event['item'])

            # If you have none of that item, return
            if itemcount == 0:
                return

            # Check if event scales
            if event['change'] < 0:

                # Find the amount of items to remove based on the scale
                remove = int(abs(event['change']) + \
                             (itemcount * SCALE[self.difficulty]))

            # Else remove a flat amount
            else:
                remove = event['change']

            # If you lose more items than you have, remove all your items
            if itemcount < remove:
                remove = itemcount

            # Create a message
            msg = _("    You lost {} {}".format(\
                str(remove), event['item']))

            # Remove the items from your inventory
            self.remove_item(event['item'], remove)

            # Adds s to pluralise nouns that need it
            if (event['item'] == 'cup' or event['item'] == 'lemon')\
               and itemcount > 1:
                msg += "s"

            # Add the messages to the event message list
            self.event_messages.append(event['text'])
            self.event_messages.append(msg)

        # Check if you got a good event
        elif event_num > BAD_ODDS[self.difficulty] and \
             event_num <= (GOOD_ODDS[self.difficulty] + \
             BAD_ODDS[self.difficulty]):

            # Generate a good event
            event = self.event_select(G_EVENTS_DICT)

            # Checks if event scales
            if event['change'] < 0:
                # Get the amount of the item you have
                itemcount = self.count_item(event['item'])

                # Find the amount of items to add based on the scale
                add = int(abs(event['change']) +\
                          (itemcount * SCALE[3 - self.difficulty]))

            # Else add a flat amount
            else:
                add = event['change']

            # Create a message
            msg = _("    You gained {} {}".format(\
                str(add), event['item']))

            # Add your new supplies to your inventory
            self.add_item(event['item'], add)

            # Adds s to pluralise nouns that need it
            if event['item'] == 'cup' or event['item'] == 'lemon':
                msg += "s"

            # Add the messages to the event message list
            self.event_messages.append(event['text'])
            self.event_messages.append(msg)

    def process_day_logic(self):
        self.clear_queue()

        # Show profit and expenses if the difficuly is less than impossible
        if self.difficulty < DIFFICULTY.index(_("Impossible")):
            self.add_msg(_("You spent {} on supplies").format(\
                    format_money(self.spent)))
            self.add_msg(_("and made {} in sales").format(\
                    format_money(self.income)))

        # Check if any profit was made
        if self.profit > 0:
            # Show the net porfit if difficulty is less than normal
            if self.difficulty < DIFFICULTY.index(_("Hard")):
                self.add_msg(_("That comes to {} in profit").format(\
                    format_money(self.profit)))
            return True

        # If no profit is made, go to the end of the day
        else:
            self.money += self.profit
            if self.money < 0:
                self.money = 0
            return False

    def process_sales(self, max_sales):

        sales = LOCATIONS[self.location]['base'] + \
            LOCATIONS[self.location]['multiple'] * \
            self.reputation[self.location]

        if self.reputation != 100:
            if self.weather == 0:
               sales *= .5
            elif self.weather == 1:
                sales *= .75

        if sales > max_sales:
            sales = max_sales

        return int(sales)

    def update_day_log(self, items):

        self.clear_queue()
        self.spent = 0

        self.start_money = self.money

        # Display the current day
        self.add_msg(_("--Day {} Log--").format(self.day))
        self.add_msg("")

        self.add_msg(_("Today's weather: {}").format(\
            self.weather_name.upper()))
        self.add_msg("")

        # Display the amount of each item you bought and for how much
        self.add_msg(_("Purchased:"))
        for item in items:
            total_bought = self.buy_item(item, items[item])
            item_name = ITEMS[self.version][item]['name']
            item_name = item_name.decode('utf8')
            if total_bought != 1:
                self.add_msg(_("{} {}s for {}").format(
                    total_bought, item_name,
                    format_money(total_bought * 
                    ITEMS[self.version][item]['cost'][self.difficulty])))
            else:
                self.add_msg(_("{} {} for {}").format(
                    total_bought, item_name,
                    format_money(total_bought * 
                    ITEMS[self.version][item]['cost'][self.difficulty])))

            self.spent += total_bought * \
                ITEMS[self.version][item]['cost'][self.difficulty]

        self.add_msg("------------------------------")
        self.add_msg(_("Total Spent: {}").format(format_money(self.spent)))
        self.add_msg("")

        # Chance of a random event to occur
        self.random_event()

        # Calculate the max number of cups of lemonade you can sell
        inventory_hold = []
        for item_key in ITEMS[self.version].keys():
            if self.recipe(item_key) == 0:
                continue
            inventory_hold.append(\
                self.count_item(item_key) / self.recipe(item_key))

        max_sales = min(inventory_hold)
        sales = self.process_sales(max_sales)

        # Calculates how much reputation you acquired today
        if sales > 0 and max_sales > sales:
            self.reputation[self.location] += \
                REP_VALUES['gain'][self.difficulty]
            if self.reputation[self.location]  > 100:
                self.reputation[self.location] = 100
        else:
            self.reputation[self.location] -= \
                REP_VALUES['lose'][self.difficulty]
            if self.reputation[self.location] < 0:
                self.reputation[self.location] = 0

        # Calculate the money you made from sales
        self.income = sales * self.price

        # Display the number of cups you sold, at what price, and the
        # total amount of money that you made
        self.add_msg(_("Sales:"))
        if sales != 1:
            self.add_msg(_("{} {}s of {} sold").format(\
                sales, SERVING_ITEM[self.version], self.version))
        else:
            self.add_msg(_("{} {} of {} sold").format(\
                sales, SERVING_ITEM[self.version], self.version))
        self.add_msg(_("    @ {} each").format(format_money(self.price)))
        self.add_msg("------------------------------")
        self.add_msg(_("Total Made: {}").format(format_money(self.income)))

        # Remove supplies required to make your number of sales
        for item_key in ITEMS[self.version].keys():
            self.remove_item(item_key, sales * self.recipe(item_key))

        self.profit = self.income - self.spent

    def process_change(self, mini_game_key):
        """
        Processes the counting game effects

        @param mini_game_key:    A dictionary of keys and values of the
                                 mini game
        """
        if self.profit > 0:
            mini_game_success = self.count_game(mini_game_key, self.profit)
            if mini_game_success:
                # Give them the money if they added
                self.money += self.profit
            else:
                self.add_msg(_("That is the incorrect amount of money. Try again."))
                return False
        return True

    def process_day_end(self):
        """
        Processes the end of the day events.
        """
        self.clear_queue()

        # Decay items
        self.decay_items()

        # Weather
        self.weather_change()

        if self.challenge and self.day ==  90:
           self.add_msg(_("Summer is over!"))
           self.add_msg(_("You have successfully completed Lemonade Stand!"))
           self.challenge_completed = True

        else:
            self.add_msg(_("Time to get some rest."))
            self.add_msg(_("It looks like it will be {} tomorrow.").format(\
                            self.weather_name))
            self.add_msg("")
            self.add_msg(_("What flavor will you make tomorrow?"))

    def buy_upgrade(self, key):
        return False

    def buy_item(self, key, quanity):
        """
        Attempts to buy as many (up to max quantity) items from
        the inventory.

        @param key:       The key of the item being added
        @param quanity:   The number of units to buy (before bulk)
        @return:          Returns total bought, -1 if you can't
                          afford any
        """
        the_item = ITEMS[self.version][key]

        total = quanity * the_item['bulk']
        cost = the_item['cost'][self.difficulty] * total

        if cost < self.money:
            self.add_item(key, total)
            return total

        else:
            bulk_price = the_item['bulk'] * the_item['cost'][self.difficulty]
            # Lets try to buy as many as we can
            can_buy = self.money / bulk_price

            if can_buy != 0:
                total = can_buy * the_item['bulk']
                self.add_item(key, total)

                return total
            else:
                return 0

    def add_item(self, key, quantity):
        """
        Adds item to inventory with correct decay flag

        @param key:     The key of the item being added
        @param quantity: The total quantity to add
        """
        total = quantity
        self.__resources[key].append(
            [ITEMS[self.version][key]['decay'], total])

    def remove_item(self, key, quantity):
        """
        Removes item from inventory

        @param key:      The key of the items to remove
        @param quantity: The amount to remove
        @return:         Returns true if successful, false if
                         they don't have enough to remove.
        """
        to_remove = quantity

        # Make copy of resource in case fail
        resource = self.__resources[key][:]

        while to_remove > 0:
            try:
                item = resource.pop(0)
            except:
                return False

            if item[1] > to_remove:
                item[1] -= to_remove
                resource.insert(0, item)
                break
            else:
                to_remove -= item[1]

        self.__resources[key] = resource
        return True

    def decay_items(self):
        """
        Decays items and removes expired items.
        """
        # Loop through all items
        for item_key in ITEMS[self.version].keys():
            new_list = []

            # Loops through all items stored in item list
            for item in self.__resources[item_key]:
                # Decrement decay and add to new list
                # ignore it if has expired
                if item[0] != 1:
                    # If item is 0, then it doesn't decay
                    if item[0] == 0:
                        new_list.append([item[0], item[1]])
                    else:
                        new_list.append([item[0]-1, item[1]])
                elif item[1] != 0:
                    self.add_msg(_("{} {}s have gone bad").format(\
                        item[1], item_key))

            # Place item back into resource list
            self.__resources[item_key] = new_list

    def count_item(self, key):
        """
        Returns the items owned under the given key

        @param key:   The key of the item to lookup
        @return:      Returns the items in inventory
        """
        count = 0

        for item in self.__resources[key]:
            count += item[1]
        return count

    def count_game(self, values, target):
        """
        Verifies the values of the counting game.

        @param values:      A dictionary (keys must match CURRENCY) and
                            values are how many of each currency type
                            are required to make the optimum change
        @return:            Returns true if they pass the mini-game
        """
        currency_values = sorted(CURRENCY.items(), key=itemgetter(1),
                                 reverse=True)

        # Set previous_value to target so it always accepts the first key
        previous_value = target
        for key, value in  currency_values:
            cal_val = (value * values[key])
            if cal_val > previous_value:
                return False
            target -= cal_val
            previous_value = value

        if target == 0:
            return True

        else:
            return False
