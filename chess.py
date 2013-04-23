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

    numbers = "12345678"
    letters = "abcdefgh"

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

    def move(self, t):
        l, n = self.pos
        p = self.board[n][l]  # Grab piece at current location
        self._checkValidMove(t)
        self.board[t[1]][t[0]] = p  # Put piece at "to" location
        self.board[n][l] = Space(self.pos)  # Set old spot as empty
        self.pos = t  # Set pieces pos to new position

    def _move(self, t):
        fl, fn = self.pos
        tl, tn = t
        x, xx  = self.letters.find(fl), self.letters.find(tl)
        y, yy  = int(fn), int(tn)
        dx     = xx - x
        dy     = yy - y
        b      = self.board
        s      = b[tn][tl]

        if dx > 0: xd = 1
        else:      xd = -1

        if dy > 0: yd = 1
        else:      yd = -1

        return fl, fn, tl, tn, x, xx, y, yy, dx, dy, s, b

    def _checkHorizontalPath(self, fl, fn, tl, tn, b):
        i, j = (self.letters.find(fl), self.letters.find(tl))
        if (j - i) > 0: d = 1
        else:           d = -1
        empty = []
        for l in self.letters[i:j:d]:
            if not b[fn][l].name:
                empty.append(True)
            else:
                empty.append(False)
        return (all(empty[1:]), b[tn][tl].name is None)

    def _checkVerticalPath(self, fl, fn, tl, tn, b):
        i, j = (int(fn), int(tn))
        if (j - i) > 0: d = 1
        else:           d = -1
        empty = []
        for n in xrange(i, j, d):
            if not b[str(n)][fl].name:
                empty.append(True)
            else:
                empty.append(False)
        return (all(empty[1:]), b[tn][tl].name is None)

    def _checkDiagonalPath(self, fl, fn, tl, tn, dx, dy, b):
        if dx > 0: xd = 1
        else:      xd = -1
        if dy > 0: yd = 1
        else:      yd = -1

        x = self.letters.find(fl)
        y = int(fn)
        empty = []
        for _ in xrange(abs(dx)):
            x += xd
            y += yd
            if b[str(y)][self.letters[x]].name is None:
                empty.append(True)
            else:
                empty.append(False)
        return (all(empty[:-1]), empty[-1])


class Space(object):
    value = 0
    color = ""
    name  = None

    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return " "


class Pawn(Piece):
    value = 1

    def __init__(self, color, pos, board):
        super(Pawn, self).__init__("pawn", color)
        self.pos = pos
        self.board = board

    def _checkValidMove(self, t):
        tl, tn = t
        fl, fn = self.pos
        b = self.board

        if self.color == "w":
            d = 1
        else:
            d = -1

        dy = (d * (int(tn) - int(fn)))
        dx = abs(self.letters.find(tl) - self.letters.find(fl))

        s = b[tn][tl]
        p = self._checkClearPath(fl, fn, tn, d, b)

        if (dy == 2) and (fn in ["2", "7"]) and (dx == 0) and p:
            return True
        elif (dy == 1) and (dx == 0) and p:
            return True
        elif (dy == 1) and (dx == 1) and (self.color == "wb".replace(s.color, "")):
            return True

        raise InvalidMove("Invalid pawn move to {}".format(t))

    def _checkClearPath(self, fl, fn, tn, d, b):
        empty = []
        for n in xrange(int(fn) + d, int(tn) + d, d):
            if b[str(n)][fl].name is None:
                empty.append(True)
            else:
                empty.append(False)
        return all(empty)


class Rook(Piece):
    value = 5

    def __init__(self, color, pos, board):
        super(Rook, self).__init__("rook", color)
        self.pos = pos
        self.board = board

    def _checkValidMove(self, t):

        fl, fn, tl, tn, x, xx, y, yy, dx, dy, s, b = self._move(t)
        if (abs(dx) > 0) and (abs(dy) > 0):
            raise InvalidMove

        if dx > 0:
            p = self._checkHorizontalPath(fl, fn, tl, tn, b)
        else:
            p = self._checkVerticalPath(fl, fn, tl, tn, b)

        if all(p):
            return True
        elif not p[0]:
            raise InvalidMove
        elif not p[1]:
            if (s.color == self.color):
                raise InvalidMove
            else:
                return True
        raise InvalidMove


