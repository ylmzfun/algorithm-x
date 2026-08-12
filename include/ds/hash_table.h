#pragma once

#include <cstddef>
#include <functional>
#include <list>
#include <stdexcept>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace ds {

// HashTable — 拉链法哈希表（separate chaining）。
// 支持 insert / erase / find / operator[]。
template <typename K, typename V, typename Hash = std::hash<K>>
class HashTable {
    struct Bucket {
        std::list<std::pair<K, V>> entries;
    };

public:
    explicit HashTable(std::size_t bucket_count = 16)
        : buckets_(bucket_count), size_(0) {}

    void insert(const K& key, const V& value) {
        if (load_factor() > 0.75) rehash(buckets_.size() * 2);
        auto& bucket = get_bucket(key);
        for (auto& [k, v] : bucket.entries) {
            if (k == key) {
                v = value;  // update
                return;
            }
        }
        bucket.entries.emplace_back(key, value);
        ++size_;
    }

    bool erase(const K& key) {
        auto& bucket = get_bucket(key);
        for (auto it = bucket.entries.begin(); it != bucket.entries.end(); ++it) {
            if (it->first == key) {
                bucket.entries.erase(it);
                --size_;
                return true;
            }
        }
        return false;
    }

    V* find(const K& key) {
        auto& bucket = get_bucket(key);
        for (auto& [k, v] : bucket.entries) {
            if (k == key) return &v;
        }
        return nullptr;
    }

    const V* find(const K& key) const {
        auto& bucket = get_bucket(key);
        for (auto& [k, v] : bucket.entries) {
            if (k == key) return &v;
        }
        return nullptr;
    }

    bool contains(const K& key) const { return find(key) != nullptr; }

    V& operator[](const K& key) {
        V* p = find(key);
        if (p) return *p;
        insert(key, V{});
        return *find(key);
    }

    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }
    std::size_t bucket_count() const { return buckets_.size(); }

private:
    Bucket& get_bucket(const K& key) {
        return buckets_[hash_(key) % buckets_.size()];
    }

    const Bucket& get_bucket(const K& key) const {
        return buckets_[hash_(key) % buckets_.size()];
    }

    double load_factor() const {
        return static_cast<double>(size_) / buckets_.size();
    }

    void rehash(std::size_t new_count) {
        std::vector<Bucket> old(new_count);
        old.swap(buckets_);
        size_ = 0;
        for (auto& bucket : old) {
            for (auto& [k, v] : bucket.entries) {
                insert(std::move(k), std::move(v));
            }
        }
    }

    std::vector<Bucket> buckets_;
    std::size_t size_;
    Hash hash_;
};

}  // namespace ds
}  // namespace algorithm_x
