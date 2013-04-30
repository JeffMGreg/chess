# encoding: utf-8

from ipdb import set_trace as trace
import copy

class InvalidMove(Exception):
    def __str__(self):
        return self.msg

class Square(object):
    #~ Parts of the board that make up the piece location.  The space is needed
    #~ for the linking_spaces method in Board
    LETTERS_NUMBERS = ("abcdefgh  ", "12345678  ")

    #~ These are the direction on how to find the neighboring squares. Origin is
    #~ at "a1", letters are along x,  numbers are along y
    #~ Increasing in letters/numbers gives +delta
    #~ Decreasing in letters/numbers gives -delta
    #~ The leading "_" is to help clean up namespace when working from cmdline
    COMPUS_DELTAS = dict(
        _N  = ( 0,  1), _S  = ( 0, -1), _E  = ( 1,  0), _W  = (-1,  0),
        _NE = ( 1,  1), _NW = (-1,  1), _SE = ( 1, -1), _SW = (-1, -1),
        #~ _L's are knight moves from the square
        _L1 = ( 1,  2), _L2 = ( 1, -2), _L3 = ( 2,  1), _L4 = ( 2, -1),
        _L5 = (-1,  2), _L6 = (-1, -2), _L7 = (-2,  1), _L8 = (-2, -1))

    #~ Translate the compus direction into the geometric direction.
    #~ H: Horizontal
    #~ V: Vertical
    #~ L: Knight
    COMPUS_TRANSLATIONS = dict(
        _N  = "V", _S  = "V", _E  = "H", _W  = "H", _NE = "D", _NW = "D", _SE = "D", _SW = "D",
        _L1 = "L", _L2 = "L", _L3 = "L", _L4 = "L", _L5 = "L", _L6 = "L", _L7 = "L", _L8 = "L")

    #~ Geographical direction around the square.  List to loop over when finding
    #~ neighbors.
    COMPUS_DIRECTIONS = ["_N" , "_S" , "_E" , "_W" , "_NE", "_NW", "_SE", "_SW",
                         "_L1", "_L2", "_L3", "_L4", "_L5", "_L6", "_L7", "_L8"]

    def __init__(self, location):
        self.location = location

    def __str__(self):
        return self.location

    def init(self, board):
        self.board = board
        self.link(board)

    def move(self, to):
        move = self.move_calculations(self.get_paths(), to)

        from_location = self.location
        if move[0]:
            if move[1] == "empassant":
                #~ move[2] is the special square that will be captured on an empassant
                move[2].piece = Empty(move[2].location)

            #~ keep track of the last move made
            self.board.last_moved = self.board.get(to)

            #~ keep a list of moves made
            self.board.update_move_list(self.location, to)

            if self.board.SHOW_BOARD:
                self.board.show()
        return move

    def get_paths(self):
        """Get all the squares that have access to attack this square."""
        paths = {"H": set(), "V": set(), "D": set(), "L": set()}
        origin = self
        for direction in self.COMPUS_DIRECTIONS:
            path = paths[self.COMPUS_TRANSLATIONS[direction]]
            path = self._get_path(direction, path)
            self = origin
            paths[self.COMPUS_TRANSLATIONS[direction]] = path
        return paths

    def _get_path(self, direction, path):
        """Get all the squares that have access to attack this square with the
        direction passed."""

        color = self.color
        while True:
            square = getattr(self, direction)
            #~ None implies we're at the edge of the board
            if square is None:
                break

            #~ colors match meaning we're attacking our own piece.  Only save up to the
            #~ piece and not the piece as we can't capture.
            if (color != "wb".replace(square.color, "")) and square.color:
                return path

            #~ colors are different meaning we're attaching a valid piece. Save up to and
            #~ including the piece first encountered.
            elif (color == "wb".replace(square.color, "")) and square.color:
                path.add(square)
                return path

            path.add(square)
            #~ L shape moves only propagate one space for every direction.
            if direction.startswith("_L"):
                return path

            #~ Set the neighbor as the current square.
            self = square
        return path

    def link(self, board):
        """Finds all the neighboring squares to this square and sets an attr
        to the neighboring object."""
        self.board = board
        for direction in self.COMPUS_DIRECTIONS:
            setattr(self, direction, self._find_neighbors(board, direction))

    def _find_neighbors(self, board, direction):
        """Finds neighbor's object in the board given compus direction."""
        neighbor = []
        for part, delta, variables in zip(self.location, self.COMPUS_DELTAS[direction], self.LETTERS_NUMBERS):
            try:
                position = variables.find(part)
                neighbor.append(variables[position + delta])
            except (ValueError, IndexError):
                return None
        try:
            return board[neighbor[0]][neighbor[1]]
        except KeyError:
            return None


