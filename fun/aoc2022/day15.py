from itertools import product, combinations, permutations
from functools import reduce
from helpers import timeit_results
import re
import numpy as np

example_data = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip()


INPUT_FILE_PATH = "fun/aoc2022/input_files/day15_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1, y_check=10, yrange=20):
    data_parsed = read_input(data)
    if part == 1:
        e, beacons = get_excluded_x(data_parsed, y_check=y_check)
        excluded = set()
        excluded = excluded.union(*[list(i) for i in e])
        r = len(excluded - beacons)
        return r
    elif part == 2:
        x, y = part2_loop(data_parsed, yrange)
        r = x * 4000000 + y
        return r


def part2_loop(data, yrange):
    for y_check in range(yrange + 1):
        e, b = get_excluded_x(data, y_check)

        x = find_non_overlap(e)
        if x <= yrange:
            return x, y_check

        if y_check % 100_000 == 0:
            print(y_check)

        if y_check == 50000:
            return 100, 500

        # a = np.zeros(yrange + 1, dtype=bool)
        # for r in e:
        #     a = a | ((r[0] <= xarr) & (xarr <= r[-1]))

        # if not a.all():
        #     x = np.where(a == False)[0][0]
        #     return x, y_check

        # if not all(any(i in r for r in e) for i in range(yrange+1)):
        #     a = [any(i in r for r in e) for i in range(yrange+1)]
        #     x = a.index(False)
        #     return x, y_check
        # if len(rr) == 1:
        #     r = rr[0]
        #     if not (r[0] <= 0 and r[-1] >= yrange):
        #         return rr, y_check
        # elif len(rr) == 2:
        #     return rr[0][-1] + 1, y_check

def find_non_overlap(ranges: list[range]):
    rs = sorted(ranges, key=lambda i: i.start)
    x = 0
    for r in rs:
        if r.start <= x < r.stop:
            x = r.stop
    return x

def reduce_ranges3(ranges: list):
    r_new = list()
    c = False
    for r1, r2 in combinations(ranges, 2):
        if range_touching(r1, r2):
            r_new.append(combine_range(r1, r2))
            c = True
        else:
            r_new.append(r1)
            r_new.append(r2)
    if c:
        return reduce_ranges(r_new)
    else:
        return r_new


def reduce_ranges(r1, r2):
    if isinstance(r1, list):
        l = []
        for r in r1:
            ra = reduce_ranges(r, r2)
            if isinstance(ra, list):
                l += ra
            else:
                l.append(ra)
        return sorted(l, key=lambda i: i[0])

    if range_touching(r1, r2):
        return combine_range(r1, r2)
    else:
        return sorted([r1, r2], key=lambda i: i[0])


def reduce_ranges2(ranges: list):
    pairs = list(combinations(ranges, 2))
    can_reduce = [range_touching(r1, r2) for r1, r2 in pairs]
    if True not in can_reduce:
        return ranges
    i = can_reduce.index(True)
    r1, r2 = pairs[i]
    rc = combine_range(r1, r2)
    r = set(ranges)
    r.remove(r1)
    r.remove(r2)
    r.add(rc)
    r = sorted(list(r), key=lambda i: i[0])
    return reduce_ranges(r)


def read_input(data: str):
    data_parsed = []
    for line in data.strip().split("\n"):
        data_parsed.append(read_line(line))
    return data_parsed


def get_excluded_x(data: list, y_check=10):
    excluded = []
    beacons = set()
    for sx, sy, bx, by in data:
        if by == y_check:
            beacons.add(bx)
        d = distance(sx, sy, bx, by)
        dd = d - abs(sy - y_check)
        if dd >= 0:
            excluded.append(range(sx - dd, sx + dd + 1))
    return excluded, beacons


def range_touching(r1, r2):
    if r1.stop() < r2.start or r2.stop < r1.start:
        return False
    else:
        return True


def combine_range(r1:range, r2:range):
    return range(min(r1.start, r2.start), max(r1.stop, r2.stop) )


def read_line(line: str):
    a = re.findall(r"(\w+)=(\d+|-\d+)", line)
    return tuple(int(i[1]) for i in a)


def distance(sx, sy, bx, by):
    return abs(by - sy) + abs(bx - sx)


if __name__ == "__main__":
    # assert solution(example_data, part=1, y_check=10) == 26
    # print("Part 1: ", solution(read_file(), part=1, y_check=2000000))

    assert solution(example_data, part=2) == 56000011
    print("Part 2: ", solution(read_file(), part=2, yrange=4000000))
    # 13784551204480

    # timeit_results(
    #     lambda: solution(read_file(), part=1), # 30 ms
    #     lambda: solution(read_file(), part=2), # 0.8 s
    #     n=5
    # )
