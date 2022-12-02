from itertools import product
from pathlib import Path
from timeit import timeit

import pandas as pd

INPUT_FILE_PATH = Path("fun/aoc2022/input_files/day02_gap.txt")

example_data = """A Y\nB X\nC Z\n"""


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read()


def part1():
    return solution_part1(read_file())


def part2():
    return solution_part2(read_file())


def solution_part1(data: str):
    m = get_score_map(get_score_part_1)
    rounds = data.strip().split("\n")
    return sum(m[i] for i in rounds)


def solution_part2(data: str):
    m = get_score_map(get_score_part_2)
    rounds = data.strip().split("\n")
    return sum(m[i] for i in rounds)


def get_score_map(score_func) -> dict:
    """
    calculate all the possibilities once
    """
    score_map = {}
    for i, j in product("ABC", "XYZ"):
        s = f"{i} {j}"
        score_map[s] = score_func(s)
    return score_map


def get_score_part_1(s: str) -> int:
    a = ord(s[0]) - 65
    select_score = ord(s[2]) - 87
    win_score = 3 * ((select_score - a) % 3)
    return select_score + win_score


def get_score_part_2(s: str) -> int:
    a = ord(s[0]) - 65
    select_score = 1 + dict(X=(a - 1) % 3, Y=a, Z=(a + 1) % 3)[s[2]]
    win_score = dict(X=0, Y=3, Z=6)[s[2]]
    return select_score + win_score


def part1_pandas():
    df = pd.read_csv(INPUT_FILE_PATH, header=None, delimiter=" ")
    df["a"] = df[0].apply(ord) - 65
    df["b"] = df[1].apply(ord) - 88
    df["win"] = (df.b - df.a + 1) % 3 - 1
    df["win_score"] = (df.win + 1) * 3
    df["select_score"] = df.b + 1
    df["score"] = df.win_score + df.select_score
    return df.score.sum()


def timeit_results():
    for func in [part1, part2, part1_pandas]:
        n = 1000
        time = timeit(func, number=n) / n
        print(f"{func.__name__}, {time:.3e} s")


if __name__ == "__main__":
    assert solution_part1(example_data) == 15
    assert solution_part2(example_data) == 12

    print(part1())
    print(part2())

    timeit_results()
    # timing results:
    # part1, 1.527e-03 s
    # part2, 1.444e-03 s
    # part1_pandas, 7.737e-03 s