class Piece(Square):

    PIECES = {"King"  : {"b": "♔", "w": "♚"},
              "Queen" : {"b": "♕", "w": "♛"},
              "Rook"  : {"b": "♖", "w": "♜"},
              "Bishop": {"b": "♗", "w": "♝"},
              "Knight": {"b": "♘", "w": "♞"},
              "Pawn"  : {"b": "♙", "w": "♟"},
              "Empty" : {"" : " "}}

    def __init__(self, location, color="", side=""):
        Square.__init__(self, location)

        self.move_count = 0
        self.color      = color
        #~ Nice name of the class
        self.name       = self.__class__.__name__
        #~ The piece that get printed
        self.symbol     = self.PIECES[self.name][self.color]
        #~ The side (Queen or King) the piece is on
        self.side       = side
        #~ A list of all team members
        self.team       = []

    def __str__(self):
        return self.symbol

    def move_calculations(self, paths, to):
        from_letter, from_number = self.location
        to_letter, to_number = to

        dx = "abcdefgh".find(to_letter) - "abcdefgh".find(from_letter)
        dy = "12345678".find(to_number) - "12345678".find(from_number)

        vpos = to in map(lambda x: x.location, paths["V"])
        dpos = to in map(lambda x: x.location, paths["D"])
        hpos = to in map(lambda x: x.location, paths["H"])
        lpos = to in map(lambda x: x.location, paths["L"])

        valid = self.move_valid_check(paths, to, dx, dy, vpos, dpos, hpos, lpos)

        if not self.check_king_safety(to):
            return False, "King exposed", None

        return valid

    def check_king_safety(self, to):
        #~ Remove the piece from the board
        from_piece = self
        from_location = self.location
        to_piece   = self.board.get(to)

        #~ self.board.set(self.location, Empty(self.location))
        self.board.set(to, from_piece)
        self.board.set(from_location, Empty(from_location))
        try:
            king, = filter(lambda x: x.name is "King", self.team)
        except ValueError:
            return True
        paths = king.get_paths()
        threats = ["Rook", "Queen", "Bishop"]
        for direction in "HVD":
            for square in paths[direction]:
                if (square.name in threats):
                    self.board.set(from_location, from_piece)
                    self.board.set(to_piece.location, to_piece)
                    return False
                    break
        return True


class Empty(Piece):
    def __init__(self, location, color=""):
        Piece.__init__(self, location)

    def move(self, *args):
        raise InvalidMove("Must select a square with a piece on it")


