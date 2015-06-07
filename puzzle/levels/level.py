"""anything connected to the game board and the creation of it"""

from copy import deepcopy

DIRECTIONS = {"up": (0, -1),
              "down": (0, 1),
              "right": (1, 0),
              "left": (-1, 0)}


class Board(object):
    """game board with all amenities"""
    def __init__(self):
        self.width = None
        self.height = None
        self.map_grid = None

        self.boxes_list = []
        self.goal_list = []
        self.player = None
        self.starting_state = {}

    def is_correct(self):
        """checking the board created from file for nonsense"""
        start = self.starting_state["player"]
        if start is None:
            return False
        if len(start) != 2 or not isinstance(start[0], (int, long)) \
                or not isinstance(start[1], (int, long)):
            return False
        if len(self.goal_list) == 0:
            return False
        if len(self.boxes_list) < len(self.goal_list):
            return False

        for box in self.boxes_list:
            if box not in self.goal_list:
                return True
        return False

    def set_map(self, map_grid, start):
        """establish starting state, board map, height and width"""
        self.starting_state = {"player": start,
                               "boxes": deepcopy(self.boxes_list)}
        self.map_grid = Map(map_grid, start)
        self.height = self.map_grid.height
        self.width = self.map_grid.width

    def save_state(self):
        """saves current state"""
        self.starting_state = {"player": self.player,
                               "boxes": deepcopy(self.boxes_list)}

    def reset(self):
        """resets board to the starting state"""
        start = self.starting_state["player"]
        self.boxes_list = deepcopy(self.starting_state["boxes"])
        self.player = start
        self.set_map(self.map_grid.map_grid, start)
        return self

    def get_tile(self, position):
        """shortcut to the grid"""
        return self.map_grid.get_tile(position)

    def is_inside(self, position):
        """check if position is inside board boundaries"""
        return self.map_grid.is_inside(position)

    def is_wall(self, position):
        """check if position marks a wall"""
        return self.map_grid.is_wall(position)

    def mirror(self):
        """create a mirrored board, but differently decorated"""
        start = self.starting_state["player"]
        start = (self.width - start[0] - 1, start[1])
        mirror = Board()
        mirror.goal_list = self.mirror_position_list(self.goal_list)
        mirror.boxes_list = self.mirror_position_list(self.boxes_list)
        mirror.player = start
        mirror.set_map(self.map_grid.map_grid[::-1], start)
        return mirror

    def mirror_position_list(self, tile_list):
        """create a list with mirrored dimensions"""
        return [(self.width - position[0] - 1, position[1]) for position in tile_list]

    def step(self, direction):
        """makes a step or pushed a box if possible"""
        direction = DIRECTIONS[direction]
        destination = self.move(self.player, direction)

        if not self.is_wall(destination):
            if destination in self.boxes_list:
                if not self.is_wall(self.move(destination, direction)) \
                        and self.move(destination, direction) not in self.boxes_list:
                    index = self.boxes_list.index(destination)
                    self.boxes_list[index] = self.move(self.boxes_list[index], direction)
                    self.player = self.move(self.player, direction)
                    return True
            else:
                self.player = self.move(self.player, direction)
                return True
        return False

    @staticmethod
    def move(what, where):
        """adjust coordinates of a grid object"""
        return what[0] + where[0], what[1] + where[1]

    def is_finished(self):
        """recognizes a finished game"""
        return all([box in self.goal_list for box in self.boxes_list])


class Map(object):
    """advanced map grid that can be interpreted by visualizer classes"""
    def __init__(self, map_obj, start):
        self.decoration_count = 20
        self.map_grid = map_obj
        self.height = len(map_obj[0])
        self.width = len(map_obj)
        self.map_grid = self.clean_map()
        self.flood_fill(start, ' ', 'o')
        self.decorate()

    def get_tile(self, position):
        """shortcut to the grid"""
        return self.map_grid[position[0]][position[1]]

    def clean_map(self):
        """deep copy of map, with all but floor and walls removed"""
        return [[self.clean_tile(element) for element in row] for row in self.map_grid]

    @staticmethod
    def clean_tile(element):
        """purge everything but floor and walls"""
#        if element in ('$', '.', '@', '+', '*', '1', '2', '3'):
        if element not in ('#', 'x'):
            return ' '
        else:
            return element

    def is_inside(self, position):
        """check if position is inside board boundaries"""
        x_value, y_value = position
        if x_value in range(self.width) and y_value in range(self.height):
            return True
        else:
            return False

    def is_wall(self, position):
        """check if position marks a wall"""
        x_value, y_value = position
        if self.is_inside(position) and self.map_grid[x_value][y_value] in ('#', 'x'):
            return True
        else:
            return False

    def flood_fill(self, position, tile, re_tile):
        """differentiate outside floor from inside floor, to be able to decorate the outside"""
        x_value, y_value = position
        if tile != re_tile and self.is_inside(position):
            # print x_value, y_value, "out of", self.width, self.height
            if self.map_grid[x_value][y_value] == tile:
                self.map_grid[x_value][y_value] = re_tile
                self.flood_fill((x_value - 1, y_value), tile, re_tile)
                self.flood_fill((x_value + 1, y_value), tile, re_tile)
                self.flood_fill((x_value, y_value - 1), tile, re_tile)
                self.flood_fill((x_value, y_value + 1), tile, re_tile)

    def decorate(self):
        """mark wall intersections as corners to display different graphics"""
        import random
        for row in self.map_grid:
            x_value = self.map_grid.index(row)
            for y_value in range(len(row)):
                # recognize corners
                if self.map_grid[x_value][y_value] == '#':
                    count_walls = 0
                    straight_line1 = 0
                    straight_line2 = 0
                    if self.is_wall((x_value, y_value - 1)):
                        count_walls += 1
                        straight_line1 += 1
                    if self.is_wall((x_value, y_value + 1)):
                        count_walls += 1
                        straight_line1 += 1
                    if self.is_wall((x_value - 1, y_value)):
                        count_walls += 1
                        straight_line2 += 1
                    if self.is_wall((x_value + 1, y_value)):
                        count_walls += 1
                        straight_line2 += 1

                    if count_walls > 2 or \
                            (count_walls == 2 and straight_line1 < 2 and straight_line2 < 2):
                        self.map_grid[x_value][y_value] = 'x'

                elif self.map_grid[x_value][y_value] == ' ' \
                        and random.randint(0, 99) < self.decoration_count:
                    self.map_grid[x_value][y_value] = str(random.choice(range(4)) + 1)
