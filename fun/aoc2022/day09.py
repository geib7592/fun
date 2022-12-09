example_data = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
example_data2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

INPUT_FILE_PATH = "fun/aoc2022/input_files/day09_gap.txt"


DIRECTIONS = {"R": [1, 0], "U": [0, 1], "D": [0, -1], "L": [-1, 0]}


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    insts = data.strip().split("\n")

    if part == 1:
        N = 2
    elif part == 2:
        N = 10

    visited = {(0, 0)}
    X = [0] * N
    Y = [0] * N
    for instruction in insts:
        direction, amount = instruction.split(" ")
        dx, dy = DIRECTIONS[direction]
        for j in range(int(amount)):
            X[0] += dx
            Y[0] += dy
            for i in range(1, len(X)):
                X[i], Y[i] = move(X[i], Y[i], X[i - 1], Y[i - 1])
            visited.add((X[i], Y[i]))
    return len(visited)


def move(Tx, Ty, Hx, Hy):
    dx = Hx - Tx
    dy = Hy - Ty
    if dy == 0 and abs(dx) > 1:
        Tx += sign(dx)
    elif dx == 0 and abs(dy) > 1:
        Ty += sign(dy)
    elif abs(dx * dy) > 1:
        Tx += sign(dx)
        Ty += sign(dy)
    return Tx, Ty


def sign(a):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    elif a == 0:
        return 0


if __name__ == "__main__":
    assert solution(example_data, part=1) == 13
    print("Part 1: ", solution(read_file(), part=1))

    assert solution(example_data, part=2) == 1
    assert solution(example_data2, part=2) == 36
    print("Part 2: ", solution(read_file(), part=2))
