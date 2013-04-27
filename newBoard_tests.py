from unittest import TestCase, main
from ipdb import set_trace as trace
from newBoard import *


class TestWhitePawnMoves(TestCase):

    def setUp(self):
        free_spaces = {letter:{number:Square(letter+number) for number in "12345678"} for letter in "abcdefgh"}
        self.b = Board(free_spaces)

    def test_first_move_one_space(self):
        self.assertEqual(self.b.a2.move("a3"), (True, "normal", None))
        self.assertEqual(self.b.a3.move("a4"), (True, "normal", None))
        self.assertEqual(self.b.a4.move("a6"), (False, "", None))

    def test_first_move_two_spaces(self):
        self.assertEqual(self.b.a2.move("a4"), (True, "normal", None))
        self.assertEqual(self.b.a4.move("a6"), (False, "", None))
        self.assertEqual(self.b.a4.move("a5"), (True, "normal", None))

    def test_normal_attack(self):
        self.b.a2.move("a4")
        self.b.a4.move("a5")
        self.b.b7.move("b6")
        self.assertEqual(self.b.a5.move("b6"), (True, "attack", None))

    def test_empassant(self):
        self.b.a2.move("a4")
        self.b.a4.move("a5")
        self.b.b7.move("b5")
        move = self.b.a5.move("b6")
        self.assertEqual(move[:2], (True, "empassant"))
        self.assertIsInstance(move[-1], Square)

    def test_empassant_invalid(self):
        self.b.a2.move("a4")
        self.b.a4.move("a5")
        self.b.b7.move("b5")
        #~ Removes empassant ability
        self.b.h7.move("h6")
        self.assertEqual(self.b.a5.move("b6"), (False, "", None))

    def test_attack_invalid(self):
        self.b.a2.move("a4")
        self.b.a7.move("a5")
        self.assertEqual(self.b.a4.move("a5"), (False, "", None))

main()
