"""action interpreters"""

import pygame.locals as key
import sys


class Player(object):
    """players' action interpreter"""
    def __init__(self):
        self.last_command = "start"
        self.commands = {"start": self.move_in_starting_screen,
                         "error": self.move_in_error_screen,
                         "freeze": self.freeze,
                         "solo": self.move_in_solo_mode,
                         "dual": self.move_in_dual_mode,
                         "switch": self.switch_levels}
        self.solo_dictionary = {key.K_LEFT: "left_A", key.K_RIGHT: "right_A", key.K_UP: "up_A",
                                key.K_DOWN: "down_A", key.K_TAB: "start", key.K_BACKSPACE: "reload",
                                key.K_n: "next", key.K_p: "previous"}
        self.dual_dictionary = {key.K_a: "left_B", key.K_d: "right_B",
                                key.K_w: "up_B", key.K_s: "down_B"}
        self.dual_dictionary.update(self.solo_dictionary)

    def command(self, context, event):
        """chooses function to call based on context"""
        self.check_if_quit(event)
        if context in self.commands:
            return self.commands[context](event)

    @staticmethod
    def check_if_quit(event):
        """the only legal way to quit the running program (in all the modules)"""
        if event.type == key.QUIT:
            sys.exit()
        elif event.type == key.KEYDOWN:
            if event.key == key.K_ESCAPE:
                sys.exit()

    def freeze(self, event):
        """is here to signal that current state should be maintained
         and no display reload is needed"""
        return self.commands[self.last_command](event)

    def move_in_starting_screen(self, event):
        """represents actions that can be made in the starting screen"""
        self.last_command = "start"
        if event.type == key.KEYDOWN:
            if event.key == key.K_s:
                return "solo"
            if event.key == key.K_d:
                return "dual"
        return "freeze"

    def move_in_error_screen(self, event):
        """represents actions that can be made in the error screen"""
        self.last_command = "error"
        if event.type == key.KEYDOWN:
            return "start"
        return "freeze"

    def move_in_solo_mode(self, event):
        """represents actions that can be made in the error screen"""
        self.last_command = "solo"
        if event.type == key.KEYDOWN:
            if event.key in self.solo_dictionary:
                return self.solo_dictionary[event.key]
        return "freeze"

    def move_in_dual_mode(self, event):
        """represents actions that can be made in the error screen"""
        self.last_command = "dual"
        if event.type == key.KEYDOWN:
            if event.key in self.dual_dictionary:
                return self.dual_dictionary[event.key]
        return "freeze"

    @staticmethod
    def switch_levels(event):
        """called by game engine to switch to next level"""
        # i need event variable for uniform function call in command
        event.key = key.KEYDOWN     # use the variable to silence a warning
        return "reload"
