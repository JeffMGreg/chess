from unittest import TestCase, main

from chess import *

class TestWhitePawnMovements(TestCase):

    def setUp(self):
        self.chess = Game()
        self.pawn = Pawn("w", "a2")
        self.chess.board["2"]["a"] = self.pawn

    def test_pawn_move_one_space_from_start(self):
        self.pawn.move("a3", self.chess)
        square = self.chess.board["3"]["a"]
        self.assertEqual(square.name, "pawn")
        self.assertEqual(square.color, "w")
        self.assertEqual(self.pawn.pos, "a3")
        self.assertEqual(self.chess.board["2"]["a"].name, None)

    def test_pawn_move_two_spaces_from_start(self):
        self.pawn.move("a4", self.chess)
        square = self.chess.board["4"]["a"]
        self.assertEqual(square.name, "pawn")
        self.assertEqual(square.color, "w")
        self.assertEqual(self.pawn.pos, "a4")
        self.assertEqual(self.chess.board["2"]["a"].name, None)

    def test_pawn_move_three_spaces_from_start(self):
        self.assertRaises(InvalidMove, self.pawn.move, "a5", self.chess)
        square = self.chess.board["5"]["a"]
        self.assertEqual(square.name, None)
        self.assertEqual(self.pawn.pos, "a2")

    def test_pawn_move_two_spaces_after_moving(self):
        self.pawn.move("a3", self.chess)
        self.assertRaises(InvalidMove, self.pawn.move, "a5", self.chess)

    def test_pawn_move_one_space_after_moving_one_space(self):
        self.pawn.move("a3", self.chess)
        self.pawn.move("a4", self.chess)

    def test_pawn_move_one_space_after_moving_two_spaces(self):
        self.pawn.move("a4", self.chess)
        self.pawn.move("a5", self.chess)

    def test_pawn_move_back(self):
        self.pawn.move("a4", self.chess)
        self.assertRaises(InvalidMove, self.pawn.move, "a3", self.chess)

    def test_pawn_move_in_occupied_space(self):
        bp = Pawn("b", "a5")
        self.chess.board['5']['a'] = bp
        self.assertRaises(InvalidMove, self.pawn.move, 'a5', self.chess)
        self.pawn.move('a4', self.chess)
        self.assertRaises(InvalidMove, self.pawn.move, 'a5', self.chess)

    def test_pawn_move_past_occupied_space(self):
        bp = Pawn("b", "a3")
        self.chess.board['3']['a'] = bp
        self.assertRaises(InvalidMove, self.pawn.move, 'a4', self.chess)

    def test_pawn_move_diag(self):
        self.assertRaises(InvalidMove, self.pawn.move, 'b3', self.chess)

class TestBlackPawnMovements(TestCase):

    def setUp(self):
        self.chess = Game()
        self.pawn = Pawn("b", "a7")
        self.chess.board["7"]["a"] = self.pawn

    def test_pawn_move_one_space_from_start(self):
        self.pawn.move("a6", self.chess)
        square = self.chess.board["6"]["a"]
        self.assertEqual(square.name, "pawn")
        self.assertEqual(square.color, "b")
        self.assertEqual(self.pawn.pos, "a6")
        self.assertEqual(self.chess.board["7"]["a"].name, None)

    def test_pawn_move_two_spaces_from_start(self):
        self.pawn.move("a5", self.chess)
        square = self.chess.board["5"]["a"]
        self.assertEqual(square.name, "pawn")
        self.assertEqual(square.color, "b")
        self.assertEqual(self.pawn.pos, "a5")
        self.assertEqual(self.chess.board["7"]["a"].name, None)

    def test_pawn_move_three_spaces_from_start(self):
        self.assertRaises(InvalidMove, self.pawn.move, "a4", self.chess)
        square = self.chess.board["4"]["a"]
        self.assertEqual(square.name, None)
        self.assertEqual(self.pawn.pos, "a7")

    def test_pawn_move_two_spaces_after_moving(self):
        self.pawn.move("a6", self.chess)
        self.assertRaises(InvalidMove, self.pawn.move, "a4", self.chess)

    def test_pawn_move_one_space_after_moving_one_space(self):
        self.pawn.move("a6", self.chess)
        self.pawn.move("a5", self.chess)

    def test_pawn_move_one_space_after_moving_two_spaces(self):
        self.pawn.move("a5", self.chess)
        self.pawn.move("a4", self.chess)

    def test_pawn_move_back(self):
        self.pawn.move("a5", self.chess)
        self.assertRaises(InvalidMove, self.pawn.move, "a6", self.chess)
        
    def test_pawn_move_in_occupied_space(self):
        wp = Pawn("w", "a4")
        self.chess.board['4']['a'] = wp
        self.assertRaises(InvalidMove, self.pawn.move, 'a4', self.chess)
        self.pawn.move("a5", self.chess)
        self.assertRaises(InvalidMove, self.pawn.move, "a4", self.chess)
        
    def test_pawn_move_past_occupied_space(self):
        wp = Pawn("w", "a6")
        self.chess.board['6']['a'] = wp
        self.assertRaises(InvalidMove, self.pawn.move, 'a5', self.chess)        
        
    def test_pawn_move_diag(self):
        self.assertRaises(InvalidMove, self.pawn.move, 'b6', self.chess)
        
