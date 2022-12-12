example_data = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

INPUT_FILE_PATH = "fun/aoc2022/input_files/day10_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    lines = data.strip().split("\n")
    v = 1
    X = []
    crt = ""
    for line in lines:
        if line.startswith("noop"):
            crt += update_crt(X, v)
            X.append(v)

        elif line.startswith("addx"):
            m = int(line.split(" ")[1])
            for i in range(2):
                crt += update_crt(X, v)
                X.append(v)
            v += m

    s = [i * X[i - 1] for i in [20, 60, 100, 140, 180, 220]]

    display(crt)
    return sum(s)


def display(crt, N=40):
    print("\n")
    for i in range(len(crt) // N):
        print(crt[i * N : N * i + N])


def update_crt(X, v, N=40):
    if v - 1 <= len(X) % N <= v + 1:
        return "▓"
    else:
        return " "


if __name__ == "__main__":
    assert solution(example_data, part=1) == 13140
    print("Part 1: ", solution(read_file(), part=1))
