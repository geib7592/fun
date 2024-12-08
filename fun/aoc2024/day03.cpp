#include <iostream>
#include <fstream>
#include <string>

bool isNum(char c) {
    return c >= '0' && c <= '9';
}

int findIndexToNum(std::string line, int i) {
    int j = 1;
    while (true) {
        if (line[i+j] == ',' || line[i+j] == ')') {
            break;
        } else if (isNum(line[i+j])) {
            j++;
        } else {
            // invalid character
            return -1;
        }
    }
    if (j < 4) {
        return j;
    } else {
        // too many digits
        return -1;
    }
}

int main() {
    // read line
    std::string filename = "input_files/day03_hgp.txt";
    // std::string filename = "input_files/test.txt";
    std::ifstream file(filename);
    std::string line;
    std::getline(file, line);
    file.close();

    // march through line and find possible commands
    int i = 0;
    int X, Y, j, sum;
    bool isEnabled = true;
    while (i < line.size()) {
        if (line.substr(i, 4) == "do()") {
            isEnabled = true;
            i += 4;
        } else if (line.substr(i, 7) == "don't()") {
            isEnabled = false;
            i += 7;
        } else if (line.substr(i, 4) == "mul(") {
            i += 4;

            if (!isEnabled) {
                continue;
            }

            // get X
            j = findIndexToNum(line, i);
            if (j == -1) {
                i++;
                continue;
            }
            X = std::stoi(line.substr(i, j));
            i += j + 1;

            // get Y
            j = findIndexToNum(line, i);
            if (j == -1) {
                i++;
                continue;
            }
            Y = std::stoi(line.substr(i, j));
            i += j + 1;

            // add to sum
            std::cout << "mul(" << X << "," << Y << ")" << std::endl;
            sum += X*Y;
        } else {
            i++;
        }
    }

    std::cout << sum << std::endl;

    return 0;
}