class Pawn(Piece):
    def __init__(self, location, color, side):
        Piece.__init__(self, location, color, side)

        #~ The direction that the piece must move, only needed with Pawns
        if self.color == "w":
            #~ Must move up the board
            self.must_move = 1
        else:
            #~ Must move down the board
            self.must_move = -1

    def move_valid_check(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        to_square = self.board.get(to)
        #~ Square to handle enpassant
        special = to_square.__getattribute__(["", "_S", "_N"][self.must_move])

        valid_moves = [
        #~ Normal attack
        ((dy * self.must_move) == 1) and dpos and (to_square.name is not "Empty"),
        #~ Move one square
        ((dy * self.must_move) == 1) and vpos and (to_square.name is "Empty"),
        #~ Move two squares on first move
        ((dy * self.must_move) == 2) and vpos and (to_square.name is "Empty") and
        (self.move_count == 0),
        #~ Enpassant
        ((dy * self.must_move) == 1) and dpos and (special.color != self.color) and
        (special.name == "Pawn") and (special.move_count == 1) and
        (self.board.last_moved == special)
        ]

        if any(valid_moves):
            self.move_count += 1
            if valid_moves[3]:
                return True, "empassant", special
            elif valid_moves[0]:
                return True, "attack", None
            else:
                return True, "normal", None
        else:
            return False, "", None


class Rook(Piece):
    def __init__(self, location, color, side):
        Piece.__init__(self, location, color, side)

    def move_valid_check(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        valid_moves = [(abs(dy) > 0) and (dx == 0) and vpos,
                       (abs(dx) > 0) and (dy == 0) and hpos]
        if any(valid_moves):
            return True, "normal", None
        else:
            return False, "", None


class Knight(Piece):
    def __init__(self, location, color, side):
        Piece.__init__(self, location, color, side)

    def move_valid_check(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        if lpos:
            return True, "normal", None
        else:
            return False, "", None


class Bishop(Piece):
    def __init__(self, location, color, side):
        Piece.__init__(self, location, color, side)

    def move_valid_check(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        if dpos:
            return True, "normal", None
        else:
            return False, "", None


class King(Piece):
    def __init__(self, location, color, side):
        Piece.__init__(self, location, color, side)

    def move_valid_check(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):

        for side in "kq":
            try:
                r, = filter(lambda x: x.name is "Rook" and x.side is "k", self.team)
            except ValueError:
                raise Exception("Rook not found in piece team")
            else:
                rooks.append(r)

        valid_moves = [
            #~ Normal King moves
            ((abs(dx) == 1) or (abs(dy) == 1)) and ((to in vpos) or (to in hpos) or (to in dpos)),
            #~ King side castle
            (dx ==  2) and (dy == 0) and (self.move_count == 0) and (rooks[0].move_count == 0) and
            (rooks[0].move_count == 0) and ("g1" in hpos),
            #~ Queen side castle
            (dx == -2) and (dy == 0) and (self.move_count == 0) and (rooks[1].move_count == 0) and
            (rooks[1].move_count == 0) and ("b1" in hpos)]

        if any(valid_moves):
            if valid_moves[1]:
                return True, "queen_side_castle", None
            elif valid_moves[2]:
                return True, "king_side_castle", None
            else:
                return True, "normal", None
        else:
            return False, "", None


class Queen(Piece):
    def __init__(self, location, color, side):
        Piece.__init__(self, location, color, side)

    def move_valid_check(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        if (to in hpos) or (to in vpos) or (to in hpos):
            return True, "normal", None
        else:
            return False, "", None


class Board(dict):

    SHOW_BOARD = True

    def __init__(self):
        board = self.setup()
        for letter_key in board:
            self[letter_key] = {}
            for number_key in board[letter_key]:
                self[letter_key][number_key] = board[letter_key][number_key]

        self.move_list  = []
        self.last_moved = None

        if self.SHOW_BOARD:
            self.setup()
            self.show()

    def __getattr__(self, location):
        return self.get(location)

    def show(self):
        #~ "┌ ┐ └ ┘ ┬ ┴ ├ ┤ ─ │ ┼"
        print " ┌───┬───┬───┬───┬───┬───┬───┬───┐"
        for number in "87654321":
            row = []
            for letter in "abcdefgh":
                row.append(self[letter][number].symbol)
            print number + "│ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │".format(*row)
            if number == "1": break
            print " ├───┼───┼───┼───┼───┼───┼───┼───┤"
        print " └───┴───┴───┴───┴───┴───┴───┴───┘"
        print "   a   b   c   d   e   f   g   h"

    def update_move_list(self, from_location, to_location):
        cl_move = "Board.{}.move(\"{}\")".format(from_location, to_location)
        self.move_list.append(cl_move)

    def get(self, location):
        letter, number = location
        return self[letter][number]

    def set(self, location, square):
        self[location[0]][location[1]] = square
        square.location = location
        #~ Every time a move is made we must relink our squares as moveing
        #~ will break links and reference the incorrect square.
        self._link_squares()

    def setup(self):
        board  = {letter:{number:None for number in "12345678"} for letter in "abcdefgh"}
        lineup = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        white = []
        black = []
        for piece, letter, side in zip(lineup, "abcdefgh", "qqqqkkkk"):
            for number, color in zip("18", "wb"):
                board[letter][number] = piece(letter + number, color, side)
                if color == "w":
                    white.append(board[letter][number])
                else:
                    black.append(board[letter][number])

            for number, color in zip("27", "wb"):
                board[letter][number] = Pawn(letter + number, color, side)
                if color == "w":
                    white.append(board[letter][number])
                else:
                    black.append(board[letter][number])

            for number in "3456":
                board[letter][number] = Empty(letter + number)

        self._set_teams(board, white, black)
        self._link_squares()
        return board

    def clear(self):
        for letter in "abcdefgh":
            for number in "12345678":
                self[letter][number] = Empty(letter + number)
        self.show()

    #~ Internal APIs -----------------------------------------------------------
    def _set_teams(self, board, white, black):
        for letter in "abcdefgh":
            for number in "12":
                board[letter][number].team = white
            for number in "78":
                board[letter][number].team = black

    def _link_squares(self):
        for letter in self.keys():
            for number in self[letter].keys():
                self[letter][number].init(self)


if __name__ == "__main__":

    b = Board()
    b.clear()

    k = King("e1", "w", "k")
    r = Rook("e2", "w", "k")
    br = Rook("e7", "b", "k")

    k.team = [k, r]
    r.team = [k, r]
    br.team = [br]

    b.set("e1", k)
    b.set("e2", r)
    b.set("e7", br)

    b.show()

    print b.e2.move("d2")
