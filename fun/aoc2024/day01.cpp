#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <tuple>

/**
 * @brief Get the number of lines in a file.
 * 
 * @param filename The name of the file to read.
 * @return int The number of lines in the file.
 */
int getNumLines(const std::string &filename) {
    std::ifstream file(filename);
    int lineCount = 0;
    std::string line;
    while (std::getline(file, line)) {
        ++lineCount;
    }
    file.close();
    return lineCount;
}

/**
 * @brief Read two columns of integers from a file.
 * 
 * @param filename The name of the file to read.
 * @param lineCount The number of lines in the file.
 * @return std::tuple<std::vector<int>, std::vector<int>> A tuple containing two vectors of integers.
 */
std::tuple<std::vector<int>, std::vector<int>> readColumns(const std::string &filename, int lineCount) {
    // initialize vectors
    std::vector<int> col1(lineCount);
    std::vector<int> col2(lineCount);

    // populate columns
    std::ifstream file(filename);
    int i = 0;
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        iss >> col1[i] >> col2[i];
        ++i;
    }
    file.close();
    
    return std::make_tuple(col1, col2);
}

/**
 * @brief Compute the total distance between two vectors of integers.
 * 
 * @param col1 The first vector of integers.
 * @param col2 The second vector of integers.
 * @return int The total distance between the two vectors.
 */
int computeDistance(std::vector<int> &col1, std::vector<int> &col2) {
    int totalDistance = 0;
    for (int i = 0; i < col1.size(); ++i) {
        totalDistance += std::abs(col1[i] - col2[i]);
    }
    return totalDistance;
}

/**
 * @brief Compute the similarity score between two vectors of integers.
 * 
 * @param col1 The first vector of integers.
 * @param col2 The second vector of integers.
 * @return int The similarity score between the two vectors.
 */
int computeSimilarityScore(std::vector<int> &col1, std::vector<int> &col2) {
    int similarityScore = 0;
    for (int i = 0; i < col1.size(); ++i) {
        // count number of times col1[i] occurs in col2
        int count = std::count(col2.begin(), col2.end(), col1[i]);
        // similarity score is the product of count and col1[i]
        similarityScore += count*col1[i];
    }
    return similarityScore;
}

int main() {
    std::string inputFilename = "input_files/day01_hgp.txt";

    // get number of lines
    int lineCount = getNumLines(inputFilename);
    std::cout << "Number of lines: " << lineCount << std::endl;

    // read columns in file
    std::vector<int> col1, col2;
    std::tie(col1, col2) = readColumns(inputFilename, lineCount);

    // sort vectors
    std::sort(col1.begin(), col1.end());
    std::sort(col2.begin(), col2.end());

    // compute distances
    int totalDistance = computeDistance(col1, col2);
    std::cout << "Total distance: " << totalDistance << std::endl;

    // compute similarity score
    int similarityScore = computeSimilarityScore(col1, col2);
    std::cout << "Similarity score: " << similarityScore << std::endl;

    return 0;
}