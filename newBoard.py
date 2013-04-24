import ipdb

class Space(object):

    #~ Parts of the board that make up the piece location.  The space is needed
    #~ for the linking_spaces method
    letters_numbers = ("abcdefgh  ", "12345678  ")
    #~ These are the direction on how to find the neighboring squares. Origin is
    #~ at "a1", letters along x numbers along y
    #~ Increasing in letters/numbers gives +delta
    #~ Decreasing in letters/numbers gives -delta
    compus_deltas = dict(
        N  = ( 0,  1), S  = ( 0, -1), E  = ( 1,  0), W  = (-1,  0),
        NE = ( 1,  1), NW = (-1,  1), SE = ( 1, -1), SW = (-1, -1),
        L1 = ( 1,  2), L2 = ( 1, -2), L3 = ( 2,  1), L4 = ( 2, -1), 
        L5 = (-1,  2), L6 = (-1, -2), L7 = (-2,  1), L8 = (-2, -1))
    
    #~ Translate the compus direction into the geometric direction.
    #~ H: Horizontal
    #~ V: Vertical
    #~ L: Knight 
    compus_translations = dict(
        N  = "V", S  = "V", E  = "H", W  = "H", NE = "D", NW = "D", SE = "D", SW = "D",
        L1 = "L", L2 = "L", L3 = "L", L4 = "L", L5 = "L", L6 = "L", L7 = "L", L8 = "L")

    #~ Geographical direction around the square
    compus_directions = ["N" , "S" , "E" , "W" , "NE", "NW", "SE", "SW",
                         "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]

    def __init__(self, location):
        self.location = location
        self.piece = None

    def __repr__(self):
        return self.location

    def init(self, board):
        self._link_spaces(board)

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
        while True:
            space = getattr(self, direction)
            #~ None implies we're at the edge of the board
            if space is None: 
                break                
            path.add(space)
            #~ L shape moves only propagate one space for every direction.
            if direction.startswith("L"): 
                return path
            self = space        
        return path
        
    def _link_spaces(self, board):
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
        
class Piece(object):pass
class Pawn(Piece):pass
class Rook(Piece):pass
class Knight(Piece):pass
class Bishop(Piece):pass
class King(Piece):pass
class Queen(Piece):pass
    

class Board(dict):
                     #~ White
    initial_layout = [("a2", Pawn), ("b2", Pawn), ("c2", Pawn), ("d2", Pawn), 
                      ("e2", Pawn), ("f2", Pawn), ("g2", Pawn), ("h2", Pawn), 
                      ("a1", Rook), ("b1", Knight), ("c1", Bishop), ("d1", Queen), 
                      ("e1", King), ("f1", Bishop), ("g1", Knight), ("h1", Rook),
                      #~ Black
                      ("a7", Pawn), ("b7", Pawn), ("c7", Pawn), ("d7", Pawn), 
                      ("e7", Pawn), ("f7", Pawn), ("g7", Pawn), ("h7", Pawn), 
                      ("a8", Rook), ("b8", Knight), ("c8", Bishop), ("d8", Queen), 
                      ("e8", King), ("f8", Bishop), ("g8", Knight), ("h8", Rook)]                      
                      
    #~ Makes a dict of all the free spaces for the board
    free_spaces = {letter:{number:Space(letter+number) for number in "12345678"} for letter in "abcdefgh"}
    
    def __init__(self, sub_dict=False):

        if sub_dict:
            self.sub = sub_dict
        else:
            self.sub = self.free_spaces

        #~ Handle the nested dicts
        for key in self.sub.keys():
            if (type(self.sub[key]) is dict):
                self[key] = Board(self.sub[key])
            else:
                self[key] = self.sub[key]

        #~ We're at the last file, we can now link our squares together.
        if key == "h":
            self._link_spaces()
                
    def __getattr__(self, location):
        letter, number = location
        return self[letter][number]

    def _link_spaces(self):
        for letter in self.keys():
            for number in self[letter].keys():
                self[letter][number].init(self)
                
    def setup_pieces(self):
        


b = Board()
