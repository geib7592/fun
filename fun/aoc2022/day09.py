from itertools import product

import numpy as np
from helpers import timeit_results

example_data = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
example_data2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

INPUT_FILE_PATH = "fun/aoc2022/input_files/day09_gap.txt"


DIRECTIONS = {"R": [1, 0], "U": [0, 1], "D": [0, -1], "L": [-1, 0]}


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    insts = data.strip().split("\n")

    Hx, Hy = (0, 0)
    Tx, Ty = (0, 0)
    if part == 1:
        been_to = set([(Tx, Ty)])
        for a in insts:
            # print(a)
            Hx, Hy, Tx, Ty, b = move(Hx, Hy, Tx, Ty, a, 0)
            # print(Hx, Hy, Tx, Ty)
            been_to.update(b)
        return len(been_to)

    elif part == 2:
        return part2(insts)


def part2(insts):
    been_to = set([(0, 0)])
    X = [0] * 10
    Y = [0] * 10
    for instruction in insts:
        # print(instruction)
        direction, amount = instruction.split(" ")
        amount = int(amount)
        d = DIRECTIONS[direction]

        for j in range(amount):
            for i in range(len(X) - 1):
                if i == 0:
                    X[i] += d[0]
                    Y[i] += d[1]

                X[i], Y[i], X[i + 1], Y[i + 1] = move(X[i], Y[i], X[i + 1], Y[i + 1])

            been_to.add(tuple([X[i + 1], Y[i + 1]]))

    l = len(been_to)
    return l


def move(Hx, Hy, Tx, Ty):
    if Hy == Ty:
        if abs(Hx - Tx) > 1:
            Tx += (Hx - Tx) // 2
    elif Hx == Tx:
        if abs(Hy - Ty) > 1:
            Ty += (Hy - Ty) // 2
    else:
        if abs(Hx - Tx) > 1:
            Tx += (Hx - Tx) // 2
            Ty += Hy - Ty
        if abs(Hy - Ty) > 1:
            Ty += (Hy - Ty) // 2
            Tx += Hx - Tx
    return Hx, Hy, Tx, Ty


if __name__ == "__main__":
    # assert solution(example_data, part=1) == 13
    # print(solution(read_file(), part=1))

    # assert solution(example_data, part=2) == 1
    assert solution(example_data2, part=2) == 36
    print(solution(read_file(), part=2))
