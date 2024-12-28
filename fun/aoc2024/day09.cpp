#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
    
std::string readFile(std::string inputFile) {
    std::ifstream file(inputFile);
    std::string line;
    std::getline(file, line);
    return line;
}

std::vector<int> unpackBlocks(std::string diskMap) {
    std::vector<int> blocks;
    for (int i = 0; i < diskMap.size(); i++) {
        // read integer
        int n = diskMap[i] - '0'; // convert char to int
        for (int j = 0; j < n; j++) {
            if (i % 2 == 0) {
                // n blocks of ID value
                blocks.push_back(i/2);
            } else {
                // n blocks of free space, denoted by -1
                blocks.push_back(-1);
            }
        }
    }
    return blocks;
}

void printBlocks(std::vector<int> blocks) {
    for (int i = 0; i < blocks.size(); i++) {
        if (blocks[i] == -1) {
            std::cout << ". ";
        } else {
            std::cout << blocks[i] << " ";
        }
    }
    std::cout << std::endl;
}

std::vector<int> moveBlocksPartOne(std::vector<int> blocks, bool debug = false) {
    for (int i = 0; i < blocks.size(); i++) {
        if (blocks[i] == -1) {
            // replace free space with last file block
            int j = blocks.size() - 1;
            while (blocks[j] == -1) {
                j--;
            }
            if (j <= i) {
                break;
            }
            blocks[i] = blocks[j];
            blocks[j] = -1;
            if (debug) {
                printBlocks(blocks);
            }
        }
    }
    return blocks;
}

std::vector<int> moveBlocksPartTwo(std::vector<int> blocks, bool debug = false) {
    int blockStart = blocks.size() - 1;
    int blockStop = blocks.size();
    std::vector<int> hasMoved;
    while (blockStart > 0) {
        // find next block
        while (blocks[blockStop-1] == -1) {
            blockStop--;
        }

        // check if block has already been moved
        if (std::find(hasMoved.begin(), hasMoved.end(), blocks[blockStop-1]) != hasMoved.end()) {
            std::cout << "block " << blocks[blockStop-1] << " has already been moved" << std::endl;
            blockStop--;
            continue;
        }

        // find block size
        blockStart = blockStop - 1;
        while (blocks[blockStart] == blocks[blockStop-1]) {
            blockStart--;
        }
        blockStart++;
        std::cout << "block of " << blocks[blockStart] << "'s found at [" << blockStart << ":" << blockStop << "]" << std::endl;

        // look for free space >= block size
        int freeStart = 0;
        int freeStop = 0;
        while (freeStop - freeStart < blockStop - blockStart && freeStop < blockStart) {
            freeStart = freeStop;

            // look for free space
            while (blocks[freeStart] != -1) {
                freeStart++;
            }

            // determine size 
            freeStop = freeStart + 1;
            while (blocks[freeStop] == -1) {
                freeStop++;
            }
            // std::cout << "free space found at [" << freeStart << ":" << freeStop << "]" << std::endl;
        }
        if (freeStop - freeStart >= blockStop - blockStart) {
            // add id to hasMoved
            hasMoved.push_back(blocks[blockStart]);

            // set values from freeStart to freeStart + (blockStop - blockStart) to blocks[blockStart]
            std::fill(blocks.begin() + freeStart, blocks.begin() + freeStart + (blockStop - blockStart), blocks[blockStart]);

            // set values from blockStart to blockStop to -1
            std::fill(blocks.begin() + blockStart, blocks.begin() + blockStop, -1);

            if (debug) {
                printBlocks(blocks);
            }
        }

        blockStop = blockStart;
    }
    return blocks;
}

long long checksum(std::vector<int> blocks) {
    long long sum = 0;
    for (int i = 0; i < blocks.size(); i++) {
        if (blocks[i] == -1) {
            continue;
        }
        sum += i*blocks[i];
    }
    return sum;
}

void solve(std::string inputFile, int part) {
    std::string diskMap = readFile(inputFile);

    std::vector<int> blocks = unpackBlocks(diskMap);
    printBlocks(blocks);

    std::vector<int> result;
    if (part == 1) {
        result = moveBlocksPartOne(blocks);
    } else {
        result = moveBlocksPartTwo(blocks);
    }

    std::cout << "checksum: " << checksum(result)<< std::endl;
}

int main() {
    // std::string inputFile = "input_files/test.txt";
    std::string inputFile = "input_files/day09_hgp.txt";

    // solve(inputFile, 1);

    solve(inputFile, 2);

    return 0;
}