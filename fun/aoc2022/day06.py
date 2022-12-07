example_data = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
INPUT_FILE_PATH = "fun/aoc2022/input_files/day06_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    if part == 1:
        # marker size
        m_size = 4
    elif part == 2:
        m_size = 14

    for i in range(len(data) - m_size):
        s = data[i : i + m_size]
        if len(set(s)) == m_size:
            return i + m_size
    return len(data)


if __name__ == "__main__":
    assert solution(example_data, part=1) == 7
    print(solution(read_file(), part=1))

    assert solution(example_data, part=2) == 19
    print(solution(read_file(), part=2))
