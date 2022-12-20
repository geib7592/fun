
example_data = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip()


INPUT_FILE_PATH = "fun/aoc2022/input_files/day18_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    lines = data.split()
    points = set(map(line2tuple, lines))

    if part == 1:
        return surface_area(points)

    if part == 2:
        seen_from_outside = flood_fill(points)
        sa = 0
        for p in points:
            sa += len((set(generate_adjacent(p)) - points) & seen_from_outside)

        return sa


def line2tuple(line):
    return tuple(map(int, line.split(",")))


def surface_area(points):
    return sum(len(set(generate_adjacent(p)) - points) for p in points)


def flood_fill(points):
    visible = set()
    next_up = [(0, 0, 0)]
    while next_up:
        point = next_up.pop()

        if point in points:
            continue
        elif point in visible:
            continue
        elif isoutside(point, points):
            continue

        visible.add(point)
        next_up += list(generate_adjacent(point))

    return visible


def isoutside(point, points):
    for i, p in enumerate(point):
        if -1 <= p <= 25:
            pass
        else:
            return True
    return False


def generate_adjacent(p):
    for s in [1, -1]:
        yield (p[0] + s, p[1], p[2])
        yield (p[0], p[1] + s, p[2])
        yield (p[0], p[1], p[2] + s)


if __name__ == "__main__":
    assert solution(example_data, part=1) == 64
    print("Part 1: ", solution(read_file(), part=1))

    assert solution(example_data, part=2) == 58
    print("Part 2: ", solution(read_file(), part=2))

    # timeit_results(
    #     lambda: solution(read_file(), part=1), # 30 ms
    #     lambda: solution(read_file(), part=2), # 0.8 s
    #     n=5
    # )
