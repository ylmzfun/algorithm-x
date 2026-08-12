#pragma once

#include <bitset>
#include <cstddef>
#include <functional>
#include <string>

namespace algorithm_x {
namespace ds {

// 布隆过滤器 — 概率型集合，可能误报但不会漏报。
// Bits: 位数组大小; HashCount: 哈希函数个数。
template <std::size_t Bits = 1024, int HashCount = 3>
class BloomFilter {
public:
    void insert(const std::string& key) {
        for (int i = 0; i < HashCount; ++i) {
            std::size_t h = hash(key, i);
            bits_.set(h % Bits);
        }
    }

    bool contains(const std::string& key) const {
        for (int i = 0; i < HashCount; ++i) {
            std::size_t h = hash(key, i);
            if (!bits_.test(h % Bits)) return false;
        }
        return true;
    }

    void clear() { bits_.reset(); }

    std::size_t size() const { return bits_.count(); }

private:
    std::size_t hash(const std::string& key, int seed) const {
        std::size_t h1 = std::hash<std::string>{}(key);
        std::size_t h2 = std::hash<std::string>{}(key + std::to_string(seed));
        return h1 + static_cast<std::size_t>(seed) * h2;
    }

    std::bitset<Bits> bits_;
};

}  // namespace ds
}  // namespace algorithm_x
