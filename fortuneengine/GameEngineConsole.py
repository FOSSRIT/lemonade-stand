#    FortuneEngine is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    FortuneEngine is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with the FortuneEngine.  If not, see <http://www.gnu.org/licenses/>.
#
#    Author: Justin Lewis  <jlew.blackout@gmail.com>

from pyconsole.pyconsole import Console


class GameEngineConsole(Console):
    """
    GameEngineConsole is a class that extends the pyconsole adding
    in game engine specific functions.
    """

    def __init__(self, gei, pos):
        """
        Init function of the GameEngineConsole

        @param gei:     Passing in the Game Engine Instance.
        @param pos:     The position tuple to place the pyconsole
                        (startx, starty, width, height)
        """
        # functions exposed to the console
        function_list = {
            "quit": gei.stop_event_loop,

            "list_objects": gei.list_objects,
            "list_drawcb": gei.list_draw_callbacks,
            "list_eventcb": gei.list_event_callbacks,
            "list_timers": gei.list_event_timers,
            "inspect": gei._inspector.inspect_object,

            "profile_draw":gei.list_draw_time,
            "profile_event":gei.list_event_time,
            "profile_timer":gei.list_timer_time,

            "set_str": gei._inspector.set_str,
            "set_int": gei._inspector.set_int,
            "set_eval": gei._inspector.set_eval,

            "fps": gei.toggle_fps,
        }

        # Ctrl + key mappings
        key_calls = {
            "d": gei.stop_event_loop,
            "m": self.console_mode,
        }

        # Call parent class's init function passing in the
        # function and key mapping dictionaries
        Console.__init__(self, gei.screen, pos,
                           functions=function_list, key_calls=key_calls,
                           vars={}, syntax={})

    def console_mode(self):
        """
        Switches console between console and python interpreter
        """
        # Deactivate Console if showing
        if self.active:
            self.set_active()
        self.setvar("python_mode",
                            not self.getvar("python_mode"))

        self.set_interpreter()
        self.set_active()
