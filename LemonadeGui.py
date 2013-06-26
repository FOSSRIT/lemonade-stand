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

import pygame
from fortuneengine.GameEngineElement import GameEngineElement
from constants import ITEMS, format_money, WEATHER, CURRENCY, DIFFICULTY, MENU
from gettext import gettext as _
from pygame import Surface, transform, image
from pygame.locals import KEYDOWN, K_RETURN, K_BACKSPACE, K_TAB,\
                          K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE,\
                          K_KP1, K_KP2, K_KP3, K_KP4, K_KP6, K_KP8, K_KP9


class LemonadeGui(GameEngineElement):

    def __init__(self):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.__font = self.game_engine.get_object('font')
        self.__shopFont = self.game_engine.get_object('shopFont')
        self.__shopNumFont = self.game_engine.get_object('shopNumFont')
        self.__menuFont= self.game_engine.get_object('menuFont')
        self.add_to_engine()

        self.game_mode = 4
        self.failed = False
        self.fail_key = 0
        self.screen_number = 0
        self.version = "lemonade"

        self.__input_keys = [ITEMS.keys(), ITEMS.keys(),CURRENCY.keys(), \
            [None], MENU, DIFFICULTY, [None]]
        self.__input_mode = [0, 0, 0, 0, 0, 0, 0]
        self.__input_string = []

        for key in self.__input_keys:
            self.__input_string.append(['0'] * len(key))

    @property
    def input(self):
        return self.__input_string

    def currency(self, index):
        """
        Returns the currency key at the specific index

        :type index: int
        :param index: The index of the list
        """
        return CURRENCY.keys()[index]

    def menu_screen(self):
        """
        Loads and changes the background image to the menu screen
        """

        menu = image.load("images/{}/ui/menu.gif".format(\
                self.version)).convert()
        self.__background = transform.scale(menu, (self.game_engine.width,
                                                    self.game_engine.height))

    def difficulty_screen(self):
        """
        Loads and changes the background image to the difficulty screen
        """

        difficulty = image.load("images/{}/ui/difficulty.gif".format(\
                self.version)).convert()
        self.__background = transform.scale(difficulty, (self.game_engine.width,
                                                    self.game_engine.height))

    def change_background(self, weather):
        """
        Loads and changes the background image to the current weather

        :type weather: int
        :param weather: The current weather in game
        """

        bg = image.load("images/{}/field/{}.gif".format(\
            self.version, WEATHER[weather])).convert()

        stand = image.load("images/{}/booth.gif".format(\
            self.version)).convert()

        stand = transform.scale(stand, (self.game_engine.width / 4,
                                                self.game_engine.height / 3))
        bg.blit(stand, (800, 375))
        self.__background = transform.scale(bg, (self.game_engine.width,
                                                 self.game_engine.height))
    
    def tutorial_screen(self):
        """
        Loads and changes the background image to the specific tutorial screen
        """

        tutorial = image.load("images/{}/tutorial/{}.png".format(\
            self.version, self.screen_number)).convert()

        self.__background = transform.scale(tutorial, (self.game_engine.width,
                                                    self.game_engine.height))

    def draw_difficulty(self, key, screen):
        """
        Displays the difficulty screen.

        :type key: int
        :param key: The value of the current difficulty setting selected

        :type screen: Surface
        :param screen: The surface to display difficutly settings on

        """

        # Spacer is the space in between the different difficulty texts
        # Interval is the interval that is added to the spacer after each word
        interval = .1725
        spacer = .3075

        # Loop through and display all the difficulty settings
        for i in range(len(DIFFICULTY)):

            play_difficulty = self.__menuFont.render("{}".format(\
                DIFFICULTY[i]), True, (0, 0, 0))
            fw, fh = play_difficulty.get_size()
            render_left = (self.game_engine.width / 2) - (fw / 2)
            render_top = (self.game_engine.height * spacer) - (fh / 2)
            screen.blit(play_difficulty, (render_left, render_top))

            if key == i:
                cup_icon = image.load("images/{}/cursor/cup.gif".format(\
                    self.version)).convert()
                cup_icon = transform.scale(cup_icon, (
                    self.game_engine.width / 10,
                    self.game_engine.height / 10))
                screen.blit(cup_icon, (self.game_engine.width / 15,
                                        render_top - 10))

            spacer += interval

    def draw_menu(self, key, screen):
        """
        Dispalys the menu screen.

        :type key: int
        :param key: The value of the current menu item selected

        :type screen: Surface
        :param screen: The surface to display menu items on
        """

        # Spacer is the space in between the different difficulty texts
        # Interval is the interval that is added to the spacer after each word
        interval = .17
        spacer = .4

        # Loop through and display all of the menu items
        for i in range(len(MENU)):

            play_menu_item = self.__menuFont.render("{}".format(\
                MENU[i]), True, (0, 0, 0))
            fw, fh = play_menu_item.get_size()
            render_left = (self.game_engine.width / 2) - (fw / 2)
            render_top = (self.game_engine.height * spacer) - (fh / 2)
            screen.blit(play_menu_item, (render_left, render_top))

            # Check if this item is currently selected
            if key == i:
                lemon_icon = image.load("images/{}/cursor/lemon.gif".format(\
                    self.version)).convert()
                lemon_icon = transform.scale(lemon_icon, (
                    self.game_engine.width / 12,
                    self.game_engine.height / 10))
                screen.blit(lemon_icon, (self.game_engine.width / 17,
                                            render_top - 10))

            spacer += interval

    def draw_log(self, messages):
        """
        Displays the daily log

        :type messages: list
        :param messages: The list of messages for the daily log
        """

        text_array = []

        # Add day log to text
        for message in messages:
            text_array.append(message)

        return self._blit_to_block(text_array, (0, 0, 0), (255, 255, 255))

    def ingredient_count(self, items, money):
        # sides are at 650 and 675
        #            /1200    /900
        #            13/24   27/36
        ingredient_block = Surface((self.game_engine.width * 11/24,
                                    self.game_engine.height * 9/36))
        ingredient_block.fill((255, 255, 255))

        icon_size = int(ingredient_block.get_width() / (len(items) * 1.5))
        icon_width = ingredient_block.get_width() / len(items)
        j = icon_size / 3
        render_top = 15 + icon_size
        for name, count in reversed(items.items()):
            icon = image.load("images/{}/icon/{}.gif".format(\
                self.version, name)).convert()
            icon = transform.scale(icon, (icon_size, icon_size))
            ingredient_block.blit(icon, (j, 10))

            # Put an item count under the icon.
            ren = self.__font.render(str(count), True, (0, 0, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            ingredient_block.blit(ren, (render_left, render_top))
            j += icon_width

        ren = self.__font.render("Money: {}".format(\
            format_money(money)), True, (0, 0, 0))
        fw, fh = ren.get_size()
        render_left = ingredient_block.get_width() / 2 - fw / 2
        render_top = (ingredient_block.get_height() - render_top) / 2 + render_top
        ingredient_block.blit(ren, (render_left, render_top))

        return ingredient_block

    def draw_help(self):
        """
        Displays the help text on the tutorial screens.
        """

        # Checks if the player is on the first tutorial sreen
        if self.screen_number == 0:
            info = self._blit_to_block([
                _("Welcome to Lemonade Stand!"),
                _("Here you will get to run your own lemonade stand."),
                _(""),
                _("This is the shop where you will be spending money"),
                _("to buy more supplies to make more lemonade."),
                _(""),
                _("The bottom right hand side of your screen displays"),
                _("your current supplies of each item and how much"),
                _("money you have to spend.")],
                (255, 255, 255),
                (0, 0, 0))

        # Checks if the player is on the second tutorial screen
        elif self.screen_number == 1:
            info = self._blit_to_block([
               _("Above each item, in yellow, displays how much of"),
               _("that item is needed to make one cup of lemonade."),
               _(""),
               _("Below each item, in black, displays how much it"),
               _("costs to buy a specific amount of that item."),
               _(""),
               _("Also below the item, you can type how many of that"),
               _("item you would like to purchase and the color of the"),
               _("text will change from black to white."),
               _(""),
               _("Use the arrow keys to switch between items.")],
               (255, 255, 255),
               (0, 0, 0))

        # Checks if the player is on the third tutorial screen
        elif self.screen_number == 2:
            info = self._blit_to_block([
                _("Here displays the current day's information."),
                _("To the left of the screen is your daily log."),
                _(""),
                _("The daily log displays:"),
                _("- The current day you are on"),
                _("- The current day's weather"),
                _("- The total number of supplies you purchased"),
                _("- How much money you spent in the shop"),
                _("- The total number of cups of lemonade you sold"),
                _("- How much money you made from selling lemonade")],
                (255, 255, 255),
                (0, 0, 0))

        # Checks if the player is on the fourth tutorial screen
        elif self.screen_number == 3:
            info = self._blit_to_block([
                _("This is the profit mini game screen!"),
                _(""),
                _("If you made it to this screen, good job!"),
                _("That means you made a profit during the"),
                _("day and you need to figure out the"),
                _("smallest amount of change you can make"),
                _("out of your profit."),
                _(""),
                _("The top right corner of the screen"),
                _("displays the amount of money you"),
                _("started with, the amount money after"),
                _("buying supplies and selling lemonade,"),
                _("and how much profit you made.")],
                (255, 255, 255),
                (0, 0, 0))

        # Checks if the player is on the fifth tutorial screen
        elif self.screen_number == 4:
            info = self._blit_to_block([
                _("You can switch between values by using"),
                _("the up and down arrow keys."),
                _(""),
                _("The current type of money you have"),
                _("selected will be highlighted by a"),
                _("white box.  While selected, you can"),
                _("enter in a value you think is correct"),
                _("to create the smallest amount of change."),
                _(""),
                _("In this case, 6 dollars and 1 dime would"),
                _("be the smallest amount of change to"),
                _("make $6.10 and then you would continue"),
                _("to the end of the day."),
                _(""),
                _("You will not be able continue to the"),
                _("end of the day until you are correct.")],
                (255, 255, 255),
                (0, 0, 0))

        return info

    def draw(self, screen, tick):

        main = self.game_engine.get_object('main')

        # Check if the user is at the menu screen
        if self.game_mode == 4:
            self.menu_screen()
            screen.blit(self.__background, (0, 0))
            self.draw_menu(self.__input_mode[self.game_mode], screen)
            return

        # Check if the user is at the difficulty screen
        if self.game_mode == 5:
            self.difficulty_screen()
            screen.blit(self.__background, (0, 0))
            self.draw_difficulty(self.__input_mode[self.game_mode], screen)
            return

        # Check if the user is in the tutorial
        if self.game_mode == 6:
            self.tutorial_screen()
            screen.blit(self.__background, (0, 0))
            info = self.draw_help()

            if self.screen_number < 2:
                render_left = 0
                render_top = self.game_engine.height * .64
                screen.blit(info, (render_left, render_top))

            if self.screen_number == 2:
                render_left = 0
                render_top = 0
                screen.blit(info, (render_left, render_top))

            if self.screen_number > 2:
                render_left = self.game_engine.width * .59
                render_top = self.game_engine.height * .47
                screen.blit(info, (render_left, render_top))

            return

        # Check if the user is at the shop
        if self.game_mode == 0:
            store = self.draw_store( \
                self.__input_mode[self.game_mode], main)
            screen.blit(store, (0, 0))

            block = self.ingredient_count(main.resource_list, main.money)
            screen.blit(block, (self.game_engine.width * 13 / 24,
                            self.game_engine.height * 27 / 36))

        # Check if the user is at the mini game screen
        elif self.game_mode == 2:
            cashbox = self.draw_mini_game( \
                self.__input_mode[self.game_mode], main)
            screen.blit(cashbox, (0, 0))

        else:
            self.change_background(main.weather)
            screen.blit(self.__background, (0, 0))

            block = self.draw_log(main.messages)
            screen.blit(block, (0, self.game_engine.height / 3))

            block = self.ingredient_count(main.resource_list, main.money)
            screen.blit(block, (self.game_engine.width * 13 / 24,
                            self.game_engine.height * 27 / 36))

            # Check if there was a random event and the uesr
            # is at the beginning of the day
            if self.game_mode == 1 and main.event_messages != []:
                block = self.draw_random_event_log(main.event_messages)
                screen.blit(block, (0, self.game_engine.height * 9 / 10))

    def draw_random_event_log(self, messages):

        text_array = []

        for message in messages:
            text_array.append(message)

        return self._blit_to_block(text_array)

    def draw_mini_game(self, key, main):
        """
        Displays the profit mini game screen.

        :type key: int
        :param key: The value of the mini game key selected

        :type main: LemonadeMain
        :param main: The main class of Lemonade Stand that contains info
        """

        # Load in the cash box image, covert it, and scale it
        cashbox = image.load("images/{}/cash-box.gif".format(\
            self.version)).convert()
        cashbox = transform.scale(cashbox,
        (self.game_engine.width, self.game_engine.height))

        # Create the spacing and the height and width for
        # the boxs that are used to selecting a value
        spacer = self.game_engine.height / ((len(CURRENCY) - 1)  * 3)
        box_width = (self.game_engine.width / 3) - 10
        box_height = (self.game_engine.height - (len(CURRENCY) + 1) * \
            (spacer)) / (len(CURRENCY))

        space_between = spacer + (self.game_engine.height / 7) - 20

        # Loop through all of the currency values
        for i in range (0, len(CURRENCY)):

            # Create the box
            outline = Surface((box_width, box_height))

            # Set the color to white if selected or black if not
            if key == i:
                color = (255, 255, 255)
            else:
                color = (0, 0, 225)

            outline.fill(color)
            cashbox.blit(outline, ((self.game_engine.width / 4) + 8,
                                    space_between))

            # Display the name of the currency next to its box
            name = self.__shopFont.render(self.currency(i), 1, (0, 0, 0))
            render_left = self.game_engine.width / 15
            cashbox.blit(name, (render_left, space_between + 10))

            # Sets the color of the amount of the currency
            if key == i:
                color = (0, 0, 255)
            else:
                color = (255, 255, 255)

            # Display the amount of the currency within the box
            amount = self.__shopNumFont.render(self.input[2][i], 1, color)
            fw, fh = amount.get_size()
            render_left = ((self.game_engine.width / 4) + 8) + \
                (box_width / 2) - (fw / 2)
            cashbox.blit(amount, (render_left, space_between + 10))

            space_between += (box_height / 2) + spacer

        color = (0, 0, 0)

        # Display current day in the log book
        day_title = self.__shopFont.render("-- Day {} --".format(\
            main.day), 1, color)
        fw, fh = day_title.get_size()
        render_top = self.game_engine.height / 15
        render_left = (self.game_engine.width * 8 / 10) - (fw / 2)
        cashbox.blit(day_title, (render_left, render_top))

        # Display the current day's starting money
        money_start = self.__shopFont.render("Start: {}".format(\
            format_money(main.start_money)), True, (0, 0, 0))
        render_top = self.game_engine.height / 5
        render_left = (self.game_engine.width * 2 / 3)
        cashbox.blit(money_start, (render_left, render_top))

        # Display the current day's ending money
        money_end = self.__shopFont.render("End: {}".format(\
            format_money(main.start_money + main.profit)), True, (0, 0, 0))
        render_top = (self.game_engine.height / 5) + fh + 5
        render_left = (self.game_engine.width * 2 / 3)
        cashbox.blit(money_end, (render_left, render_top))

        # Display the current day's total profit
        profit = self.__shopFont.render("Profit: {}".format(\
            format_money(main.profit)), True, (0, 0, 0))
        render_top = (self.game_engine.height / 5) + (fh * 4) - 20
        render_left = (self.game_engine.width * 2 / 3)
        cashbox.blit(profit, (render_left, render_top))

        # Display if the user passed or failed the mini game
        if self.failed == True:
            if self.__input_mode[2] == self.fail_key:
                fail = self.__shopFont.render("Incorrect!", True, (255, 0, 0))
                fw, fh = fail.get_size()
                render_top = (self.game_engine.height * 6 / 13)
                render_left = (self.game_engine.width * 8 / 10)
                cashbox.blit(fail, (render_left - (fw / 2), render_top))

                try_again = self.__shopFont.render( \
                    "Please try again.", True, (255, 0, 0))
                fw, fh = try_again.get_size()
                cashbox.blit(try_again, (render_left - (fw / 2) , \
                    render_top + fh))

            else:
                self.failed = False

        return cashbox

    def draw_store(self, key, main):
        """
        Displays the store interface

        :type key: int
        :param key: The value of the selected item

        :type main: LemonadeMain
        :param main: The main class of Lemonade Stand that contains info
        """
        store = image.load("images/{}/store-outline.gif".format(\
            self.version)).convert()
        store = transform.scale(store,
        (self.game_engine.width, self.game_engine.height))

        # Store item display.
        spacer = self.game_engine.width / (len(ITEMS) * 4)
        icon_size = (self.game_engine.width - (len(ITEMS)+ 1) * \
                                    (spacer)) / len(ITEMS)
        j = spacer
        # Loop through all of the current items
        for num, name in enumerate(ITEMS):
            outline = Surface((icon_size, icon_size))
            if num == key:
                outline.fill((255, 255, 255))
            else:
                outline.fill((0, 0, 0))
            icon = image.load("images/{}/icon/{}.gif".format(\
                self.version, name)).convert()
            icon = transform.scale(icon,
                    (icon_size * 8 / 10, icon_size * 8 / 10))
            outline.blit(icon, (icon_size / 10, icon_size / 10 ))
            store.blit(outline, (j, self.game_engine.height / 4 - 12))

            # Display pricing info under the item.
            ren = self.__shopFont.render("{} for {}".format(\
                format_money(\
                ITEMS[name]["cost"][main.difficulty] * ITEMS[name]["bulk"]),
                ITEMS[name]["bulk"]), True, (0, 0, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            render_top = self.game_engine.height / 4 + icon_size - 15
            store.blit(ren, (render_left, render_top))

            # Display an item count under the icon.
            if self.__input_string[0][num] != '0':
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)

            ren = self.__shopNumFont.render(self.__input_string[0][num],
                                            1, color)
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            store.blit(ren, (render_left, self.game_engine.height * 6 / 10 - 20))

            # Put the amount of the item needed for the current recipe
            ren = self.__shopNumFont.render("x{}".format(\
                main.current_recipe[name]), 1, (255, 240, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            store.blit(ren, (render_left, self.game_engine.height / 6 - 5))

            j += icon_size + spacer

        # Title above recipe
        ren = self.__shopNumFont.render("Ingredients for {} {}:".format(\
            main.current_recipe['name'], self.version), 1, (255, 240, 0))
        render_left = 5
        render_top = self.game_engine.height / 11
        store.blit(ren, (render_left, render_top))

        # Title above inventory
        ren = self.__shopNumFont.render("Current Supplies:", 1, (255, 240, 0))
        render_left = self.game_engine.width * 8 / 15
        render_top = self.game_engine.height * 7 / 10 - 18
        store.blit(ren, (render_left, render_top))

        return store

    def _blit_to_block(self, text_array, text_color=(0, 0, 0),
                       block_color=(255, 255 ,255)):
        """
        Takes an array of strings with optional text and background colors,
        creates a Surface to house them, blits the text and returns the
        Surface.
        """

        rendered_text = []
        font_width = []
        font_height = []

        for text in text_array:
            ren = self.__font.render(text, True, text_color)
            rendered_text.append(ren)
            fw, fh = ren.get_size()
            font_width.append(fw)
            font_height.append(fh)

        block = Surface((max(font_width) + 20, sum(font_height) + 20))
        block.fill(block_color)

        h = 10
        for text in rendered_text:
            block.blit(text, (10, h))
            h += font_height[0]

        return block

    def event_handler(self, event):
        """
        Responds to any events that happen during the course of the game.
        """

        if event.type == KEYDOWN:
            if event.key in [K_RETURN, K_KP1]:
                # Process Data

                main = self.game_engine.get_object('main')

                # Check if you are in the main menu
                if self.game_mode == 4:

                    # Check if the player chose 'Normal'
                    if self.__input_mode[self.game_mode] == 0:
                        self.game_mode = 5

                    # Check if the player chose 'Challenge'
                    elif self.__input_mode[self.game_mode] == 1:
                        main.challenge = True
                        self.game_mode = 5

                    # Check if the player chose 'Tutorial'
                    elif self.__input_mode[self.game_mode] == 2:
                        self.game_mode = 6

                    return

                # Check if you are in the difficulty settings
                if self.game_mode == 5:
                    main.populate_resources(self.__input_mode[self.game_mode])
                    self.game_mode = 0
                    return

                # Check if the player is watching the tutorial
                if self.game_mode == 6:

                    self.screen_number += 1

                    # Check if the player is done with the tutorial
                    if self.screen_number == 5:
                        self.screen_number = 0
                        self.game_mode = 4

                    return

                item_list = {}
                for i in range(0, len(self.__input_keys[self.game_mode])):
                    item_list[self.__input_keys[self.game_mode][i]] = \
                                int(self.__input_string[self.game_mode][i])
                    self.__input_string[self.game_mode][i] = "0"

                #Checks if you are leaving the shop to begin day
                if self.game_mode == 0:
                    self.game_mode = 1
                    main.update_day_log(item_list)

                #Checks if you are at the beginning of the day
                elif self.game_mode == 1:

                    #Checks if you made profit from the day
                    #If you made profit, sends you to the mini game
                    if (main.process_day_logic()):
                        self.game_mode = 2

                    #If you didn't make profit, sends you to end of the day
                    else:
                        self.game_mode = 3
                        main.process_day_end()

                #Checks if you are doing the profit mini game
                elif self.game_mode == 2:

                    #Checks if you gave the correct amount of change
                    if main.process_change(item_list):
                        self.game_mode = 3
                        main.process_day_end()

                    else:
                        self.failed = True
                        self.fail_key = self.__input_mode[2]

                #Checks if you completed your day, returns you to the shop
                elif self.game_mode == 3:
                    if main.challenge_completed:
                        main.reset_game()
                        self.game_mode = 4

                    else:
                        self.game_mode = 0
                        main.day += 1

            # Checks if the player hit the escape key to quit
            elif event.key == K_ESCAPE:
                self.game_engine.stop_event_loop()

            # Checks if the player hit the backspace key
            elif event.key == K_BACKSPACE:
                handle = self.__input_string[self.game_mode]\
                            [self.__input_mode[self.game_mode]]

                if len(handle) == 1:
                    handle = "0"
                else:
                    handle = handle[0:-1]

                self.__input_string[self.game_mode][self.__input_mode[\
                                    self.game_mode]] = handle

                # Returns you back to the main menu if you are currently in
                # the tutorial, challegne screen, or difficulty selection
                if self.game_mode > 4:
                    self.screen_number = 0
                    self.game_mode = 4

            # Go to the next field
            elif event.key in [K_TAB, K_DOWN, K_RIGHT, K_KP2, K_KP6]:
                self.__input_mode[self.game_mode] = \
                    (self.__input_mode[self.game_mode] + 1) %\
                        len(self.__input_keys[self.game_mode])

            # Go up to previous field
            elif event.key in [K_UP, K_LEFT, K_KP4, K_KP8]:
                self.__input_mode[self.game_mode] = \
                    (self.__input_mode[self.game_mode] - 1) %\
                        len(self.__input_keys[self.game_mode])

            # Text input, only handles numbers (ascii 48 - 58)
            elif event.key >= 48 and event.key <= 58:
                key = str(event.unicode)

                handle = self.__input_string[self.game_mode]\
                    [self.__input_mode[self.game_mode]]

                if handle == "0":
                    handle = key
                else:
                    handle = "{}{}".format(handle, key)

                self.__input_string[self.game_mode][self.__input_mode[\
                    self.game_mode]] = handle

            # Increment
            elif event.key == K_KP9:

                handle = int(self.__input_string[self.game_mode]\
                    [self.__input_mode[self.game_mode]])

                handle += 1

                self.__input_string[self.game_mode][self.__input_mode[\
                    self.game_mode]] = "{}".format(handle)

            # Decrement
            elif event.key == K_KP3:

                handle = int(self.__input_string[self.game_mode]\
                    [self.__input_mode[self.game_mode]])

                if handle > 0:
                    handle -= 1

                self.__input_string[self.game_mode][self.__input_mode[\
                    self.game_mode]] = "{}".format(handle)

        self.game_engine.set_dirty()
