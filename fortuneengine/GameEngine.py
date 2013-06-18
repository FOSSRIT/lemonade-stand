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

import pygame
from time import time
from GameEngineConsole import GameEngineConsole
from GameInspect import GameInspect
from DrawableFontObject import DrawableFontObject
from Scene import Scene


class GameEngine(object):
    """
    The Fortune Engine GameEngine is a main loop wrapper around pygame.
    It manages the event and drawing loops allowing the user to just
    register for user events and drawing time in the draw loop.
    """
    instance = None

    def __init__(self, width=1200, height=900, always_draw=False,
                 fps_cap=15, version=False, title="FortuneEngine"):
        """
        Constructor for the game engine.

        @param width:        Window width
        @param height:       Window height
        @param always_draw:  Boolean to set the animation mode to always
                             draw vs draw when set_dirty is called
        @param fps_cap:      Sets the framerate cap. Set to 0 to disable
                             the cap. Warning: setting the cap to 0 when
                             always draw = False will cause cpu 100% when
                             not driving.
        @param version:      If true, use new rendering system, false uses
                             only the draw system
        @param title:        Window Title
        """
        GameEngine.instance = self
        pygame.init()
        pygame.mouse.set_visible(False)
        self.__version = version #true is new, false is old

        # Window Settings
        self.width = width
        self.height = height
        size = width, height
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.__fps = DrawableFontObject("", pygame.font.Font(None, 17))
        self.__fps.setPosition(0, 0)
        self.__scene = Scene(self.__fps)

        # Engine Internal Variables
        self.__fps_cap = fps_cap
        self.__showfps = False
        self.__dirty = True
        self.__always_draw = always_draw
        self.__font = pygame.font.Font(None, 17)
        self.__run_event = False

        # Variables to hold game engine elements and callbacks
        self.__event_cb = []
        self.__draw_lst = []
        self.__object_hold = {}


        # Game Timers
        self.__active_event_timers = []
        self.__active_event_timers_tick = []

        # Game Clock
        self.clock = pygame.time.Clock()
        self.__tick_time = 0

        # Inspector
        self._inspector = GameInspect(self.__object_hold)

        # Time Profiler Timers
        self.__draw_time = {}
        self.__draw_calls = {}
        self.__event_time = {}
        self.__event_calls = {}
        self.__timer_time = {}
        self.__timer_calls = {}

        # Initialize Py Console
        self.console = GameEngineConsole(self, (0, 0, width, height / 2))

        # Disable Mouse Usage
        # TODO Allow mouse motion on request
        pygame.event.set_blocked(pygame.MOUSEMOTION)

    def set_dirty(self):
        """
        Sets the dirty flag to force the engine to draw the next time
        it enters the draw flag.
        """
        self.__dirty = True

    def get_scene(self):
        """
        Returns the scene object

        @return:    Returns the scene object held by the game engine
        """
        return self.__scene

    def start_event_timer(self, function_cb, time):
        """
        Starts a timer that fires a user event into the queue every "time"
        milliseconds

        @param function_cb:     The function to call when timer fires
        @param time:            Milliseconds between fires
        """
        avail_timer = len(self.__active_event_timers)

        if avail_timer + pygame.USEREVENT < pygame.NUMEVENTS:
            if function_cb not in self.__active_event_timers:
                self.__timer_time[str(function_cb)] = 0
                self.__timer_calls[str(function_cb)] = 0

                self.__active_event_timers.append(function_cb)
                self.__active_event_timers_tick.append(time)
                pygame.time.set_timer(pygame.USEREVENT + avail_timer, time)
            else:
                print "ERROR TIMER IN LIST"
        else:
            print "Ran out of timers :("
            self.stop_event_loop()

    def stop_event_timer(self, function_cb):
        """
        Stops the timer that has id from firing

        @param function_cb:     The function registered with the timer that
                                should be canceled
        """
        try:
            timer_id = self.__active_event_timers.index(function_cb)
        except ValueError:
            return

        pygame.time.set_timer(pygame.USEREVENT + timer_id, 0)
        del self.__active_event_timers[timer_id]
        del self.__active_event_timers_tick[timer_id]

        # Timers have been removed, now need to clear any events
        # already fired and in the queue
        pygame.event.clear(pygame.USEREVENT + timer_id)

    def list_event_timers(self):
        """
        returns a list of configured timers, if the timers has a time of 0 the
        timer is disabled
        """
        timer_list = "Event Timers:\n"
        i = 0
        for timer_item in self.__active_event_timers:
            timer_list += "\t%d: %d\n" % (timer_item,
                          self.__active_event_timers_tick[i])
            i = i + 1

        return timer_list

    def list_timer_time(self):
        """
        Returns a string representation of the time the game spends
        in each timer callback.
        """
        mystr = "Timer Times:\n\tName\tCalls\tTotal Time\tAvg"
        for key in self.__timer_time:
            timer_times = self.__timer_time[key]
            timer_calls = self.__timer_calls[key]
            if timer_calls == 0:
                avg = 0
            else:
                avg = timer_times / timer_calls

            mystr = "%s\n\t%s\n\t\t%d\t%f\t%f" % \
                    (mystr, key, timer_calls, timer_times, avg)
        return mystr

    def start_main_loop(self):
        """
        Starts the game loop.

        This function does not return until after the game loop exits
        """
        self.__run_event = True
        self._event_loop()

    def _draw(self, tick_time):
        """
        Draws all elements in draw callback to the screen

        @param tick_time:       The amount of time passed since last
                                draw cycle. (should be produced by
                                pygamme.clock.tick method)
        """
        screen = self.screen

        # If console is active, we want to draw console, pausing
        # game drawing (events are still being fired, just no
        # draw updates.
        if self.__version:
            if self.console.active:
                self.console.draw()
                pygame.display.flip()
            else:
                for fnc in self.__draw_lst:
                    start = time()
                    fnc()
                    self.__draw_time[str(fnc)] += time() - start
                    self.__draw_calls[str(fnc)] += 1
                # Print Frame Rate
                if self.__showfps:
                    self.__fps.changeText('FPS: %d' % self.clock.get_fps(),
                                                      (255, 255, 255))
                else:
                    self.__fps.changeText('')
                self.__scene.update(tick_time)
                pygame.display.update(self.__scene.draw(screen))
        else:
            if self.console.active:
                self.console.draw()
                pygame.display.flip()
            else:
                for fnc in self.__draw_lst:
                    start = time()
                    fnc(screen, tick_time)
                    self.__draw_time[str(fnc)] += time() - start
                    self.__draw_calls[str(fnc)] += 1
                # Print Frame Rate
                if self.__showfps:
                    text = self.__font.render('FPS: %d' % \
                           self.clock.get_fps(), False, (255, 255, 255),
                           (159, 182, 205))
                    screen.blit(text, (0, 0))
                pygame.display.flip()

    def _event_loop(self):
        """
        The main event loop.
        """
        while self.__run_event:

            event = pygame.event.poll()

            # Handle Game Quit Message
            if event.type == pygame.QUIT:
                self.__run_event = False

            # No-Op sent, draw if set to always draw
            elif event.type == pygame.NOEVENT:
                # Tick even if not drawing
                # We want to pause the cpu from getting into a
                # 100% usage looping on the poll until something
                # becomes dirty
                self.__tick_time += self.clock.tick(self.__fps_cap)
                if self.__always_draw or self.__dirty:
                    self.__dirty = False
                    self._draw(self.__tick_time)
                    self.__tick_time = 0


            # Handle User event Timers
            elif event.type >= pygame.USEREVENT and \
                event.type < pygame.NUMEVENTS:

                timer_id = event.type - pygame.USEREVENT

                # Call timer
                str_rep = str(self.__active_event_timers[timer_id])
                start = time()
                self.__active_event_timers[timer_id]()
                self.__timer_time[str_rep] += time() - start
                self.__timer_calls[str_rep] += 1

            # Check if we should activate the console
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w \
                    and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.console.set_active()
                self.set_dirty()

            # Pass event to console
            elif self.console.process_input(event):
                self.set_dirty()

            # Pass events to all others
            else:
                # Make a copy first so that adding events don't get fired
                # right away
                list_cp = self.__event_cb[:]

                # Reverse list so that newest stuff is on top
                # TODO: cache this list
                list_cp.reverse()

                for cb in list_cp:
                    # Fire the event for all in cb and stop
                    # if the callback returns True
                    start = time()
                    retur_val = cb(event)
                    self.__event_time[str(cb)] += time() - start
                    self.__event_calls[str(cb)] += 1

                    if retur_val:
                        break

    def stop_event_loop(self):
        """
        Sends a pygame.QUIT event into the event queue which
        exits the event loop
        """
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def add_event_callback(self, cb):
        """
        Adds event callback to the event callback stack

        @param cb:  Callback to be added to the stack when events are fired.
        """
        self.__event_time[str(cb)] = 0
        self.__event_calls[str(cb)] = 0
        self.__event_cb.append(cb)

    def remove_event_callback(self, cb):
        """
        Removes an event from the event callback stack

        @param cb:       The callback to remove from the event callback stack
        @return:         Returns true if successful in removing callback
        """
        try:
            self.__event_cb.remove(cb)
            return True
        except:
            return False

    def list_event_callbacks(self):
        """
        Returns a string representation of all events registered with the game
        engine
        """
        event_callbacks = "Event Listeners:\n"
        for eventlst in self.__event_cb:
            event_callbacks = "%s\t%s\n" % (event_callbacks, str(eventlst))
        return event_callbacks

    def list_event_time(self):
        """
        Returns a string representation of the time the game spends
        in each event callback.
        """
        mystr = "Event Times:\n\tName\tCalls\tTotal Time\tAvg"
        for key in self.__event_time:
            event_times = self.__event_time[key]
            event_calls = self.__event_calls[key]
            if event_calls == 0:
                avg = 0
            else:
                avg = event_times / event_calls

            mystr = "%s\n\t%s\n\t\t%d\t%f\t%f" % \
                    (mystr, key, event_calls, event_times, avg)
        return mystr

    def add_draw_callback(self, fnc):
        """
        Adds a callback to the draw list.  Function will be passed the
        game screen it should draw too.

        @param fnc:    The function to call when system is drawing
        """

        self.__draw_time[str(fnc)] = 0
        self.__draw_calls[str(fnc)] = 0
        self.__draw_lst.append(fnc)

    def pop_draw_callback(self):
        """
        Removes top of draw stack and returns it

        @return:         Returns the top callback function that was removed
        """
        return self.__draw_lst.pop()

    def clear_draw_callback(self):
        """
        Empties draw callback stack
        """
        self.__draw_lst = []

    def remove_draw_callback(self, fnc):
        """
        Removes a draw callback from the game engine draw function

        @param fnc:      The callback function to remove
        @return:         Returns true if successful removal of the function
        """
        try:
            self.__draw_lst.remove(fnc)
            return True
        except:
            return False

    def list_draw_callbacks(self):
        """
        Lists all the draw callbacks currently registered with the game engine
        """

        callbacks = "Draw Callbacks:\n"
        for eventlst in self.__draw_lst:
            callbacks += "\t%s\n" % str(eventlst)
        return callbacks

    def list_draw_time(self):
        """
        Returns a string representation of the time the game spends
        in each drawing callback.
        """
        mystr = "Drawing Times:\n\tName\tCalls\tTotal Time\tAvg"
        for key in self.__draw_time:
            draw_times = self.__draw_time[key]
            draw_calls = self.__draw_calls[key]
            if draw_calls == 0:
                avg = 0
            else:
                avg = draw_times / draw_calls

            mystr = "%s\n\t%s\n\t\t%d\t%f\t%f" % \
                    (mystr, key, draw_calls, draw_times, avg)
        return mystr

    def has_object(self, name):
        """
        Returns true if object is stored in game engine

        @param name:     Name of the object to check if exists
        @return:         Returns true if object found
        """
        return name in self.__object_hold

    def add_object(self, name, obj):
        """
        Adds an object to the game engine datastore

        @param name:     The name used to store the object
        @param obj:      The object to store
        """
        self.__object_hold[name] = obj

    def get_object(self, name):
        """
        Returns an object from the game engine datastore

        @param name:     The name of object to return
        @return:         Returns the object
        """
        return self.__object_hold[name]

    def remove_object(self, name):
        """
        Removes an object from the game engine datastore

        @param name:     The name of the object to remove
        @return:         Returns true on successful removal
        """
        try:
            del self.__object_hold[name]
            return True
        except:
            return False

    def list_objects(self):
        """
        Returns a sting of registered objects
        """
        objlist = "Objects Registered:\n"
        for eventlst in self.__object_hold:
            objlist += "\t%s\n" % str(eventlst)
        return objlist

    def toggle_fps(self):
        """
        Toggles fps display
        """
        self.__showfps = not self.__showfps

    def art_scale(self, original, expected, width=True):
        if width:
            return int(self.width / float(expected) * float(original))
        else:

            return int(self.height / float(expected) * float(original))
