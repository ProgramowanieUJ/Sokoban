"""this is the game engine that uses generated level files"""

from puzzle.game_engine.game_engine import GameEngine
from puzzle.levels import Generator
from puzzle.levels import LevelReader
import os


class GenGameEngine(GameEngine):
    """this is the game engine that uses generated level files"""

    def __init__(self):
        """sets up a base for level generation with pre prepared level templates"""
        super(GenGameEngine, self).__init__()
        self.base = self.load_base()

    def load_base(self):
        """loads base for generation using the level reader"""
        return self.level_reader.read_file_plain(os.path.join('game_engine', 'sokoban.txt'))

    def switch_level(self, command, index):
        """sets the level the window is supposed to show"""
        if command == "next":
            index += 1
            if index < len(self.levels) - 1:
                self.window.level = self.levels[index]
            else:
                if index >= len(self.base):
                    index = 0

                level = None
                while level is None:
                    generator = Generator(self.base[index])
                    map_grid = generator.generate_board()
                    level = LevelReader().build_level(map_grid)
                    if level is None:
                        index += 1

                self.levels.append(level)
                self.window.level = level
        elif command == "previous":
            if index > 0:
                index -= 1
                self.window.level = self.levels[index]
        return index
