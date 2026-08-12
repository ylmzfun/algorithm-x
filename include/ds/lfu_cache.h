#pragma once

#include <cstddef>
#include <list>
#include <stdexcept>
#include <unordered_map>
#include <utility>

namespace algorithm_x {
namespace ds {

// LFU Cache — evicts least frequently used item, LRU tie-break.
template <typename K, typename V>
class LFUCache {
public:
    explicit LFUCache(std::size_t capacity) : capacity_(capacity) {
        if (capacity == 0) throw std::invalid_argument("capacity must be > 0");
    }

    V* get(const K& key) {
        auto it = key_map_.find(key);
        if (it == key_map_.end()) return nullptr;
        int freq = it->second->freq;
        auto& old_list = freq_map_[freq];
        Entry entry = *it->second;
        old_list.erase(it->second);
        if (old_list.empty()) { freq_map_.erase(freq); if (min_freq_ == freq) ++min_freq_; }
        entry.freq++;
        auto& new_list = freq_map_[entry.freq];
        new_list.push_front(entry);
        it->second = new_list.begin();
        return &(new_list.begin()->value);
    }

    void put(const K& key, const V& value) {
        auto it = key_map_.find(key);
        if (it != key_map_.end()) {
            it->second->value = value;
            get(key);
            return;
        }
        if (key_map_.size() >= capacity_) {
            auto& min_list = freq_map_[min_freq_];
            K evict = min_list.back().key;
            key_map_.erase(evict);
            min_list.pop_back();
            if (min_list.empty()) freq_map_.erase(min_freq_);
        }
        Entry entry{key, value, 1};
        auto& flist = freq_map_[1];
        flist.push_front(entry);
        key_map_[key] = flist.begin();
        min_freq_ = 1;
    }

    std::size_t size() const { return key_map_.size(); }
    std::size_t capacity() const { return capacity_; }

private:
    struct Entry { K key; V value; int freq; };
    using EntryIter = typename std::list<Entry>::iterator;
    std::size_t capacity_;
    int min_freq_ = 0;
    std::unordered_map<K, EntryIter> key_map_;
    std::unordered_map<int, std::list<Entry>> freq_map_;
};

}  // namespace ds
}  // namespace algorithm_x
