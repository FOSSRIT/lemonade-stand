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

from fortuneengine.GameEngineElement import GameEngineElement
from constants import ITEMS, format_money, WEATHER, CURRENCY
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
        self.__shopNumFontBig = self.game_engine.get_object('shopNumFontBig')
        self.add_to_engine()

        self.game_mode = 0
        self.failed = False
        self.fail_key= 0

        self.__input_keys = [ITEMS.keys(), ITEMS.keys(),CURRENCY.keys(), [None]]
        self.__input_mode = [0, 0, 0, 0]
        self.__input_string = []
        for key in self.__input_keys:
            self.__input_string.append(['0'] * len(key))

    def currency(self, num):
        return CURRENCY.keys()[num]

    @property
    def input(self):
        return self.__input_string

    def splash(self):
        splash = image.load("images/splash.gif")
        self.__background = transform.scale(splash, (self.game_engine.width,
                                                     self.game_engine.height))

    def change_background(self, weather):
        bg = image.load("images/field_%s.gif" % WEATHER[weather]).convert()
        stand = image.load("images/booth.gif").convert()
        bg.blit(stand, (720, 450))
        self.__background = transform.scale(bg, (self.game_engine.width,
                                                 self.game_engine.height))

    def draw_log(self, messages):

        # Add Buy Dialog
        text_array = []
        if self.game_mode == 2:
            text_array.append(_("- How much did you make -"))
            text_array.append("")

            for i in range(0, len(self.__input_keys[self.game_mode])):
                if i == self.__input_mode[self.game_mode]:
                    t = ">"

                else:
                    t = " "

                text_array.append("%s %s: %s" % \
                (t, self.__input_keys[self.game_mode][i],
                self.__input_string[self.game_mode][i]))
            text_array.append("")

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
            icon = image.load("images/icon-%s.gif" % name).convert()
            icon = transform.scale(icon, (icon_size, icon_size))
            ingredient_block.blit(icon, (j, 10))

            # Put an item count under the icon.
            ren = self.__font.render(str(count), True, (0, 0, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            ingredient_block.blit(ren, (render_left, render_top))
            j += icon_width

        ren = self.__font.render("Funds: %s" % format_money(money), True, (0, 0, 0))
        fw, fh = ren.get_size()
        render_left = ingredient_block.get_width() / 2 - fw / 2
        render_top = (ingredient_block.get_height() - render_top) / 2 + render_top
        ingredient_block.blit(ren, (render_left, render_top))

        return ingredient_block

    def draw_help(self):
        main = self.game_engine.get_object('main')

        #Check if the game is currently in the shop
        if self.game_mode == 0:
            block = self._blit_to_block([
                _("Type in the number you want to buy of each item")],
                (255, 255,255), (0, 0, 0))

        elif self.game_mode == 1:
            block = self._blit_to_block([_("This is where you will see how much you spent on each supply,"),
                                        _("how many cups of lemonade you sold, and how much you made.")])

        #Check if the game is currently is in the profit mini game
        elif self.game_mode == 2:
            block = self._blit_to_block([_("You made %s. You need to put your money away for safekeeping." % format_money(main.profit)),
                                         _("Enter the number of dollars, quarters, dimes, nickels, and pennies that you have made.")])

        #Check if the game is currently at the end of the day
        else:
            block = self._blit_to_block([_("Weather can affect the amount of lemonade you sell."),
                                         _("Watch the weather each day to see how it changes sales."),
                                         _("Press Enter to return back to the shop and begin your next day.")])

        return block

    def draw(self, screen, tick):
    
        self.game_engine.set_dirty()
        main = self.game_engine.get_object('main')
        if main.splash:
            self.splash()
            screen.blit(self.__background, (0, 0))
            return

        if self.game_mode == 0:
            store = self.draw_store( \
                self.__input_mode[self.game_mode], main)
            screen.blit(store, (0, 0))

            block = self.ingredient_count(main.resource_list, main.money)
            screen.blit(block, (self.game_engine.width * 13 / 24,
                            self.game_engine.height * 27 / 36))

        elif self.game_mode == 2:
            cashbox = self.draw_mini_game( \
                self.__input_mode[self.game_mode], main)
            screen.blit(cashbox, (0, 0))

        else:
            self.change_background(main.weather)
            screen.blit(self.__background, (0, 0))

            block = self.draw_log(main.messages)
            screen.blit(block, (0, self.game_engine.height / 4))

            block = self.ingredient_count(main.resource_list, main.money)
            screen.blit(block, (self.game_engine.width * 13 / 24,
                            self.game_engine.height * 27 / 36))
        #if main.day == 1:
        #    block = self.draw_help()

         #   if self.game_mode == 0:
          #      width = self.game_engine.width/2 - block.get_width()/2
           #     height = 0

            #    screen.blit(self._blit_to_block([
             #   _("Your mother was nice enough to"),
              #  _("give you a few starting supplies.")],
              #   (255, 255,255), (0, 0, 0)),
               #  (self.game_engine.width / 5,
                # 9 * self.game_engine.height / 10))
           # else:
            #    width = 0
             #   height = self.game_engine.height  / 10

           # screen.blit(block, (width, height))

    def draw_mini_game(self, key, main):

        # Load in the cash box image, covert it, and scale it
        cashbox = image.load("images/cash-box.gif").convert()
        cashbox = transform.scale(cashbox,
        (self.game_engine.width, self.game_engine.height))

        # Create the spacing and the height and width for
        # the boxs that are used to selecting a value
        spacer = self.game_engine.height / ((len(CURRENCY) - 1)  * 3)
        box_width = (self.game_engine.width / 3) - 10
        box_height = (self.game_engine.height - (len(CURRENCY) + 1) * \
            (spacer)) / (len(CURRENCY))

        j = spacer + (self.game_engine.height / 7) - 20

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
            cashbox.blit(outline, ((self.game_engine.width / 4) + 8, j))

            # Display the name of the currency next to its box
            name = self.__shopFont.render(self.currency(i), 1, (0, 0, 0))
            render_left = self.game_engine.width / 15
            cashbox.blit(name, (render_left, j + 10))

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
            cashbox.blit(amount, (render_left, j + 10))

            j += (box_height / 2) + spacer

        color = (0, 0, 0)
        
        # Display current day in the log book
        day_title = self.__shopFont.render("-- Day %s --" % main.day, 1, color)
        fw, fh = day_title.get_size()
        render_top = self.game_engine.height / 15
        render_left = (self.game_engine.width * 8 / 10) - (fw / 2)
        cashbox.blit(day_title, (render_left, render_top))

        # Display the current day's starting money
        money_start = self.__shopFont.render("Start: %s" % \
            format_money(main.start_money), True, (0, 0, 0))
        render_top = self.game_engine.height / 5
        render_left = (self.game_engine.width * 2 / 3)
        cashbox.blit(money_start, (render_left, render_top))

        # Display the current day's ending money
        money_end = self.__shopFont.render("End: %s" % \
            format_money(main.start_money + main.profit), True, (0, 0, 0))
        render_top = (self.game_engine.height / 5) + fh + 5
        render_left = (self.game_engine.width * 2 / 3)
        cashbox.blit(money_end, (render_left, render_top))

        # Display the current day's total profit
        profit = self.__shopFont.render("Profit: %s" % \
            format_money(main.profit), True, (0, 0, 0))
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
        """Draws the store interface, including currently selected items."""

        store = image.load("images/store-outline.gif").convert()
        store = transform.scale(store,
        (self.game_engine.width, self.game_engine.height))

        # Store apron text.
        #block_arr = [Surface((self.game_engine.width / 4, self.game_engine.height / 6))] * 3
        #h = self.game_engine.width * 7 / 24
        #j = self.game_engine.width / 12
        #for num, block in enumerate(block_arr):
        #    store.blit(block, (j, 20))
        #    j += h

        # Store item display.
        spacer = self.game_engine.width / (len(ITEMS) * 4)
        icon_size = (self.game_engine.width - (len(ITEMS)+ 1) * (spacer)) / len(ITEMS)
        j = spacer
        for num, name in enumerate(ITEMS):
            outline = Surface((icon_size, icon_size))
            if num == key:
                outline.fill((255, 255, 255))
            else:
                outline.fill((0, 0, 0))
            icon = image.load("images/icon-%s.gif" % name).convert()
            icon = transform.scale(icon, (icon_size * 8 / 10, icon_size * 8 / 10))
            outline.blit(icon, (icon_size / 10, icon_size / 10 ))
            store.blit(outline, (j, self.game_engine.height / 4 - 12))

            # Put pricing info under the item.
            ren = self.__shopFont.render("%s for %d" % (format_money(ITEMS[name]["cost"] * ITEMS[name]["bulk"]),
                            ITEMS[name]["bulk"]), True, (0, 0, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            store.blit(ren, (render_left, self.game_engine.height / 4 + icon_size - 15))

            # Put an item count under the icon.
            if self.__input_string[0][num] != '0':
                color = (255, 255, 255)
            else:
                color = (0, 0, 0) 

            ren = self.__shopNumFont.render(self.__input_string[0][num], 1, color)
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            store.blit(ren, (render_left, self.game_engine.height * 6 / 10 - 20))

            # Put the amount of the item needed for the current recipe
            ren = self.__shopNumFont.render("x%d" % main.current_recipe[name], 1, (255, 240, 0))
            fw, fh = ren.get_size()
            render_left = j + (icon_size / 2) - (fw / 2)
            store.blit(ren, (render_left, self.game_engine.height / 6 - 5))

            j += icon_size + spacer

        # Title above recipe
        ren = self.__shopNumFont.render("Ingredients for %s lemonade:" % main.current_recipe['name'], 1, (255, 240, 0))
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

                if main.splash:
                    main.splash = not main.splash
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
                    self.game_mode = 0
                    main.day += 1

            elif event.key == K_ESCAPE:
                self.game_engine.stop_event_loop()

            elif event.key == K_BACKSPACE:
                handle = self.__input_string[self.game_mode]\
                            [self.__input_mode[self.game_mode]]

                if len(handle) == 1:
                    handle = "0"
                else:
                    handle = handle[0:-1]

                self.__input_string[self.game_mode][self.__input_mode[\
                                    self.game_mode]] = handle

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
                    handle = "%s%s" % (handle, key)

                self.__input_string[self.game_mode][self.__input_mode[\
                    self.game_mode]] = handle

            # Increment
            elif event.key == K_KP9:

                handle = int(self.__input_string[self.game_mode]\
                    [self.__input_mode[self.game_mode]])

                handle += 1

                self.__input_string[self.game_mode][self.__input_mode[\
                    self.game_mode]] = "%s" % handle

            # Decrement
            elif event.key == K_KP3:

                handle = int(self.__input_string[self.game_mode]\
                    [self.__input_mode[self.game_mode]])

                if handle > 0:
                    handle -= 1

                self.__input_string[self.game_mode][self.__input_mode[\
                    self.game_mode]] = "%s" % handle

        self.game_engine.set_dirty()
