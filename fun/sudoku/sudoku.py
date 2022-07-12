from collections import Counter
import os


class SudokuBoard:
    def __init__(self, debug=False):
        self.debug = debug
        self.update_counter = 0

        self.load_test_board()
        self.print_state()

        self.p_state = self._get_initial_possible_state()

        self._update_p_state_from_state()
        # self.iteratively_solve()

        self.reduce_possible_state()

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
        self.state = list(map(int, s))
        assert self.isValid()

    def _get_initial_possible_state(self):
        pstate = set(range(1, 10))
        pstate = [pstate.copy() for i in range(9 * 9)]
        return pstate

    def isValid(self):
        # check for values outside 0-9 integers
        c = Counter(self.state)
        if len(set(c.keys()) - set(range(10))) > 0:
            return False

        # now check for duplicates within rows, cols, & squares
        for element in self._generate_board_elements():
            if self._contains_illegal_repeats(element):
                return False
        return True

    def isSolved(self):
        return 0 not in self.state

    @staticmethod
    def _contains_illegal_repeats(board_element: list):
        c = Counter(board_element)
        if 0 in c:
            num_empty = c.pop(0)
        return len(set(c.values()) - {1}) > 0

    def rows(self, state=None):
        state = state if state else self.state
        yield from self._list_chunks(state, 9)

    def row_indices(self, state=None):
        state = state if state else self.state
        yield from self._list_chunks_indicies(state, 9)

    def cols(self, state=None):
        state = state if state else self.state
        n = 9  # n columns
        for i in range(n):
            yield state[i::n]

    def col_indices(self, state=None):
        state = state if state else self.state
        n = 9  # n columns
        for i in range(n):
            yield range(i, len(state), n)

    def squares(self, state=None):
        s = state if state else self.state
        n = 9  # n squares
        three_chunks = list(self._list_chunks(s, 3))
        for i in range(n):
            a = three_chunks[(i % 3) + 9 * (i // 3) :: 3][:3]
            yield [i for j in a for i in j]

    def square_indices(self, state=None):
        s = state if state else self.state
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

    def _generate_board_elements_and_pstate(self):
        yield from zip(self.rows(), self.rows(state=self.p_state))
        yield from zip(self.cols(), self.cols(state=self.p_state))
        yield from zip(self.squares(), self.squares(state=self.p_state))

    def _generate_board_elements_indices(self):
        yield from self.row_indices()
        yield from self.col_indices()
        yield from self.square_indices()

    def print_state(self):
        os.system("clear")
        s = "\n"
        for i, row in enumerate(self.rows()):
            for j, el in enumerate(row):
                p = " " if el == 0 else str(el)
                s += f"{p} "
                if j % 3 == 2:
                    s += " "
            s += "\n"
            if i % 3 == 2:
                s += "\n"
        print(s)

    def update_state(self, idx, value):
        self.update_counter += 1

        self.state[idx] = value
        self.p_state[idx] = {value}
        if self.debug:
            assert self.isValid(), "invalid board"
        self.print_state()

        if self.isSolved():
            print(f"Solved.")

    def reduce_possible_state(self):
        count = 0
        for row_i in self._generate_board_elements_indices():
            row = [self.state[i] for i in row_i]
            c = Counter(row)
            # check if there's only one missing in row/col/square
            if c.get(0) == 1:
                v = set(range(1, 10)) - set(row)
                idx = row.index(0)
                state_idx = row_i[idx]
                value = v.pop()
                try:
                    self.update_state(state_idx, value)
                except:
                    raise RuntimeError
                self.reduce_possible_state()

        for row_i in self._generate_board_elements_indices():
            row = [self.state[i] for i in row_i]
            # check if row/col/square can eliminate possibilities
            vals = set(row)
            for i in row_i:
                if self.state[i] != 0:
                    continue

                possibilities = self.p_state[i] - vals
                if len(possibilities) == 1:
                    self.update_state(i, possibilities.pop())
                    self.reduce_possible_state()

                elif len(possibilities) == 0:
                    raise RuntimeError

        # now do a check for if there's only one place
        # a certain value exists as a possibility
        for row_i in self._generate_board_elements_indices():
            ps = (self.p_state[i] for i in row_i)
            c = Counter(j for i in ps for j in i)
            if 1 in c.values():
                ...

    def iteratively_solve(self):
        iterations = 1
        changes = self.reduce_possible_state()
        while changes > 0:
            iterations += 1
            changes = self.reduce_possible_state()
            self.print_state()
        return

    def _update_p_state_from_state(self):
        for i, v in enumerate(self.state):
            if v != 0:
                self.p_state[i] = {v}

    def _update_state_from_p_state(self):
        count = 0
        for i, v in enumerate(self.p_state):
            if len(v) == 1 and self.state[i] == 0:
                self.state[i] = v[0]
                count += 1
                assert self.isValid(), "not a valid board"
        return count


if __name__ == "__main__":
    S = SudokuBoard(debug=True)
    ...
