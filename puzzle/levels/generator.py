"""classes for generation of board objects"""

import random as rand
import copy


class Template(object):
    """representation of map fragment template for map generation"""

    def __init__(self, grid):
        self.grid = grid

    def width(self):
        """returns width of template"""
        return len(self.grid)

    def height(self):
        """returns height of template"""
        return len(self.grid[0])

    def glue_on(self, map_object, position):
        """sticks a template on object"""
        x_offset = -1
        for row in self.grid:
            x_offset += 1
            y_offset = -1
            for element in row:
                y_offset += 1
                map_object[position[0] + x_offset][position[1] + y_offset] = element


class Generator(object):
    """map grid that creates a template for level generation"""
    def __init__(self, map_obj):
        self.map_grid = map_obj
        self.height = len(map_obj[0])
        self.width = len(map_obj)
        self.start = self.find_start('@')

        self.templates = [Template([["o", "o"], ["o", "o"], ["o", "o"]]),
                          Template([["o", "o"], ["o", "o"]]),
                          Template([["o", "o", "o"], ["o", "#", "o"], ["o", "o", "o"]])]

        self.goal_count = 0
        self.box_count = 0

    def find_start(self, sign):
        """locates start symbol"""
        for row in self.map_grid:
            if sign in row:
                return self.map_grid.index(row), row.index(sign)
        return None

    def generate_board(self):
        """board factory method"""
        self.clean_map()
        self.flood_fill(self.start, ' ', 'o')
        self.straighten_edges()

        for template in self.templates:
            self.attach_template(template)

        self.start = self.find_start('o')

        self.flood_fill(self.start, 'o', ' ')
        self.mark_edges(self.start, '#', "$")
        self.thin_walls()
        self.flood_fill(self.start, 'o', ' ')
        self.mark_edges(self.start, '$', "#")

        map_copy = copy.deepcopy(self.map_grid)
        while self.goal_count < 3:
            self.plant_goals(map_copy, self.start)
            if self.goal_count >= 3:
                self.map_grid = map_copy
            else:
                map_copy = copy.deepcopy(self.map_grid)
                self.goal_count = 0

        self.flood_fill(self.start, ' ', 'o')

        map_copy = copy.deepcopy(self.map_grid)
        while self.box_count < self.goal_count:
            self.box_count = 0
            self.plant_boxes(map_copy, self.start)
            if self.box_count >= self.goal_count:
                self.map_grid = map_copy
            else:
                map_copy = copy.deepcopy(self.map_grid)
                self.box_count = 0

        if self.map_grid[self.start[0]][self.start[1]] == '.':
            self.map_grid[self.start[0]][self.start[1]] = '+'
        else:
            self.map_grid[self.start[0]][self.start[1]] = '@'

        return [''.join(line) for line in self.map_grid]

    def get_tile(self, position):
        """shortcut to the grid"""
        return self.map_grid[position[0]][position[1]]

    def clean_map(self):
        """deep copy of map, with all but floor and walls removed"""
        self.map_grid = [[self.clean_tile(element) for element in row] for row in self.map_grid]

    @staticmethod
    def clean_tile(element):
        """purge everything but floor and walls"""
        if element not in ('#', 'x'):
            return ' '
        else:
            return element

    def straighten_edges(self):
        """fills the outer edges of the map with walls"""
        self.map_grid = [[self.swap(element, ' ', '#') for element in row] for row in self.map_grid]

    @staticmethod
    def swap(element, old, new):
        """swaps element if it equals a specified element"""
        if element == old:
            return new
        else:
            return element

    def thin_walls(self):
        """opposite of straighten_edges; makes walls thin again"""
        self.map_grid = [[self.swap(element, '#', ' ') for element in row] for row in self.map_grid]

    def is_inside(self, position):
        """check if position is inside board boundaries"""
        return position[0] in range(self.width) and position[1] in range(self.height)

    def attach_template(self, template):
        """sticks a template to the surface of map"""
        # I need to keep a layer of walls at the edges
        x_pos = rand.randint(1, self.width - template.width() - 1)
        y_pos = rand.randint(1, self.height - template.height() - 1)
        template.glue_on(self.map_grid, (x_pos, y_pos))

    def is_wall(self, position):
        """check if position marks a wall"""
        return self.is_inside(position) and self.map_grid[position[0]][position[1]] in ('#', 'x')

    def flood_fill(self, position, tile, re_tile):
        """differentiate outside floor from inside floor, to be able to decorate the outside"""
        # this version walks over goals
        x_value, y_value = position
        if tile != re_tile and self.is_inside(position):
            tile_pattern = self.map_grid[x_value][y_value]
            if tile_pattern == tile:
                self.map_grid[x_value][y_value] = re_tile
            if tile_pattern == '.':
                self.map_grid[x_value][y_value] = ','
            if tile_pattern in (tile, '.'):
                self.flood_fill((x_value - 1, y_value), tile, re_tile)
                self.flood_fill((x_value + 1, y_value), tile, re_tile)
                self.flood_fill((x_value, y_value - 1), tile, re_tile)
                self.flood_fill((x_value, y_value + 1), tile, re_tile)

    def mark_edges(self, position, tile, re_tile):
        """mark walls at the edge of the inside area"""
        x_value, y_value = position
        if tile != re_tile and self.is_inside(position):
            if self.map_grid[x_value][y_value] not in (tile, re_tile, "o"):
                self.map_grid[x_value][y_value] = "o"
                self.mark_edges((x_value - 1, y_value), tile, re_tile)
                self.mark_edges((x_value + 1, y_value), tile, re_tile)
                self.mark_edges((x_value, y_value - 1), tile, re_tile)
                self.mark_edges((x_value, y_value + 1), tile, re_tile)
            elif self.map_grid[x_value][y_value] == tile\
                    and self.map_grid[x_value][y_value] != re_tile:
                self.map_grid[x_value][y_value] = re_tile

    def plant_goals(self, map_grid, position):
        """plant goals in the inside area;
        map grid must be the same size as the main map"""
        x_value, y_value = position
        if self.is_inside(position):
            if map_grid[x_value][y_value] == 'o':
                if rand.randint(0, 99) > 7:
                    map_grid[x_value][y_value] = ' '
                else:
                    map_grid[x_value][y_value] = '.'
                    self.goal_count += 1
