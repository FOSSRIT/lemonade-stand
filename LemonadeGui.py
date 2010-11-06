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
                          K_DOWN, K_UP, K_ESCAPE,\
                          K_KP1, K_KP2, K_KP3, K_KP8, K_KP9


class LemonadeGui(GameEngineElement):

    def __init__(self):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.__font = self.game_engine.get_object('font')
        self.add_to_engine()

        self.game_mode = 0

        self.__input_keys = [ITEMS.keys(), CURRENCY.keys(), []]
        self.__input_mode = [0, 0]
        self.__input_string = []
        self.__input_string.append(['0'] * len(self.__input_keys[0]))
        self.__input_string.append(['0'] * len(self.__input_keys[1]))

    def change_background(self, weather):
        bg = image.load("images/field_%s.gif" % WEATHER[weather]).convert()
        stand = image.load("images/booth.gif").convert()
        bg.blit(stand, (720, 450))
        self.__background = transform.scale(bg, (self.game_engine.width,
                                                 self.game_engine.height))

    def draw_log(self, messages, day_no):
        # Add Buy Dialog
        text_array = []
        if self.game_mode == 0:
            text_array.append(_("- Buy Options  -"))
        elif self.game_mode == 1:
            text_array.append(_("- How much did you make -"))

        for i in range(0, len(self.__input_keys[self.game_mode])):
            if i == self.__input_mode[self.game_mode]:
                t = ">"

            else:
                t = " "

            if self.game_mode == 0:
                text_array.append(_("%s %s(%d @ %s each): %s") % \
                 (t, ITEMS[self.__input_keys[0][i]]['name'],
                 ITEMS[self.__input_keys[0][i]]['bulk'],
                 format_money(\
                    ITEMS[self.__input_keys[0][i]]['cost']),
                self.__input_string[0][i]))
            else:
                text_array.append("%s %s: %s" % \
                (t, self.__input_keys[self.game_mode][i],
                self.__input_string[self.game_mode][i]))


        # Add day log to text
        text_array.append("")
        text_array.append(_("- Day %s Log -" % day_no))
        for message in messages:
            text_array.append(message)
        
        return self._blit_to_block(text_array, (0, 0, 0), (255, 255, 255))

    def data_block(self, main):
        text_arr = [
            _("Weather: %s") % WEATHER[main.weather]]

        # Add Lemonade Recipe
        text_arr.append("")
        text_arr.append(_("- Recipe -"))

        for item_key in ITEMS:
            text_arr.append("   %s: %d" % \
                (ITEMS[item_key]['name'], main.recipe(item_key)))

        return self._blit_to_block(text_arr)

    def ingredient_count(self, items, money):
        # sides are at 650 and 675
        #            /1200    /900
        #            13/24   27/36
        ingredient_block = Surface((self.game_engine.width * 11/24,
                                    self.game_engine.height * 9/36))
        ingredient_block.fill((0, 0, 255))
        
        icon_size = int(ingredient_block.get_width() / (len(items) * 1.5))
        icon_width = ingredient_block.get_width() / len(items)
        j = icon_size / 3
        render_top = 15 + icon_size
        for name, count in items.items():
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

    def draw(self, screen, tick):
        main = self.game_engine.get_object('main')
        self.change_background(main.weather)
        screen.blit(self.__background, (0, 0))

        block = self.data_block(main)
        screen.blit(block, (10, 10))

        block = self.draw_log(main.messages, main.day)
        screen.blit(block, (0, self.game_engine.height * 4 / 9))

        block = self.ingredient_count(main.resource_list, main.money)
        screen.blit(block, (self.game_engine.width * 13 / 24,
                            self.game_engine.height * 27 / 36))

    def _blit_to_block(self, text_array, text_color=(255, 255, 255),
                       block_color=(0, 0, 0)):
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

                item_list = {}
                for i in range(0, len(self.__input_keys[self.game_mode])):
                    item_list[self.__input_keys[self.game_mode][i]] = \
                                int(self.__input_string[self.game_mode][i])
                    self.__input_string[self.game_mode][i] = "0"
                main = self.game_engine.get_object('main')
                if self.game_mode == 0:

                    #Will return true if go to profit game
                    if(main.process_day_logic(item_list)):
                        self.game_mode = 1
                    else:
                        self.game_mode = 2

                elif self.game_mode == 1:
                    mini_game_success = main.process_change(item_list)
                    if mini_game_success:
                        main.process_day_end()
                        self.game_mode = 2

                elif self.game_mode == 2:
                    self.game_mode = 0

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
            elif event.key in [K_TAB, K_DOWN, K_KP2]:
                self.__input_mode[self.game_mode] = \
                    (self.__input_mode[self.game_mode] + 1) %\
                        len(self.__input_keys[self.game_mode])

            # Go up to previous field
            elif event.key in [K_UP, K_KP8]:
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
                    self.game_mode]] = handle

            # Decrement
            elif event.key == K_KP3:

                handle = int(self.__input_string[self.game_mode]\
                    [self.__input_mode[self.game_mode]])
                
                if handle > 0:
                    handle -= 1

                self.__input_string[self.game_mode][self.__input_mode[\
                    self.game_mode]] = handle

            self.game_engine.set_dirty()
