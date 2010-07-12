from fortuneengine.GameEngineElement import GameEngineElement

STARTING_MONEY = 1000
ITEMS = {
        'cup': {
            'name':'Cups',
            'cost':10,
            'decay':0,
            'peritem':1,
            'bulk':25
            },
        'lemon': {
            'name':'Lemons',
            'cost':75,
            'decay':5,
            'peritem':2,
            'bulk':1
            },
        'sugar': {
            'name':'Sugar',
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

        for item_key in ITEMS.keys():
            self.__resources[item_key] = []

        self.__weather = 0

        # run weather

        # run random

        # Register with game engine
        #self.add_to_engine()

    def process_day( self, items ):
        self.__day += 1

        # Process Item Payment

        # People Buy
        
        # Handle Change

        # Day earnings

        # Decay items
        self.decay_items()

        # Weather

        # Random event

    def add_item(self, key, quanity):
        total = quanity * ITEMS[key]['bulk']
        cost = ITEMS[key]['cost'] * total

        if cost < self.__resources['money']:
            self.__resources['money'] -= cost
            self.__resources[key].append([ITEMS[key]['decay'], total])
            return True

        else:
            return False

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
