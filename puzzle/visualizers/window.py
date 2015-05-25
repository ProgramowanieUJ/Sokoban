"""this is the advanced graphics module"""

import puzzle.visualizers.graphics as graphics
import pygame
import pygame.locals as key


KEYS = {"left_A": "left", "right_A": "right",
        "up_A": "up", "down_A": "down",
        "left_B": "left", "right_B": "right",
        "up_B": "up", "down_B": "down"}


class Window(object):
    """window graphics and logic"""
    def __init__(self):
        pygame.init()

        self.window_width = pygame.display.list_modes(32)[0][0]
        self.window_height = pygame.display.list_modes(32)[0][1]
        self.surface_display = self.new_surface()
        self.dicts = graphics.Graphics()

        self.draw_text(["loading . . ."], 100)
        pygame.display.update()

        self.commands = {"start": self.start_screen,
                         "error": self.display_error_screen,
                         "solo": self.display_solo_game,
                         "freeze": self.freeze,
                         "dual": self.display_dual_game,
                         "reload": self.reload_game}
        self.mode = "solo"
        self.level = None

    def reset_level(self):
        """returns level to starting state"""
        self.level = (self.level[0].reset(), self.level[0].mirror())

    def new_surface(self):
        """creates new display"""
        return pygame.display.set_mode((self.window_width, self.window_height))
        # return pygame.display.set_mode((self.window_width, self.window_height),
        #                               pygame.FULLSCREEN, 32)

    def display(self, command):
        """respond to players command"""
        if command in self.commands:
            return self.commands[command]()
        if command in KEYS:
            if self.mode == "solo":
                return self.redraw_solo_level(command)
            if self.mode == "dual":
                return self.redraw_dual_level(command)

    def draw_text(self, instructions, top_coordinates):
        """draw text in window"""
        for text in instructions:
            instructions_surface =\
                self.dicts.basic_font.render(text, 1, self.dicts.colors["white"])
            instructions_rectangle = instructions_surface.get_rect()
            top_coordinates += 10  # pixels between lines.
            instructions_rectangle.top = top_coordinates
            instructions_rectangle.centerx = self.window_width / 2
            top_coordinates += instructions_rectangle.height
            self.surface_display.blit(instructions_surface, instructions_rectangle)
        return top_coordinates

    def draw_picture(self, picture, top_coordinates):
        """display picture in window"""
        rectangle = self.dicts.images_dictionary[picture].get_rect()
        rectangle.top = top_coordinates
        rectangle.centerx = self.window_width / 2
        top_coordinates += rectangle.height

        self.surface_display.blit(self.dicts.images_dictionary[picture], rectangle)
        return top_coordinates

    @staticmethod
    def loop(command):
        """maintain state until event"""
        while True:
            for event in pygame.event.get():
                if event.type == key.QUIT or event.type == key.KEYDOWN:
                    return command, event

    def freeze(self):
        """maintain state"""
        return self.loop("freeze")

    def reload_game(self):
        """returns the board to original state"""
        self.reset_level()
        if self.mode == "solo":
            return self.display_solo_game()
        if self.mode == "dual":
            return self.display_dual_game()

    def start_screen(self):
        """show start screen"""
        self.reset_level()

        instructions = ['Push the stars over the marks.',
                        'S - starts solo game, D - starts dual game',
                        'WASD - Player 1 move, Arrow keys - Player 2 move',
                        'Backspace - reset level, Esc - quit.',
                        'N - next level, B - go back a level.']

        pygame.display.set_caption('SOKOBAN')

        self.surface_display = self.new_surface()
        self.surface_display.fill(self.dicts.colors["green"])
        top_coordinates = self.draw_picture('title', 50)
        self.draw_text(instructions, top_coordinates)

        pygame.display.update()

        return self.loop("start")

    def display_error_screen(self):
        """show error screen"""
        self.reset_level()

        instructions = ['No level file found',
                        'Push any key to get back to menu']

        self.surface_display = self.new_surface()
        self.surface_display.fill(self.dicts.colors["green"])
        top_coordinates = self.draw_picture('error', 100)
        self.draw_text(instructions, top_coordinates)

        pygame.display.update()

        return self.loop("error")

    def display_dual_game(self):
        """shows dual game board"""
        self.mode = "dual"

        if self.level is None:
            return self.display_error_screen()
        else:
            level_a = self.level[0]
            level_b = self.level[1]

            width = (self.window_width-30)/2
            height = self.window_height-20
            self.surface_display.fill(self.dicts.colors["green"])
            surface_a = self.draw_level(level_a, width, height)
            rectangle_a = surface_a.get_rect()
            rectangle_a.center = (self.window_width/4, self.window_height/2)

            surface_b = self.draw_level(level_b, width, height)
            rectangle_b = surface_b.get_rect()
            rectangle_b.center = (0.75 * self.window_width, self.window_height/2)

            divide = pygame.Surface((10, self.window_height))
            divide.fill(self.dicts.colors["dark green"])
            line = surface_b.get_rect()
            line.left = self.window_width/2 - 5

            self.surface_display.blit(surface_a, rectangle_a)
            self.surface_display.blit(surface_b, rectangle_b)
            self.surface_display.blit(divide, line)
            pygame.display.update()

        if level_a.is_finished() or level_b.is_finished():
            return self.loop("next")
        return self.loop("dual")

    def display_solo_game(self):
        """shows solo game board"""
        self.mode = "solo"

        if self.level is None:
            return self.display_error_screen()
        else:
            self.surface_display.fill(self.dicts.colors["green"])
            level_surface = self.draw_level(self.level[0],
                                            self.window_width - 20, self.window_height - 20)
            rectangle = level_surface.get_rect()
            rectangle.center = (self.window_width/2, self.window_height/2)
            self.surface_display.blit(level_surface, rectangle)
            pygame.display.update()

        if self.level[0].is_finished():
            return self.loop("next")

        return self.loop("solo")

    def draw_level(self, level, background_width, background_height):
        """draws level from the board"""
        tile_size = {"width": 50, "height": 85, "floor": 40}

        surface_width = level.width * tile_size["width"]
        surface_height = level.height * tile_size["floor"] + tile_size["height"]

        map_surface = pygame.Surface((surface_width, surface_height))
        map_surface.fill(self.dicts.colors["light green"])

        for x_value in range(level.width):
            for y_value in range(level.height):
                position = (x_value, y_value)
                tile = level.map_grid.get_tile(position)
                rectangle = pygame.Rect((x_value * tile_size["width"],
                                         y_value * tile_size["floor"],
                                         tile_size["width"], tile_size["height"]))

                if tile in self.dicts.tile_mapping:
                    map_surface.blit(self.dicts.tile_mapping[tile], rectangle)
                elif tile in self.dicts.decoration_mapping:
                    map_surface.blit(self.dicts.tile_mapping[' '], rectangle)

                if tile in self.dicts.decoration_mapping:
                    map_surface.blit(self.dicts.decoration_mapping[tile], rectangle)
                elif position in level.boxes_list:
                    if position in level.goal_list:
                        map_surface.blit(self.dicts.images_dictionary['covered goal'], rectangle)
                    map_surface.blit(self.dicts.images_dictionary['star'], rectangle)
                elif position in level.goal_list:
                    map_surface.blit(self.dicts.images_dictionary['uncovered goal'], rectangle)

                if position == level.player:
                    map_surface.blit(self.dicts.player_image, rectangle)

        if level.is_finished():
            win_image = self.dicts.images_dictionary["win"]
            if win_image.get_rect().width > surface_width:
                win_image = pygame.transform.scale(win_image,
                                                   (surface_width, win_image.get_rect().height))
            rectangle = win_image.get_rect()
            rectangle.top = 20
            rectangle.centerx = surface_width / 2
            map_surface.blit(win_image, rectangle)

        return self.resize_surface(map_surface, background_width, background_height)

    @staticmethod
    def resize_surface(map_surface, background_width, background_height):
        """in particular allows the double board surface to be matched to the screen size"""
        surface_width = map_surface.get_width()
        surface_height = map_surface.get_height()
        if surface_height > background_height:
            surface_width = surface_width * background_height / surface_height
            surface_height = background_height
            map_surface = pygame.transform.scale(map_surface,
                                                 (surface_width, surface_height))
        if surface_width > background_width:
            surface_height = surface_height * background_width / surface_width
            surface_width = background_width
            map_surface = pygame.transform.scale(map_surface,
                                                 (surface_width, surface_height))
        return map_surface

    def redraw_solo_level(self, direction):
        """reaction to the direction keys"""
        self.level[0].step(KEYS[direction])
        return self.display_solo_game()

    def redraw_dual_level(self, direction):
        """reaction to the direction keys"""
        if direction.endswith("A"):
            self.level[1].step(KEYS[direction])
        elif direction.endswith("B"):
            self.level[0].step(KEYS[direction])
        return self.display_dual_game()
