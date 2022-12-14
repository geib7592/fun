import json
from functools import cmp_to_key
from math import prod

example_data = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]

""".strip()


INPUT_FILE_PATH = "fun/aoc2022/input_files/day13_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    if part == 1:
        pairs = data.split("\n\n")
        r = {}
        for i, pair in enumerate(pairs):
            L1, L2 = list(map(json.loads, pair.split("\n")))
            n = check_order(L1, L2)
            r[i + 1] = n
        return sum([k for k, v in r.items() if v == 1])

    if part == 2:
        lines = data.replace("\n\n", "\n").split("\n")
        lines = list(map(json.loads, lines))
        dividers = [[[2]], [[6]]]
        lines += dividers
        s = sorted(lines, key=cmp_to_key(check_order), reverse=True)
        return prod(s.index(i) + 1 for i in dividers)


def check_order(L1, L2):
    """
    Return: 
        1 for correct order
        0 for tie
        -1 for incorrect order
    """
    l1 = iter(L1)
    l2 = iter(L2)

    lstop = False
    rstop = False
    try:
        left = next(l1)
    except StopIteration:
        lstop = True
    try:
        right = next(l2)
    except StopIteration:
        rstop = True

    if lstop and not rstop:
        return 1
    elif lstop and rstop:
        return 0
    elif rstop and not lstop:
        return -1

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif right < left:
            return -1
        elif right == left:
            return check_order(l1, l2)

    elif isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]

    val = check_order(left, right)
    if val != 0:
        return val
    else:
        return check_order(l1, l2)


if __name__ == "__main__":
    assert solution(example_data, part=1) == 13
    print("Part 1: ", solution(read_file(), part=1))

    assert solution(example_data, part=2) == 140
    print("Part 2: ", solution(read_file(), part=2))
