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

import inspect


class GameInspect(object):
    """
    GameInspect is a class that can inspect and modify object trees.

    The top most object must be a dictionary
    """

    def __init__(self, object_root):
        """
        Init function of the GameInspect class.

        @param object_root:     The root dictionary of the tree
        """
        self.root = object_root

    def drilldown_object(self, objectname):
        """
        Takes the objectname string and tries to find the object that it is
        representing and returns that object.

        Example: battle.enemy_list[1].sprite._images[1]

        @param objectname:  The string that represents the object's path.
        @return:            Returns the object requested
        @raise Exception:   Throws an Exception with the string being the
                            path error.
        """
        last = "empt"
        obj = "empt"
        last_token = ""

        # Objects are separated by the period (".") symbol
        object_tokens = objectname.split(".")

        # Check if the first part of the name is registered with the
        # game engine as that is our starting point
        try:
            obj = self.root[object_tokens[0]]
            last = obj
            last_token = object_tokens[0]

        except KeyError:
            raise Exception("%s is not registered with the game engine" %
                   object_tokens[0])

        # Handles dot notation for sub modules by looping through the tokens
        for token in object_tokens[1:]:

            # Splits the dictionary/list token ("[")
            dict_token = token.split('[')
            try:
                last = obj
                obj = getattr(obj, dict_token[0])
                last_token = dict_token[0]

            except:
                raise Exception("Error finding member element: %s" % token)

            # Handles dictionaries
            for d_token in dict_token[1:]:
                if d_token[-1] == "]":
                    d_token = d_token[:-1]
                    # Try list notation first then try dictionary notation
                    try:
                        key = int(d_token)
                    except:
                        key = d_token

                    try:
                        last = obj
                        obj = obj[key]
                        last_token = key
                    except:
                        raise Exception("Unable to find %s" % key)

                else:
                    raise Exception("Invalid Syntax, expected ] at end of %s" %
                                    d_token)

        return obj, last, last_token

    def set_eval(self, objectname, statement):
        """
        Sets the object referenced by objectname to a value returned by
        passing the string stored in the val parameter to an eval statement.

        @param objectname:  A string representation of the location
                            of the object being inspected in relation
                            to the game engine registered object.
        @param statement:   A string to be evaluated and set to the object.
        """
        try:
            obj, last, last_token = self.drilldown_object(objectname)
        except Exception, detail:
            return str(detail)

        try:
            setattr(last, last_token, eval(str(statement)))
        except Exception, detail:
            return str(detail)

    def set_str(self, objectname, val):
        """
        Sets the object referenced by objectname to a string passed into the
        val parameter.

        @param objectname:  A string representation of the location
                            of the object being inspected in relation
                            to the game engine registered object.
        @param val:         A string to be set as the value of the object.
        """
        try:
            obj, last, last_token = self.drilldown_object(objectname)
        except Exception, detail:
            return str(detail)

        setattr(last, last_token, val)

    def set_int(self, objectname, val):
        """
        Sets the object referenced by objectname to an integer passed into the
        val parameter. It may be a string that holds the int as it will be
        type casted.

        @param objectname:  A string representation of the location
                            of the object being inspected in relation
                            to the game engine registered object.
        @param val:         An int/string containing an int to be set as
                            the value of the object.
        """
        try:
            obj, last, last_token = self.drilldown_object(objectname)
        except Exception, detail:
            return str(detail)

        try:
            setattr(last, last_token, int(val))
        except:
            return str(detail)

    def inspect_object(self, objectname):
        """
        Displays information about the object path it is passed

        @param objectname:  A string representation of the location
                            of the object being inspected in relation
                            to the game engine registered object.
        """
        try:
            obj, last, last_token = self.drilldown_object(objectname)

        except Exception, detail:
            return str(detail)

        classname = obj.__class__.__name__

        # If it has the __dict__ attribute, it is an object we can inspect
        if hasattr(obj, "__dict__"):
            attribute_list = "Attributes:"
            attributes = obj.__dict__
            for attribute_key in attributes.keys():
                attribute_list = "%s\n\t%s:%s" % (attribute_list,
                                 attribute_key, str(attributes[attribute_key]))

            # Inspect the object for all its methods
            method_list = inspect.getmembers(obj, inspect.ismethod)
            if method_list != []:

                # Loop through the methods in the object and print them
                # to the console
                attribute_list = "%s\n\nMethods:" % attribute_list
                for method in method_list:
                    attribute_list = "%s\n\t%s" % (attribute_list, method[0])

                    # Inspect the arguments to the current method
                    args, vargs, kwargs, local = inspect.getargspec(method[1])

                    # Display function arguments
                    attribute_list = "%s\n\t\tArgs: %s" % \
                        (attribute_list, ",".join(args))

                    # Display * and ** arguments if they were found
                    if vargs:
                        attribute_list = "%s\n\t\tVArgs: %s" % \
                            (attribute_list, ",".join(vargs))

                    # Display KW Arguments if they were found
                    if kwargs:
                        attribute_list = "%s\n\t\tKWArgs: %s" % \
                            (attribute_list, ",".join(kwargs))

        # If dictionary, show keys
        elif hasattr(obj, "keys"):
            attribute_list = "Dictionary Items:"

            for d_obj in obj.keys():
                attribute_list = "%s\n\t%s:%s" % (attribute_list, d_obj,
                                                  str(obj[d_obj]))

        # If list, iterate over the list and show its values
        elif type(obj).__name__ == 'list':
            i = 0
            attribute_list = "List Items:"
            for item in obj:
                attribute_list = "%s\n\t%d:%s" % (attribute_list, i, str(item))
                i = i + 1

        # We don't know what it is, so just display string representation
        # of the object in question
        else:
            attribute_list = str(obj)

        return "Class: %s\n%s" % (classname, attribute_list)
