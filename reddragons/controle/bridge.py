
"""
This module was created to interact with the FIRAClient
located on https://github.com/yapiraUFPR/FIRAClient

This interaction is made with the file libfira.cpp,
witch generates the shared object libfira.so used here.

The classes located here use the lib subspace to store
their respective client data.
"""

__author__ = "Artur Coelho - github.com/arturtcoelho"

# The main import for this bridge,
import ctypes
import os
# imports most used types from ctypes import c_double, \
from ctypes import (c_double,
                    c_char_p,
                    c_uint16,
                    c_int32,
                    c_bool)

from math import fmod, pi

# Loads the compiled shared library based on libfira.cpp
# See README.md to compile and usage

# The lib object will contain the C++ local clients
# witch save their respective data
print(os.listdir())
try:
    lib = ctypes.cdll.LoadLibrary('libfira.so')
    print('1')
except Exception as e:
    try:
        lib = ctypes.cdll.LoadLibrary('./FIRAClient/libfira.so')
        print('2')
    except Exception as e:
        try:
            lib = ctypes.cdll.LoadLibrary('../FIRAClient/libfira.so')
            print('3')
        except Exception as e:
            print("Could not open lib in any directory")
            exit()

# set the return types for the lib functions (to double)
lib.vision_get_ball_x.restype = c_double
lib.vision_get_ball_y.restype = c_double
lib.vision_get_ball_vx.restype = c_double
lib.vision_get_ball_vy.restype = c_double
lib.vision_robot_x.restype = c_double
lib.vision_robot_y.restype = c_double
lib.vision_robot_angle.restype = c_double
lib.vision_robot_vx.restype = c_double
lib.vision_robot_vy.restype = c_double
lib.vision_robot_vangle.restype = c_double

NUM_BOTS = 3

LENGTH = 1.7 / 2.0
WIDTH = 1.3 / 2.0