class TestPawnAttacks(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.wp = Pawn('w', 'a4')
        self.bp = Pawn('b', 'b5')
        self.wp2 = Pawn('w', 'b5')
        self.bp2 = Pawn('b', 'c4')
        
    def test_white_pawn_normal_attack(self):
        self.chess.board['4']['a'] = self.wp
        self.chess.board['5']['b'] = self.bp
        self.wp.move('b5', self.chess)

    def test_black_pawn_normal_attack(self):
        self.chess.board['4']['a'] = self.wp
        self.chess.board['5']['b'] = self.bp
        self.bp.move('a4', self.chess)        

    def test_white_pawn_attacks_white(self):
        self.chess.board['4']['a'] = self.wp
        self.chess.board['5']['b'] = self.wp2
        self.assertRaises(InvalidMove, self.wp.move, 'b5', self.chess)

    def test_black_pawn_attacks_black(self):
        self.chess.board['5']['b'] = self.bp
        self.chess.board['4']['c'] = self.bp2
        self.assertRaises(InvalidMove, self.bp.move, 'c4', self.chess)

class TestWhiteRookMovements(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.r = Rook('w', 'a1')
        self.chess.board['1']['a'] = self.r
    
    def test_move_rook_v(self):
        self.r.move('a2', self.chess)
        self.r.move('a8', self.chess)
        self.r.move('a1', self.chess)
        
    def test_move_rook_h(self):
        self.r.move('b1', self.chess)
        self.r.move('h1', self.chess)
        self.r.move('a1', self.chess)

    def test_move_rook_d(self):
        self.assertRaises(InvalidMove, self.r.move, 'b2', self.chess)
        self.assertRaises(InvalidMove, self.r.move, 'h8', self.chess)

class TestBlackRookMovements(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.r = Rook('b', 'a8')
        self.chess.board['8']['a'] = self.r
        
    def test_move_rook_v(self):
        self.r.move('a7', self.chess)
        self.r.move('a1', self.chess)
        self.r.move('a8', self.chess)
        
    def test_move_room_h(self):
        self.r.move('b8', self.chess)
        self.r.move('h8', self.chess)
        self.r.move('a8', self.chess)
        
    def test_move_rook_d(self):
        self.assertRaises(InvalidMove, self.r.move, 'b7', self.chess)
        self.assertRaises(InvalidMove, self.r.move, 'h1', self.chess)
        
class TestRookAttacks(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.wr = Rook('w', 'a1')
        self.wp1 = Pawn('w', 'a3')
        self.bp1 = Pawn('b', 'c1')
        
        self.chess.board['1']['a'] = self.wr
        self.chess.board['3']['a'] = self.wp1
        self.chess.board['1']['c'] = self.bp1
        
        self.br = Rook('b', 'h8')
        self.wp2 = Pawn('w', 'h6')
        self.bp2 = Pawn('b', 'f8')
        
        self.chess.board['8']['h'] = self.br
        self.chess.board['6']['h'] = self.wp2
        self.chess.board['8']['f'] = self.bp2
        
    def test_w_rook_attack_same_color(self):
        self.assertRaises(InvalidMove, self.wr.move, 'a3', self.chess)
        
    def test_w_rook_attack_different_color(self):
        self.wr.move('c1', self.chess)
        self.assertEqual(self.chess.board['1']['c'].name, "rook")
        
    def test_b_rook_attack_same_color(self):
        self.assertRaises(InvalidMove, self.br.move, 'f8', self.chess)
    
    def test_b_rook_attack_different_color(self):
        self.br.move('h6', self.chess)
        self.assertEqual(self.chess.board['6']['h'].name, "rook")
    
    def test_w_rook_attack_through_piece(self):
        self.assertRaises(InvalidMove, self.wr.move, 'h1', self.chess)

    def test_b_rook_attack_through_piece(self):
        self.assertRaises(InvalidMove, self.br.move, 'h1', self.chess)

class TestWhiteKnightMoves(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.k = Knight('w', 'a1')
        self.chess.board['1']['a'] = self.k
        
    def test_valid_move(self):
        self.k.move('c2', self.chess)
        self.k.move('a1', self.chess)
        self.k.move('b3', self.chess)
        
    def test_invalid_move(self):
        self.assertRaises(InvalidMove, self.k.move, 'b2', self.chess)
        self.assertRaises(InvalidMove, self.k.move, 'b1', self.chess)
        self.assertRaises(InvalidMove, self.k.move, 'a2', self.chess)
        
class TestWhiteKnightAttacks(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.k = Knight('w', 'a1')
        self.wp = Pawn('w', 'b3')
        self.bp = Pawn('b', 'c2')
        
        self.chess.board['1']['a'] = self.k
        self.chess.board['3']['b'] = self.wp
        self.chess.board['2']['c'] = self.bp
        
    def test_attack_same_color(self):
        self.assertRaises(InvalidMove, self.k.move, 'b3', self.chess)
    
    def test_attack_different_color(self):
        self.k.move('c2', self.chess)

class TestBlackKnightAttacks(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.k = Knight('b', 'a1')
        self.bp = Pawn('b', 'b3')
        self.wp = Pawn('w', 'c2')
        
        self.chess.board['1']['a'] = self.k
        self.chess.board['3']['b'] = self.bp
        self.chess.board['2']['c'] = self.wp
        
    def test_attack_same_color(self):
        self.assertRaises(InvalidMove, self.k.move, 'b3', self.chess)
    
    def test_attack_different_color(self):
        self.k.move('c2', self.chess)

class TestWhiteBishopMovements(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.b = Bishop('w', 'a1')
        self.chess.board['1']['a'] = self.b
        
    def test_valid_move(self):
        self.b.move('h8', self.chess)
        self.b.move('a1', self.chess)
        self.b.move('c3', self.chess)
        self.b.move('e1', self.chess)

class TestBlackBishopMovements(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.b = Bishop('b', 'a1')
        self.chess.board['1']['a'] = self.b
        
    def test_valid_move(self):
        self.b.move('h8', self.chess)
        self.b.move('a1', self.chess)
        self.b.move('c3', self.chess)
        self.b.move('e1', self.chess)

    def test_invalid_move(self):
        self.assertRaises(InvalidMove, self.b.move, 'b8', self.chess)
        
class TestWhiteBishopAttacks(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.b = Bishop('w', 'a1')
        self.p = Bishop('b', 'b2')
        self.chess.board['1']['a'] = self.b
        self.chess.board['2']['b'] = self.p
        
    def test_attack_different_color(self):
        self.b.move('b2', self.chess)
        
    def test_attack_through_piece(self):
        self.assertRaises(InvalidMove, self.b.move, 'h8', self.chess)
        
    def test_attack_same_color(self):
        self.chess.board['2']['b'] = Pawn('w', 'b2')
        self.assertRaises(InvalidMove, self.b.move, 'b2', self.chess)

class TestBlackBishopAttacks(TestCase):
    
    def setUp(self):
        self.chess = Game()
        self.b = Bishop('b', 'a1')
        self.p = Bishop('w', 'b2')
        self.chess.board['1']['a'] = self.b
        self.chess.board['2']['b'] = self.p
        
    def test_attack_different_color(self):
        self.b.move('b2', self.chess)
        
    def test_attack_through_piece(self):
        self.assertRaises(InvalidMove, self.b.move, 'h8', self.chess)
        
    def test_attack_same_color(self):
        self.chess.board['2']['b'] = Pawn('b', 'b2')
        self.assertRaises(InvalidMove, self.b.move, 'b2', self.chess)

main()
