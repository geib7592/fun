from itertools import product
import re
from helpers import timeit_results
import numpy as np
import scipy.sparse as ss

example_data = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip()


INPUT_FILE_PATH = "fun/aoc2022/input_files/day16_gap.txt"


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()

def parse_input(data:str):
    p = []
    data = data.replace(',', '')
    for line in data.split('\n'):
        a = line.split(' ')[1]
        r = int(line.split('=')[1].split(';')[0])
        b = line.split(' to ')[1]
        b = b.split(' ')[1:]
        p.append( (a, r, b))
    return p

def make_graph(p:list):
    nodes = [i[0] for i in p]
    flows = [i[1] for i in p]
    g = np.zeros([len(nodes), len(nodes)], dtype=int)
    for i, row in enumerate(p):
        g[i,i]=row[1]
        for n in row[2]:
            idx = nodes.index(n)
            g[i, idx] = 1

    return nodes, g

def solution(data: str, part=1):
    p = parse_input(data)
    nodes, g = make_graph(p)
    graph = ss.csr_matrix(g)
    sp, pred = ss.csgraph.shortest_path(graph, return_predecessors=True)
    DFSG = ss.csgraph.depth_first_tree( graph, 0, directed=False)
    DFSO = ss.csgraph.depth_first_order(graph, 0, directed=False)
    p = [nodes[i] for i in DFSO[0]]
    print(p)

    time_left = 30
    

    return 


if __name__ == "__main__":
    assert solution(example_data, part=1) == 24
    print("Part 1: ", solution(read_file(), part=1))

    assert solution(example_data, part=2) == 93
    print("Part 2: ", solution(read_file(), part=2))

    timeit_results(
        lambda: solution(read_file(), part=1), # 30 ms
        lambda: solution(read_file(), part=2), # 0.8 s
        n=5
    )