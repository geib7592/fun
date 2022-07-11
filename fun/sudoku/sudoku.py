import collections

import numpy as np


class SudokuBoard:
    def __init__(self):
        self.state = np.zeros([9, 9], dtype=int)
        self.load_test_board()
        self.print_state()

    def load_test_board(self):
        s = (
            "003020600"
            "900305001"
            "001806400"
            "008102900"
            "700000008"
            "006708200"
            "002609500"
            "800203009"
            "005010300"
        )
        self.state = np.array(list(map(int, s))).reshape(9, 9)
        assert self.isValid()

    def isValid(self):

        # check for values outside 0-9 integers
        flat_state = self.state.flatten()
        c = collections.Counter(flat_state)
        if len(set(c.keys()) - set(range(10))) > 0:
            return False

        for element in self._generate_board_elements():
            if self._contains_illegal_repeats(element):
                return False

        return True

    @staticmethod
    def _contains_illegal_repeats(board_element: np.ndarray):
        c = collections.Counter(board_element.flatten())
        num_empty = c.pop(0)
        return len(set(c.values()) - {1}) > 0

    def _generate_board_elements(self):
        for row in self.state:
            yield row

        for col in self.state.T:
            yield col

        for i in range(3):
            for j in range(3):
                yield self.state[3 * i : 3 * i + 3, 3 * j : 3 * j + 3].flatten()

    def print_state(self):
        s = ""
        for i, row in enumerate(self.state):
            for j, el in enumerate(row):
                s += f"{el} "
                if j % 3 == 2:
                    s += " "
            s += "\n"
            if i % 3 == 2:
                s += "\n"
        print(s)


if __name__ == "__main__":
    S = SudokuBoard()
    ...