class Entity():
    '''
    Class used to determine the position, speed and direction
    of any entity on the field.
    '''
    def __init__(self, x=0, y=0, vx=0, vy=0, a=0, va=0, index=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.a = a
        self.va = va
        self.index = index

# youcan remove or modify these functions as you wish,
# these are used here mainly to run the example main
def convert_width(w) -> float:
    """
    Converts width from the simulator data to centimetres
    with origin point on bottom left corner of field
    """
    try:
        return (WIDTH + w) * 100
    except TypeError:
        return 0

def inverse_width(w) -> float:
    try:
        return (w / 100) - WIDTH
    except TypeError:
        return 0

def convert_length(d) -> float:
    """
    Converts width from the simulator data to centimetres
    with origin point on bottom left corner of field
    """
    try:
        return (LENGTH + d) * 100
    except TypeError:
        return 0

def inverse_length(d) -> float:
    try:
        return (d / 100) - LENGTH
    except TypeError:
        return 0

def convert_angle(a) -> float:
    """
    Converts the angle from full radians to
    -Pi/2 to Pi/2 radians range
    """
    try:
        angle = fmod(a, 2*pi)
        if (angle < -pi):
            return angle + 2*pi
        if (angle > pi):
            return angle - 2*pi
        return angle
    except TypeError:
        return 0


# Client classes

class Vision():
    """
    Class for the vision client,
    Use one instance at a time to minimize network errors.
    """

    def __init__(self, mray, addr = "224.0.0.1", port = 10002):
        """
        Constructor initialized with adress and port

        default address: "224.0.0.1"
        default port: 10002
        Fetches the first field.
        """

        self.mray = mray

        # we need to convert the string type
        c_string = addr.encode('utf-8')
        lib.actuator_init.argtypes = [c_char_p, c_uint16, c_bool]

        lib.vision_init(c_string, c_uint16(port))
        # already update once
        self.update()

    def update(self):
        """Fetches client data."""
        return lib.vision_update_field()

    def get_field_data(self):
        '''
            Returns a dict with the field info, 2 lists of entities
            one for each team robots and a ball entity
        '''

        field = dict()
        field["mray"] = self.mray
        try:
            field["yellow"] = [self.get_robot(i, True) for i in range(NUM_BOTS)]
            field["blue"] = [self.get_robot(i, False) for i in range(NUM_BOTS)]
            if self.mray:
                field["our_bots"] = field["yellow"]
                field["their_bots"] = field["blue"]
            else:
                field["our_bots"] = field["blue"]
                field["their_bots"] = field["yellow"]

            field["ball"] = self.get_ball()
        except TypeError:
            return None

        return field

    def get_ball(self):
        """
        Returns a Entity with the ball data
        Use after the update method.
        """

        try:
            # fills and return the new object
            ball = Entity()
            # positions
            ball.x = convert_length(lib.vision_get_ball_x())
            ball.y = convert_width(lib.vision_get_ball_y())
            # speds
            ball.vx = lib.vision_get_ball_vx()
            ball.vy = lib.vision_get_ball_vy()
        except TypeError:
            return None

        return ball

    def get_robot(self, index, yellow):
        """
        Returns a Entity with the bot data
        bot is given by index and get_yellow parametres
        Use after the update method.
        """

        try:
            # fills and return bot object
            # get position
            bot = Entity()
            bot.x = convert_length(
                lib.vision_robot_x(c_int32(index), c_bool(yellow)))
            bot.y = convert_width(
                lib.vision_robot_y(c_int32(index), c_bool(yellow)))
            bot.a = convert_angle(
                lib.vision_robot_angle(c_int32(index), c_bool(yellow)))
            # get speeds
            bot.vx = lib.vision_robot_vx(c_int32(index), c_bool(yellow))
            bot.vy = lib.vision_robot_vy(c_int32(index), c_bool(yellow))
            bot.va = lib.vision_robot_vangle(c_int32(index), c_bool(yellow))
            bot.index = index

        except TypeError:
            return None
        return bot

    def __del__(self):
        """Closes network conection"""
        lib.vision_term()

class Referee():
    """
    Referee client class,
    Use one instance at a time to minimize network errors.
    """

    def __init__(self, mray, addr = "224.5.23.2", port = 10003):
        """
        Initialize client on addr and port

        default adress: "224.5.23.2"
        default port: 10003
        Fetches the first data.
        """

        self.mray = mray

        # we need to convert the string type
        c_string = addr.encode('utf-8')
        lib.referee_init.argtypes = [c_char_p, c_uint16]

        lib.referee_init(c_string, c_uint16(port))
        self.update()

    def update(self):
        """Fetches new referee data."""
        lib.referee_update()

    def get_data(self):
        """
        Returns a dict with the new data from referee
        or default values (game stoped).
        """
        data = dict()

        try:
            data["foul"] = self.interrupt_type()
            data["yellow"] = self.color() == 1
            data["quad"] = self.get_quadrant()

            data["game_on"] = data["foul"] == 6
            data["our"] = data["yellow"] and self.mray
            data["is_game_halt"] = data["foul"] == 7
        except TypeError:
            return None

        return data

    def interrupt_type(self):
        """
        returns the type of interrupt
        being it a foul, game_on or halt
        From libfira.cpp:
            FREE_KICK = 0
            PENALTY_KICK = 1
            GOAL_KICK = 2
            FREE_BALL = 3
            KICKOFF = 4
            STOP = 5
            GAME_ON = 6
            HALT = 7
        """
        return lib.referee_get_interrupt_type()

    def color(self):
        """
        Returns interrupt color data from libira:
            BLUE = 0,
            YELLOW = 1,
            NONE = 2,
        """
        return lib.referee_interrupt_color()

    def get_quadrant(self):
        """
        returns quadrant on witch foul happened from:
            NO_QUADRANT = 0,
            QUADRANT_1 = 1,
            QUADRANT_2 = 2,
            QUADRANT_3 = 3,
            QUADRANT_4 = 4,
        """
        return lib.referee_get_interrupt_quadrant()

    def __del__(self):
        """Closes network conection."""
        lib.referee_term()

class Actuator():
    """
    Actuator client class,
    Use one instance at a time to minimize network errors.
    """

    def __init__(self, my_robots_are_yellow, addr = "224.0.0.1", port = 10002):
        """
        Initialize client on addr and port

        default adress: "224.0.0.1",
        default port: 10002
        requires bool team_color to indicate later comands.
        """

        # we need to convert the string type
        c_string = addr.encode('utf-8')
        lib.actuator_init.argtypes = [c_char_p, c_uint16, c_bool]

        lib.actuator_init(c_string,
                            c_uint16(port),
                            c_bool(my_robots_are_yellow))

    def send(self, index, left, right):
        """
        sends motor speeds for one robot indicated by
        index on team initialized.
        """
        lib.actuator_send_command(c_int32(index),
                                    c_double(left),
                                    c_double(right))

    def send_all(self, speeds):
        """sends a list of speed commands based on the passed list of dicts"""
        for s in speeds:
            try:
                self.send(s["index"], s["left"], s["right"])
            except Exception as e:
                print("speed exception:", e)

    def stop(self):
        for i in range(NUM_BOTS):
            self.send(i, 0, 0)

    def __del__(self):
        """Closes network conection."""
        lib.actuator_term()

class Replacer():
    """
    Actuator client class,
    Use one instance at a time to minimize network errors.
    """

    def __init__(self, my_robots_are_yellow, addr = "224.5.23.2", port = 10004):
        """
        Initialize client on addr and port

        default adress: "224.5.23.2"
        default port: 10004
        requires bool team_color to later comands.
        """
        c_string = addr.encode('utf-8')
        lib.actuator_init.argtypes = [c_char_p, c_uint16, c_bool]

        lib.replacer_init(c_string,
                            c_uint16(port),
                            c_bool(my_robots_are_yellow))

    def place(self, index, x, y, angle):
        """
            Sends a index indicated bot to x, y and angle.
            *Needs to use seld.send() to actualy send, or use place_all
        """
        lib.replacer_place_robot(c_int32(index),
                                    c_double(inverse_length(x)),
                                    c_double(inverse_width(y)),
                                    c_double(angle))
        #lib.replacer_send_frame()

    def place_all(self, placement):
        """Sends a list of Entities locations"""
        for p in placement:
            try:
                self.place(p.index, p.x, p.y, p.a)
            except Exception as e:
                print("placement exception:", e)

        lib.replacer_send_frame()

    def send(self):
        '''Actualy sends the frame'''
        lib.replacer_send_frame()

    def __del__(self):
        """Closes network conection."""
        lib.replacer_term()

# Base test run
if __name__ == "__main__":
    try:
        mray = False

        # initializes all classes with default ports
        vision = Vision(mray)
        referee = Referee(mray)
        actuator = Actuator(mray)
        replacer = Replacer(mray)
    except Exception as e:
        print("An error occured during execution:", e)
        exit()
    print()
    print("Test completed!")
