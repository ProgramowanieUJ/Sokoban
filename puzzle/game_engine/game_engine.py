"""this is the game engine that uses loaded level files"""

from puzzle.visualizers.window import Window
from puzzle.players.player import Player
from puzzle.levels import LevelReader


class PlainGameEngine(object):
    """this is the game engine that uses loaded level files"""

    def __init__(self, level_file):
        """initializes game engine with the level file"""
        self.window = Window()
        self.player = Player()

        self.level_reader = LevelReader()
        self.levels = self.load_levels(level_file)

    def load_levels(self, level_file):
        """loads level using the level reader"""
        return self.level_reader.read_levels_file(level_file)

    def switch_level(self, index):
        """sets the level the window is supposed to show"""
        if index < len(self.levels) - 1:
            self.window.level = self.levels[index+1]

    def run(self):
        """the game's main loop"""
        self.window.level = self.levels[0]
        keyword, event = self.window.display("start")

        for index in range(len(self.levels)):

            while keyword != "break":
                keyword = self.player.command(keyword, event)
                keyword, event = self.window.display(keyword)

            self.switch_level(index)
            keyword = "next"
