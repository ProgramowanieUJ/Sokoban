"""contains the game engine that uses loaded level files"""

from puzzle.game_engine.game_engine import GameEngine


class PlainGameEngine(GameEngine):
    """this is the game engine that uses loaded level files"""

    def __init__(self, level_file):
        """initializes game engine with the level file"""
        super(PlainGameEngine, self).__init__()
        self.levels = self.load_levels(level_file)

    def load_levels(self, level_file):
        """loads level using the level reader"""
        return self.level_reader.read_levels_file(level_file)

    def switch_level(self, command, index):
        """sets the level the window is supposed to show"""
        if command == "next":
            if index < len(self.levels) - 1:
                self.window.level = self.levels[index+1]
                index += 1
        elif command == "previous":
            if index > 0:
                self.window.level = self.levels[index-1]
                index -= 1
        return index
