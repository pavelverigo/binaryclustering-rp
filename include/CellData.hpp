#pragma once

#include <cstdint>
#include <vector>

class CellData {
public:
    int size;
    std::vector<uint64_t> chunks;
    int popcount;
    CellData() {}
    CellData(int size, std::vector<uint64_t> &&chunks, int popcount) : size(size), chunks(std::move(chunks)), popcount(popcount) {}
    CellData(int size, const std::vector<uint64_t> &chunks, int popcount) : size(size), chunks(chunks), popcount(popcount) {}
};