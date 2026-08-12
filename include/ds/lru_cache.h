#pragma once

#include <cstddef>
#include <list>
#include <stdexcept>
#include <unordered_map>
#include <utility>

namespace algorithm_x {
namespace ds {

// LRUCache — 基于哈希表 + 双向链表的 LRU 缓存。
// // 调用示例：
//   LRUCache<int, std::string> cache(3);
//   cache.put(1, "one");
//   cache.get(1);  // "one"
template <typename K, typename V>
class LRUCache {
public:
    explicit LRUCache(std::size_t capacity) : capacity_(capacity) {
        if (capacity == 0) {
            throw std::invalid_argument("LRUCache: capacity must be > 0");
        }
    }

    V* get(const K& key) {
        auto it = map_.find(key);
        if (it == map_.end()) return nullptr;
        // move to front
        list_.splice(list_.begin(), list_, it->second);
        return &it->second->second;
    }

    void put(const K& key, const V& value) {
        auto it = map_.find(key);
        if (it != map_.end()) {
            it->second->second = value;
            list_.splice(list_.begin(), list_, it->second);
            return;
        }
        if (list_.size() >= capacity_) {
            auto last = list_.back();
            map_.erase(last.first);
            list_.pop_back();
        }
        list_.emplace_front(key, value);
        map_[key] = list_.begin();
    }

    bool contains(const K& key) const { return map_.find(key) != map_.end(); }

    std::size_t size() const { return list_.size(); }
    std::size_t capacity() const { return capacity_; }
    bool empty() const { return list_.empty(); }

private:
    using ListIterator = typename std::list<std::pair<K, V>>::iterator;

    std::list<std::pair<K, V>> list_;
    std::unordered_map<K, ListIterator> map_;
    std::size_t capacity_;
};

}  // namespace ds
}  // namespace algorithm_x
