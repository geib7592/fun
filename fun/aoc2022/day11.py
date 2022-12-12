from collections import defaultdict
from math import lcm

example_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

INPUT_FILE_PATH = "fun/aoc2022/input_files/day11_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


class Monkey:
    def __init__(self, input_data, divisor=3):
        self.input_data = input_data
        self.parse_input()
        self.inspect_count = 0
        self.divisor = divisor

    def parse_input(self):
        for line in self.input_data.strip().split("\n"):
            line: str = line.strip()
            if line.startswith("Monkey"):
                n = int(line.split(" ")[1].split(":")[0])
                self.n = n
            elif line.startswith("Starting"):
                items = line.split(": ")[1]
                self.items = list(map(int, items.split(",")))
            elif line.startswith("Operation"):
                op = line.split("=")[1]
                self.operation = lambda old: eval(op)
            elif line.startswith("Test"):
                self.divisible = int(line.split("by")[1])
            elif line.startswith("If true"):
                self.if_true = int(line.split("monkey")[1])
            elif line.startswith("If false"):
                self.if_false = int(line.split("monkey")[1])

    def inspect(self):
        new_items = []
        for i, item in enumerate(self.items):
            self.inspect_count += 1
            worry_level = self.operation(item) // self.divisor
            new_items.append(worry_level)
        self.items = new_items

    def throw(self):
        throw = defaultdict(list)
        for item in self.items:
            if item % self.divisible == 0:
                throw[self.if_true].append(item)
            else:
                throw[self.if_false].append(item)
        self.items = []
        return throw

    def catch(self, items: list):
        self.items += items


def solution(data: str, part=1):
    inputs = data.split("\n\n")
    monkeys = []
    for i in inputs:
        divisor = 3 if part == 1 else 1
        monkeys.append(Monkey(i, divisor=divisor))

    LCM = lcm(*[m.divisible for m in monkeys])

    N = 20 if part == 1 else 10000
    for round in range(N):
        for monkey in monkeys:
            monkey: Monkey
            monkey.inspect()
            thrown = monkey.throw()
            for m, item in thrown.items():
                monkeys[m].catch([i % LCM for i in item])

    inspect_counts = [m.inspect_count for m in monkeys]
    return sorted(inspect_counts)[-2] * sorted(inspect_counts)[-1]


if __name__ == "__main__":
    assert solution(example_data, part=1) == 10605
    print("Part 1: ", solution(read_file(), part=1))

    assert solution(example_data, part=2) == 2713310158
    print("Part 2: ", solution(read_file(), part=2))
