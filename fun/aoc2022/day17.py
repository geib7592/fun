from itertools import product, repeat, cycle
import re
from helpers import timeit_results
import numpy as np
import scipy.sparse as ss
from math import sin, cos, pi, atan2
import sys, os

example_data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

rocks = {
    "-": ((0, 1, 2, 3), (0, 0, 0, 0)),
    "+": ((0, 1, 1, 1, 2), (1, 0, 1, 2, 1)),
    "L": ((0, 1, 2, 2, 2), (0, 0, 0, 1, 2)),
    "I": ((0, 0, 0, 0), (0, 1, 2, 3)),
    "o": ((0, 0, 1, 1), (0, 1, 0, 1)),
}

INPUT_FILE_PATH = "fun/aoc2022/input_files/day17_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    if part == 1:
        Nrocks = 2022
    else:
        Nrocks = 1_000_000_000_000
    height = 0
    time = 0
    rock_gen = cycle(rocks.values())
    wind_gen = cycle(data)

    X = list(range(7))
    Y = [0] * 7
    points = {(X[i], Y[i]) for i in range(7)}
    x, y = next(rock_gen)
    rpoints = {(x[i] + 2, y[i] + height + 4) for i in range(len(y))}
    rock_number = 1

    while rock_number <= Nrocks:
        wind = next(wind_gen)
        blown = blow_rock(rpoints, wind)
        if not any(d in points for d in blown):
            rpoints = blown

        dropped = {(p[0], p[1] - 1) for p in rpoints}

        if any(d in points for d in dropped):
            points = points | rpoints
            points = get_top_points(points)

            y_max = max(p[1] for p in points)
            points = {(p[0], p[1] - y_max) for p in points}
            height += y_max

            x, y = next(rock_gen)
            rpoints = {(x[i] + 2, y[i] + height + 4) for i in range(len(y))}
            rock_number += 1
            if rock_number % 1000 ==0:
                print(rock_number)
        else:
            rpoints = dropped

    return height


def show(points):
    x = 0
    y_max = max(p[1] for p in points)
    y_min = min(p[1] for p in points)
    y = y_min
    s = ""
    while y <= y_max:
        if (x, y) in points:
            s += "#"
        else:
            s += "."

        if x == 6:
            x = 0
            y += 1
            s += "\n"
        else:
            x += 1
    s = reversed(s.split('\n'))
    for i in s:
        print(i)


def blow_rock(points, wind):
    x = [p[0] for p in points]
    if wind == "<":
        if min(x) == 0:
            return points
        else:
            return {(p[0] - 1, p[1]) for p in points}
    elif wind == ">":
        if max(x) == 6:
            return points
        else:
            return {(p[0] + 1, p[1]) for p in points}


def get_top_points(points):
    # start at top left, then flood fill
    y_max = max(p[1] for p in points)
    y_min = min(p[1] for p in points)

    visible = set()
    next_up = [(0, y_max + 1)]

    while next_up:
        point = next_up.pop()
        if point in points:
            continue
        elif point in visible:
            continue
        elif point[0] < 0 or point[0] > 6 or point[1] < y_min or point[1] > y_max + 1:
            continue

        visible.add(point)
        next_up += list(generate_adjacent(point))

    new_points = {p for p in points if any(i in visible for i in generate_adjacent(p))}

    # os.system('clear')
    # show(new_points)
    return new_points



def generate_adjacent(point):
    for s in [1, -1]:
        yield point[0] + s, point[1]
        yield point[0], point[1] + s


def rot45(p, s=1):
    return (round(sin(atan2(*p) + s * pi / 4)), round(cos(atan2(*p) + s * pi / 4)))


def vec_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


if __name__ == "__main__":
    assert solution(example_data, part=1) == 3068
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
