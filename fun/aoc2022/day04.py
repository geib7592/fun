INPUT_FILE_PATH = "fun/aoc2022/input_files/day04_gap.txt"


def generate_example_lines():
    example_data = "2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8"
    for line in example_data.split("\n"):
        yield line


def generate_file_lines():
    with open(INPUT_FILE_PATH, "r") as f:
        for line in f:
            yield line


def solution(lines_generator, part=1):
    if part == 1:
        return len(list(filter(is_full_overlap, lines_generator())))
    elif part == 2:
        return len(list(filter(is_partial_overlap, lines_generator())))


def split_line(single: str):
    a, b = single.split(",")
    a1, a2 = map(int, a.split("-"))
    b1, b2 = map(int, b.split("-"))
    return a1, a2, b1, b2


def is_full_overlap(single: str):
    """
    single is string like 2-3,4-5
    """
    if not single:
        return False
    a1, a2, b1, b2 = split_line(single)
    if a1 <= b1 <= b2 <= a2:
        return True
    elif b1 <= a1 <= a2 <= b2:
        return True
    return False


def is_partial_overlap(single: str):
    """
    single is string like 2-3,4-5
    """
    if not single:
        return False
    a1, a2, b1, b2 = split_line(single)
    if a1 <= b1 <= a2:
        return True
    elif b1 <= a1 <= b2:
        return True
    return False


if __name__ == "__main__":
    assert solution(generate_example_lines, part=1) == 2
    print(solution(generate_file_lines, part=1))

    assert solution(generate_example_lines, part=2) == 4
    print(solution(generate_file_lines, part=2))
