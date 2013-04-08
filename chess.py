
class InvalidPiece(Exception): pass
class InvalidMove(Exception): pass

import ipdb

DEBUG = False

class Chess(object):

    LETTERS = "abcdefgh"

    def __init__(self):
        self.board = self.initializeBord()
        #~ self.drawBord()
        
        # Casteling information
        self.white_king_moved = False
        self.white_king_rook_moved = False
        self.white_queen_rook_moved = False
        
        self.black_king_moves = False
        self.black_king_rook_moved = False
        self.black_queen_rook_moved = False
        
        # En pawn sant
        self.previous_move = None

    def initializeBord(self):
        bord = {n:{l:" " for l in "abcdefgh"} for n in "12345678"}
        for n in "12345678":
            rank = bord[n]
            for i, l in enumerate("abcdefgh"):
                if n == "1":
                    rank[l] = "rnbqkbnr"[i]
                elif n == "2":
                    rank[l] = "p"
                elif n == "7":
                    rank[l] = "P"
                elif n == "8":
                    rank[l] = "RNBQKBNR"[i]
        return bord

    def drawBoard(self):
        ranks = []
        for n in "12345678":
            rank = self.board[n]
            ranks.append("| {a} | {b} | {c} | {d} | {e} | {f} | {g} | {h} |".format(**rank))

        for i, rank in enumerate(ranks[::-1], start=1):
            print "  +---+---+---+---+---+---+---+---+"
            print "{} {}".format(9-i, rank)
        print "  +---+---+---+---+---+---+---+---+"
        print "    a   b   c   d   e   f   g   h"


    def move(self, piece, to):
        l, n = piece.lower()
        piece = self.board[n][l]

        self.checkValidMove(piece, l+n, to)

        self.board[n][l] = " "

        l, n = to.lower()
        self.board[n][l] = piece


    def checkValidMove(self, p, f, t):

        if DEBUG == True:
            import ipdb; ipdb.set_trace()

        if p == " ": raise InvalidPiece

        if p in ["p", "P"]:
            self.checkValidPawnMove(p, f, t)

        if p in ["r", "R"]:
            self.checkValidRookMove(p, f, t)

        if p in ["b", "B"]:
            self.checkValidBishopMove(p, f, t)
            
        if p in ["n", "N"]:
            self.checkValidKnightMove(p, f, t)
            
        if p in ["k", "K"]:
            self.checkValidKingMove(p, f, t)

    def checkValidKingMove(self, p, f, t):
        
        tl, tn = t
        fl, fn = f
        
        dy = int(tn) - int(fn)
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)
        
        square = self.board[tn][tl]
        
        if abs(dx) > 1:
            pass
            # Castle move
        if abs(dy) > 1:
            raise InvalidMove
            
        if (square.islower() == p.islower()) or (square.isupper() == p.isupper()):
            raise InvalidMove
            

    def checkValidKnightMove(self, p, f, t):
                
        tl, tn = t
        fl, fn = f
        
        dy = abs(int(tn) - int(fn))
        dx = abs(self.LETTERS.find(tl) - self.LETTERS.find(fl))
        
        square = self.board[tn][tl]
        
        if ((dx == 2) and (dy == 1)) or ((dx == 1) and (dy == 2)):
            if square == ' ':
                return True
            if (square.islower() == p.islower()) or (square.isupper() == p.isupper()):
                raise InvalidMove
        raise InvalidMove

    def checkValidBishopMove(self, p, f, t):

        tl, tn = t
        fl, fn = f

        dy = (int(tn) - int(fn))
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)

        path   = self.checkClearPath("d", f, t)
        square = self.board[tn][tl]

        if all(path):
            return True

        if not path[0]:
            raise InvalidMove


        if not path[1]:
            if (square.islower() == p.islower()) or (square.isupper() == p.isupper()):
                raise InvalidMove
            else:
                return True
        raise InvalidMove


    def checkValidRookMove(self, p, f, t):

        tl, tn = t
        fl, fn = f

        dy = (int(tn) - int(fn))
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)

        if (abs(dx) > 0) and (abs(dy) > 0):
            raise InvalidMove

        if (abs(dx) > 0):
            path = self.checkClearPath("h", f, t)
        else:
            path = self.checkClearPath("v", f, t)
        square = self.board[tn][tl]

        if all(path):
            return True

        if not path[0]:
            raise InvalidMove

        if not path[1]:
            if (square.islower() == p.islower()) or (square.isupper() == p.isupper()):
                raise InvalidMove
            else:
                return True
        raise InvalidMove

    def checkValidPawnMove(self, p, f, t):

        tl, tn = t
        fl, fn = f

        if p.islower(): d = 1
        else:           d = -1

        dy = (d * (int(tn) - int(fn)))
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)
        
        square = self.board[t[1]][t[0]]

        if (dy == 2) and (fn in ["2", "7"]) and (dx == 0) and all(self.checkClearPath("v", f, t)):
            return True

        if (dy == 1) and (dx == 0) and all(self.checkClearPath("v", f, t)):
            return True

        if (dy == 1) and (abs(dx) == 1) and ((square.islower() == p.upper()) or (square.isupper() == p.islower())):
            return True

        raise InvalidMove

    def checkClearPath(self, path, f, t):
        """h v d k"""

        if path == "h":
            a, b = (self.LETTERS.find(f[0]), self.LETTERS.find(t[0]))
            if (b - a) > 0: d = 1
            else: d = -1

            empty = []
            for l in self.LETTERS[a:b:d]:
                if self.board[f[1]][l] == " ":
                    empty.append(True)
                else:
                    empty.append(False)
            return (all(empty[1:]), self.board[t[1]][t[0]] == " ")

        elif path == "v":
            a, b = (int(f[1]), int(t[1]))
            if (b - a) > 0: d = 1
            else: d = -1

            empty = []
            for n in xrange(a, b, d):
                if self.board[str(n)][f[0]] == " ":
                    empty.append(True)
                else:
                    empty.append(False)
            return (all(empty[1:]), self.board[t[1]][t[0]] == " ")

        elif path == "d":
            x = (self.LETTERS.find(f[0]), self.LETTERS.find(t[0]))
            dx = x[1] - x[0]
            y = (int(f[1]), int(t[1]))
            dy = y[1] - y[0]

            if dx > 0: xd = 1
            else:      xd = -1

            if dy > 0: yd = 1
            else:      yd = -1

            try:
                if abs(dy/float(dx)) != 1:
                    raise InvalidMove
            except ZeroDivisionError:
                raise InvalidMove

            a = self.LETTERS.find(f[0])
            b = int(f[1])
            empty = []
            for _ in xrange(abs(dx)):
                a += xd
                b += yd
                if self.board[str(b)][self.LETTERS[a]] == " ":
                    empty.append(True)
                else:
                    empty.append(False)

            return (all(empty[:-1]), empty[-1])

if __name__ == "__main__":
    chess = Chess()
    chess.drawBoard()
