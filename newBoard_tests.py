from unittest import TestCase, main

from newBoard import *


class TestWhitePawnMoves(TestCase):
    
    def setUp(self):
        self.b = Board()
        self.b.a2.piece = Pawn(self.b.a2, 'w')
        
    def test_pawn_move_one_N(self):
        self.assertEqual(self.b.a2.move("a3"), True)

    def test_pawn_move_two_N_from_start(self):
        self.assertEqual(self.b.a2.move("a4"), True)

    def test_pawn_move_two_N_after_already_moved(self):
        self.b.a2.piece.move_count = 1
        self.assertRaises(InvalidMove, self.b.a2.move, "a4")

    def test_pawn_move_three_N(self):
        self.assertRaises(InvalidMove, self.b.a2.move, "a5")

main()
