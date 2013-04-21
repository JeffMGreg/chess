# encoding: utf-8


class Error(Exception):
    def __init__(self, msg=""):
        self.msg = msg

class InvalidColor(Error):
    def __str__(self):
        return "Incalid color \"{}\". Valid colors: W, B, White and Black".format(self.msg)

class InvalidPiece(Error):
    def __str__(self):
        return "Invalid piece \"{}\".  Valid selections: King, Queen, Rook, Bishop, Knight and Pawn".format(self.msg)

class InvalidMove(Error):
    def __str__(self):
        return self.msg


class Piece(object):

    pieces = {"king"  : {"b": "♔", "w": "♚"},
              "queen" : {"b": "♕", "w": "♛"},
              "rook"  : {"b": "♖", "w": "♜"},
              "bishop": {"b": "♗", "w": "♝"},
              "knight": {"b": "♘", "w": "♞"},
              "pawn"  : {"b": "♙", "w": "♟"}}

    def __init__(self, piece, color):
        try:
            group = self.pieces[piece.lower()]
        except KeyError:
            raise InvalidPiece(piece)
        else:
            try:
                self.piece = group[color[0].lower()]
            except KeyError:
                raise InvalidColor(color)
            else:
                self.color = color[0].lower()

        self.name = piece

    def __repr__(self):
        return "{} @ {}".format(self.piece, self.pos)

    def __str__(self):
        return self.piece

    def move(self, f, t):
        p = self._getPieceFrom(f)
        self._checkValidMove(f, t)
        self._setPieceTo(p, t)
        self._clearOldSpot(f)

    def _clearOldSpot(self, location):
        l, n = location.lower()
        self.board[n][l] = " "
        return True

    def _getPieceFrom(self, location):
        l, n = location.lower()
        p = self.board[n][l]
        if p == " ":
            raise InvalidMove("Must select a square with a piece on it")
        else:
            return p

    def _setPieceTo(self, piece, location):
        l, n = location.lower()
        self.board[n][l] = piece
        return True

class Pawn(Piece):
    value = 1

    def __init__(self, color, pos):
        super(Pawn, self).__init__("pawn", color)
        self.pos = pos

    def _checkValidMove(self, f, t):
        print "is valid"

class Rook(Piece):
    value = 5

    def __init__(self, color, pos):
        super(Rook, self).__init__("rook", color)
        self.pos = pos


class Knight(Piece):
    value = 3

    def __init__(self, color, pos):
        super(Knight, self).__init__("knight", color)
        self.pos = pos


class Bishop(Piece):
    value = 3

    def __init__(self, color, pos):
        super(Bishop, self).__init__("bishop", color)
        self.pos = pos


class Queen(Piece):
    value = 9

    def __init__(self, color, pos):
        super(Queen, self).__init__("queen", color)
        self.pos = pos


class King(Piece):
    value = 1000

    def __init__(self, color, pos):
        super(King, self).__init__("king", color)
        self.pos = pos


class Board(object):

    letters = "abcdefgh"
    numbers = "12345678"

    def initBoard(self):
        self.board = {n:{l:" " for l in self.letters} for n in self.numbers}

        lineup = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for piece, letter in zip(lineup, self.letters):
            for number, color in zip("18", "wb"):
                self.board[number][letter] = piece(color, letter + number)
            for number, color in zip("27", "wb"):
                self.board[number][letter] = Pawn(color, letter + number)

    def move(self, f, t):
        pass

    def showBoard(self):

        ranks = []

        tl, tr, bl, br = "┌ ┐ └ ┘".split()
        t, b, l, r  = "┬ ┴ ├ ┤".split()
        h, v, x = "─ │ ┼".split()

        s = "{v} {a} {v} {b} {v} {c} {v} {d} {v} {e} {v} {f} {v} {g} {v} {h} {v}"
        hs = "{}{}{}".format(h, h, h)
        p = (tl, hs, t, hs, t, hs, t, hs, t, hs, t, hs, t, hs, t, hs, tr)
        print "  {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(*p)
        for n in "12345678":
            rank = self.board[n]
            ranks.append(s.format(v=v, **rank))
        for i, rank in enumerate(ranks[::-1], start=1):
            print "{} {}".format(9-i, rank)
            if 9-i == 1:
                break
            p = (l, hs, x, hs, x, hs, x, hs, x, hs, x, hs, x, hs, x, hs, r)
            print "  {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(*p)
        p = (bl, hs, b, hs, b, hs, b, hs, b, hs, b, hs, b, hs, b, hs, br)
        print "  {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(*p)
        print "    a   b   c   d   e   f   g   h"


'''
class Chess(object):

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
            path = self.checkClearPath("h", f, t)
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
'''

if __name__ == "__main__":
    b = Board()
    b.initBoard()

    p = Rook('w', 'a1')




    b.showBoard()
