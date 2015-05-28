"""contains LevelReader"""

from os import path
from puzzle.levels import level as lev


class LevelReader(object):
    """allows one to create a board object based on a file"""
    def __init__(self):
        self.levels = []

    @staticmethod
    def read_file(filename):
        """puts lines from file in a list"""
        level_map = open(filename, 'r')
        levels = level_map.readlines()
        if not levels[-1].endswith("\n"):
            levels.append("\n")
        level_map.close()
        return levels

    @staticmethod
    def clean_line(line):
        """ensures correct format"""
        line = line.rstrip("\r\n")

        if ';' in line:  # starts a comment, so cut the comment off
            line = line[:line.find(';')]

        return line

    @staticmethod
    def pad_lines(raw_level):
        """ensures correct width"""
        level_width = max([len(element) for element in raw_level])
        return [list(element + (' ' * (level_width - len(element)))) for element in raw_level]

    def build_level(self, level):
        """creates board object and its mirror image from raw data lines"""
        board = lev.Board()

        start = None
        for line in level:
            x_value = level.index(line)
            y_value = -1
            for element in line:
                y_value += 1
                if element in ('@', '+'):
                    start = (x_value, y_value)
                    board.player = start
                if element in ('.', '+', '*'):
                    board.goal_list.append((x_value, y_value))
                if element in ('$', '*'):
                    board.boxes_list.append((x_value, y_value))

        level = self.pad_lines(level)

        board.save_state(start)
        board.set_map(level)
        if not board.is_correct():
            return None
        else:
            return board, board.mirror()

    def read_levels_file(self, filename):
        """returns board object created from file"""
        if not path.exists(filename):
            # run error message here
            return None
        else:
            all_raw_levels = self.read_file(filename)

            # clean previous data
            self.levels = []

            level_lines = []  # contains the lines for a single level's map.
            for line in all_raw_levels:
                line = self.clean_line(line)

                if line != '':
                    level_lines.append(line)
                elif line == '' and len(level_lines) > 0:
                    # level_lines contains now all lines for a single level
                    board = self.build_level(level_lines)
                    if board is not None:
                        self.levels.append(board)
                    level_lines = []

            return self.levels

    def read_file_plain(self, filename):
        """returns board object created from file"""
        if not path.exists(filename):
            # run error message here
            return None
        else:
            all_raw_levels = self.read_file(filename)

            # clean previous data
            self.levels = []

            level_lines = []  # contains the lines for a single level's map.
            for line in all_raw_levels:
                line = self.clean_line(line)

                if line != '':
                    level_lines.append(line)
                elif line == '' and len(level_lines) > 0:
                    # level_lines contains now all lines for a single level
                    grid = self.pad_lines(level_lines)
                    if grid is not None:
                        self.levels.append(grid)
                    level_lines = []

        return self.levels
