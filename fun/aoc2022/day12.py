from math import inf
import re
import numpy as np
from scipy.sparse.csgraph import shortest_path

example_data = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()


INPUT_FILE_PATH = "fun/aoc2022/input_files/day12_gap.txt"


class S:
    def __init__(self, data: str):
        self.input_data = data
        self.len_y = data.count("\n") + 1
        self.s: str = data.replace("\n", "")
        self.len_x = len(self.s) // self.len_y
        self.i_start = self.s.find("S")
        self.i_end = self.s.find("E")
        self.s = self.s.replace("S", "a")
        self.s = self.s.replace("E", "z")

    def dijkstra(self):
        self.dist = [inf] * len(self.s)
        self.prev = [None] * len(self.s)
        self.dist[self.i_start] = 0
        self.Q = set(range(len(self.s)))

        while self.Q:
            u = self.get_vertex_min_dist()
            if u is None:
                return
            self.Q.remove(u)

            for v in self.get_accessible_neighbors(u):

                if v not in self.Q:
                    continue

                alt = self.dist[u] + 1
                if alt < self.dist[v]:
                    self.dist[v] = alt
                    self.prev[v] = u
        return

    def get_total_dist(self, idx):
        d = 0
        while idx != self.i_start:
            d += 1
            idx = self.prev[idx]
        return d

    def get_vertex_min_dist(self):
        m = inf
        idx_min = None
        for idx in self.Q:
            if self.dist[idx] < m:
                m = self.dist[idx]
                idx_min = idx

        if idx_min is None:
            return idx_min

        return idx_min

    def get_accessible_neighbors(self, idx: int):
        n = []  # all neighbors
        x, y = idx % self.len_x, idx // self.len_x
        if x > 0:
            n.append(idx - 1)
        if x < self.len_x - 1:
            n.append(idx + 1)

        if y > 0:
            n.append(idx - self.len_x)
        if y < self.len_y - 1:
            n.append(idx + self.len_x)

        # accessible neighbors
        allowed = lambda j: self.allowed_move(idx, j)
        an = list(filter(allowed, n))
        return an

    def allowed_move(self, i, j):
        """from i to j"""
        return ord(self.s[j]) - ord(self.s[i]) < 2

    def create_graph(self):
        g = np.zeros([len(self.s), len(self.s)])
        for i, v in enumerate(self.s):
            an = self.get_accessible_neighbors(i)
            for j in an:
                g[i, j] = 1
        return g


def read_file():
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


def solution(data: str, part=1):
    grid = S(data)
    grid.dijkstra()
    r = grid.dist[grid.i_end]
    if part == 1:
        return r

    if part == 2:
        r_min = r
        N = grid.s.count("a")
        for i, i_s in enumerate(re.finditer("a", grid.s)):
            grid.i_start = i_s.start()
            grid.dijkstra()
            if grid.dist[grid.i_end] < r_min:
                r_min = grid.dist[grid.i_end]
                print(f"r_min updated to {r_min} at iteration {i+1} of {N}")
        return r_min


def solution_scipy(data: str, part=1):
    grid = S(data)
    g = grid.create_graph()
    sp = shortest_path(g)

    if part == 1:
        return int(sp[grid.i_start, grid.i_end])

    if part == 2:
        return int(min(sp[i_s.start(), grid.i_end] for i_s in re.finditer("a", grid.s)))


if __name__ == "__main__":
    assert solution_scipy(example_data, part=1) == 31
    print("Part 1: ", solution_scipy(read_file(), part=1))

    assert solution_scipy(example_data, part=2) == 29
    print("Part 2: ", solution_scipy(read_file(), part=2))

    # assert solution(example_data, part=1) == 31
    # print("Part 1: ", solution(read_file(), part=1))

    # assert solution(example_data, part=2) == 29
    # print("Part 2: ", solution(read_file(), part=2))
