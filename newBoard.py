# encoding: utf-8

from ipdb import set_trace as trace

class InvalidMove(Exception):
    def __str__(self):
        return self.msg

class Square(object):
    #~ Parts of the board that make up the piece location.  The space is needed
    #~ for the linking_spaces method in Board
    letters_numbers = ("abcdefgh  ", "12345678  ")

    #~ These are the direction on how to find the neighboring squares. Origin is
    #~ at "a1", letters are along x,  numbers are along y
    #~ Increasing in letters/numbers gives +delta
    #~ Decreasing in letters/numbers gives -delta
    #~ The leading "_" is to help clean up namespace when working from cmdline
    compus_deltas = dict(
        _N  = ( 0,  1), _S  = ( 0, -1), _E  = ( 1,  0), _W  = (-1,  0),
        _NE = ( 1,  1), _NW = (-1,  1), _SE = ( 1, -1), _SW = (-1, -1),
        #~ _L's are knight moves from the square
        _L1 = ( 1,  2), _L2 = ( 1, -2), _L3 = ( 2,  1), _L4 = ( 2, -1),
        _L5 = (-1,  2), _L6 = (-1, -2), _L7 = (-2,  1), _L8 = (-2, -1))

    #~ Translate the compus direction into the geometric direction.
    #~ H: Horizontal
    #~ V: Vertical
    #~ L: Knight
    compus_translations = dict(
        _N  = "V", _S  = "V", _E  = "H", _W  = "H", _NE = "D", _NW = "D", _SE = "D", _SW = "D",
        _L1 = "L", _L2 = "L", _L3 = "L", _L4 = "L", _L5 = "L", _L6 = "L", _L7 = "L", _L8 = "L")

    #~ Geographical direction around the square.  List to loop over when finding
    #~ neighbors.
    compus_directions = ["_N" , "_S" , "_E" , "_W" , "_NE", "_NW", "_SE", "_SW",
                         "_L1", "_L2", "_L3", "_L4", "_L5", "_L6", "_L7", "_L8"]

    def __init__(self, location):
        self.location = location
        self.piece = Empty(location)

    def __str__(self):
        return self.location

    def init(self, board):
        self.board = board
        self._link_squares(board)

    def move(self, to):
        move = self.piece.move(self.get_paths(), to)

        if move[0]:
            #~ Sets the piece square to the to square
            self.piece.square = self.board.get(to)
            self.board.get(to).piece = self.piece
            self.piece = Empty(self.location)
            if move[1] == "empassant":
                move[2].piece = Empty(move[2].location)


            self.board.last_moved = self.board.get(to)
            self.board.update_move_list(self.location, to)

            if self.board.SHOW_BOARD:
                self.board.show()

        return move

    def get_paths(self):
        """Get all the squares that have access to attack this square."""
        paths = {"H": set(), "V": set(), "D": set(), "L": set()}
        origin = self
        for direction in self.compus_directions:
            path = paths[self.compus_translations[direction]]
            path = self._get_path(direction, path)
            self = origin
            paths[self.compus_translations[direction]] = path
        return paths

    def _get_path(self, direction, path):
        """Get all the squares that have access to attack this square with the
        direction passed."""
        current_color = self.piece.color
        while True:
            square = getattr(self, direction)
            #~ None implies we're at the edge of the board
            if square is None:
                break

            #~ colors match meaning we're attacking our own piece.  Only save up to the
            #~ piece and not the piece as we can't capture.
            if (current_color != "wb".replace(square.piece.color, "")) and square.piece.color:
                return path

            #~ colors are different meaning we're attaching a valid piece. Save up to and
            #~ including the piece first encountered.
            elif (current_color == "wb".replace(square.piece.color, "")) and square.piece.color:
                path.add(square)
                return path

            path.add(square)
            #~ L shape moves only propagate one space for every direction.
            if direction.startswith("_L"):
                return path

            #~ Set the neighbor as the current square.
            self = square
        return path

    def _link_squares(self, board):
        """Finds all the neighboring squares to this square and sets an attr
        to the neighboring object."""
        for direction in self.compus_directions:
            setattr(self, direction, self._find_neighbors(board, direction))

    def _find_neighbors(self, board, direction):
        """Finds neighbor's object in the board given compus direction."""
        neighbor = []
        for part, delta, variables in zip(self.location, self.compus_deltas[direction], self.letters_numbers):
            try:
                position = variables.find(part)
                neighbor.append(variables[position + delta])
            except (ValueError, IndexError):
                return None
        try:
            return board[neighbor[0]][neighbor[1]]
        except KeyError:
            return None


class Piece(object):

    pieces = {"King"  : {"b": "♔", "w": "♚"},
              "Queen" : {"b": "♕", "w": "♛"},
              "Rook"  : {"b": "♖", "w": "♜"},
              "Bishop": {"b": "♗", "w": "♝"},
              "Knight": {"b": "♘", "w": "♞"},
              "Pawn"  : {"b": "♙", "w": "♟"},
              "Empty" : {"" : " "}}

    def __init__(self, square, color="", side=""):
        self.move_count = 0
        self.square     = square
        self.color      = color
        self.name       = self.__class__.__name__
        self.piece      = self.pieces[self.name][self.color]
        self.side       = side

    def __str__(self):
        return self.piece

    def move(self, paths, to):
        from_letter, from_number = self.square.location
        to_letter, to_number = to

        dx = "abcdefgh".find(to_letter) - "abcdefgh".find(from_letter)
        dy = "12345678".find(to_number) - "12345678".find(from_number)

        vpos = to in map(lambda x: x.location, paths["V"])
        dpos = to in map(lambda x: x.location, paths["D"])
        hpos = to in map(lambda x: x.location, paths["H"])
        lpos = to in map(lambda x: x.location, paths["L"])

        return self._move(paths, to, dx, dy, vpos, dpos, hpos, lpos)