class Knight(Piece):
    value = 3

    def __init__(self, color, pos, board):
        super(Knight, self).__init__("knight", color)
        self.pos = pos
        self.board = board

    def _checkValidMove(self, t):
        fl, fn, tl, tn, x, xx, y, yy, dx, dy, s, b = self._move(t)
        if ((abs(dx) == 2) and (abs(dy) == 1)) or ((abs(dx) == 1) and (abs(dy) == 2)):
            if s.name is None:
                return True
            if s.color == self.color:
                raise InvalidMove
            else:
                return True
        raise InvalidMove


class Bishop(Piece):
    value = 3

    def __init__(self, color, pos, board):
        super(Bishop, self).__init__("bishop", color)
        self.pos = pos
        self.board = board

    def _checkValidMove(self, t):
        fl, fn, tl, tn, x, xx, y, yy, dx, dy, s, b = self._move(t)

        try:
            if abs(float(dx)/dy) != 1:
                raise InvalidMove
        except ZeroDivisionError:
            raise InvalidMove

        p = self._checkDiagonalPath(fl, fn, tl, tn, dx, dy, b)

        if all(p):
            return True
        if not p[0]:
            raise InvalidMove
        if not p[1]:
            if self.color == s.color:
                raise InvalidMove
            else:
                return True
        raise InvalidMove


class Queen(Piece):
    value = 9

    def __init__(self, color, pos, board):
        super(Queen, self).__init__("queen", color)
        self.pos = pos
        self.board = board

    def _checkValidMove(self, t):
        fl, fn, tl, tn, x, xx, y, yy, dx, dy, s, b = self._move(t)

        if (abs(dx) > 0) and (dy == 0):
            return self._checkHorizontalPath(fl, fn, tl, tn, b)
        elif (dx == 0) and (abs(dy) > 0):
            return self._checkVerticalPath(fl, fn, tl, tn, b)
        else:
            try:
                if abs(float(dx)/dy) != 1:
                    raise InvalidMove
            except ZeroDivisionError:
                raise InvalidMove
            return self._checkDiagonalPath(fl, fn, tl, tn, dx, dy, b)


class King(Piece):
    value = 1000

    def __init__(self, color, pos, board):
        super(King, self).__init__("king", color)
        self.pos = pos
        self.board = board

    def _checkValidMove(self, t):
        fl, fn, tl, tn, x, xx, y, yy, dx, dy, s, b = self._move(t)

        if (abs(dx) > 1) or (abs(dy) > 1):
            raise InvalidMove
        if s.name is None:
            return True
        if s.color != self.color:
            return True
        raise InvalidMove


class Game(object):

    def __init__(self):
        self.board = {n:{l:Space(l+n) for l in "abcdefgh"} for n in "12345678"}

    def initBoard(self):
        lineup = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for piece, letter in zip(lineup, "abcdefgh"):
            for number, color in zip("18", "wb"):
                self.board[number][letter] = piece(color, letter + number)
            for number, color in zip("27", "wb"):
                self.board[number][letter] = Pawn(color, letter + number)

    def move(self, f, t):
        l, n = f.lower()
        p = self.board[n][l]
        if p.name:
            p.move(t)
        else:
            raise InvalidMove("Must select a square with a piece on it")

    def showBoard(self):
        tl, tr, bl, br = "┌ ┐ └ ┘".split()
        t, b, l, r  = "┬ ┴ ├ ┤".split()
        h, v, x = "─ │ ┼".split()

        s = "{v} {a} {v} {b} {v} {c} {v} {d} {v} {e} {v} {f} {v} {g} {v} {h} {v}"
        hs = "{}{}{}".format(h, h, h)
        p = (tl, hs, t, hs, t, hs, t, hs, t, hs, t, hs, t, hs, t, hs, tr)
        print "  {}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(*p)
        ranks = []
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


