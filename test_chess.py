from unittest import TestCase, main

from chess import *

class TestPawnMovements(TestCase):

    def setUp(self):
        self.chess = Board()
        self.pawn = Pawn('w', 'a2')
        self.chess.board['2']['a'] = self.pawn

    def test_setUp(self):
        pass

    def test_pawn_move_one_space_from_start(self):

        self.pawn.move('a3', self.chess.board)
        square = self.chess.board['3']['a']
        self.assertEqual(square.name, "pawn")
        self.assertEqual(square.color, "w")
        self.assertEqual(self.pawn.pos, 'a3')
        self.assertEqual(self.chess.board['2']['a'].name, None)

    def test_pawn_move_two_spaces_from_start(self):

        self.pawn.move('a4', self.chess.board)
        square = self.chess.board['4']['a']
        self.assertEqual(square.name, "pawn")
        self.assertEqual(square.color, "w")
        self.assertEqual(self.pawn.pos, "a4")
        self.assertEqual(self.chess.board['2']['a'].name, None)

    def test_pawn_move_three_spaces_from_start(self):

        self.assertRaises(InvalidMove, self.pawn.move, 'a5', self.chess.board)
        square = self.chess.board['5']['a']
        self.assertEqual(square.name, None)
        self.assertEqual(self.pawn.pos, "a2")

    def test_pawn_move_two_spaces_after_moving(self):

        self.pawn.move('a3', self.chess.board)
        self.assertRaises(InvalidMove, self.pawn.move, 'a5', self.chess.board)

    def test_pawn_move_one_space_after_moving_one_space(self):

        self.pawn.move('a3', self.chess.board)
        self.pawn.move('a4', self.chess.board)

    def test_pawn_move_one_space_after_moving_two_spaces(self):

        self.pawn.move('a4', self.chess.board)
        self.pawn.move('a5', self.chess.board)

    def test_pawn_move_back(self):

        self.pawn.move('a4', self.chess.board)
        self.assertRaises(InvalidMove, self.pawn.move, 'a3', self.chess.board)


main()
