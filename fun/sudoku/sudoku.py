from collections import Counter
import os
from itertools import islice

VALUES = set(range(1, 10))


class SudokuBoard:
    def __init__(self, state=None, debug=False, show_state=True, name=None):
        self.name = name
        self.debug = debug
        self.show_state = show_state
        self.update_counter = 0
        self.p_state = self._get_initial_possible_state()
        self.initial_state = state

        if state is not None:
            self._update_p_state_from_state(state)
            assert self.isValid, "not a valid state"
        else:
            self._update_p_state_from_state(self.load_test_board())

        self.print_state()

    def add_hint(self):
        idx, value = self.reduce_possible_state()
        if value != 0:
            self.update_state(idx, value)
        else:
            "uh oh"

    def solve(self):
        while not self.isSolved():
            self.add_hint()
        if self.isSolved() and self.isValid():
            return 0
        else:
            return -1

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
        return list(map(int, s))

    def _get_initial_possible_state(self):
        pstate = [VALUES.copy() for i in range(9 * 9)]
        return pstate

    def isValid(self):
        # check for values outside 0-9 integers
        s = set(self.generate_simple_state())
        if len(s - set(range(10))) > 0:
            return False

        # check for duplicates within rows, cols, & squares
        for element_indices in self._generate_board_elements_indices():

            if self._contains_illegal_repeats(
                self.indicies_to_definite_state(element_indices)
            ):
                return False

        return True

    def isSolved(self):
        return set(len(i) for i in self.p_state) == {1}

    def _contains_illegal_repeats(self, element):
        c = Counter(element)
        if 0 in c:
            c.pop(0)
        return len(set(c.values()) - {1}) > 0

    def rows(self):
        state = self.p_state
        yield from self._list_chunks(state, 9)

    def row_indices(self):
        state = self.p_state
        yield from self._list_chunks_indicies(state, 9)

    def cols(self):
        state = self.p_state
        for col_i in self.col_indices(state=state):
            yield [state[i] for i in col_i]

    def col_indices(self):
        n = 9  # n columns
        for i in range(n):
            yield range(i, n * n, n)

    def squares(self):
        s = self.p_state
        n = 9  # n squares
        three_chunks = list(self._list_chunks(s, 3))
        for i in range(n):
            a = three_chunks[(i % 3) + 9 * (i // 3) :: 3][:3]
            yield [i for j in a for i in j]

    def square_indices(self):
        s = self.p_state
        n = 9  # n squares
        three_chunks = list(self._list_chunks_indicies(s, 3))
        for i in range(n):
            a = three_chunks[(i % 3) + 9 * (i // 3) :: 3][:3]
            yield [i for j in a for i in j]

    @staticmethod
    def _list_chunks(s: list, n: int):
        for i in range(0, len(s), n):
            yield s[i : i + n]

    @staticmethod
    def _list_chunks_indicies(s: list, n: int):
        for i in range(0, len(s), n):
            yield range(i, i + n)

    def _generate_board_elements(self):
        yield from self.rows()
        yield from self.cols()
        yield from self.squares()

    def _generate_board_elements_indices(self):
        yield from self.row_indices()
        yield from self.col_indices()
        yield from self.square_indices()

    def print_state(self):
        os.system("clear")
        if self.name:
            print(self.name)
        s = "╔═════╦═════╦═════╗\n"
        for i, rowi in enumerate(self.row_indices()):
            s += "║"
            for j, el in enumerate(self.p_state[j] for j in rowi):
                p = " " if len(el) > 1 else str(*el)
                s += f"{p}"

                s += "║" if j % 3 == 2 else "│"
            s += "\n"
            if i == 2 or i == 5:
                s += "╠═════╬═════╬═════╣\n"
            elif i == 8:
                s += "╚═════╩═════╩═════╝\n"
        print(s)

    def update_state(self, idx, value):
        self.update_counter += 1

        self.p_state[idx] = {value}
        if self.debug:
            assert self.isValid(), "invalid board"

        if self.show_state:
            self.print_state()

    def _find_one_missing(self, element_indices) -> tuple:
        """
        check if there's only one missing in row/col/square
        element_indices: generator of indices for a row, column, or square
        """
        row = list(self.indicies_to_definite_state(element_indices))
        if row.count(0) == 1:
            v = VALUES - set(row)
            state_idx = element_indices[row.index(0)]
            value = v.pop()
            return state_idx, value
        else:
            return 0, 0

    def _eliminate_possibilities(self, element_indices) -> tuple:
        """
        check if row/col/square can eliminate possibilities
        element_indices: generator of indices for a row, column, or square
        """
        vals = set(self.indicies_to_definite_state(element_indices))
        for i in element_indices:
            possibilities = self.p_state[i]

            if len(possibilities) == 1:
                continue

            possibilities -= vals  # this line removes the eliminated possibilites
            if len(possibilities) == 1:
                return i, possibilities.pop()

            assert len(possibilities) > 0, "something went wrong"

        return 0, 0

    def _check_for_one_place(self, element_indices) -> tuple:
        """
        check if there's only one place a certain value can be

        element_indices: generator of indices for a row, column, or square
        """
        ps = filter(self.indefinite, (self.p_state[i] for i in element_indices))
        c = Counter(j for i in ps for j in i)
        if 1 in c.values():
            value = {v: k for k, v in c.items()}[1]
            for i in element_indices:
                if value in self.p_state[i]:
                    return i, value
        return 0, 0

    def _eliminate_based_on_undetermined_squares(self, element_indices) -> tuple:
        """
        if you know a number occurs in a particular part
        of a row/col/square, you might be able to eliminate possibilities
        in other rows/cols/squares
        """
        d = element_indices[-1] - element_indices[0]
        element_type = {8: "row", 72: "col", 20: "square"}[d]
        row_definite = list(self.indicies_to_definite_state(element_indices))
        row = list(self.indicies_to_possibilites(element_indices))
        row_grouped_in_thirds = [
            row[i].union(row[i + 1], row[i + 2]) for i in range(0, 9, 3)
        ]
        row_transpose_grouped_in_thirds = [
            row[i].union(row[i + 3], row[i + 6]) for i in range(0, 3)
        ]
        for val in VALUES:
            if val in row_definite:
                continue
            val_in_thirds = [val in i for i in row_grouped_in_thirds]
            val_trans_in_thirds = [val in i for i in row_transpose_grouped_in_thirds]
            if val_in_thirds.count(True) == 1 or (
                element_type == "square" and val_trans_in_thirds.count(True) == 1
            ):
                # that value is only found in one third of the row/col/square
                idxs = [idx for i, idx in enumerate(element_indices) if val in row[i]]
                if element_type in ["row", "col"]:
                    ids = self._get_square_indicies_containing(idxs[0])

                elif element_type == "square":  # square
                    idx_diff = idxs[-1] - idxs[0]
                    if idx_diff < 3:
                        ids = self._get_row_indicies_containing(idxs[0])
                    else:
                        ids = self._get_col_indicies_containing(idxs[0])

                for i in ids:
                    if i not in idxs:
                        if val in self.p_state[i]:
                            self.p_state[i].remove(val)
        return 0, 0

    def _get_square_indicies_containing(self, idx):
        for sq in self.square_indices():
            if idx in sq:
                return sq

    def _get_row_indicies_containing(self, idx):
        for sq in self.row_indices():
            if idx in sq:
                return sq

    def _get_col_indicies_containing(self, idx):
        for sq in self.col_indices():
            if idx in sq:
                return sq

    def reduce_possible_state(self):
        if self.isSolved():
            return 0, 0

        for element_indices in self._generate_board_elements_indices():
            for func in [
                self._find_one_missing,
                self._eliminate_possibilities,
                self._check_for_one_place,
                self._eliminate_based_on_undetermined_squares,
            ]:
                idx, value = func(element_indices)
                if value != 0:
                    return idx, value

        return 0, 0

    def _update_p_state_from_state(self, state):
        for i, v in enumerate(state):
            if v != 0:
                self.p_state[i] = {v}

    @staticmethod
    def definite(s: set):
        return len(s) == 1

    @staticmethod
    def indefinite(s: set):
        return len(s) > 1

    def generate_simple_state(self):
        yield from self.indefinite_to_definite_state(self.p_state)

    def indefinite_to_definite_state(self, state):
        for p in state:
            yield p.copy().pop() if len(p) == 1 else 0

    def indicies_to_possibilites(self, indicies):
        for i in indicies:
            yield self.p_state[i]

    def indicies_to_definite_state(self, indicies):
        yield from self.indefinite_to_definite_state(
            self.indicies_to_possibilites(indicies)
        )


def gen_test_boards():
    d = os.path.dirname(__file__)
    fn = os.path.join(d, "easy50.txt")
    with open(fn, "r") as f:
        for line in f:
            yield line


def solve_all_test_boards():
    for i, board_str in enumerate(gen_test_boards()):
        print(f"Board {i}")
        S = SudokuBoard(state_str_to_list(board_str), debug=True, name=f"Board {i}")
        S.solve()


def state_str_to_list(state_str):
    return list(map(int, state_str.strip()))


if __name__ == "__main__":
    solve_all_test_boards()

    S = SudokuBoard(debug=False)
    S.print_state()
    S.solve()

    ...
