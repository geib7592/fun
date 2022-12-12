from collections import defaultdict
from math import lcm

example_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

INPUT_FILE_PATH = "fun/aoc2022/input_files/day12_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    return


if __name__ == "__main__":
    assert solution(example_data, part=1) == 31
    print("Part 1: ", solution(read_file(), part=1))

    # assert solution(example_data, part=2) == 2713310158
    # print("Part 2: ", solution(read_file(), part=2))
