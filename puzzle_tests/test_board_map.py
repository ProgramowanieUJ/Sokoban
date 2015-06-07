"""testing Map used by Board"""

from puzzle.levels import Map
from puzzle.levels import LevelReader
from puzzle_tests.maps import MAP_CORNERS
import unittest
import os


class TestMap(unittest.TestCase):
    """testing Map used by Board"""
    def __init__(self, *args, **kwargs):
        """init"""
        super(TestMap, self).__init__(*args, **kwargs)
        self.level_reader = None
        self.map = None

    def setUp(self):
        """setUp"""
        self.level_reader = LevelReader()
        levels = LevelReader().read_file_plain(os.path.join("files", "sokoban.txt"))
        self.map = Map(levels[6], (9, 4))

    def test_get_tile(self):
        """checks if getting file char by coordinates works correctly"""
        for j in range(self.map.height - 1):
            for i in range(self.map.width - 1):
                self.assertEqual(self.map.get_tile((i, j)), self.map.map_grid[i][j])

    def test_get_absent_tile(self):
        """this kind of numeration is not fine"""
        self.assertEqual(self.map.get_tile((-1, -3)), None)

    def test_clean_map(self):
        """checks if cleaning leaves nothing but walls and floor"""
        clean_map = self.map.clean_map()
        for j in range(self.map.height - 1):
            for i in range(self.map.width - 1):
                self.assertEqual(clean_map[i][j]
                                 in ('#', 'x', ' '), True, "Map wasn't purged")

    def test_is_inside(self):
        """checks if positions inside map grid are recognized"""
        for j in range(self.map.height - 1):
            for i in range(self.map.width - 1):
                self.assertEqual(self.map.is_inside((i, j)), True, str(i)+str(j))

    def test_is_outside(self):
        """checks if positions outside map grid are not recognized"""
        self.assertEqual(self.map.is_inside((0, 29)), False, str(0)+str(29))
        self.assertEqual(self.map.is_inside((-1, 4)), False, str(0)+str(29))
        self.assertEqual(self.map.is_inside((24, 1)), False, str(0)+str(29))
        self.assertEqual(self.map.is_inside((40, 50)), False, str(0)+str(29))

    def test_is_wall(self):
        """checks if position is indeed wall"""
        for j in range(self.map.height - 1):
            for i in range(self.map.width - 1):
                self.assertEqual(self.map.is_wall((i, j)),
                                 self.map.map_grid[i][j] in ('#', 'x'), str(i)+str(j))

        self.assertEqual(self.map.is_wall((-1, -10)), False, "Doesn't check if is inside")

    def test_flood_fill(self):
        """checks if area was colored"""
        self.map.flood_fill((9, 4), ' ', '7')
        new_map = self.map.clean_map()
        self.assertEqual([len([element for element in line if not element.strip(' #x7')])
                          for line in new_map], [self.map.height] * self.map.width)

    def test_put_corners(self):
        """checks if area was colored"""
        print "corners:"
        test_s = MAP_CORNERS
        test_map = self.map.clean_map()
        for i in range(self.map.width):
            print ''.join(test_map[i])
            self.assertEqual(''.join(test_map[i]), test_s[i])

if __name__ == '__main__':
    unittest.main()
