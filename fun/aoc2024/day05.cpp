#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <cstdio>
#include <algorithm>

std::vector<int> readList(std::string line) {
    std::vector<int> list;
    int i = 0;
    while (i < line.size()) {
        int j = line.find(',', i);
        if (j == std::string::npos) {
            list.push_back(std::stoi(line.substr(i, line.size()-i)));
            break;
        }
        list.push_back(std::stoi(line.substr(i, j-i)));
        i = j + 1;
    }
    return list;
}

bool isValid(std::vector<int> list, std::unordered_map<int, std::vector<int>> rules) {
    for (int i = 1; i < list.size(); i++) {
        if (rules.find(list[i]) != rules.end()) {
            // check if list[i] is before its rule values
            std::vector<int> rule = rules[list[i]];
            for (int j = 0; j < i; j++) {
                if (std::find(rule.begin(), rule.end(), list[j]) != rule.end()) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main() {
    std::string filename = "input_files/day05_hgp.txt";
    // std::string filename = "input_files/test.txt";
    std::ifstream file(filename);
    std::string line;

    std::unordered_map<int, std::vector<int>> rules;
    int middleSum = 0;
    while (std::getline(file, line)) {
        if (line.find('|') != std::string::npos) {
            // add rule to map of rules 
            int i = line.find('|');
            int ruleKey = std::stoi(line.substr(0, i));
            int ruleValue = std::stoi(line.substr(i+1, line.size()-i-1));
            rules[ruleKey].push_back(ruleValue);
        } else if (line.find(',') != std::string::npos) {
            // read list
            std::vector<int> list = readList(line);
            // evaluate if list satisfies rule
            if (isValid(list, rules)) {
                middleSum += list[(list.size() - 1)/2];
            }
        }
    };

    std::cout << "Middle sum: " << middleSum << std::endl;

    return 0;
}