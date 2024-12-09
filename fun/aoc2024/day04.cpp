#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdio>

bool checkN(std::vector<std::string> &lines, int i, int j, int m, int n) {
    if (j + 3 < n) {
        if (lines[i][j+1] == 'M' && lines[i][j+2] == 'A' && lines[i][j+3] == 'S') {
            return true;
        }
    }   
    return false;
}
bool checkNE(std::vector<std::string> &lines, int i, int j, int m, int n) {
    if (i - 3 >= 0 && j + 3 < n) {
        if (lines[i-1][j+1] == 'M' && lines[i-2][j+2] == 'A' && lines[i-3][j+3] == 'S') {
            return true;
        }
    }
    return false;
}
bool checkE(std::vector<std::string> &lines, int i, int j, int m, int n) {
    if (i - 3 >= 0) {
        if (lines[i-1][j] == 'M' && lines[i-2][j] == 'A' && lines[i-3][j] == 'S') {
            return true;
        }
    }
    return false;
}
bool checkSE(std::vector<std::string> &lines, int i, int j, int m, int n) {
    if (i - 3 >= 0 && j - 3 >= 0) {
        if (lines[i-1][j-1] == 'M' && lines[i-2][j-2] == 'A' && lines[i-3][j-3] == 'S') {
            return true;
        }
    }
    return false;
}
bool checkS(std::vector<std::string> &lines, int i, int j, int m, int n) {
    if (j - 3 >= 0) {
        if (lines[i][j-1] == 'M' && lines[i][j-2] == 'A' && lines[i][j-3] == 'S') {
            return true;
        }
    }
    return false;
}
bool checkSW(std::vector<std::string> &lines, int i, int j, int m, int n) {
    if (i + 3 < m && j - 3 >= 0) {
        if (lines[i+1][j-1] == 'M' && lines[i+2][j-2] == 'A' && lines[i+3][j-3] == 'S') {
            return true;
        }
    }
    return false;
}
bool checkW(std::vector<std::string> &lines, int i, int j, int m, int n) {
    if (i + 3 < m) {
        if (lines[i+1][j] == 'M' && lines[i+2][j] == 'A' && lines[i+3][j] == 'S') {
            return true;
        }
    }
    return false;
}
bool checkNW(std::vector<std::string> &lines, int i, int j, int m, int n) {
    if (i + 3 < m && j + 3 < n) {
        if (lines[i+1][j+1] == 'M' && lines[i+2][j+2] == 'A' && lines[i+3][j+3] == 'S') {
            return true;
        }
    }
    return false;
}

// // Direction vectors for N, NE, E, SE, S, SW, W, NW
// const std::vector<std::pair<int, int>> directions = {
//     {0, 1}, {1, 1}, {1, 0}, {1, -1},
//     {0, -1}, {-1, -1}, {-1, 0}, {-1, 1}
// };

// bool numPatterns(const std::vector<std::string> &lines, int i, int j, 
//                  int m, int n, const std::string &pattern) {
//     int count = 0;
//     for (const auto &dir : directions) {
//         int x = i, y = j;
//         bool match = true;
//         for (char c : pattern) {
//             x += dir.first;
//             y += dir.second;
//             if (x < 0 || x >= m || y < 0 || y >= n) {
//                 match = false;
//                 break;
//             } else if (lines[x][y] != c) {
//                 match = false;
//                 break;
//             }
//         }
//         if (match) {
//             printf("Found XMAS from (%d, %d) to (%d, %d)\n", i, j, x, y);
//             count++;
//         }
//     }
//     return count;
// }

int main() {
    // read lines into a vector of strings
    std::string filename = "input_files/day04_hgp.txt";
    // std::string filename = "input_files/test.txt";
    std::ifstream file(filename);
    std::string line;
    std::vector<std::string> lines;
    while (std::getline(file, line)) {
        lines.push_back(line);
    };
    file.close();

    int m = lines.size(); // num rows
    int n = lines[0].size(); // num cols

    // for each 'X' in matrix, check if it is part of "XMAS"
    int xmasCount = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (lines[i][j] == 'X') {
                if (checkN(lines, i, j, m, n)) {
                    xmasCount++;
                }
                if (checkNE(lines, i, j, m, n)) {
                    xmasCount++;
                }
                if (checkE(lines, i, j, m, n)) {
                    xmasCount++;
                }
                if (checkSE(lines, i, j, m, n)) {
                    xmasCount++;
                }
                if (checkS(lines, i, j, m, n)) {
                    xmasCount++;
                }
                if (checkSW(lines, i, j, m, n)) {
                    xmasCount++;
                }
                if (checkW(lines, i, j, m, n)) {
                    xmasCount++;
                }
                if (checkNW(lines, i, j, m, n)) {
                    xmasCount++;
                }
                // xmasCount += numPatterns(lines, i, j, m, n, "MAS");
            }
        }
    }
    
    printf("Number of XMASs: %d\n", xmasCount);

    // for each 'A' in matrix, check if it is part of "X-MAS"
    int xMasCount = 0;
    for (int i = 1; i < m-1; i++) {
        for (int j = 1; j < n-1; j++) {
            if (lines[i][j] == 'A') {
                bool NESW1 = (lines[i+1][j+1] == 'M' && lines[i-1][j-1] == 'S');
                bool NESW2 = (lines[i+1][j+1] == 'S' && lines[i-1][j-1] == 'M');
                bool NWSE1 = (lines[i+1][j-1] == 'M' && lines[i-1][j+1] == 'S');
                bool NWSE2 = (lines[i+1][j-1] == 'S' && lines[i-1][j+1] == 'M');
                if ((NESW1 || NESW2) && (NWSE1 || NWSE2)) {
                    xMasCount++;
                }
            }
        }
    }
    
    printf("Number of X-MASs: %d\n", xMasCount);

    return 0;
}