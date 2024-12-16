#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <chrono>

// position and orientation of guard
struct GuardState {
    std::pair<int, int> pos;
    std::pair<int, int> ori;
};

// positions and orientations along a path
struct Path {
    std::vector<std::pair<int, int>> positions;
    std::vector<std::pair<int, int>> orientations;
};

// indices of each obstacle on map and max indices
struct Map {
    std::vector<std::pair<int, int>> obstacles;
    int m;
    int n;
};

// convert character to orientation
std::pair<int, int> getOrientation(char c) {
    switch (c) {
        case '^':
            return {-1, 0};
        case 'v':
            return {1, 0};
        case '<':
            return {0, -1};
        case '>':
            return {0, 1};
        default:
            return {0, 0};
    }
}

// move guard in the direction of orientation
void moveGuard(GuardState &guard, Map &map) {
    // potential new position
    std::pair<int, int> new_pos = {guard.pos.first + guard.ori.first, guard.pos.second + guard.ori.second};
    if (std::find(map.obstacles.begin(), map.obstacles.end(), new_pos) != map.obstacles.end()) {
        // guard hit an obstacle! turn right 
        if (guard.ori.first == 0) {
            guard.ori.first = guard.ori.second;
            guard.ori.second = 0;
        } else {
            guard.ori.second = -guard.ori.first;
            guard.ori.first = 0;
        }
        new_pos = {guard.pos.first + guard.ori.first, guard.pos.second + guard.ori.second};
    }
    guard.pos = new_pos;
}

// trace out guard path
Path tracePath(GuardState guard, Map &map, int *nLoops = nullptr) {
    Path path;
    while (true) {
        auto it = std::find(path.positions.begin(), path.positions.end(), guard.pos); // returns iterator
        if (it == path.positions.end()) {
            // guard has not visited this position yet, add to path
            path.positions.push_back(guard.pos);
            path.orientations.push_back(guard.ori);
        } else {
            int i = std::distance(path.positions.begin(), it); // get index of copy
            if (path.orientations[i] == guard.ori) {
                // guard has visited this position before and was in the same orientation -> loop detected
                std::cout << "Loop detected!" << std::endl;
                if (nLoops) {
                    (*nLoops)++;
                }
                break;
            }
        }
        moveGuard(guard, map);
        if (guard.pos.first < 0 || guard.pos.first >= map.m || guard.pos.second < 0 || guard.pos.second >= map.n) {
            // guard has left the map
            break;
        }
    }
    return path;
}

// print map with guard path to file
void printPath(Path &path, Map &map, std::string filename) {
    // print map with guard path to file
    std::ofstream out(filename);
    for (int i = 0; i < map.m; i++) {
        for (int j = 0; j < map.n; j++) {
            if (std::find(path.positions.begin(), path.positions.end(), std::make_pair(i, j)) != path.positions.end()) {
                out << 'X';
            } else if (std::find(map.obstacles.begin(), map.obstacles.end(), std::make_pair(i, j)) != map.obstacles.end()) {
                out << '#';
            } else {
                out << '.';
            }
        }
        out << std::endl;
    }
    out.close();
    std::cout << "Path printed to " << filename << std::endl;
}

int main() {
    std::string filename = "input_files/day06_hgp.txt";
    // std::string filename = "input_files/test.txt";
    std::ifstream file(filename);
    std::string line;

    // load map and guard from file
    GuardState initGuardState;
    Map map;
    int i = 0;
    int j;
    while (std::getline(file, line)) {
        j = 0;
        for (char c : line) {
            if (c == '#') {
                map.obstacles.push_back({i, j});
            } else if (c == '^' || c == 'v' || c == '<' || c == '>') {
                initGuardState.pos = {i, j};
                initGuardState.ori = getOrientation(c);
            }
            j++;
        }
        i++;
    }
    // set map dimensions
    map.m = i; 
    map.n = j;

    // trace out guard path
    Path path = tracePath(initGuardState, map);

    // print path to file
    printPath(path, map, "path.txt");

    std::cout << "Path length: " << path.positions.size() << std::endl;

    // add obstacles one-by-one to map
    int nLoops = 0;
    Map newMap = map; // start with copy of map
    newMap.obstacles.reserve(map.obstacles.size() + 1); // reserve space for one additional obstacle
    i = 0;
    for (std::pair<int, int> obstacle : path.positions) { // only add obstacles in original path
        std::cout << i++ << "/" << path.positions.size() << std::endl;
        newMap.obstacles.push_back(obstacle);
        Path path = tracePath(initGuardState, newMap, &nLoops);
        newMap.obstacles.pop_back();
    }
    std::cout << "Number of loops: " << nLoops << std::endl;

    return 0;
}