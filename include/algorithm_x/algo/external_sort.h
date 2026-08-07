#pragma once

#include <algorithm>
#include <cstddef>
#include <fstream>
#include <functional>
#include <queue>
#include <string>
#include <vector>

namespace algorithm_x {
namespace algo {

// 外部排序 — 模拟 external merge sort。
// 读取整数文本文件，分块排序，k-way 归并写入输出。
inline void external_sort(const std::string& input_file,
                           const std::string& output_file,
                           std::size_t memory_size = 1000) {
    // Read integers from input
    std::ifstream in(input_file);
    std::vector<int> data;
    int val;
    while (in >> val) data.push_back(val);

    // If fits in memory, just sort
    if (data.size() <= memory_size) {
        std::sort(data.begin(), data.end());
        std::ofstream out(output_file);
        for (int v : data) out << v << " ";
        return;
    }

    // Split into chunks, sort each, write to temp files
    std::vector<std::string> temp_files;
    for (std::size_t i = 0; i < data.size(); i += memory_size) {
        std::size_t end = std::min(i + memory_size, data.size());
        std::sort(data.begin() + static_cast<long>(i),
                  data.begin() + static_cast<long>(end));

        std::string tmp = output_file + ".tmp" + std::to_string(temp_files.size());
        std::ofstream tmp_out(tmp);
        for (std::size_t j = i; j < end; ++j) tmp_out << data[j] << "\n";
        temp_files.push_back(tmp);
    }

    // k-way merge using min-heap
    struct Entry {
        int val;
        std::size_t file_idx;
        bool operator>(const Entry& o) const { return val > o.val; }
    };

    std::vector<std::ifstream> readers;
    std::priority_queue<Entry, std::vector<Entry>, std::greater<>> pq;

    for (std::size_t i = 0; i < temp_files.size(); ++i) {
        readers.emplace_back(temp_files[i]);
        int x;
        if (readers.back() >> x) {
            pq.push({x, i});
        }
    }

    std::ofstream out(output_file);
    bool first = true;
    while (!pq.empty()) {
        auto top = pq.top();
        pq.pop();
        if (!first) out << " ";
        out << top.val;
        first = false;

        int x;
        if (readers[top.file_idx] >> x) {
            pq.push({x, top.file_idx});
        }
    }

    // Clean up temp files
    for (auto& f : temp_files) std::remove(f.c_str());
}

}  // namespace algo
}  // namespace algorithm_x
