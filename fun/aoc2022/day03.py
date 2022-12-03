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
        return sum(get_score(get_common_types(bags)))
    elif part == 2:
        return sum(get_score(get_common_part2(bags)))


def get_common_types(bags):
    for bag in bags:
        slot1 = set(bag[: len(bag) // 2])
        slot2 = set(bag[len(bag) // 2 :])
        yield from slot1 & slot2


def get_common_part2(bags):
    for i in range(0, len(bags), 3):
        group = bags[i : i + 3]
        yield from set(group[0]).intersection(*group[1:])


def get_score(common_types):
    for t in common_types:
        if ord(t) <= ord("Z"):
            yield ord(t) - ord("A") + 27
        else:
            yield ord(t) - ord("a") + 1


if __name__ == "__main__":
    assert solution(example_data, part=1) == 157
    print(solution(read_file(), part=1))

    assert solution(example_data, part=2) == 70
    print(solution(read_file(), part=2))
