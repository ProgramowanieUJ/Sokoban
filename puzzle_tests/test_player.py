"""testing Player"""

from puzzle.players import Player
import unittest
import pygame.locals as key
import pygame


class TestPlayer(unittest.TestCase):
    """testing Player"""

    def __init__(self, *args, **kwargs):
        """test board init"""
        super(TestPlayer, self).__init__(*args, **kwargs)
        self.player = None
        # commands: error freeze solo dual switch
        self.solo_dictionary = None
        self.dual_dictionary = None

    def setUp(self):
        """setup before each test"""
        self.player = Player()
        self.solo_dictionary = {key.K_LEFT: "left_A", key.K_RIGHT: "right_A", key.K_UP: "up_A",
                                key.K_DOWN: "down_A", key.K_TAB: "start", key.K_BACKSPACE: "reload",
                                key.K_n: "next", key.K_p: "previous"}
        self.dual_dictionary = {key.K_a: "left_B", key.K_d: "right_B",
                                key.K_w: "up_B", key.K_s: "down_B"}
        self.dual_dictionary.update(self.solo_dictionary)

    def test_freeze(self):
        """is here to signal that current state should be maintained
         and no display reload is needed"""
        event = pygame.event.Event(key.KEYDOWN, key=key.K_LEFT)
        command = self.player.move_in_starting_screen(event)
        event = pygame.event.Event(key.KEYDOWN, key=key.K_s)
        self.assertEqual(self.player.command(command, event), "solo")

    def test_move_in_starting_screen(self):
        """checks actions that can be made in the starting screen"""
        event = pygame.event.Event(key.KEYDOWN, key=key.K_s)
        self.assertEqual(self.player.command("start", event), "solo")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_d)
        self.assertEqual(self.player.command("start", event), "dual")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_a)
        self.assertEqual(self.player.command("start", event), "freeze")
        self.assertEqual(self.player.last_command, "start")

    def test_move_in_error_screen(self):
        """checks actions that can be made in the error screen"""
        event = pygame.event.Event(key.KEYDOWN, key=key.K_s)
        self.assertEqual(self.player.command("error", event), "start")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_d)
        self.assertEqual(self.player.command("error", event), "start")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_a)
        self.assertEqual(self.player.command("error", event), "start")
        self.assertEqual(self.player.last_command, "error")

    def test_move_in_solo_mode(self):
        """checks actions that can be made in the error screen"""
        event = pygame.event.Event(key.KEYDOWN, key=key.K_b)
        self.assertEqual(self.player.command("solo", event), "freeze")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_LEFT)
        self.assertEqual(self.player.command("solo", event), self.solo_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_RIGHT)
        self.assertEqual(self.player.command("solo", event), self.solo_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_UP)
        self.assertEqual(self.player.command("solo", event), self.solo_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_DOWN)
        self.assertEqual(self.player.command("solo", event), self.solo_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_TAB)
        self.assertEqual(self.player.command("solo", event), self.solo_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_BACKSPACE)
        self.assertEqual(self.player.command("solo", event), self.solo_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_n)
        self.assertEqual(self.player.command("solo", event), self.solo_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_p)
        self.assertEqual(self.player.command("solo", event), self.solo_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_w)
        self.assertEqual(self.player.command("solo", event), "freeze")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_s)
        self.assertEqual(self.player.command("solo", event), "freeze")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_a)
        self.assertEqual(self.player.command("solo", event), "freeze")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_d)
        self.assertEqual(self.player.command("solo", event), "freeze")
        self.assertEqual(self.player.last_command, "solo")

    def test_move_in_dual_mode(self):
        """represents actions that can be made in the error screen"""
        event = pygame.event.Event(key.KEYDOWN, key=key.K_b)
        self.assertEqual(self.player.command("dual", event), "freeze")
        event = pygame.event.Event(key.KEYDOWN, key=key.K_LEFT)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_RIGHT)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_UP)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_DOWN)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_TAB)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_BACKSPACE)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_n)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_p)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_w)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_s)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_a)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        event = pygame.event.Event(key.KEYDOWN, key=key.K_d)
        self.assertEqual(self.player.command("dual", event), self.dual_dictionary[event.key])
        self.assertEqual(self.player.last_command, "dual")

    def test_switch_levels(self):
        """tests switching levels command"""
        event = pygame.event.Event(key.KEYDOWN, key=key.K_d)
        self.assertEqual(self.player.command("switch", event), "reload")

if __name__ == '__main__':
    unittest.main()
