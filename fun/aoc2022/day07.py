example_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


INPUT_FILE_PATH = "fun/aoc2022/input_files/day07_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    fs = parse_filesystem(data.strip().split("\n"))
    ds = calc_dir_sizes(fs)

    if part == 1:
        return sum(filter(lambda x: x <= 100000, ds))

    elif part == 2:
        total_available = 70000000
        total_used = ds[0]
        space_needed = 30000000
        need_to_delete_at_least = space_needed - total_available + total_used
        for i in sorted(ds):
            if i >= need_to_delete_at_least:
                return i


def parse_filesystem(data):
    fs = {}  # filesystem
    drs = []  # list to track directories of current path
    for line in data:
        line: str
        if line.startswith("$ cd .."):
            drs.pop()

        elif line.startswith("$ cd"):
            cwd = line.split("cd")[1].strip()
            drs.append(cwd)

        elif line.startswith("$ ls"):
            continue

        elif line.startswith("dir"):
            continue

        else:
            size, fname = line.split(" ")
            a = fs
            for dname in drs:
                if dname not in a:
                    a[dname] = {}
                a = a[dname]
            a[fname] = int(size)
    return fs


def calc_dir_size(fs: dict):
    s = 0
    for v in fs.values():
        if isinstance(v, dict):
            s += calc_dir_size(v)
        elif isinstance(v, int):
            s += v
    return s


def calc_dir_sizes(fs: dict):
    ds = []
    for k, v in fs.items():
        if isinstance(v, dict):
            ds.append(calc_dir_size(v))
            ds += calc_dir_sizes(v)
    return ds


if __name__ == "__main__":
    assert solution(example_data, part=1) == 95437
    print(solution(read_file(), part=1))

    assert solution(example_data, part=2) == 24933642
    print(solution(read_file(), part=2))
