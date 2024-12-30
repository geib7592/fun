#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>

using namespace std;

int m, n;

vector<vector<int>> readFile(string inputFile) {
    ifstream file(inputFile);
    string line;
    vector<string> lines;
    while (getline(file, line)) {
        lines.push_back(line);
    }
    m = lines.size();
    n = lines[0].size();
    vector<vector<int>> topo(m, vector<int>(n));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (lines[i][j] == '.') {
                topo[i][j] = -1;
            } else {
                topo[i][j] = lines[i][j] - '0';
            }
        }
    }
    return topo;
}

vector<pair<int, int>> getPositions(vector<vector<int>> &topo, int val) {
    vector<pair<int, int>> positions;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (topo[i][j] == val) {
                positions.push_back({i, j});
            }
        }
    }
    return positions;
}

vector<pair<int, int>> getNeighbors(pair<int, int> pos) {
    int i = pos.first;
    int j = pos.second;
    vector<pair<int, int>> neighbors;
    if (i > 0) {
        neighbors.push_back({i - 1, j});
    }
    if (i < m - 1) {
        neighbors.push_back({i + 1, j});
    }
    if (j > 0) {
        neighbors.push_back({i, j - 1});
    }
    if (j < n - 1) {
        neighbors.push_back({i, j + 1});
    }
    return neighbors;
}

vector<pair<int, int>> getPossibleMoves(vector<vector<int>> &topo, pair<int, int> pos) {
    int i = pos.first;
    int j = pos.second;
    vector<pair<int, int>> neighbors = getNeighbors(pos);
    vector<pair<int, int>> possibleMoves;
    for (auto neighbor : neighbors) {
        if (topo[neighbor.first][neighbor.second] == topo[i][j] + 1) {
            possibleMoves.push_back(neighbor);
        }
    }
    return possibleMoves;
}

void getAccessiblePositions(vector<vector<int>> &accessiblePositions, vector<vector<int>> &topo, pair<int, int> pos) {
    if (accessiblePositions[pos.first][pos.second] != 1) {
        accessiblePositions[pos.first][pos.second] = 1;
    }
    vector<pair<int, int>> possibleMoves = getPossibleMoves(topo, pos);
    for (auto move : possibleMoves) {
        getAccessiblePositions(accessiblePositions, topo, move);
    }
}

void clearMatrix(vector<vector<int>> &matrix) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            matrix[i][j] = 0;
        }
    }
}

void numPaths(vector<vector<int>> &topo, pair<int, int> pos, int &count) {
    if (topo[pos.first][pos.second] == 9) {
        count += 1;
    } else {
        vector<pair<int, int>> possibleMoves = getPossibleMoves(topo, pos);
        if (possibleMoves.size() != 0) {
            for (auto move : possibleMoves) {
                numPaths(topo, move, count);
            }
        }
    }
}
    
void solve(string inputFile, int part) {
    vector<vector<int>> topo = readFile(inputFile);
    vector<pair<int, int>> trailheads = getPositions(topo, 0);
    vector<pair<int, int>> peaks = getPositions(topo, 9);
    vector<vector<int>> accessiblePositions(m, vector<int>(n));
    int sum = 0;
    for (auto trailhead : trailheads) {
        if (part == 1) {
            clearMatrix(accessiblePositions);
            getAccessiblePositions(accessiblePositions, topo, trailhead);
            for (auto peak : peaks) {
                sum += accessiblePositions[peak.first][peak.second];
            }
        } else {
            numPaths(topo, trailhead, sum);
        }
    }
    cout << sum << endl;
}

int main() {
    // string inputFile = "input_files/test.txt";
    string inputFile = "input_files/day10_hgp.txt";

    // solve(inputFile, 1);

    solve(inputFile, 2);

    return 0;
}