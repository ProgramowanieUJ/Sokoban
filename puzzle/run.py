"""this script starts the game"""

import os
from puzzle.game_engine import PlainGameEngine

PlainGameEngine(os.path.join('game_engine', 'sokoban.txt')).run()
