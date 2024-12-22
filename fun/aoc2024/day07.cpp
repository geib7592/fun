#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <cmath>

std::pair<long long, std::vector<long long>> parseLine(std::string line) {
    std::vector<long long> inputs;
    std::istringstream iss(line);
    std::string token;

    // first token is target value
    std::getline(iss, token, ' ');
    long long targetValue = std::stoll(token.substr(0, token.length() - 1));

    // the rest are inputs
    while (std::getline(iss, token, ' ')) {
        inputs.push_back(std::stoll(token));
    }

    return {targetValue, inputs};
}

std::vector<int> numberToBinaryVector(int number, int numBits) {
    std::vector<int> binaryVector(numBits, 0);
    for (int i = 0; i < numBits; ++i) {
        if ((number & (1 << i)) != 0) { // check if ith bit is set
            binaryVector[numBits - 1 - i] = 1; 
        } else {
            binaryVector[numBits - 1 - i] = 0;
        }
    }
    return binaryVector;
}

std::vector<int> numberToTernaryVector(int number, int numBits) {
    std::vector<int> ternaryVector(numBits, 0);
    for (int i = 0; i < numBits; ++i) {
        ternaryVector[numBits - 1 - i] = number % 3;
        number /= 3;
    }
    return ternaryVector;
}

bool checkOperatorPattern(long long &targetValue, std::vector<long long> &inputs, std::vector<int> &operatorPattern) {
    int n = inputs.size();
    long long total = inputs[0];
    for (int i = 0; i < n - 1; i++) {
        if (operatorPattern[i] == 0) {
            // add inputs[i + 1] to total
            total += inputs[i + 1];
        } else if (operatorPattern[i] == 1) {
            // multiply inputs[i + 1] to total
            total *= inputs[i + 1];
        } else {
            // concatenate inputs[i + 1] to total
            total = total * std::pow(10, std::to_string(inputs[i + 1]).length()) + inputs[i + 1];
        }
        if (total > targetValue) {
            return false;
        }
    }
    return total == targetValue;
}

bool isPossible(long long &targetValue, std::vector<long long> &inputs, int part) {
    int n = inputs.size();
    std::vector<int> operatorPattern(n-1, 0);

    // 2^(n-1) possible operator patterns for part 1,
    // 3^(n-1) possible operator patterns for part 2
    for (int i = 0; i < std::pow(part+1, n-1); i++) { 
        if (part == 1) {
            // convert i to binary number of length n-1
            operatorPattern = numberToBinaryVector(i, n-1);
        } else {
            // convert i to ternary number of length n-1
            operatorPattern = numberToTernaryVector(i, n-1);
        }

        // check if this operator pattern yields the target value
        if (checkOperatorPattern(targetValue, inputs, operatorPattern)) {
            return true;
        }
    }
    return false;
}

void solve(std::string inputFile, int part) {
    std::ifstream file(inputFile);
    std::string line;
    long long total = 0;
    while (std::getline(file, line)) {
        auto [targetValue, inputs] = parseLine(line);

        if (isPossible(targetValue, inputs, part)) {
            total += targetValue;    
        }
    }

    std::cout << "Total: " << total << std::endl;
}

int main() {
    // std::string inputFile = "input_files/test.txt";
    std::string inputFile = "input_files/day07_hgp.txt";

    // solve(inputFile, 1);

    solve(inputFile, 2);

    return 0;
}