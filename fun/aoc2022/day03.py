INPUT_FILE_PATH = "fun/aoc2022/input_files/day03_gap.txt"

example_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read()


def solution(data: str, part=1):
    bags = data.strip().split("\n")
    if part == 1:
        s = get_score(get_common_types(bags))
    elif part == 2:
        s = get_score(get_common_part2(bags))
    return s


def get_common_types(bags):
    common = []
    for bag in bags:
        slot1 = set(bag[: len(bag) // 2])
        slot2 = set(bag[len(bag) // 2 :])
        common += list(slot1 & slot2)
    return common


def get_score(common_types):
    s = 0
    for t in common_types:
        if ord(t) <= ord("Z"):
            s += ord(t) - ord("A") + 27
        else:
            s += ord(t) - ord("a") + 1
    return s


def get_common_part2(bags):
    common = []
    n = len(bags)
    for i in range(0, n, 3):
        group = bags[i : i + 3]
        c = set(group[0]) & set(group[1]) & set(group[2])
        common.append(c.pop())
    return common


assert solution(example_data, part=1) == 157
print(solution(read_file(), part=1))

assert solution(example_data, part=2) == 70
print(solution(read_file(), part=2))