class Empty(Piece):
    def __init__(self, square):
        Piece.__init__(self, square)

    def move(self, *args):
        raise InvalidMove("Must select a square with a piece on it")


class Pawn(Piece):
    def __init__(self, square, color, side):
        Piece.__init__(self, square, color, side)

        #~ The direction that the piece must move, only needed with Pawns
        if self.color == "w":
            #~ Must move up the board
            self.must_move = 1
        else:
            #~ Must move down the board
            self.must_move = -1

    def _move(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        to_square = self.square.board.get(to)
        #~ Square to handle enpassant
        special = to_square.__getattribute__(["", "_S", "_N"][self.must_move])

        valid_moves = [
        #~ Normal attack
        ((dy * self.must_move) == 1) and dpos and (to_square.piece.name is not "Empty"),
        #~ Move one square
        ((dy * self.must_move) == 1) and vpos and (to_square.piece.name is "Empty"),
        #~ Move two squares on first move
        ((dy * self.must_move) == 2) and vpos and (to_square.piece.name is "Empty") and
        (self.move_count == 0),
        #~ Enpassant
        ((dy * self.must_move) == 1) and dpos and (special.piece.color != self.color) and
        (special.piece.name == "Pawn") and (special.piece.move_count == 1) and
        (self.square.board.last_moved == special)
        ]

        if any(valid_moves):
            self.move_count += 1
            if valid_moves[3]:
                #~ return True, "enpassant:" + ["", "_S", "_N"][self.must_move]
                return True, "empassant", special
            elif valid_moves[0]:
                return True, "attack", None
            else:
                return True, "normal", None
        else:
            return False, "", None


class Rook(Piece):
    def __init__(self, square, color, side):
        Piece.__init__(self, square, color, side)

    def _move(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        valid_moves = [(abs(dy) > 0) and (dx == 0) and vpos,
                       (abs(dx) > 0) and (dy == 0) and hpos]
        if any(valid_moves):
            return True, "normal", None
        else:
            return False, "", None


class Knight(Piece):
    def __init__(self, square, color, side):
        Piece.__init__(self, square, color, side)

    def _move(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        if lpos:
            return True, "normal", None
        else:
            return False, "", None


class Bishop(Piece):
    def __init__(self, square, color, side):
        Piece.__init__(self, square, color, side)

    def _move(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        if dpos:
            return True, "normal", None
        else:
            return False, "", None


class King(Piece):
    def __init__(self, square, color, side):
        Piece.__init__(self, square, color, side)

    def _move(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):

        ipdb.set_trace()

        rooks = []
        for side in "kq":
            try:
                r, = filter(lambda x: x.name is "Rook" and x.side is "k", self.square.piece.team)
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
                return True, "queen_side_castle"
            elif valid_moves[2]:
                return True, "king_side_castle"
            else:
                return True, "normal"
        else:
            return False, ""


class Queen(Piece):
    def __init__(self, square, color, side):
        Piece.__init__(self, square, color, side)

    def _move(self, paths, to, dx, dy, vpos, dpos, hpos, lpos):
        if (to in hpos) or (to in vpos) or (to in hpos):
            return True, "normal"
        else:
            return False, ""


class Board(dict):

    SHOW_BOARD = False

    def __init__(self, sub=False):
        for key in sub.keys():
            if (type(sub[key]) is dict):
                self[key] = Board(sub[key])
            else:
                self[key] = sub[key]
        self.move_list = []

        #~ We're at the last file, we can now link our squares together.
        if key == "h":
            self.last_moved = None
            self._link_squares()
            self._setup_pieces()
            if self.SHOW_BOARD:
                self.show()

    def show(self):
        #~ "┌ ┐ └ ┘ ┬ ┴ ├ ┤ ─ │ ┼"
        print " ┌───┬───┬───┬───┬───┬───┬───┬───┐"
        for number in "87654321":
            row = []
            for letter in "abcdefgh":
                row.append(self.get(letter + number).piece)
            print number + "│ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │".format(*row)
            if number == "1": break
            print " ├───┼───┼───┼───┼───┼───┼───┼───┤"
        print " └───┴───┴───┴───┴───┴───┴───┴───┘"
        print "   a   b   c   d   e   f   g   h"

    def update_move_list(self, from_location, to_location):
        cl_move = "Board.{}.move(\"{}\")".format(from_location, to_location)
        self.move_list.append(cl_move)

    def __getattr__(self, location):
        letter, number = location
        return self[letter][number]

    def get(self, location):
        letter, number = location
        return self[letter][number]

    def _link_squares(self):
        for letter in self.keys():
            for number in self[letter].keys():
                self[letter][number].init(self)

    def _setup_pieces(self):
        lineup = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        white = []
        black = []
        for piece, letter, side in zip(lineup, "abcdefgh", "qqqqkkkk"):
            for number, color in zip("18", "wb"):
                square = self.get(letter+number)
                player = piece(square, color, side)
                if color == "w":
                    white.append(player)
                else:
                    black.append(player)
                square.piece = player

            for number, color in zip("27", "wb"):
                square = self.get(letter+number)
                player = Pawn(square, color, side)
                if color == "w":
                    white.append(player)
                else:
                    black.append(player)
                square.piece = player
        self._assign_team(white, black)

    def _assign_team(self, white, black):
        for letter in "abcdefgh":
            for number in "12":
                self.get(letter + number).piece.team = white
            for number in "78":
                self.get(letter + number).piece.team = black

if __name__ == "__main__":
    b = Board({letter:{number:Square(letter+number) for number in "12345678"} for letter in "abcdefgh"})