#                    print self.goal_count
                self.plant_goals(map_grid, (x_value - 1, y_value))
                self.plant_goals(map_grid, (x_value + 1, y_value))
                self.plant_goals(map_grid, (x_value, y_value - 1))
                self.plant_goals(map_grid, (x_value, y_value + 1))

    def plant_boxes(self, map_grid, position):
        """plant boxes in the inside area;
        map grid must be the same size as the main map"""
        x_value, y_value = position
        if self.is_inside(position):
            tile = map_grid[x_value][y_value]

            if tile in ('o', ','):
                if self.box_count >= self.goal_count or rand.randint(0, 99) > 20:
                    if tile == 'o':
                        map_grid[x_value][y_value] = ' '
                    if tile == ',':
                        map_grid[x_value][y_value] = '.'
                else:
                    if tile == ',':
                        map_grid[x_value][y_value] = '*'
                        self.box_count += 1
                    elif self.can_place_box(map_grid, position):
                        map_grid[x_value][y_value] = '$'
                        self.box_count += 1
                    else:
                        map_grid[x_value][y_value] = ' '

                self.plant_boxes(map_grid, (x_value - 1, y_value))
                self.plant_boxes(map_grid, (x_value + 1, y_value))
                self.plant_boxes(map_grid, (x_value, y_value - 1))
                self.plant_boxes(map_grid, (x_value, y_value + 1))

    @staticmethod
    def ends_in_corner(map_grid, position, x_offset, y_offset):
        """checks if box that is leaning on the wall can be pushed away from it"""
        x_walk, y_walk = position
        corner = False
        while map_grid[x_walk + x_offset][y_walk + y_offset] != ' '\
                and map_grid[x_walk][y_walk] == ' ':
            if y_offset != 0 and x_offset == 0:
                x_walk -= 1
            if y_offset == 0 and x_offset != 0:
                y_walk -= 1
        if map_grid[x_walk][y_walk] != ' ':
            corner = True

        if not corner:
            while map_grid[x_walk + x_offset][y_walk + y_offset] != ' '\
                    and map_grid[x_walk][y_walk] == ' ':
                if y_offset != 0 and x_offset == 0:
                    x_walk += 1
                if y_offset == 0 and x_offset != 0:
                    y_walk += 1
            if map_grid[x_walk][y_walk] != ' ':
                corner = True

        return corner

    def can_place_box(self, map_grid, position):
        """checks if box can be placed"""
        x_value, y_value = position
        if map_grid[x_value][y_value] in ('o', ','):
            count_walls = 0
            straight_line1 = 0
            straight_line2 = 0

            # if map_grid[x_value][y_value - 1] in ('$', '*') or\
            # map_grid[x_value][y_value + 1] in ('$', '*') or\
            # map_grid[x_value - 1][y_value] in ('$', '*') or\
            # map_grid[x_value + 1][y_value] in ('$', '*'):
            # return False

            way_horizontal_blocked = False
            way_vertical_blocked = False

            if self.is_wall((x_value, y_value - 1)):
                count_walls += 1
                straight_line1 += 1

                way_horizontal_blocked = self.ends_in_corner(map_grid, (x_value, y_value), 0, -1)

            if self.is_wall((x_value, y_value + 1)):
                count_walls += 1
                straight_line1 += 1

                way_horizontal_blocked = self.ends_in_corner(map_grid, (x_value, y_value), 0, 1)

            if self.is_wall((x_value - 1, y_value)):
                count_walls += 1
                straight_line2 += 1

                way_vertical_blocked = self.ends_in_corner(map_grid, (x_value, y_value), -1, 0)

            if self.is_wall((x_value + 1, y_value)):
                count_walls += 1
                straight_line2 += 1

                way_vertical_blocked = self.ends_in_corner(map_grid, (x_value, y_value), 1, 0)

            if way_vertical_blocked or way_horizontal_blocked:
                return False
            if count_walls > 2 or \
                    (count_walls == 2 and straight_line1 < 2 and straight_line2 < 2):
                return False
            else:
                return True
        return False
