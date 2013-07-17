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
import pygame
from fortuneengine.GameEngineElement import GameEngineElement
from constants import ITEMS, format_money, WEATHER, CURRENCY, DIFFICULTY,\
    MENU, UPGRADES, RECIPES, LANGUAGE

from gettext import gettext as _
import gettext
lang = gettext.translation('Lemonade', '/usr/share/locale/', languages = ['es'])
_ = lang.ugettext
from pygame import Surface, transform, image
from pygame.locals import KEYDOWN, K_RETURN, K_BACKSPACE, K_TAB, \
    K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, \
    K_KP1, K_KP2, K_KP3, K_KP4, K_KP6, K_KP8, \
    K_KP9, K_SPACE


class LemonadeGui(GameEngineElement):

    def __init__(self):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.__font = self.game_engine.get_object('font')
        self.__shopFont = self.game_engine.get_object('shopFont')
        self.__shopNumFont = self.game_engine.get_object('shopNumFont')
        self.__menuFont = self.game_engine.get_object('menuFont')
        self.add_to_engine()

        self.main = self.game_engine.get_object('main')

        self.game_mode = 8
        self.failed = False
        self.fail_key = 0
        self.screen_number = 0
        self.version = self.main.version
		self.version_name = _(self.version)
        self.__input_keys = [ITEMS[self.version].keys(),
                             ITEMS[self.version].keys(), CURRENCY.keys(),
                             RECIPES[self.version].keys(), MENU, DIFFICULTY,
                             [None], UPGRADES[self.version], LANGUAGE]
        self.__input_mode = [0, 0, 0, 0, 0, 0, 0, 0, 0]
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

        menu = image.load("images/{}/ui/menu.gif".format(
            self.version)).convert()
        self.__background = transform.scale(menu, (self.game_engine.width,
                                                   self.game_engine.height))

    def language_screen(self):
        """
        Loads and changes the background image to the language screen
        """

        language = image.load("images/{}/ui/menu.gif".format(
            self.version)).convert()
        self.__background = transform.scale(language,
                                            (self.game_engine.width,
                                             self.game_engine.height))

    def difficulty_screen(self):
        """
        Loads and changes the background image to the difficulty screen
        """

        difficulty = image.load("images/{}/ui/difficulty.gif".format(
            self.version)).convert()
        self.__background = transform.scale(difficulty,
                                            (self.game_engine.width,
                                             self.game_engine.height))

    def change_background(self, weather):
        """
        Loads and changes the background image to the current weather

        :type weather: int
        :param weather: The current weather in game
        """

        bg = image.load("images/{}/field/{}.gif".format(
            self.version, WEATHER[weather])).convert()

        stand = image.load("images/{}/booth.gif".format(
            self.version)).convert()

        bg.blit(stand, (850, 315))
        self.__background = transform.scale(bg, (self.game_engine.width,
                                                 self.game_engine.height))

    def tutorial_screen(self):
        """
        Loads and changes the background image to the specific tutorial screen
        """

        tutorial = image.load("images/{}/tutorial/{}.png".format(
            self.version, self.screen_number)).convert()

        self.__background = transform.scale(tutorial,
                                            (self.game_engine.width,
                                             self.game_engine.height))

    def upgrade_screen(self):
        """
        Loads and changes the background image to the specfic upgrade screen
        """

        upgrade = image.load("images/{}/upgrades/upgrades.png".format(
            self.version)).convert()
        self.__background = transform.scale(upgrade, (self.game_engine.width,
                                                      self.game_engine.height))

    def draw_upgrade(self, key, screen):
        """
        Displays the upgrade shop screen.

        :type key: int
        :param key: The value of the current upgrade selected

        :type screen: Surface
        :param screen: The surface to display the ugrades on
        """

        # Spacer is the space in between the different difficulty texts
        # Interval is the interval that is added to the spacer after each word
        interval = .15
        spacer = .3

        for i in range(len(self.__input_keys[self.game_mode])):

            # Draws the name of the upgrade
            upgrade_name = self.__shopFont.render(_("{}").format(
                UPGRADES[self.version][i]['name']), True, (0, 0, 0))
            fw, fh = upgrade_name.get_size()
            render_left = (self.game_engine.width * .075)
            render_top = (self.game_engine.height * spacer) - (fh / 2)
            screen.blit(upgrade_name, (render_left, render_top))

            # Draws the cost of the upgrade
            upgrade_cost = self.__shopFont.render(_("{}").format(
                format_money(UPGRADES[self.version][i]['cost'] +
                             UPGRADES[self.version][i]['cost'] * 1.5 *
                             self.main.upgrades[1]['level'][i])),
                True, (0, 0, 0))
            fw, fh = upgrade_cost.get_size()
            render_left = (self.game_engine.width * .375) - (fw / 2)
            screen.blit(upgrade_cost, (render_left, render_top))

            # Draws the level of the upgrade
            upgrade_level = self.__shopFont.render(_("{}").format(
                UPGRADES[self.version][i]['level'] +
                self.main.upgrades[1]['level'][i]),
                True, (0, 0, 0))
            fw, fh = upgrade_level.get_size()
            render_left = (self.game_engine.width * .62) - (fw / 2)
            screen.blit(upgrade_level, (render_left, render_top))

            # Displays a cursor next to the selected upgrade
            if key == i:
                lemon_icon = image.load("images/{}/cursor/lemon.gif".format(
                    self.version)).convert()
                lemon_icon = transform.scale(lemon_icon, (
                    self.game_engine.width / 17,
                    self.game_engine.height / 15))
                iw, ih = lemon_icon.get_size()
                render_left = (self.game_engine.width * .005)
                screen.blit(lemon_icon, (render_left, render_top - (iw / 6)))

            # Draws the info for the upgrade
            level = self.main.upgrades[1]['level'][i]
            if level > (len(self.main.upgrades[1]['level']) - 1):
                level = len(self.main.upgrades[1]['level']) - 1

            top_buffer = len(UPGRADES[self.version][i]['info'][level]) / 2
            if top_buffer < 1:
                top_buffer = 0

            render_top = render_top - fw * top_buffer
            for line in UPGRADES[self.version][i]['info'][level]:
                upgrade_info = self.__font.render(_("{}").format(
                    line), True, (0, 0, 0))
                fw, fh = upgrade_info.get_size()
                render_left = (self.game_engine.width * .77)
                screen.blit(upgrade_info, (render_left, render_top))
                render_top += fh

            spacer += interval

        # Draw the item name tab
        item_name = self.__menuFont.render(_("Name"), True, (0, 0, 0))
        fw, fh = item_name.get_size()
        render_left = (self.game_engine.width * .14) - (fw / 2)
        render_top = (self.game_engine.height * .075) - (fh / 2)
        screen.blit(item_name, (render_left, render_top))

        # Draw the item cost tab
        item_cost = self.__menuFont.render(_("Cost"), True, (0, 0, 0))
        fw, fh = item_cost.get_size()
        render_left = (self.game_engine.width * .375) - (fw / 2)
        screen.blit(item_cost, (render_left, render_top))

        # Draw the item level tab
        item_level = self.__menuFont.render(_("Level"), True, (0, 0, 0))
        fw, fh = item_level.get_size()
        render_left = (self.game_engine.width * .62) - (fw / 2)
        screen.blit(item_level, (render_left, render_top))

        # Draw the item info tab
        item_info = self.__menuFont.render(_("Info"), True, (0, 0, 0))
        fw, fh = item_info.get_size()
        render_left = (self.game_engine.width * .855) - (fw / 2)
        screen.blit(item_info, (render_left, render_top))

        # Draw the player's money
        player_money = self.__shopFont.render(_("Money: {}".format(
            format_money(self.main.money))), True, (0, 0, 0))
        fw, fh = player_money.get_size()
        render_left = (self.game_engine.width * .15) - (fw / 2)
        render_top = (self.game_engine.height * .9) - (fh / 2)
        screen.blit(player_money, (render_left, render_top))

    def draw_language(self, key, screen):
        """
        Displays the language screen.

        :type key: int
        :param key: The value of the current language setting selected

        :type screen: Surface
        :param screen: The surface to display language settings on
        """

        # Spacer is the space in between the different difficulty texts
        # Interval is the interval that is added to the spacer after each word
        interval = .1725
        spacer = .3075

        for i in range(len(LANGUAGE)):

            language = self.__menuFont.render("{}".format(
                LANGUAGE[i]), True, (0, 0, 0))
            fw, fh = language.get_size()
            render_left = (self.game_engine.width / 2) - (fw / 2)
            render_top = (self.game_engine.width * spacer) - (fh / 2)
            screen.blit(language, (render_left, render_top))

            if key == i:
                cup_icon = image.load("images/{}/cursor/cup.gif".format(
                    self.version)).convert()
                cup_icon = transform.scale(cup_icon, (
                    self.game_engine.width / 10,
                    self.game_engine.height / 10))
                screen.blit(cup_icon, (self.game_engine.width / 15,
                                       render_top - 10))

            spacer += interval

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

            play_difficulty = self.__menuFont.render(
                DIFFICULTY[i].decode('utf8'), True, (0, 0, 0))
            fw, fh = play_difficulty.get_size()
            render_left = (self.game_engine.width / 2) - (fw / 2)
            render_top = (self.game_engine.height * spacer) - (fh / 2)
            screen.blit(play_difficulty, (render_left, render_top))

            if key == i:
                cup_icon = image.load("images/{}/cursor/cup.gif".format(
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
            menu_item = MENU[i]
            menu_item = menu_item.decode('utf8')
            play_menu_item = self.__menuFont.render(menu_item, True, (0, 0, 0))
            fw, fh = play_menu_item.get_size()
            render_left = (self.game_engine.width / 2) - (fw / 2)
            render_top = (self.game_engine.height * spacer) - (fh / 2)
            screen.blit(play_menu_item, (render_left, render_top))

            # Check if this item is currently selected
            if key == i:
                lemon_icon = image.load("images/{}/cursor/lemon.gif".format(
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

        main = self.game_engine.get_object('main')
        text_array = []

        # Add day log to text
        for message in messages:
            text_array.append(message)

        return self._blit_to_block(text_array,
                                   (0, 0, 0),
                                   (255, 255, 255),
                                   False)

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
            icon = image.load("images/{}/icon/{}.gif".format(
                self.version, name)).convert()
            icon = transform.scale(icon, (icon_size, icon_size))
            ingredient_block.blit(icon, (j, 10))

            # Put an item count under the icon.
            ren = self.__font.render(str(count), True, (0, 0, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            ingredient_block.blit(ren, (render_left, render_top))
            j += icon_width

        ren = self.__font.render(_("Money: {}").format(
            format_money(money)), True, (0, 0, 0))
        fw, fh = ren.get_size()
        render_left = ingredient_block.get_width() / 2 - fw / 2
        render_top = (ingredient_block.get_height() -
                      render_top) / 2 + render_top
        ingredient_block.blit(ren, (render_left, render_top))

        return ingredient_block

    def draw_help(self):
        """
        Displays the help text on the tutorial screens.
        """

        # Checks if the player is on the first tutorial sreen
        if self.screen_number == 0:
            info = self._blit_to_block(
                _("""Welcome to Lemonade Stand!
Here you will get to run your own lemonade stand.

This is the shop where you will be spending money
to buy more supplies to make more lemonade.

The bottom right hand side of your screen displays
your current supplies of each item and how much
money you have to spend."""),
                (255, 255, 255),
                (0, 0, 0))

        # Checks if the player is on the second tutorial screen
        elif self.screen_number == 1:
            info = self._blit_to_block(
                _("""Above each item, in yellow, displays how much of
that item is needed to make one cup of lemonade.

Below each item, in black, displays how much it
costs to buy a specific amount of that item.

Also below the item, you can type how many of that
item you would like to purchase and the color of the
text will change from black to white.

Use the arrow keys to switch between items."""),
                (255, 255, 255),
                (0, 0, 0))

        # Checks if the player is on the third tutorial screen
        elif self.screen_number == 2:
            info = self._blit_to_block(
                _("""Here displays the current day's information.
To the left of the screen is your daily log.

The daily log displays:
- The current day you are on
- The current day's weather
- The total number of supplies you purchased
- How much money you spent in the shop
- The total number of cups of lemonade you sold
- How much money you made from selling lemonade"""),
                (255, 255, 255),
                (0, 0, 0))

        # Checks if the player is on the fourth tutorial screen
        elif self.screen_number == 3:
            info = self._blit_to_block(
                _("""This is the profit mini game screen!

If you made it to this screen, good job!
That means you made a profit during the
day and you need to figure out the
smallest amount of change you can make
out of your profit.

The top right corner of the screen
displays the amount of money you
started with, the amount money after
buying supplies and selling lemonade
and how much profit you made."""),
                (255, 255, 255),
                (0, 0, 0))

        # Checks if the player is on the fifth tutorial screen
        elif self.screen_number == 4:
            info = self._blit_to_block(
                _("""You can switch between values by using
the up and down arrow keys.

The current type of money you have
selected will be highlighted by a
white box.  While selected, you can
enter in a value you think is correct
to create the smallest amount of change.

In this case, 6 dollars and 1 dime would
be the smallest amount of change to
make $6.10 and then you would continue
to the end of the day.

You will not be able continue to the
end of the day until you are correct."""),
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

        # Check if the user is at the difficulty screen
        elif self.game_mode == 5:
            self.difficulty_screen()
            screen.blit(self.__background, (0, 0))
            self.draw_difficulty(self.__input_mode[self.game_mode], screen)

        # Check if the user is in the tutorial
        elif self.game_mode == 6:
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

        # Check if the player is in the upgrade shop
        elif self.game_mode == 7:
            self.upgrade_screen()
            screen.blit(self.__background, (0, 0))
            self.draw_upgrade(self.__input_mode[self.game_mode], screen)

        # Check if the player is in the language selection screen
        elif self.game_mode == 8:
            self.language_screen()
            screen.blit(self.__background, (0, 0))
            self.draw_language(self.__input_mode[self.game_mode], screen)

        # Check if the player is at the shop
        elif self.game_mode == 0:
            store = self.draw_store(
                self.__input_mode[self.game_mode], main)
            screen.blit(store, (0, 0))

            block = self.ingredient_count(main.resource_list, main.money)
            screen.blit(block, (self.game_engine.width * 13 / 24,
                                self.game_engine.height * 27 / 36))

        # Check if the player is at the beginning of the day
        elif self.game_mode == 1:
            self.change_background(main.weather)
            screen.blit(self.__background, (0, 0))

            block = self.draw_log(main.messages)
            screen.blit(block, (0, self.game_engine.height / 3))

            block = self.ingredient_count(main.resource_list, main.money)
            screen.blit(block, (self.game_engine.width * 13 / 24,
                                self.game_engine.height * 27 / 36))

            # Check if there was a random event
            if main.event_messages != []:
                block = self.draw_random_event_log(main.event_messages)
                screen.blit(block, (0, self.game_engine.height * 9 / 10))

        # Check if the player is at the mini game screen
        elif self.game_mode == 2:
            cashbox = self.draw_mini_game(
                self.__input_mode[self.game_mode], main)
            screen.blit(cashbox, (0, 0))

        else:
            self.change_background(main.weather)
            screen.blit(self.__background, (0, 0))

            block = self.draw_log(main.messages)
            screen.blit(block, (0, self.game_engine.height * .5))

            block = self.ingredient_count(main.resource_list, main.money)
            screen.blit(block, (self.game_engine.width * 13 / 24,
                                self.game_engine.height * 27 / 36))

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
        cashbox = image.load("images/{}/cash-box.gif".format(
            self.version)).convert()
        cashbox = transform.scale(cashbox,
                                  (self.game_engine.width,
                                   self.game_engine.height))

        # Create the spacing and the height and width for
        # the boxs that are used to selecting a value
        spacer = self.game_engine.height / ((len(CURRENCY) - 1) * 3)
        box_width = (self.game_engine.width / 3) - 10
        box_height = (self.game_engine.height - (len(CURRENCY) + 1) *
                      (spacer)) / (len(CURRENCY))

        space_between = spacer + (self.game_engine.height / 7) - 20

        # Loop through all of the currency values
        for i in range(0, len(CURRENCY)):

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
            render_left = (((self.game_engine.width / 4) + 8) +
                           (box_width / 2) - (fw / 2))

            cashbox.blit(amount, (render_left, space_between + 10))

            space_between += (box_height / 2) + spacer

        color = (0, 0, 0)

        # Display current day in the log book
        day_title = self.__shopFont.render(_("-- Day {} --").format(
            main.day), 1, color)
        fw, fh = day_title.get_size()
        render_top = self.game_engine.height / 15
        render_left = (self.game_engine.width * 8 / 10) - (fw / 2)
        cashbox.blit(day_title, (render_left, render_top))

        # Display the current day's starting money
        money_start = self.__shopFont.render(_("Start: {}").decode('utf8').format(\
            format_money(main.start_money)), True, (0, 0, 0))
        render_top = self.game_engine.height / 5
        render_left = (self.game_engine.width * 2 / 3)
        cashbox.blit(money_start, (render_left, render_top))

        # Display the current day's ending money
        money_end = self.__shopFont.render(_("End: {}").decode('utf8').format(\
            format_money(main.start_money + main.profit)), True, (0, 0, 0))
        render_top = (self.game_engine.height / 5) + fh + 5
        render_left = (self.game_engine.width * 2 / 3)
        cashbox.blit(money_end, (render_left, render_top))

        # Display the current day's total profit
        if main.difficulty < 2:
            profit = self.__shopFont.render(_("Profit: {}").decode('utf8').format(\
                format_money(main.profit)), True, (0, 0, 0))
            render_top = (self.game_engine.height / 5) + (fh * 4) - 20
            render_left = (self.game_engine.width * 2 / 3)
            cashbox.blit(profit, (render_left, render_top))

        # Display if the user passed or failed the mini game
        if self.failed:
            if self.__input_mode[2] == self.fail_key:
                fail = self.__shopFont.render(_("Incorrect!").decode('utf8'), True, (255, 0, 0))
                fw, fh = fail.get_size()
                render_top = (self.game_engine.height * 6 / 13)
                render_left = (self.game_engine.width * 8 / 10)
                cashbox.blit(fail, (render_left - (fw / 2), render_top))

                try_again = self.__shopFont.render( \
                    _("Please try again.").decode('utf8'), True, (255, 0, 0))
                fw, fh = try_again.get_size()
                cashbox.blit(try_again, (render_left - (fw / 2),
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
        store = image.load("images/{}/store-outline.gif".format(
            self.version)).convert()
        store = transform.scale(store,
                                (self.game_engine.width,
                                self.game_engine.height))

        # Store item display.
        spacer = self.game_engine.width / ((len(main.current_recipe) - 2) * 4)
        icon_size = (self.game_engine.width - (len(main.current_recipe) - 2) *
                     (3 * spacer) / 2) / (len(main.current_recipe) - 2)
        j = spacer

        # Loop through all of the current items
        for num, name in enumerate(ITEMS[self.version]):
            outline = Surface((icon_size, icon_size))
            if num == key:
                outline.fill((255, 255, 255))
            else:
                outline.fill((0, 0, 0))
            icon = image.load("images/{}/icon/{}.gif".format(
                self.version, name)).convert()
            icon = transform.scale(icon,
                                   (icon_size * 8 / 10, icon_size * 8 / 10))
            icon_render_top = self.game_engine.height * .38 - (icon_size / 2)
            outline.blit(icon, (icon_size / 10, icon_size / 10))
            store.blit(outline, (j, icon_render_top))

            # Display pricing info under the item.
            ren = self.__shopFont.render(_("{} for {}").format(
                format_money(
                    ITEMS[self.version][name]["cost"][main.difficulty] *
                    ITEMS[self.version][name]["bulk"]),
                ITEMS[self.version][name]["bulk"]), True, (0, 0, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            render_top = icon_render_top + icon_size + (fh / 10)
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
            store.blit(ren, (render_left, self.game_engine.height * .58))

            # Put the amount of the item needed for the current recipe
            ren = self.__shopNumFont.render(_("x{}").format(
                main.current_recipe[name]), 1, (255, 240, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            render_top = icon_render_top - fh
            store.blit(ren, (render_left, render_top))

            j += icon_size + spacer

        # Draw the player's upgrades
        spacer = .1
        interval = .15

        for index in range(0, self.main.upgrades[0]):
            if self.main.upgrades[1]['level'][index] > 0:
                icon_size = self.game_engine.width / 15
                icon = image.load("images/{}/upgrades/{}.gif".format(
                    self.version,
                    self.main.upgrades[1]['name'][index]))
                icon = transform.scale(icon, (icon_size, icon_size))
                render_left = self.game_engine.width * spacer - (icon_size / 2)
                render_left_icon = render_left - (icon_size / 2)
                render_top = self.game_engine.height * .7
                store.blit(icon, (render_left_icon, render_top))

                upgrade_level = self.__font.render(_("Level: {}".format(
                    self.main.upgrades[1]['level'][index])), True, (0, 0, 0))
                fw, fh = upgrade_level.get_size()
                render_left_level = render_left - (fw / 2)
                render_top = render_top + icon_size
                store.blit(upgrade_level, (render_left_level, render_top))

                upgrade_capacity = self.__font.render(_("Capacity: {}".format(
                    self.main.upgrades[1]['capacity'][index])),
                    True, (0, 0, 0))
                fw, fh = upgrade_capacity.get_size()
                render_left_capacity = render_left - (fw / 2)
                render_top = render_top + (fh / 2) + 10
                store.blit(upgrade_capacity,
                           (render_left_capacity, render_top))

                spacer += interval

        # Title above recipe
        ren = self.__shopNumFont.render(_("Ingredients for ") + \
            self.version_name + " " + \
            main.current_recipe['name'].decode('utf8') \
            + ":", 1, (255, 240, 0))
        render_left = 5
        render_top = self.game_engine.height / 11
        store.blit(ren, (render_left, render_top))

        # Title above inventory
        ren = self.__shopNumFont.render(_("Current Supplies:"), 1, (255, 240, 0))
        render_left = self.game_engine.width * 8 / 15
        render_top = self.game_engine.height * .68
        store.blit(ren, (render_left, render_top))

        return store

    def _blit_to_block(self, text_array, text_color=(0, 0, 0),
                       block_color=(255, 255 ,255), fill_block=True):
        """
        Takes an array of strings with optional text and background colors,
        creates a Surface to house them, blits the text and returns the
        Surface.
        """

        rendered_text = []
        font_width = []
        font_height = []

        if isinstance(text_array, basestring):
            text_array = text_array.split('\n')

        for text in text_array:
            try:
                ren = self.__font.render(text.decode('utf8'), True, text_color)
            except UnicodeEncodeError:
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

                # Check if the player is in the main menu
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

                # Check if the player is in the difficulty settings
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

                if self.game_mode == 7:
                    upgrade_info = []
                    for i in range(0, len(self.__input_keys[self.game_mode])):
                        if i == self.__input_mode[self.game_mode]:
                            upgrade_info.append(UPGRADES
                                                [self.version][i]['name'])
                            upgrade_info.append(UPGRADES
                                                [self.version][i]['cost'])
                            upgrade_info.append(UPGRADES
                                                [self.version][i]['capacity'])
                else:
                    item_list = {}
                    for i in range(0, len(self.__input_keys[self.game_mode])):
                        item_list[self.__input_keys[self.game_mode][i]] = \
                            int(self.__input_string[self.game_mode][i])
                        self.__input_string[self.game_mode][i] = "0"

                #Checks if the player is leaving the shop to begin day
                if self.game_mode == 0:
                    self.game_mode = 1
                    main.update_day_log(item_list)

                # Checks if the player is at the beginning of the day
                elif self.game_mode == 1:

                    # Sends the player to the profit mini game if profit
                    if (main.process_day_logic()):
                        self.game_mode = 2

                    # Sends the player to the end of the day if no profit
                    else:
                        self.game_mode = 3
                        main.process_day_end()

                # Checks if the player is doing the profit mini game
                elif self.game_mode == 2:

                    # Checks if the player gave the correct amount of change
                    if main.process_change(item_list):
                        self.game_mode = 3
                        main.process_day_end()

                    else:
                        self.failed = True
                        self.fail_key = self.__input_mode[self.game_mode]

                # Checks if the player completed the day, return to the shop
                # Saves recipe choice before returning to the shop
                elif self.game_mode == 3:
                    if main.challenge_completed:
                        main.reset_game()
                        self.game_mode = 4

                    else:
                        main.current_recipe = RECIPES[self.version][ \
                            self.__input_keys[self.game_mode][ \
                            self.__input_mode[self.game_mode]]]
                        main.prices = main.current_recipe['cost']
                        self.game_mode = 0
                        main.day += 1

                # Checks if the player is in the upgrade shop
                elif self.game_mode == 7:
                    if main.process_buy_upgrade(upgrade_info):
                        return

                # Checks if the player is in language selection
                elif self.game_mode == 8:
                    self.game_mode = 4

            # Checks if the player hit space to enter the upgrade shop
            elif event.key == K_SPACE and self.game_mode == 0:
                self.game_mode = 7

            # Checks if the player hit the escape key to quit
            elif event.key == K_ESCAPE:
                self.game_engine.stop_event_loop()

            # Checks if the player hit the backspace key
            elif event.key == K_BACKSPACE:
                handle = self.__input_string[
                    self.game_mode][
                        self.__input_mode[self.game_mode]]

                if len(handle) == 1:
                    handle = "0"
                else:
                    handle = handle[0:-1]

                self.__input_string[
                    self.game_mode][self.__input_mode[self.game_mode]] = handle

                # Returns you back to the main menu if you are currently in
                # the tutorial, challegne screen, or difficulty selection
                if self.game_mode > 4 and self.game_mode != 7:
                    self.screen_number = 0
                    self.game_mode = 4

                # Returns the player back to the shop from the upgrades shop
                if self.game_mode == 7:
                    self.game_mode = 0

            # Go to the next field
            elif event.key in [K_TAB, K_DOWN, K_RIGHT, K_KP2, K_KP6]:
                self.__input_mode[self.game_mode] = \
                    ((self.__input_mode[self.game_mode] + 1) %
                     len(self.__input_keys[self.game_mode]))

            # Go up to previous field
            elif event.key in [K_UP, K_LEFT, K_KP4, K_KP8]:
                self.__input_mode[self.game_mode] = \
                    ((self.__input_mode[self.game_mode] - 1) %
                     len(self.__input_keys[self.game_mode]))

            # Text input, only handles numbers (ascii 48 - 58)
            elif event.key >= 48 and event.key <= 58:
                key = str(event.unicode)

                handle = self.__input_string[
                    self.game_mode][self.__input_mode[self.game_mode]]

                if handle == "0":
                    handle = key
                else:
                    handle = "{}{}".format(handle, key)

                self.__input_string[
                    self.game_mode][self.__input_mode[self.game_mode]] = handle

            # Increment
            elif event.key == K_KP9:

                handle = int(self.__input_string[self.game_mode]
                             [self.__input_mode[self.game_mode]])

                handle += 1

                self.__input_string
                [self.game_mode]
                [self.__input_mode[self.game_mode]] = "{}".format(handle)

            # Decrement
            elif event.key == K_KP3:

                handle = int(self.__input_string[self.game_mode]
                             [self.__input_mode[self.game_mode]])

                if handle > 0:
                    handle -= 1

                self.__input_string[self.game_mode][self.__input_mode[
                    self.game_mode]] = "{}".format(handle)

        self.game_engine.set_dirty()
