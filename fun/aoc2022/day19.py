from itertools import product, repeat, cycle
import re
from helpers import timeit_results
import numpy as np
import scipy.sparse as ss
from math import sin, cos, pi, atan2
import sys, os

example_data = """
1
2
-3
3
-2
0
4
""".strip()


INPUT_FILE_PATH = "fun/aoc2022/input_files/day19_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution1(data: str, part=1):
    init_data = list(map(int, data.split()))
    {i: init_data[i] for i in range(len(init_data))}

    indices = list(range(len(init_data)))
    N = len(init_data)
    for i in range(len(init_data)):
        moveby = init_data[i]
        indices_copy = indices.copy()
        indices[i] = (indices[i] + moveby) % N
        change_idx = list(range(abs(moveby)))
        for j in change_idx:
            # change all indicies between indicies_copy[i] and indicies[i]
            idx = (indices_copy[i] + sign(moveby) * (j + 1)) % N
            idx2 = indices_copy.index(idx)
            indices[idx2] = (indices_copy[idx2] - sign(moveby)) % N

        new_list = [init_data[k] for k in indices]

        print(indices)
    return


def solution(data: str, part=1):
    init_data = list(map(int, data.split()))
    d = {i: init_data[i] for i in range(len(init_data))}

    indices = list(range(len(init_data)))
    N = len(init_data)
    l = init_data.copy()
    for i in range(len(init_data)):
        moveby = init_data[i]
        indices_copy = indices.copy()
        idx = indices_copy.index(i)
        v = indices.pop(idx)
        indices.insert((idx + moveby) % N, v)
    return


def sign(a):
    if a > 0:
        return 1
    else:
        return -1


if __name__ == "__main__":
    assert solution(example_data, part=1) == 3
    print("Part 1: ")
    print(solution(read_file(), part=1))

    assert solution(example_data, part=2) == 1514285714288
    print("Part 2: ")
    print(solution(read_file(), part=2))

    # timeit_results(
    #     lambda: solution(read_file(), part=1), # 30 ms
    #     lambda: solution(read_file(), part=2), # 0.8 s
    #     n=5
    # )
