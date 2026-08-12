#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace perf {

// 简易定长块内存池（自由链表）。
// BlockSize: 每块大小; BlockCount: 块数。
template <std::size_t BlockSize, std::size_t BlockCount>
class MemoryPool {
public:
    MemoryPool() {
        pool_ = new char[BlockSize * BlockCount];
        // 构建自由链表
        for (std::size_t i = 0; i < BlockCount; ++i) {
            auto* ptr = reinterpret_cast<void**>(pool_ + i * BlockSize);
            *ptr = (i + 1 < BlockCount) ? (pool_ + (i + 1) * BlockSize) : nullptr;
        }
        free_list_ = pool_;
    }

    ~MemoryPool() { delete[] pool_; }

    void* allocate() {
        if (free_list_ == nullptr) return nullptr;
        void* block = free_list_;
        free_list_ = *reinterpret_cast<void**>(free_list_);
        return block;
    }

    void deallocate(void* ptr) {
        *reinterpret_cast<void**>(ptr) = free_list_;
        free_list_ = ptr;
    }

    std::size_t block_size() const { return BlockSize; }
    std::size_t capacity() const { return BlockCount; }

private:
    char* pool_;
    void* free_list_;
};

}  // namespace perf
}  // namespace algorithm_x
