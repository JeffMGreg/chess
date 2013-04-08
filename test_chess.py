from unittest import TestCase, main

from chess import *

class TestPawnMovements(TestCase):

    def setUp(self):
        self.chess = Chess()

    def test_move_pawn_more_than_two_spaces(self):
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'p', 'a2', 'a5')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'P', 'a7', 'a4')

    def test_move_pawn_two_spaces_from_start(self):
        self.assertTrue(self.chess.checkValidPawnMove('p', 'a2', 'a4'))
        self.assertTrue(self.chess.checkValidPawnMove('P', 'a7', 'a5'))

    def test_move_pawn_one_space_from_start(self):
        self.assertTrue(self.chess.checkValidPawnMove('p', 'a2', 'a3'))
        self.assertTrue(self.chess.checkValidPawnMove('P', 'a7', 'a6'))

    def test_move_pawn_two_spaces_after_start(self):
        self.chess.move('a2', 'a3')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'p', 'a3', 'a5')
        self.chess.move('a7', 'a6')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'P', 'a6', 'a4')

    def test_white_pawn_doesnt_move(self):
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'p', 'a2', 'a2')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'P', 'a7', 'a7')

    def test_move_to_taken_square(self):
        self.chess.move('a7', 'a5')
        self.chess.move('a2', 'a4')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'p', 'a4', 'a5')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'P', 'a5', 'a4')

    def test_move_pawn_with_piece_in_the_way(self):
        self.chess.move('a7', 'a5')
        self.chess.move('a5', 'a4')
        self.chess.move('a4', 'a3')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'p', 'a2', 'a4')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'P', 'a3', 'a2')

    def test_move_pawn_diagonal(self):
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'p', 'a2', 'b4')
        self.assertRaises(InvalidMove, self.chess.checkValidPawnMove, 'p', 'a2', 'b3')
        self.chess.move('b7', 'b5')
        self.chess.move('b5', 'b4')
        self.chess.move('b4', 'b3')
        self.assertTrue(self.chess.checkValidPawnMove('p', 'a2', 'b3'))

    def test_move_white_rook(self):
        self.assertRaises(InvalidMove, self.chess.move, 'a1', 'a2')
        self.assertRaises(InvalidMove, self.chess.move, 'a1', 'a3')
        self.assertRaises(InvalidMove, self.chess.move, 'a1', 'b1')
        self.assertRaises(InvalidMove, self.chess.move, 'a1', 'c1')
        self.assertRaises(InvalidMove, self.chess.move, 'a1', 'a7')
        self.assertRaises(InvalidMove, self.chess.move, 'a1', 'a8')
        self.assertRaises(InvalidMove, self.chess.move, 'a1', 'b2')
        self.assertRaises(InvalidMove, self.chess.move, 'a1', 'c3')
        self.chess.move('a2', 'a4')
        self.chess.move('a1', 'a3')
        self.chess.move('a3', 'b3')
        self.chess.move('b3', 'h3')
        self.chess.move('h3', 'h4')
        self.chess.move('h4', 'h6')
        self.assertRaises(InvalidMove, self.chess.move, 'h6', 'h2')
        self.assertRaises(InvalidMove, self.chess.move, 'h6', 'h1')
        self.assertRaises(InvalidMove, self.chess.move, 'h6', 'h8')
        self.chess.move('h6', 'h7')
        self.assertEqual(self.chess.board['7']['h'], 'r')
        self.assertRaises(InvalidMove, self.chess.move, 'h7', 'f5')

    def test_move_black_rook(self):
        self.assertRaises(InvalidMove, self.chess.move, 'a8', 'a7')
        self.assertRaises(InvalidMove, self.chess.move, 'a8', 'a6')
        self.assertRaises(InvalidMove, self.chess.move, 'a8', 'b8')
        self.assertRaises(InvalidMove, self.chess.move, 'a8', 'c8')
        self.assertRaises(InvalidMove, self.chess.move, 'a8', 'a2')
        self.assertRaises(InvalidMove, self.chess.move, 'a8', 'a1')
        self.assertRaises(InvalidMove, self.chess.move, 'a8', 'b7')
        self.assertRaises(InvalidMove, self.chess.move, 'a8', 'c6')
        self.chess.move('a7', 'a5')
        self.chess.move('a8', 'a6')
        self.chess.move('a6', 'b6')
        self.chess.move('b6', 'h6')
        self.chess.move('h6', 'h5')
        self.chess.move('h5', 'h3')
        self.assertRaises(InvalidMove, self.chess.move, 'h3', 'h7')
        self.assertRaises(InvalidMove, self.chess.move, 'h3', 'h8')
        self.assertRaises(InvalidMove, self.chess.move, 'h3', 'h1')
        self.chess.move('h3', 'h2')
        self.assertEqual(self.chess.board['2']['h'], 'R')
        self.assertRaises(InvalidMove, self.chess.move, 'h2', 'f4')

    def test_diag_path(self):

        self.assertRaises(InvalidMove, self.chess.checkClearPath, 'd', 'a1', 'b1')
        self.assertRaises(InvalidMove, self.chess.checkClearPath, 'd', 'a1', 'a2')
        self.assertTrue(self.chess.checkClearPath('d', 'a1', 'b2'))

        self.assertEqual(self.chess.checkClearPath('d', 'a3', 'd6'), (True, True))
        self.assertEqual(self.chess.checkClearPath('d', 'a6', 'd3'), (True, True))
        self.assertEqual(self.chess.checkClearPath('d', 'd6', 'a3'), (True, True))
        self.assertEqual(self.chess.checkClearPath('d', 'd3', 'a6'), (True, True))

        self.assertEqual(self.chess.checkClearPath('d', 'a2', 'f7'), (True, False))
        self.assertEqual(self.chess.checkClearPath('d', 'a7', 'f2'), (True, False))
        self.assertEqual(self.chess.checkClearPath('d', 'f7', 'a2'), (True, False))
        self.assertEqual(self.chess.checkClearPath('d', 'f2', 'a7'), (True, False))

        self.chess.move('b2', 'b3')
        self.chess.move('b7', 'b6')

        self.assertEqual(self.chess.checkClearPath('d', 'a2', 'f7'), (False, False))
        self.assertEqual(self.chess.checkClearPath('d', 'a7', 'f2'), (False, False))
        self.assertEqual(self.chess.checkClearPath('d', 'f7', 'a2'), (False, False))
        self.assertEqual(self.chess.checkClearPath('d', 'f2', 'a7'), (False, False))

    def test_bishop_moves(self):

        self.assertRaises(InvalidMove, self.chess.move, 'c1', 'a3')
        self.assertRaises(InvalidMove, self.chess.move, 'c1', 'a1')
        self.assertRaises(InvalidMove, self.chess.move, 'c1', 'a1')

        self.chess.move('d2', 'd3')
        self.chess.move('c1', 'e3')

        self.assertRaises(InvalidMove, self.chess.move, 'e3', 'f2')

        self.chess.move('e3', 'a7')

        self.assertEqual(self.chess.board['7']['a'], 'b')
        self.chess.move('a7', 'b6')
        self.assertRaises(InvalidMove, self.chess.move, 'b6', 'd8')

    def test_knight_moves(self):

        self.assertRaises(InvalidMove, self.chess.move, 'b1', 'd2')        
        self.chess.move('b8', 'c6')
        
        self.assertEqual(self.chess.board['6']['c'], 'N')

    def test_king_moves(self):
        
        self.assertRaises(InvalidMove, self.chess.move, 'e1', 'e2')
        self.assertRaises(InvalidMove, self.chess.move, 'e1', 'd1')
        self.assertRaises(InvalidMove, self.chess.move, 'e1', 'd1')
        

main()
