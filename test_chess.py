from unittest import TestCase, main

from chess import *

class TestPawnMovements(TestCase):

    def setUp(self):
        self.chess = Chess()

    def test_checkClearPath_H_positive_dx_clear_path(self):
        self.chess.board['3']['a'] = 'r'
        self.assertTrue(self.chess.checkClearPath('a3', 'h3'), (True, True))
        self.assertTrue(self.chess.checkClearPath('a3', 'b3'), (True, True))
        
        self.chess.board['3']['a'] = 'R'
        self.assertTrue(self.chess.checkClearPath('a3', 'h3'), (True, True))
        self.assertTrue(self.chess.checkClearPath('a3', 'b3'), (True, True))

        self.chess.board['3']['a'] = 'q'
        self.assertTrue(self.chess.checkClearPath('a3', 'h3'), (True, True))
        self.assertTrue(self.chess.checkClearPath('a3', 'b3'), (True, True))

        self.chess.board['3']['a'] = 'Q'
        self.assertTrue(self.chess.checkClearPath('a3', 'h3'), (True, True))
        self.assertTrue(self.chess.checkClearPath('a3', 'b3'), (True, True))
        
        self.chess.board['3']['a'] = 'k'
        self.assertTrue(self.chess.checkClearPath('a3', 'h3'), (True, True))
        self.assertTrue(self.chess.checkClearPath('a3', 'b3'), (True, True))
        
        self.chess.board['3']['a'] = 'K'
        self.assertTrue(self.chess.checkClearPath('a3', 'h3'), (True, True))
        self.assertTrue(self.chess.checkClearPath('a3', 'b3'), (True, True))
        
    def test_checkClearPath_H_negative_dx_clear_path(self):
        self.chess.board['3']['h'] = 'r'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (True, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))
        
        self.chess.board['3']['h'] = 'R'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (True, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))

        self.chess.board['3']['h'] = 'q'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (True, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))

        self.chess.board['3']['h'] = 'Q'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (True, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))
        
        self.chess.board['3']['h'] = 'k'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (True, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))
        
        self.chess.board['3']['h'] = 'K'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (True, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))
        
    def test_checkClearPath_H_negative_dx_block_path(self):
        self.chess.board['3']['d'] = 'p'
        self.chess.board['3']['h'] = 'r'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))
        
        self.chess.board['3']['h'] = 'R'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))

        self.chess.board['3']['h'] = 'q'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))

        self.chess.board['3']['h'] = 'Q'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))
        
        self.chess.board['3']['h'] = 'k'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))
        
        self.chess.board['3']['h'] = 'K'
        self.assertEqual(self.chess.checkClearPath('h3', 'a3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('h3', 'g3'), (True, True))
        
    def test_checkClearPath_H_positve_dx_block_path(self):
        self.chess.board['3']['d'] = 'p'
        self.chess.board['3']['a'] = 'r'
        self.assertEqual(self.chess.checkClearPath('a3', 'h3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('a3', 'b3'), (True, True))
        
        self.chess.board['3']['a'] = 'R'
        self.assertEqual(self.chess.checkClearPath('a3', 'h3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('a3', 'b3'), (True, True))

        self.chess.board['3']['a'] = 'q'
        self.assertEqual(self.chess.checkClearPath('a3', 'h3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('a3', 'b3'), (True, True))

        self.chess.board['3']['a'] = 'Q'
        self.assertEqual(self.chess.checkClearPath('a3', 'h3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('a3', 'b3'), (True, True))
        
        self.chess.board['3']['a'] = 'k'
        self.assertEqual(self.chess.checkClearPath('a3', 'h3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('a3', 'b3'), (True, True))
        
        self.chess.board['3']['a'] = 'K'
        self.assertEqual(self.chess.checkClearPath('a3', 'h3'), (False, True))
        self.assertEqual(self.chess.checkClearPath('a3', 'b3'), (True, True))
        
        
        
main()
