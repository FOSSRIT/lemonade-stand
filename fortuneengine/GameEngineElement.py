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

from fortuneengine.GameEngine import GameEngine
#from fortuneengine.DrawableFontObject import DrawableFontObject
#from fortuneengine.DrawableObject import DrawableObject
#from fortuneengine.DynamicDrawableObject import DynamicDrawableObject


class GameEngineElement(object):
    """
    The GameEngineElement is a helper object that can be extended by
    other classes. When the class is extended, it will automatically
    register its self for the event and draw loops with the game engine.
    """

    def __init__(self, has_draw=True, has_event=True):
        """
        Default constructor for GameEngineElement

        @param  has_draw:    boolean to signify if element should be drawn
        @param  has_event:   boolean to signify whether the element should be
                             given events from the queue
        """
        self.__has_draw = has_draw
        self.__has_event = has_event
        self.__in_engine = False
        self.game_engine = GameEngine.instance
        self.__ddo_list = []

    def is_in_engine(self):
        """
        Returns true if object has been registered with the game engine.
        """
        return self.__in_engine
    
    def add_to_scene(self, objects):
        """
        Adds some objects to the DynamicDrawableObject list and the
        game engine's scene.
        
        @param  objects:    A list of DynamicDrawableObjects
        """
        
        self.game_engine.get_scene().addObjects(objects)
        self.__ddo_list += objects

    def add_to_engine(self):
        """
        Registers the object with the game engine. Registers draw and event
        call backs separately if they were set to true in the constructor.
        """
        if not self.__in_engine:
            self.__in_engine = True

            if self.__has_draw:
                self.game_engine.add_draw_callback(self.draw)

            if self.__has_event:
                self.game_engine.add_event_callback(self.event_handler)

    def remove_from_engine(self):
        """
        Removes the object from the correct queues in the engine
        """
        if self.__in_engine:
            self.__in_engine = False

            if self.__has_draw:
                self.game_engine.remove_draw_callback(self.draw)

            if self.__has_event:
                self.game_engine.remove_event_callback(self.event_handler)
                
            if not (self.__ddo_list == []):
                for object in self.__ddo_list:
                    self.game_engine.get_scene().removeObject(object)
                

    def event_handler(self, event):
        """
        This method should be overridden by the user-specified class that
        extends this GameEngineElement class. This method specifies how that
        class will handle events given to it by the engine.

        @return:    true if the user wants to prevent the event from
                    continuing down the queue
        """
        pass

    def draw(self, screen):
        """
        This method should be overridden by the user-specified class that
        extends this GameEngineElement class. This method specifies how the
        class will be drawn.
        """
        pass
