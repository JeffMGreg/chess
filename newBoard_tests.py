from unittest import TestCase, main
from ipdb import set_trace as trace
from newBoard import *


class TestWhitePawnMoves(TestCase):

    def setUp(self):
        free_spaces = {letter:{number:Square(letter+number) for number in "12345678"} for letter in "abcdefgh"}
        self.b = Board(free_spaces)
        self.b.SHOW_BOARD = False

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

    def test_empassant_on_non_pawn(self):
        self.b.d2.move("d4")
        self.b.d4.move("d5")
        self.b.e7.move("e5")
        self.b.f8.move("c5")
        self.assertEqual(self.b.d5.move("c6"), (False, "", None))


class TestBlackPawnMoves(TestCase):

    def setUp(self):
        free_spaces = {letter:{number:Square(letter+number) for number in "12345678"} for letter in "abcdefgh"}
        self.b = Board(free_spaces)
        self.b.SHOW_BOARD = False

    def test_first_move_one_space(self):
        self.assertEqual(self.b.a7.move("a6"), (True, "normal", None))
        self.assertEqual(self.b.a6.move("a5"), (True, "normal", None))
        self.assertEqual(self.b.a5.move("a3"), (False, "", None))

    def test_first_move_two_spaces(self):
        self.assertEqual(self.b.a7.move("a5"), (True, "normal", None))
        self.assertEqual(self.b.a5.move("a3"), (False, "", None))
        self.assertEqual(self.b.a5.move("a4"), (True, "normal", None))

    def test_normal_attack(self):
        self.b.b2.move("b4")
        self.b.b4.move("b5")
        self.b.a7.move("a6")
        self.assertEqual(self.b.a6.move("b5"), (True, "attack", None))

    def test_empassant(self):
        self.b.a7.move("a5")
        self.b.a5.move("a4")
        self.b.b2.move("b4")
        move = self.b.a4.move("b3")
        self.assertEqual(move[:2], (True, "empassant"))
        self.assertIsInstance(move[-1], Square)

    def test_empassant_invalid(self):
        self.b.a7.move("a5")
        self.b.a5.move("a4")
        self.b.b2.move("b4")
        #~ Removes empassant ability
        self.b.h7.move("h6")
        self.assertEqual(self.b.a4.move("b3"), (False, "", None))

    def test_attack_invalid(self):
        self.b.a2.move("a4")
        self.b.a7.move("a5")
        self.assertEqual(self.b.a5.move("a4"), (False, "", None))

class TestRookMoves(TestCase):

    def setUp(self):
        free_spaces = {letter:{number:Square(letter+number) for number in "12345678"} for letter in "abcdefgh"}
        self.b = Board(free_spaces)
        self.b.SHOW_BOARD = False
        self.b.a2.move("a4")
        self.b.a7.move("a5")

    def test_move_vertical(self):
        self.assertEqual(self.b.a1.move("a3"), (True, "normal", None))
        self.assertEqual(self.b.a8.move("a6"), (True, "normal", None))

    def test_move_horizonal(self):
        self.b.a1.move("a3")
        self.b.a8.move("a6")
        self.assertEqual(self.b.a3.move("h3"), (True, "normal", None))
        self.assertEqual(self.b.a6.move("h6"), (True, "normal", None))

    def test_move_diagonal(self):
        self.b.a1.move("a3")
        self.b.a8.move("a6")
        self.assertEqual(self.b.a3.move("c5"), (False, "", None))
        self.assertEqual(self.b.a6.move("c4"), (False, "", None))

    def test_attack_team_vertical(self):
        self.assertEqual(self.b.a1.move("a4"), (False, "", None))
        self.assertEqual(self.b.a8.move("a5"), (False, "", None))

    def test_attack_team_horizontal(self):
        self.assertEqual(self.b.a1.move("b1"), (False, "", None))
        self.assertEqual(self.b.a8.move("b8"), (False, "", None))

    def test_attack_team_diagonal(self):
        self.assertEqual(self.b.a1.move("b2"), (False, "", None))
        self.assertEqual(self.b.a8.move("b7"), (False, "", None))

    def test_attack_enemy_vertical(self):
        self.b.a1.move("a3")
        self.b.a3.move("b3")
        self.assertEqual(self.b.b3.move("b8"), (False, "", None))
        self.assertEqual(self.b.b3.move("b7"), (True, "normal", None))

        self.b.a8.move("a6")
        self.b.a6.move("b6")
        self.assertEqual(self.b.b6.move("b1"), (False, "", None))
        self.assertEqual(self.b.b6.move("b2"), (True, "normal", None))

class TestKnightMoves(TestCase):

    def setUp(self):
        free_spaces = {letter:{number:Square(letter+number) for number in "12345678"} for letter in "abcdefgh"}
        self.b = Board(free_spaces)
        self.b.SHOW_BOARD = False

    def test_move(self):
        self.assertEqual(self.b.b1.move("c3"), (True, "normal", None))

    def test_move_invalid(self):
        self.assertEqual(self.b.b1.move("d2"), (False, "", None))

    def test_attack(self):
        self.b.c7.move("c5")
        self.b.c5.move("c4")
        self.b.c4.move("c3")
        self.assertEqual(self.b.b1.move("c3"), (True, "normal", None))



main()
