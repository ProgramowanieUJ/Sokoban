"""testing Generator"""

from puzzle_tests.maps import FLOOD_FILL
from puzzle_tests.maps import MARKED_EDGES
from puzzle_tests.maps import THIN_EDGES
from puzzle_tests.maps import FULL_EDGES
from puzzle.levels import LevelReader
from puzzle.levels import Generator
import unittest
import os


class TestGenerator(unittest.TestCase):
    """testing Generator"""

    def __init__(self, *args, **kwargs):
        """test board init"""
        super(TestGenerator, self).__init__(*args, **kwargs)
        self.level_reader = None
        self.levels = None
        self.map_grid = None
        self.generator = None

    def setUp(self):
        """setup before each test"""
        self.level_reader = LevelReader()
        levels = LevelReader().read_file_plain(os.path.join("files", "sokoban.txt"))
        self.map_grid = levels[6]
        self.generator = Generator(self.map_grid)

    def test_glue_on(self):
        """checks if template is added in correct place"""
        map_grid = self.map_grid
        template = self.generator.templates[0]
        template.glue_on(map_grid, (1, 1))
        for j_value in [value + 1 for value in range(template.height() - 1)]:
            for i_value in [value + 1 for value in range(template.width() - 1)]:
                self.assertEqual(map_grid[i_value][j_value], 'o', str(i_value)+str(j_value))

    def test_attach_template(self):
        """checks how the template is attached"""
        map_grid = self.map_grid
        template = self.generator.templates[0]
        template.glue_on(map_grid, (1, 1))
        for j_value in [value + 1 for value in range(template.height() - 1)]:
            for i_value in [value + 1 for value in range(template.width() - 1)]:
                self.assertEqual(map_grid[i_value][j_value], 'o', str(i_value)+str(j_value))

    def test_get_tile(self):
        """checks if getting file char by coordinates works correctly"""
        for j_value in range(self.generator.height - 1):
            for i_value in range(self.generator.width - 1):
                self.assertEqual(self.generator.get_tile((i_value, j_value)),
                                 self.generator.map_grid[i_value][j_value])

    # @unittest.expectedFailure
    def test_get_absent_tile(self):
        """this kind of numeration is not fine"""
        self.assertEqual(self.generator.get_tile((-1, -3)), None)

    def test_clean_map(self):
        """checks if cleaning leaves nothing but walls and floor"""
        self.generator.clean_map()
        clean_map = self.generator.map_grid
        for j in range(self.generator.height - 1):
            for i in range(self.generator.width - 1):
                self.assertEqual(clean_map[i][j]
                                 in ('#', 'x', ' '), True, "Map wasn't purged")

    def test_find_start(self):
        """tests locating start symbol"""
        position = self.generator.find_start('@')
        self.assertEqual(position, (4, 5))
        self.generator.map_grid[4][5] = ' '
        position = self.generator.find_start('@')
        self.assertEqual(position, None)

    def test_straighten_edges(self):
        """checks that function fills up edges"""
        check_s = FULL_EDGES
        self.generator.clean_map()
        self.generator.flood_fill((4, 5), ' ', 'k')
        self.generator.straighten_edges()
        self.generator.flood_fill((4, 5), 'k', ' ')
        test_s = ["".join(line) for line in self.generator.map_grid]

        for index in range(len(check_s) - 1):
            self.assertEqual(check_s[index], test_s[index])

    def test_mark_edges(self):
        """checks that function marks the very edges"""
        self.generator.clean_map()
        self.generator.flood_fill((4, 5), ' ', 'k')
        self.generator.straighten_edges()
        self.generator.flood_fill((4, 5), 'k', ' ')
        self.generator.mark_edges((4, 5), '#', '8')
        self.generator.flood_fill((4, 5), 'o', ' ')
        test_s = MARKED_EDGES
        check_s = ["".join(line) for line in self.generator.map_grid]

        for index in range(len(check_s) - 1):
            self.assertEqual(check_s[index], test_s[index])

    def test_thin_walls(self):
        """checks that function marks the very edges"""
        self.generator.clean_map()
        self.generator.flood_fill((4, 5), ' ', 'k')
        self.generator.straighten_edges()
        self.generator.flood_fill((4, 5), 'k', ' ')
        self.generator.mark_edges((4, 5), '#', '8')
        self.generator.thin_walls()
        self.generator.flood_fill((4, 5), 'o', ' ')
        test_s = THIN_EDGES
        check_s = ["".join(line) for line in self.generator.map_grid]
        for index in range(len(check_s) - 1):
            self.assertEqual(check_s[index], test_s[index])

    def test_is_inside(self):
        """checks if positions inside map grid are recognized"""
        for j in range(self.generator.height - 1):
            for i in range(self.generator.width - 1):
                self.assertEqual(self.generator.is_inside((i, j)), True, str(i)+str(j))

    def test_is_outside(self):
        """checks if positions outside map grid are not recognized"""
        self.assertEqual(self.generator.is_inside((0, 29)), False, str(0)+str(29))
        self.assertEqual(self.generator.is_inside((-1, 4)), False, str(0)+str(29))
        self.assertEqual(self.generator.is_inside((24, 1)), False, str(0)+str(29))
        self.assertEqual(self.generator.is_inside((40, 50)), False, str(0)+str(29))

    def test_is_wall(self):
        """checks if position is indeed wall"""
        for j in range(self.generator.height - 1):
            for i in range(self.generator.width - 1):
                self.assertEqual(self.generator.is_wall((i, j)),
                                 self.generator.map_grid[i][j] in ('#', 'x'), str(i)+str(j))

        self.assertEqual(self.generator.is_wall((-1, -10)), False, "Doesn't check if is inside")

    def test_flood_fill(self):
        """checks if area was colored"""
        self.generator.clean_map()
        self.generator.flood_fill((4, 5), ' ', 'H')
        test_s = FLOOD_FILL

        check_s = ["".join(line) for line in self.generator.map_grid]
        for index in range(len(test_s) - 1):
            self.assertEqual(check_s[index], test_s[index])

    def test_plant_goals(self):
        """algorithm is based on flood fill, and flood fill works"""
        self.generator.plant_goals(self.generator.map_grid, (4, 5))
        count = 0
        for j_value in range(self.generator.height - 1):
            for i_value in range(self.generator.width - 1):
                if self.generator.map_grid[i_value][j_value] == '.':
                    count += + 1
        self.assertEqual(count > 0, True, "low probability event")

    def test_plant_boxes(self):
        """algorithm is based on flood fill, and flood fill works"""
        self.generator.plant_boxes(self.generator.map_grid, (4, 5))
        count = 0
        for j_value in range(self.generator.height - 1):
            for i_value in range(self.generator.width - 1):
                if self.generator.map_grid[i_value][j_value] == '.':
                    count += + 1
        self.assertEqual(count > 0, True, "low probability event")

    def test_ends_in_corner(self):
        """checks if box can 'fall off' a slope or is stuck alongside a wall"""
        check = self.generator.ends_in_corner(self.generator.map_grid, (3, 8), -1, 0)
        self.assertEqual(check, True)
        check = self.generator.ends_in_corner(self.generator.map_grid, (3, 8), 0, 1)
        self.assertEqual(check, True)
        check = self.generator.ends_in_corner(self.generator.map_grid, (6, 7), -1, 0)
        self.assertEqual(check, True)
        check = self.generator.ends_in_corner(self.generator.map_grid, (6, 8), 0, 1)
        self.assertEqual(check, False)

    def test_can_place_box(self):
        """checks if box can be inserted"""
        self.generator.flood_fill((4, 5), ' ', 'o')
        check = self.generator.can_place_box(self.generator.map_grid, (2, 6))
        self.assertEqual(check, False)
        check = self.generator.can_place_box(self.generator.map_grid, (5, 9))
        self.assertEqual(check, False)
        check = self.generator.can_place_box(self.generator.map_grid, (7, 6))
        self.assertEqual(check, False)

if __name__ == '__main__':
    unittest.main()
