#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <unordered_map>
    
// grid dimensions
int m, n;

// antennas[key] is a vector of the 2D indices of all atennas with label `key`
std::unordered_map<char, std::vector<std::pair<int, int>>> loadAntennas(std::string inputFile) {
    std::ifstream file(inputFile);
    std::string line;
    std::unordered_map<char, std::vector<std::pair<int, int>>> antennas;
    int i, j = 0;
    while (std::getline(file, line)) {
        for (j = 0; j < line.size(); j++) {
            if (line[j] != '.') {
                antennas[line[j]].push_back(std::make_pair(i, j));
            }
        }
        i++;
    }
    // grid dimensions
    m = i;
    n = j;
    return antennas;
}

bool isInGrid(std::pair<int, int> p) {
    return (0 <= p.first) && (p.first < m) && (0 <= p.second) && (p.second < n);
}

bool isUnique(std::vector<std::pair<int, int>> list, std::pair<int, int> item) {
    return std::find(list.begin(), list.end(), item) == list.end();
}

std::vector<std::pair<int, int>> findAntinodes(std::unordered_map<char, std::vector<std::pair<int, int>>> antennas, int part) {
    std::vector<std::pair<int, int>> antinodes;
    std::vector<std::pair<int, int>> positions;
    int nNodes = (part == 1) ? 1 : m*n; // number of antinodes to create in each direction
    int notIncludeStations = 2 - part; // part 1 does not include stations in the antinode list, part 2 does
    int d1, d2;
    std::pair<int, int> apos;
    for (auto a : antennas) {
        positions = a.second;
        for (int i = 0; i < positions.size() - 1; i++) {
            for (int j = i + 1; j < positions.size(); j++) {
                // index displacement vector {d1, d2}
                d1 = positions[i].first - positions[j].first;
                d2 = positions[i].second - positions[j].second;

                // create nNodes antinodes in each direction
                for (int k : {i, j}) {
                    int dir = (k == i) ? 1 : -1;
                    for (int l = notIncludeStations; l <= nNodes; l++) { // l = 0 is the station itself
                        apos = {positions[k].first + dir*l*d1, positions[k].second + dir*l*d2};
                        if (isInGrid(apos)) {
                            if (isUnique(antinodes, apos)) {
                                antinodes.push_back(apos);
                            }
                        } else {
                            break;
                        }
                    }
                }
            }
        }
    }
    return antinodes;
}

void printAntinodes(std::vector<std::pair<int, int>> antinodes) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            std::pair<int, int> p = {i, j};
            if (isUnique(antinodes, p)) {
                std::cout << '.';
            } else {
                std::cout << '#';
            }
        }
        std::cout << std::endl;
    }
}

void solve(std::string inputFile, int part) {
    auto antennas = loadAntennas(inputFile);

    auto antinodes = findAntinodes(antennas, part);

    printAntinodes(antinodes);

    std::cout << "Number of antinodes: " << antinodes.size() << std::endl;
}

int main() {
    // std::string inputFile = "input_files/test.txt";
    std::string inputFile = "input_files/day08_hgp.txt";

    solve(inputFile, 1);

    solve(inputFile, 2);

    return 0;
}