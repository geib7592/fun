from itertools import product
from helpers import timeit_results
example_data = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()


INPUT_FILE_PATH = "fun/aoc2022/input_files/day14_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    rocks = set()
    for line in data.strip().split("\n"):
        rocks = rocks | read_line(line)

    sand = get_points(rocks, part=part)
    # display(sand, rocks)
    return len(sand)


def get_points(rocks: set, part=1):
    points = rocks.copy()
    maxy = max(p[1] for p in rocks)
    y_floor = maxy + 1
    pstart = (500, 0)
    x, y = pstart
    while True:
        if part == 1 and y == maxy:
            break
        elif part == 2 and y == y_floor:
            points.add((x, y))
            x, y = pstart
        elif (x, y + 1) not in points:
            y += 1
        elif (x - 1, y + 1) not in points:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in points:
            x += 1
            y += 1
        else:
            points.add((x, y))
            if part == 2 and y == 0:
                break
            x, y = pstart

    return points - rocks


def read_line(line: str):
    points = set()
    parts = line.split("->")
    for i, p in enumerate(parts[:-1]):
        x1, y1 = tuple(map(int, p.split(",")))
        x2, y2 = tuple(map(int, parts[i + 1].split(",")))

        xr = range(min([x1, x2]), max([x1, x2]) + 1)
        yr = range(min([y1, y2]), max([y1, y2]) + 1)
        for x, y in product(xr, yr):
            points.add((x, y))

    return points


def display(sand, rocks):
    points = sand | rocks
    maxy = max(p[1] for p in points)
    maxx = max(p[0] for p in points)
    minx = min(p[0] for p in points)
    s = ""
    for y in range(maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) in rocks:
                s += "#"
            elif (x, y) in sand:
                s += "o"
            else:
                s += "."
        s += "\n"
    print(s)
    return s


if __name__ == "__main__":
    assert solution(example_data, part=1) == 24
    print("Part 1: ", solution(read_file(), part=1))

    assert solution(example_data, part=2) == 93
    print("Part 2: ", solution(read_file(), part=2))

    timeit_results(
        lambda: solution(read_file(), part=1), # 30 ms
        lambda: solution(read_file(), part=2), # 0.8 s
        n=5
    )