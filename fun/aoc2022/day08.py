from itertools import product

import numpy as np
from helpers import timeit_results

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

    if part == 1:
        for i in range(4):
            dr = np.rot90(d, i)
            m = np.diff(np.maximum.accumulate(dr, axis=1), axis=1) != 0
            m = m.astype(int)
            b = np.append(np.ones([d.shape[0], 1], int), m, axis=1)
            b = np.rot90(b, k=-i)
            r = r | b
        return r.sum()

    elif part == 2:
        # really slow, but whatever
        for i, j in product(range(1, d.shape[0] - 1), range(1, d.shape[0] - 1)):
            a1 = find_view_in_direction(reversed(d[i, : j + 1]))
            b1 = find_view_in_direction(d[i, j:])
            a2 = find_view_in_direction(reversed(d[: i + 1, j]))
            b2 = find_view_in_direction(d[i:, j])
            r[i, j] = a1 * b1 * a2 * b2
        return r.max()


def find_view_in_direction(d1d):
    a = iter(d1d)
    first = next(a)
    for i, k in enumerate(a):
        if k >= first:
            break
    return i + 1


def load_to_list(data):
    d = []
    for line in data.strip().split("\n"):
        d.append(list(map(int, list(line))))
    return d


if __name__ == "__main__":
    assert solution(example_data, part=1) == 21
    print(solution(read_file(), part=1))

    assert solution(example_data, part=2) == 8
    print(solution(read_file(), part=2))

    timeit_results(
        lambda: solution(read_file(), part=1),  # 2.5 ms
        lambda: solution(read_file(), part=2),  # 79 ms
        n=10,
    )
