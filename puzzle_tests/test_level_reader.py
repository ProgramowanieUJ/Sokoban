"""testing LevelReader"""

from puzzle_tests.maps import FULL_TEST_STRING
from puzzle.levels import LevelReader
import unittest
import os


class TestLevelReader(unittest.TestCase):
    """testing LevelReader"""

    def __init__(self, *args, **kwargs):
        """init"""
        super(TestLevelReader, self).__init__(*args, **kwargs)
        self.level_reader = None
        self.full_test_string = None

    def setUp(self):
        """setup"""
        self.level_reader = LevelReader()

        self.full_test_string = FULL_TEST_STRING

    def test_read_file(self):
        """checks that the whole file is read and an empty line is added;
        if wrong, writes out coordinates of differing chars"""
        check_s = self.full_test_string
        test_s = self.level_reader.read_file(os.path.join("files", "level_reader.txt"))
        test_s = "".join(test_s)
        diff = [i for i in xrange(len(check_s)) if check_s[i] != test_s[i]]
        self.assertEqual([], diff, diff)

    def test_clean_line(self):
        """checks that function removes only \n\r and chars after ;"""
        check_s = "abc"
        test_s = self.level_reader.clean_line("abc\n")
        self.assertEqual(check_s, test_s, test_s)
        check_s = "abc"
        test_s = self.level_reader.clean_line("abc\r")
        self.assertEqual(check_s, test_s, test_s)
        check_s = "ab"
        test_s = self.level_reader.clean_line("ab;c")
        self.assertEqual(check_s, test_s, test_s)
        check_s = "abcdef4534''?.>"
        test_s = self.level_reader.clean_line("abcdef4534''?.>")
        self.assertEqual(check_s, test_s, test_s)

    def test_pad_lines(self):
        """checks that function makes line length even"""
        check_s = self.full_test_string
        test_s = self.level_reader.pad_lines(check_s)
        evened_out = sum([len(line) == len(test_s[0]) for line in test_s])
        self.assertEqual(len(test_s), evened_out, "uneven level")

    def test_wrong_filename_board(self):
        """checks if the file entered is the file read"""
        check_s = self.full_test_string
        test_s = self.level_reader.read_levels_file(check_s)
        self.assertEqual(test_s, None, "Some file was read")

    def test_check_count_board(self):
        """checks whether raw level boundaries are recognized"""
        test_s = self.level_reader.read_levels_file(os.path.join("files", "sokoban.txt"))
        self.assertEqual(len(test_s), 50, "Level count can't be " + str(len(test_s)))

    def test_nonsense_data_board(self):
        """checks reaction for nonsense data"""
        test_s = self.level_reader.read_levels_file\
            (os.path.join("files", "data_error.txt"))
        self.assertEqual(len(test_s), 1,
                         "Levels with errors were accepted: " + str(len(test_s) - 1))

    def test_wrong_filename_plain(self):
        """checks if the file entered is the file read"""
        check_s = self.full_test_string
        test_s = self.level_reader.read_file_plain(check_s)
        self.assertEqual(test_s, None, "Some file was read")

    def test_check_count_plain(self):
        """checks whether raw level boundaries are recognized"""
        test_s = self.level_reader.read_file_plain(os.path.join("files", "sokoban.txt"))
        self.assertEqual(len(test_s), 50, "Level count can't be " + str(len(test_s)))

    def test_nonsense_data_plain(self):
        """checks reaction for nonsense data"""
        test_s = self.level_reader.read_file_plain(os.path.join("files", "data_error.txt"))
        self.assertEqual(len(test_s), 1,
                         "Levels with errors were accepted: " + str(len(test_s) - 1))

if __name__ == '__main__':
    unittest.main()
