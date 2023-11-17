from itertools import product
import re
from helpers import timeit_results
import numpy as np
import scipy.sparse as ss
from ast import literal_eval
import operator
from string import ascii_uppercase

example_data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""


# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)

INPUT_FILE_PATH = "fun/aoc2022/input_files/day22_gap.txt"

DIR = '>v<^'

def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read()


def parse_input(data: str):
    mappa, inst = data.split("\n\n")
    numbers = list(map(int, re.split("[A-Z]", inst)))
    directions = "".join(re.split("[0-9]", inst)).strip()
    mappa = [list(i) for i in mappa.split("\n")]
    max_len = max(len(row) for row in mappa)
    for i, row in enumerate(mappa):
        if len(row) < max_len:
            row += [' '] * (max_len - len(row))
    return mappa , numbers, directions


def solution(data: str, part=1):
    mappa, numbers, directions = parse_input(data)
    row = 0
    col = mappa[row].index(".")
    facing = 0
    walks = iter(numbers)
    turns = iter(directions)
    while True:
        try:
            w = next(walks)
        except:
            break
        for i in range(w):
            mappa[row][col] = DIR[facing]
            row, col, stuck = step(row, col, facing, mappa)
            if stuck:
                break

        try:
            t = next(turns)
        except:
            break
        facing = (facing + {"L": -1, "R": 1}[t]) % 4

    r =1000 * (row+1) + 4 * (col+1) + facing
    return r


def step(row, col, facing, mappa):
    dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][facing]
    r_new = (row + dy) % len(mappa)
    c_new = (col + dx) % len(mappa[r_new])
    if mappa[r_new][c_new] in DIR+".":
        return r_new, c_new, False
    elif mappa[r_new][c_new] == "#":
        return row, col, True
    elif mappa[r_new][c_new] == " ":
        r, c, stuck =  step(r_new, c_new, facing, mappa)
        if stuck:
            return row, col, stuck
        else:
            return r, c, stuck

    return

def show(mappa):
    print('\n'.join([''.join(i for i in j) for j in mappa]))

if __name__ == "__main__":
    # assert solution(example_data, part=1) == 6032
    print("Part 1: ", solution(read_file(), part=1))

    # assert solution(example_data, part=1) == 152
    # print("Part 1: ", solution(read_file(), part=1))
