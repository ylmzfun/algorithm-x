#pragma once

#include <cstddef>
#include <list>
#include <mutex>
#include <shared_mutex>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace concurrent {

// 细粒度锁并发哈希表 — 每个桶独立加锁。
template <typename K, typename V>
class ConcurrentHashTable {
public:
    explicit ConcurrentHashTable(std::size_t bucket_count = 16)
        : buckets_(bucket_count), mutexes_(bucket_count) {}

    void insert(const K& key, const V& value) {
        std::size_t idx = hash_(key) % buckets_.size();
        std::unique_lock<std::shared_mutex> lock(mutexes_[idx]);
        for (auto& [k, v] : buckets_[idx]) {
            if (k == key) { v = value; return; }
        }
        buckets_[idx].emplace_back(key, value);
    }

    V* find(const K& key) {
        std::size_t idx = hash_(key) % buckets_.size();
        std::shared_lock<std::shared_mutex> lock(mutexes_[idx]);
        for (auto& [k, v] : buckets_[idx]) {
            if (k == key) return &v;
        }
        return nullptr;
    }

    bool erase(const K& key) {
        std::size_t idx = hash_(key) % buckets_.size();
        std::unique_lock<std::shared_mutex> lock(mutexes_[idx]);
        for (auto it = buckets_[idx].begin(); it != buckets_[idx].end(); ++it) {
            if (it->first == key) {
                buckets_[idx].erase(it);
                return true;
            }
        }
        return false;
    }

private:
    using Bucket = std::list<std::pair<K, V>>;
    std::vector<Bucket> buckets_;
    mutable std::vector<std::shared_mutex> mutexes_;
    std::hash<K> hash_;
};

}  // namespace concurrent
}  // namespace algorithm_x
