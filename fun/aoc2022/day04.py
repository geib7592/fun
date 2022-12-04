import re

INPUT_FILE_PATH = "fun/aoc2022/input_files/day04_gap.txt"


example_data = "2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    """faster version that parses the file once at the beginning"""
    data = list(map(int, re.split("-|,|\n", data)))
    s = 0
    for i in range(0, len(data), 4):
        a1, a2, b1, b2 = data[i : i + 4]
        if part == 1:
            if (a1 <= b1 <= b2 <= a2) or (b1 <= a1 <= a2 <= b2):
                s += 1
        elif part == 2:
            if (a1 <= b1 <= a2) or (b1 <= a1 <= b2):
                s += 1
    return s


def solution_old(lines_generator, part=1):
    if part == 1:
        return len(list(filter(is_full_overlap, lines_generator())))
    elif part == 2:
        return len(list(filter(is_partial_overlap, lines_generator())))


def generate_example_lines():
    for line in example_data.split("\n"):
        yield line


def generate_file_lines():
    with open(INPUT_FILE_PATH, "r") as f:
        for line in f:
            yield line


def split_line(single: str):
    """
    single is string like 2-3,4-5
    """
    a1, b, b2 = single.split("-")
    a2, b1 = b.split(",")
    return map(int, (a1, a2, b1, b2))


def is_full_overlap(single: str):
    if not single:
        return False
    a1, a2, b1, b2 = split_line(single)
    if a1 <= b1 <= b2 <= a2:
        return True
    elif b1 <= a1 <= a2 <= b2:
        return True
    return False


def is_partial_overlap(single: str):
    if not single:
        return False
    a1, a2, b1, b2 = split_line(single)
    if a1 <= b1 <= a2:
        return True
    elif b1 <= a1 <= b2:
        return True
    return False


if __name__ == "__main__":
    assert solution(example_data, part=1) == 2
    print(solution(read_file(), part=1))

    assert solution(example_data, part=2) == 4
    print(solution(read_file(), part=2))
