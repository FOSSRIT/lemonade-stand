from fortuneengine.GameEngineElement import GameEngineElement
from random import randint
from gettext import gettext as _

STARTING_MONEY = 1000
MAX_MSG = 10
ITEMS = {
        'cup': {
            'name':_('Cups'),
            'cost':10,
            'decay':0,
            'peritem':1,
            'bulk':25
            },
        'lemon': {
            'name':_('Lemons'),
            'cost':75,
            'decay':5,
            'peritem':2,
            'bulk':1
            },
        'sugar': {
            'name':_('Sugar'),
            'cost':5,
            'decay':0,
            'peritem':1,
            'bulk':100}
    }

class LemonadeMain(GameEngineElement):
    def __init__(self):
        GameEngineElement.__init__(self, has_draw=False, has_event=True)
        self.__day = 1
        self.__resources = {'money':STARTING_MONEY}

        # Populate resources with item keys
        for item_key in ITEMS.keys():
            self.__resources[item_key] = []

        self.__weather = 0
        self.__msg_queue = []

        # run weather
        self.weather_change()

        # run random
        self.random_event()

        # Register with game engine
        #self.add_to_engine()

    def add_msg(self, mesg):
        self.__msg_queue.append( mesg )
        if len(self.__msg_queue) > MAX_MSG:
            self.__msg_queue.pop(0)

    def weather_change(self):
        """
        Randomly change the weather, but not more than one unit away
        """
        self.__weather += randint(-1, 1)

        # It looks like its going to rain tomorrow
        if self.__weather <= -1:
            self.__weather = -1
            self.add_msg(_("It looks like it is going to rain tomorrow"))

        elif self.__weather == 0:
            self.add_msg(_("It looks like it will be nice tomorrow"))

        # Tomorrow looks to be very hot
        elif self.__weather >= 1:
            self.__weather = 1
            self.add_msg(_("It looks like it will be very hot tomorrow"))

    def random_event(self):
        """
        Attempt to run random events
        """
        event = randint(0, 10)

        if event == 0:
            # TODO: STEAL RANDOM ITEM NOT HARD CODE
            itemcount = self.count_item('sugar')
            if itemcount >= 10:
                self.remove_item('sugar', 10)
            else:
                self.remove_item('sugar', itemcount)

            self.add_msg(_('Ants steal some of your supplies!'))

        elif event == 1:
            self.add_item('lemon', 10)

            self.add_msg(_('A lemon truck crashes in front of your stand!'))

        elif event == 2:
            self.add_item('cup', 10)
            self.add_msg(_('It starts raining cups!'))

    def process_day( self, items ):
        self.__day += 1

        # Process Item Payment
        for item in items:
            status = self.buy_item( item, items[item] )
            if status == -1:
                self.add_msg(_("You can't afford any units of %s.") % \
                    ITEMS[item]['name'])

            else:
                self.add_msg(_("Bought %d units of %s.") % \
                    (items[item], ITEMS[item]['name']))
        # People Buy

        # Handle Change

        # Day earnings

        # Decay items
        self.decay_items()

        # Weather
        self.weather_change()

        # Random event
        self.random_event()

    def buy_item(self, key, quanity):
        """
        Attempts to buy as many (up to max quantity) items from
        the inventory.

        @param key:       The key of the item being added
        @param quanity:   The number of units to buy (before bulk)
        @return:          Returns total bought, -1 if you can't
                          afford any
        """
        the_item = ITEMS[key]

        total = quanity * the_item['bulk']
        cost = the_item['cost'] * total

        if cost < self.__resources['money']:
            self.__resources['money'] -= cost
            self.add_item(key, total)
            return total

        else:
            bulk_price = the_item['bulk'] * the_item['cost']
            # Lets try to buy as many as we can
            can_buy = self.__resources['money'] / bulk_price

            if can_buy != 0:
                total = can_buy * the_item['bulk']
                self.__resources['money'] -= can_buy * bulk_price
                self.add_item(key, total)

                return total
            else:
                return -1

    def add_item(self, key, quantity):
        """
        Adds item to inventory with correct decay flag

        @param key:     The key of the item being added
        @param quantity: The total quantity to add
        """
        total = quantity
        self.__resources[key].append([ITEMS[key]['decay'], total])

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
                resource.insert(0,item)
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
        for item_key in ITEMS.keys():
            new_list = []

            # Loops through all items stored in item list
            for item in self.__resources[item_key]:
                # Decrement decay and add to new list
                # ignore it if has expired
                if item[0] != 1:
                    # If item is 0, then it doesn't decay
                    if item[0] == 0:
                        new_list.append( [item[0], item[1]] )
                    else:
                        new_list.append( [item[0]-1, item[1]] )

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
