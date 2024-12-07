#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <chrono>

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    std::ifstream file("input_files/day01_hgp.txt");

    // count lines
    int lineCount = 0;
    std::string line;
    while (std::getline(file, line)) {
        ++lineCount;
    }
    std::cout << "Number of lines: " << lineCount << std::endl;

    // allocate vectors
    std::vector<int> col1(lineCount);
    std::vector<int> col2(lineCount);

    // read file again
    file.clear();
    file.seekg(0, std::ios::beg);

    // populate cols
    int i = 0;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        iss >> col1[i] >> col2[i];
        ++i;
    }
    file.close();

    // sort vectors
    std::sort(col1.begin(), col1.end());
    std::sort(col2.begin(), col2.end());

    // compute distances
    int totalDistance = 0;
    for (int i = 0; i < lineCount; ++i) {
        totalDistance += std::abs(col1[i] - col2[i]);
    }
    std::cout << "Total distance: " << totalDistance << std::endl;

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Elapsed time: " << elapsed.count() * 1e6 << " us" << std::endl;

    return 0;
}