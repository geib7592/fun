import re

INPUT_FILE_PATH = "fun/aoc2022/input_files/day05_gap.txt"


example_data = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def get_initial_state(data):
    s = re.split("[0-9]", data, maxsplit=1)[0]
    a = s.split("\n")
    b = [i[1::4] for i in a]
    state = []
    for row in reversed(b):
        if not b:
            continue

        if len(state) == 0:
            for i in row:
                state.append([])

        for i, el in enumerate(row):
            if el.strip():
                state[i].append(el)

    return state


def parse_instructions(data):
    s = re.split("move | from | to ", data)[1:]
    m = map(int, s)
    while True:
        try:
            yield next(m), next(m), next(m)
        except StopIteration:
            break


def solution(data: str, part=1):
    state = get_initial_state(data)
    for inst in parse_instructions(data):
        if part == 1:
            for num in range(inst[0]):
                state[inst[2] - 1].append(state[inst[1] - 1].pop())
        elif part == 2:
            state[inst[2] - 1] += state[inst[1] - 1][-inst[0] :]
            state[inst[1] - 1] = state[inst[1] - 1][: -inst[0]]

    s = ""
    for stack in state:
        s += stack.pop()
    return s


if __name__ == "__main__":

    assert solution(example_data, part=1) == "CMZ"
    print(solution(read_file(), part=1))

    assert solution(example_data, part=2) == "MCD"
    print(solution(read_file(), part=2))
