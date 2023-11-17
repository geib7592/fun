from itertools import product
import re
from helpers import timeit_results
import numpy as np
import scipy.sparse as ss
from ast import literal_eval
import operator
from pprint import pprint
from string import digits

example_data = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip()

operators = {
    "*": operator.mul,
    "+": operator.add,
    "-": operator.sub,
    "/": operator.floordiv,
}

INPUT_FILE_PATH = "fun/aoc2022/input_files/day21_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1, method=1):
    lines = data.split("\n")
    data: dict = {}
    for line in lines:
        a, b = line.split(": ")
        data[a] = b
    if part == 1:
        if method == 1:
            return evaluate(data, "root")
        elif method ==2:
            data['root'] = data.pop('root')  # put root at end
            d = simplify(data)
            return eval(d['root'].replace('/', '//'))


    a, op, b = data.pop("root").split()
    data[a] = b
    data.pop("humn")

    data_new = invert(data, "humn")

    return evaluate(data_new, "humn")

count=0
def invert(data: dict, name: str):
    pprint(simplify(data), sort_dicts=False)
    global count
    dnew = {}
    done = False
    for k, v in data.items():
        if name not in v or done:
            dnew[k] = v
            continue
        
        done = True
        if k == 'humn':
            a = 1

        knext = k
        a, op, b = v.split()
        c = a if b == name else b
        if op == "+":
            new = f"{k} - {c}"
        elif op == "*":
            new = f"{k} / {c}"
        elif op == "-":
            if b == name:
                new = f"{c} - {k}"
            else:
                new = f"{c} + {k}"
        elif op == "/":
            if b == name:
                new = f"{c} / {k}"
            else:
                new = f"{c} * {k}"
    
    dnew[name] = new
    count += 1
    # return dnew
    return invert(dnew, knext)

def simplify(data:dict):
    d = data.copy()
    while len(d) > 1:
        d2 = {}
        key = next(iter(d))
        value = d.pop(key)
        for k, v in d.items():
            if key not in v:
                d2[k] = v
            else:
                d2[k] = v.replace(key, f"({value})")

        d = d2
    return d

def simplify2(data:dict):
    d = data.copy()
    while len(list(filter(only_digits, d.values()))) > 0:
        d2 = d.copy()
        for k, v in d.items():
            if only_digits(v):
                d2.pop(k)
                for k2, v2 in d.items():
                    if k in v2:
                        d2[k2] = v2.replace(k, v)
        d = d2
        pprint(d)    
    return d
                

def only_digits(s):
    return len(set(s) - set(digits)) == 0

# def evaluate_func(data, name):
#     expression = data[name]
#     if name == 'humn':
#         return lambda humn: humn
#     try:
#         int(expression)
#         return lambda: int(expression)
#     except ValueError:
#         a, op, b = expression.split()
#         return lambda humn: operators[op](evaluate(data, a), evaluate(data, b))


def evaluate(data, name):
    expression = data[name]
    try:
        return int(expression)
    except ValueError:
        a, op, b = expression.split()
        return operators[op](evaluate(data, a), evaluate(data, b))


if __name__ == "__main__":
    assert solution(example_data, part=1) == 152
    print("Part 1: ", solution(read_file(), part=1))

    assert solution(example_data, part=2) == 301
    print("Part 2: ", solution(read_file(), part=2))

    timeit_results(
        lambda: solution(read_file(), part=1),
        lambda: solution(read_file(), part=2),
        n=5,
    )
