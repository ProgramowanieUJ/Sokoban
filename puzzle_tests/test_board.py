"""testing Board"""

from puzzle_tests.maps import MAP_CORNERS
from puzzle.levels import Map
from puzzle.levels import Board
from puzzle.levels import LevelReader
import unittest
import os


class TestBoard(unittest.TestCase):
    """testing Board"""

    def __init__(self, *args, **kwargs):
        """init"""
        super(TestBoard, self).__init__(*args, **kwargs)
        self.level_reader = None
        self.levels = None
        self.board = None

    def setUp(self):
        """setup"""
        self.level_reader = LevelReader()
        self.levels = LevelReader().read_file_plain(os.path.join("files", "sokoban.txt"))
        self.board = Board()
        self.board.set_map(self.levels[6], (9, 4))

    def test_set_map(self):
        """checks if map setup works; it depends nearly entirely on Map __init__"""
        self.board.goal_list.extend([(1, 1), (2, 2), (3, 3)])
        self.board.set_map(self.levels[6], (9, 4))

        self.assertEqual(self.board.starting_state["player"], (9, 4))
        self.assertEqual(self.board.goal_list, [(1, 1), (2, 2), (3, 3)])
        self.assertEqual(type(self.board), Board)
        self.assertEqual(type(self.board.map_grid), Map)
        test_s = MAP_CORNERS
        test_map = self.board.map_grid.clean_map()
        for i in range(self.board.width):
            self.assertEqual(''.join(test_map[i]), test_s[i])

    def test_reset(self):
        """checks if map reset works"""
        self.board.starting_state["player"] = (3, 7)
        self.board.goal_list.extend([(1, 1), (2, 2), (3, 3)])
        self.assertEqual(self.board.starting_state["player"], (3, 7))

        test_s = ["     y     x####x  ", " i  x##x  xx    #  ", "  x#x 5#  #  ## x#x",
                  "x#x  h x##x #     #", "#   e             #", "# s    ## x#x   x#x",
                  "xx# ###  u# x###x  ", " #   m  x#x        ", " #  fx##x   n      ",
                  " x###x        w    "]

        self.board.set_map(self.levels[6], (9, 4))
        self.assertEqual(self.board.starting_state["player"], (9, 4))
        self.assertEqual(self.board.goal_list, [(1, 1), (2, 2), (3, 3)])

        for i in range(self.board.width):
            self.assertNotEqual(''.join(self.board.map_grid.map_grid[i]), test_s[i])

    def test_get_tile(self):
        """checks if getting file char by coordinates works correctly"""
        for j in range(self.board.height - 1):
            for i in range(self.board.width - 1):
                self.assertEqual(self.board.get_tile((i, j)), self.board.map_grid.map_grid[i][j])

    def test_get_absent_tile(self):
        """this kind of numeration is not fine"""
        self.assertEqual(self.board.get_tile((-1, -3)), None)

    def test_is_inside(self):
        """checks if positions inside map grid are recognized"""
        for j in range(self.board.height - 1):
            for i in range(self.board.width - 1):
                self.assertEqual(self.board.is_inside((i, j)), True, str(i)+str(j))

    def test_is_outside(self):
        """checks if positions outside map grid are not recognized"""
        self.assertEqual(self.board.is_inside((0, 29)), False, str(0)+str(29))
        self.assertEqual(self.board.is_inside((-1, 4)), False, str(0)+str(29))
        self.assertEqual(self.board.is_inside((24, 1)), False, str(0)+str(29))
        self.assertEqual(self.board.is_inside((40, 50)), False, str(0)+str(29))

    def test_is_wall(self):
        """checks if position is indeed wall"""
        for j in range(self.board.height - 1):
            for i in range(self.board.width - 1):
                self.assertEqual(self.board.is_wall((i, j)),
                                 self.board.map_grid.map_grid[i][j] in ('#', 'x'), str(i)+str(j))

        self.assertEqual(self.board.is_wall((-1, -10)), False, "Doesn't check if is inside")

    def test_mirror(self):
        """checks if board is mirror image"""
        self.board.goal_list.extend([(1, 1), (2, 2), (3, 3)])
        self.board.set_map(self.levels[6], (9, 4))
        mirror = self.board.mirror()

        test_s = MAP_CORNERS

        self.assertEqual(mirror.starting_state["player"], (mirror.width - 10, 4))
        self.assertEqual(mirror.goal_list, [(mirror.width - 2, 1), (mirror.width - 3, 2),
                                            (mirror.width - 4, 3)])

        mirror = Map(mirror.map_grid.map_grid[::-1], (mirror.width - 10, 4))
        mirror = mirror.clean_map()
        for i in range(self.board.width):
            self.assertEqual(''.join(mirror[i]), test_s[i])

    def test_step(self):
        """checks how the player can move"""
        self.board.goal_list = [(4, 1), (3, 5)]
        self.board.player = (4, 2)
        self.assertEqual(self.board.step("left"), False)
        self.assertEqual(self.board.player, (4, 2))
        self.assertEqual(self.board.step("right"), True)
        self.assertEqual(self.board.player, (5, 2))
        self.assertEqual(self.board.step("up"), True)
        self.assertEqual(self.board.player, (5, 1))
        self.assertEqual(self.board.step("down"), True)
        self.assertEqual(self.board.player, (5, 2))

        self.board.goal_list = [(4, 1), (3, 5)]
        self.board.player = (4, 3)
        self.assertEqual(self.board.step("left"), True)
        self.assertEqual(self.board.player, (3, 3))
        self.assertEqual((4, 1) in self.board.goal_list, True)

        self.board.goal_list = [(4, 1), (3, 5)]
        self.board.player = (4, 1)
        self.assertEqual(self.board.step("left"), False)

    def test_is_finished(self):
        """checks if finished state is recognized"""
        self.board.goal_list = [(4, 1), (3, 5)]
        self.board.boxes_list = [(5, 1), (5, 5)]
        self.assertEqual(self.board.is_finished(), False)
        self.board.boxes_list = [(4, 1), (3, 5)]
        self.assertEqual(self.board.is_finished(), True)

    def test_is_correct(self):
        """checks if board is correct"""
        # goal list 0
        self.assertEqual(self.board.is_correct(), False)
        self.board.goal_list = [(0, 1)]
        self.board.boxes_list = [(0, 2)]
        self.assertEqual(self.board.is_correct(), True)
        self.board.boxes_list = [(0, 1)]
        self.assertEqual(self.board.is_correct(), False)
        self.board.player = None
        self.assertEqual(self.board.is_correct(), False)
        # goal and boxes list count doesn't match
        self.board.player = (4, 6)
        self.board.goal_list.extend((4, 2))
        self.assertEqual(self.board.is_correct(), False)

if __name__ == '__main__':
    unittest.main()
