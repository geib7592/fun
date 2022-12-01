from pathlib import Path
from timeit import timeit

import pandas as pd

INPUT_FILE_PATH = Path("fun/aoc2022/input_files/day1.txt")


def day1_part1():
    with open(INPUT_FILE_PATH, "r") as f:
        group_sum = 0
        max_sum = 0
        for line in f:
            if line == "\n":
                if group_sum > max_sum:
                    max_sum = group_sum
                group_sum = 0
            else:
                group_sum += int(line)
    return max_sum


def day1_part2():
    with open(INPUT_FILE_PATH, "r") as f:
        group_sum = 0
        group_sums = []
        for line in f:
            if line == "\n":
                group_sums.append(group_sum)
                group_sum = 0
            else:
                group_sum += int(line)
    gs = reversed(sorted(group_sums))
    return sum(next(gs) for _ in range(3))


def day1_part1_pandas():
    df = pd.read_csv(INPUT_FILE_PATH, skip_blank_lines=False, header=None)
    df["groups"] = df.isnull().cumsum()
    return int(df.groupby("groups").sum().max())


def day1_part2_pandas():
    df = pd.read_csv(INPUT_FILE_PATH, skip_blank_lines=False, header=None)
    df["groups"] = df.isnull().cumsum()
    dfg = df.groupby("groups").sum()
    return int(dfg.sort_values(0).tail(3).sum())


def timeit_results():
    for func in [day1_part1, day1_part1_pandas, day1_part2, day1_part2_pandas]:
        n = 100
        time = timeit(func, number=n) / n
        print(f"{func.__name__}, {time:.3e} s")


if __name__ == "__main__":
    timeit(day1_part2_pandas, number=1000)
