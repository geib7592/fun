from collections import defaultdict
from pprint import pprint
import numpy as np

example_data = """
30373
25512
65332
33549
35390
"""

INPUT_FILE_PATH = "fun/aoc2022/input_files/day08_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    d = np.array(load_to_list(data))
    r = np.zeros_like(d)
    for i in range(4):
        dr = np.rot90(d, i)
        m = np.diff(np.maximum.accumulate(dr, axis=1), axis=1) != 0
        m = m.astype(int)
        b = np.append(np.ones([d.shape[0], 1], int), m, axis=1)
        b = np.rot90(b, k=-i)
        r = r | b

    if part == 1:
        return r.sum()
        ...
    elif part == 2:
        ...


def load_to_list(data):
    d = []
    for line in data.strip().split("\n"):
        d.append(list(map(int, list(line))))
    return d


if __name__ == "__main__":
    assert solution(example_data, part=1) == 21
    print(solution(read_file(), part=1))

    # assert solution(example_data, part=2) == 19
    # print(solution(read_file(), part=2))
