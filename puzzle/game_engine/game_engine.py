"""this is the game engine that uses loaded level files"""

from puzzle.visualizers.window import Window
from puzzle.players.player import Player
from puzzle.levels import LevelReader


class GameEngine(object):
    """abstract game engine, not meant to be run as is"""

    def __init__(self):
        """initializes game engine with the level file"""
        self.window = Window()
        self.player = Player()

        self.level_reader = LevelReader()
        self.levels = []

    def switch_level(self, command, index):
        """method that has be implemented in child classes"""
        pass

    def run(self):
        """the game's main loop"""
        index = -1
        index = self.switch_level("next", index)
        keyword, event = self.window.display("start")

        while index < len(self.levels):

            while keyword != "next" and keyword != "previous":
                keyword = self.player.command(keyword, event)
                if keyword != "next" and keyword != "previous":
                    keyword, event = self.window.display(keyword)

            index = self.switch_level(keyword, index)
            keyword = "switch"
