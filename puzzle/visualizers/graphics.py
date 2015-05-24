"""the Graphics class delivers all graphics for Window class"""

import pygame
import os


class Graphics(object):
    """the Window class depends on Graphics for all colors and images"""
    def __init__(self):
        pygame.init()

        self.colors = self.get_colors()
        self.basic_font = pygame.font.SysFont('comicsansms', 22)
        self.image_paths = self.get_all_images()
        self.images_dictionary = self.get_images_dictionary()
        self.tile_mapping = self.get_tiles()
        self.decoration_mapping = self.get_decorations()
        self.player_image = self.get_player()

    @staticmethod
    def path_of(file_name):
        """creates a proper file path"""
        return os.path.join('visualizers', 'images', file_name)

    @staticmethod
    def get_colors():
        """creates a color dictionary"""
        return {"green": (102, 204, 0),
                "white": (255, 255, 255),
                "light green": (178, 255, 102),
                "dark green": (25, 100, 0)}

    def get_all_images(self):
        """creates an image path dictionary"""
        return {'uncovered goal': self.path_of('red_selector.png'),
                'covered goal': self.path_of('selector.png'),
                'star': self.path_of('star.png'),
                'corner': self.path_of('wall.png'),
                'wall': self.path_of('corner.png'),
                'inside floor': self.path_of('plain_block.png'),
                'outside floor': self.path_of('grass_block.png'),
                'title': self.path_of('star_title.png'),
                'boy': self.path_of('boy.png'),
                'rock': self.path_of('rock.png'),
                'short tree': self.path_of('short_tree.png'),
                'tall tree': self.path_of('tall_tree.png'),
                'ugly tree': self.path_of('bush.png'),
                'error': self.path_of('error.png'),
                'win': self.path_of('win.png')}

    def get_images_dictionary(self):
        """creates a ready image dictionary"""
        return {'uncovered goal': pygame.image.load(self.image_paths['uncovered goal']),
                'covered goal': pygame.image.load(self.image_paths['covered goal']),
                'star': pygame.image.load(self.image_paths['star']),
                'corner': pygame.image.load(self.image_paths['corner']),
                'wall': pygame.image.load(self.image_paths['wall']),
                'inside floor': pygame.image.load(self.image_paths['inside floor']),
                'outside floor': pygame.image.load(self.image_paths['outside floor']),
                'title': pygame.image.load(self.image_paths['title']),
                'boy': pygame.image.load(self.image_paths['boy']),
                'rock': pygame.image.load(self.image_paths['rock']),
                'short tree': pygame.image.load(self.image_paths['short tree']),
                'tall tree': pygame.image.load(self.image_paths['tall tree']),
                'ugly tree': pygame.image.load(self.image_paths['ugly tree']),
                'error': pygame.image.load(self.image_paths['error']),
                'win': pygame.image.load(self.image_paths['win'])}

    def get_tiles(self):
        """creates a tile dictionary"""
        return {'x': self.images_dictionary['corner'],
                '#': self.images_dictionary['wall'],
                'o': self.images_dictionary['inside floor'],
                ' ': self.images_dictionary['outside floor']}

    def get_decorations(self):
        """creates a decorations dictionary"""
        return {'1': self.images_dictionary['rock'],
                '2': self.images_dictionary['short tree'],
                '3': self.images_dictionary['tall tree'],
                '4': self.images_dictionary['ugly tree']}

    def get_player(self):
        """returns player image"""
        return self.images_dictionary['boy']
