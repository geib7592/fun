example_data = """
1
2
-3
3
-2
0
4
""".strip()

INPUT_FILE_PATH = "fun/aoc2022/input_files/day19_gap.txt"
KEY = 811589153


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    init_data = list(map(int, data.split()))

    Nloops = 1
    if part == 2:
        init_data = [KEY * i for i in init_data]
        Nloops = 10

    # 'indices' is a map from original position to new position.
    # original position is index, new position is value
    indices = list(range(len(init_data)))
    N = len(init_data)

    for n in range(Nloops):
        for i in range(N):
            moveby = init_data[i]
            idx = indices.index(i)
            v = indices.pop(idx)
            ins = idx + moveby  # where to insert
            if ins == 0 and moveby != 0:
                # not sure why, but in this case, put at end, not beginning
                indices.append(v)
            else:
                indices.insert(ins % (N - 1), v)

    new_data = [init_data[i] for i in indices]
    zero_idx = new_data.index(0)
    s = sum(new_data[(zero_idx + i) % N] for i in [1000, 2000, 3000])
    return s


if __name__ == "__main__":
    assert solution(example_data, part=1) == 3
    print("Part 1: ")
    print(solution(read_file(), part=1))  # 0.1 s

    assert solution(example_data, part=2) == 1623178306
    print("Part 2: ")
    print(solution(read_file(), part=2))  # 1.5 s

