

class Space(object):

    letters = "abcdefgh "
    numbers = "12345678 "

    def __init__(self, location):
        self.location = location

    def __repr__(self):
        return self.location

    def get_path(self):
        path = []
        while True:
            space = self.east
            if space is None:
                break
            else:
                self = self.east
                path.append(self)
        return path

    def link_spaces(self, board):
        for direction in ["north", "south", "east", "west"]:
            setattr(self, direction, self._to_90s(board, direction))

        for direction in ["north_east", "north_west", "south_east", "south_west"]:
            setattr(self, direction, self._to_45s(board, direction))

    def _to_90s(self, board, direction):
        letter, number = self.location

        if direction == "north":
            delta, variable = 1, self.numbers
        elif direction == "east":
            delta, variable = 1, self.letters
        elif direction == "west":
            delta, variable = -1, self.letters
        elif direction == "south":
            delta, variable = -1, self.numbers
        else:
            raise Exception("Invalid direction")

        try:
            if direction in ["north", "south"]:
                number = variable[variable.find(number) + delta]
            else:
                letter = variable[variable.find(letter) + delta]
        except (ValueError, IndexError):
            return None
        else:
            try:
                return board[letter][number]
            except KeyError:
                return None

    def _to_45s(self, board, direction):
        letter, number = self.location

        if direction == "north_east":
            dx, dy = 1, 1
        elif direction == "north_west":
            dx, dy = -1, 1
        elif direction == "south_east":
            dx, dy = 1, -1
        elif direction == "south_west":
            dx, dy = -1, -1
        else:
            raise Exception("Invalid direction")

        try:
            number = self.numbers[self.numbers.find(number) + dy]
        except (ValueError, IndexError):
            return None

        try:
            letter = self.letters[self.letters.find(letter) + dx]
        except (ValueError, IndexError):
            return None

        try:
            return board[letter][number]
        except KeyError:
            return None

board = {letter:{number:Space(letter+number) for number in "12345678"} for letter in "abcdefgh"}

for letter in board.keys():
    for number in board[letter].keys():
        board[letter][number].link_spaces(board)
