#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>

int main() {
    std::ifstream file("input_files/day02_hgp.txt");

    int safeCount = 0;
    std::string line;
    while (std::getline(file, line)) {
        bool rowIsSafe = true; // if this is still true by the end, the row is safe

        std::istringstream iss(line);

        // allocate 
        int num1;
        iss >> num1; // first number
        int num2;
        bool isFirst = true;
        bool isIncreasing;

        // loop over numbers in row
        while (iss >> num2) {
            // first time only: determine if increasing or decreasing
            if (isFirst) {
                isIncreasing = num1 < num2;
                isFirst = false; // only do this once
            }

            // check if difference is between 1 and 3 and if it is consistently increasing or decreasing
            if (std::abs(num1 - num2) < 1 || std::abs(num1 - num2) > 3 || ((num1 < num2) != isIncreasing)) {
                rowIsSafe = false; 
                break;
            }

            // replace num1 with num2 for next iteration
            num1 = num2;
        }

        if (rowIsSafe) {
            safeCount++;
        }
    }

    std::cout << safeCount << " reports are safe." << std::endl;

    return 0;
}