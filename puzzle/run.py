"""this script starts the game"""

import os
from puzzle.game_engine.game_engine import PlainGameEngine

PlainGameEngine(os.path.join('levels', 'sokoban.txt')).run()
