#pragma once

#include <cstddef>

namespace algorithm_x {
namespace perf {

// Force the compiler to predict that `cond` is likely true.
// Usage: if (LIKELY(ptr != nullptr)) { ... }
#define LIKELY(cond)   __builtin_expect(static_cast<bool>(cond), 1)
#define UNLIKELY(cond) __builtin_expect(static_cast<bool>(cond), 0)

// Prefetch a memory address for reading (locality = 3 → L1 cache).
inline void prefetch_read(const void* addr) {
    __builtin_prefetch(addr, 0, 3);
}

// Prefetch for writing.
inline void prefetch_write(const void* addr) {
    __builtin_prefetch(addr, 1, 3);
}

// 确保变量从内存重新读取（防止编译器优化掉重复读）。
template <typename T>
inline T load_acquire(const T& var) {
    return __atomic_load_n(&var, __ATOMIC_ACQUIRE);
}

// 确保变量写入对多线程可见。
template <typename T>
inline void store_release(T& var, T value) {
    __atomic_store_n(&var, value, __ATOMIC_RELEASE);
}

// Cache-aligned struct — ensures the struct starts at a cache line boundary.
// Usage: struct alignas(HARDWARE_CACHE_LINE) MyStruct { ... };
#ifdef __APPLE__
constexpr std::size_t HARDWARE_CACHE_LINE = 128;  // Apple Silicon
#else
constexpr std::size_t HARDWARE_CACHE_LINE = 64;
#endif

// 简单的伪共享防护填充。
template <typename T, std::size_t CacheLine = HARDWARE_CACHE_LINE>
struct alignas(CacheLine) CacheAligned {
    T value;
    // 剩余部分填充到 cache line 边界
private:
    char padding_[CacheLine > sizeof(T) ? CacheLine - sizeof(T) : 1]{};
};

}  // namespace perf
}  // namespace algorithm_x
