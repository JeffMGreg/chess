# encoding: utf-8

class InvalidPiece(Exception): pass
class InvalidMove(Exception): pass

import ipdb

DEBUG = False

class Chess(object):

    LETTERS = "abcdefgh"

    PIECES = {'K': '♔',
              'Q': '♕',
              'R': '♖',
              'B': '♗',
              'N': '♘',
              'P': '♙',
              'k': '♚',
              'q': '♛',
              'r': '♜',
              'b': '♝',
              'n': '♞',
              'p': '♟'}

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
                    rank[l] = self.PIECES["rnbqkbnr"[i]]
                elif n == "2":
                    rank[l] = self.PIECES["p"]
                elif n == "7":
                    rank[l] = self.PIECES["P"]
                elif n == "8":
                    rank[l] = self.PIECES["RNBQKBNR"[i]]
        return bord

    def drawBoard(self):
        ranks = []
        
        tl = '┌'
        tr = '┐'
        t  = '┬'
        h  = '─'
        v  = '│'
        bl = '└'
        br = '┘'
        x  = '┼'
        l  = '├'
        r  = '┤'
        b  = '┴'
        
        hs = '{}{}{}'.format(h, h, h)
        print "  {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(tl, hs, t, hs, t, hs, t, hs, t, hs, t, hs, t, hs, t, hs, tr)
        for n in "12345678":
            rank = self.board[n]
            ranks.append("{v} {a} {v} {b} {v} {c} {v} {d} {v} {e} {v} {f} {v} {g} {v} {h} {v}".format(v=v, **rank))


        for i, rank in enumerate(ranks[::-1], start=1):
            print "{} {}".format(9-i, rank)
            if 9-i == 1:
                break
            print "  {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(l, hs, x, hs, x, hs, x, hs, x, hs, x, hs, x, hs, x, hs, r)
            
        print "  {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(bl, hs, b, hs, b, hs, b, hs, b, hs, b, hs, b, hs, b, hs, br)
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

        tl, tn = t
        fl, fn = f
        
        dy = int(tn) - int(fn)
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)

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

    def checkValidPawnMove(self, p, f, t):

        tl, tn = t
        fl, fn = f

        if p.islower(): d = 1
        else:           d = -1

        dy = (d * (int(tn) - int(fn)))
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)
        
        square = self.board[tn][tl]
        path = self.checkClearPath("v", f, t)


        if (dy == 2) and (fn in ["2", "7"]) and (dx == 0) and all(path):
            return True

        if (dy == 1) and (dx == 0) and all(path):
            return True

        if (dy == 1) and (abs(dx) == 1) and ((square.islower() == p.upper()) or (square.isupper() == p.islower())):
            return True

        raise InvalidMove

    def checkValidQueenMove(self, p, f, t):
        
        tl, tn = t
        fl, fn = f
        
        dy = int(tn) - int(fn)
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)
        
        square = self.board[tn][tl]
        try:
            path = self.checkClearPath('h', f, t)
        except InvalidMove:
            try:
                path = self.checkClearPath("v", f, t)
            except InvalidMove:
                try: 
                    path = self.checkClearPath("d", f, t)
                except InvalidMove:
                    raise InvalidMove
        
        if (square.islower() == p.islower()) or (square.isupper() == p.isupper()):
            raise InvalidMove
            
        if path[0]:
            return True
        
        raise InvalidMove
        
    def checkValidKingMove(self, p, f, t):
        
        tl, tn = t
        fl, fn = f
        
        dy = int(tn) - int(fn)
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)
        
        square = self.board[tn][tl]
        
        if (square.islower() == p.islower()) or (square.isupper() == p.isupper()):
            raise InvalidMove        
        
        if abs(dx) > 1:
            pass
            # Castle move
        if abs(dy) > 1:
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

    def checkClearPath(self, f, t):
        """h v d k"""
                
        tl, tn = t
        fl, fn = f

        dy = (int(tn) - int(fn))
        dx = self.LETTERS.find(tl) - self.LETTERS.find(fl)
        
        from_square = self.board[fn][fl]
        to_square   = self.board[tn][tl]
        if (abs(dx) > 0) and (abs(dy) == 0) and from_square.lower() in 'rqk':
            path = "h"
        elif (abs(dx) == 0) and (abs(dy) > 0) and from_square.lower() in 'rqkp':
            path = "v"
        elif (abs(dx) > 0) and (abs(dy) > 0) and from_square.lower() in 'bq':
            try:
                if abs(dy/float(dx)) == 1:
                    path = "d"
                else:
                    raise InvalidMove
            except ZeroDivisionError:
                raise InvalidMove
        elif (((abs(dx) == 2) and (abs(dy) == 1)) or ((abs(dx) == 1) and (abs(dy) == 2))) and (from_square.lower() in 'n'):
            path = 'n'


        empty = []            
        #~ Horizontal Moves ----------------------------------------------------
        if path == "h":
            a, b = (self.LETTERS.find(fl), self.LETTERS.find(tl))
            if (b - a) > 0: d = 1
            else:           d = -1

            for l in self.LETTERS[a:b:d]:
                if self.board[fn][l] == " ":
                    empty.append(True)
                else:
                    empty.append(False)
            return (all(empty[1:]), to_square == " ")

        #~ Vertical Moves ------------------------------------------------------
        elif path == "v":
            a, b = (int(fn), int(tn))
            if (b - a) > 0: d = 1
            else:           d = -1

            for n in xrange(a, b, d):
                if self.board[str(n)][fl] == " ":
                    empty.append(True)
                else:
                    empty.append(False)
            return (all(empty[1:]), to_square == " ")

        #~ Diagonal Moves ------------------------------------------------------
        elif path == "d":

            if dx > 0: xd = 1
            else:      xd = -1

            if dy > 0: yd = 1
            else:      yd = -1

            x = self.LETTERS.find(fl)
            y = int(fn)
            for _ in xrange(abs(dx)):
                x += xd
                y += yd
                if self.board[str(y)][self.LETTERS[x]] == " ":
                    empty.append(True)
                else:
                    empty.append(False)

            return (all(empty[:-1]), empty[-1])

if __name__ == "__main__":
    chess = Chess()
    chess.drawBoard()
