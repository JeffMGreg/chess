from unittest import TestCase, main

from newBoard import *


class TestWhitePawnMoves(TestCase):
    
    def setUp(self):
        self.b = Board()

    def tearDown(self):
        del self.b

    def test_first_move_one_space(self):
        self.assertEqual(self.b.a2.move("a3"), (True, "normal"))
        self.assertEqual(self.b.a3.move("a4"), (True, "normal"))

    def test_first_move_two_spaces(self):
        self.assertEqual(self.b.a2.move("a4"), (True, "normal"))
        self.assertEqual(self.b.a4.move("a6"), (False, ""))
        self.assertEqual(self.b.a4.move("a5"), (True, "normal"))

main()
