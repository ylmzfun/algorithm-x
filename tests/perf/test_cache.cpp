#include "algorithm_x/perf/cache.h"

#include <cstddef>

#include "gtest/gtest.h"

using namespace algorithm_x::perf;

namespace {

TEST(LikelyUnlikely, CompilesAndEvaluatesCorrectly) {
    int x = 0;
    if (LIKELY(x == 0)) {
        x = 1;
    }
    EXPECT_EQ(x, 1);

    if (UNLIKELY(x != 1)) {
        x = 0;
    }
    EXPECT_EQ(x, 1);
}

TEST(Prefetch, DoesNotCrash) {
    int data[1024] = {};
    prefetch_read(data);
    prefetch_read(data + 512);
    prefetch_write(data);
    prefetch_write(data + 256);
    SUCCEED();
}

TEST(AtomicHelpers, LoadAcquireStoreRelease) {
    int val = 42;
    int loaded = load_acquire(val);
    EXPECT_EQ(loaded, 42);

    store_release(val, 99);
    EXPECT_EQ(val, 99);
}

TEST(HardwareConstant, CacheLinePositive) {
    EXPECT_GT(HARDWARE_CACHE_LINE, static_cast<std::size_t>(0));
}

TEST(CacheAligned, SizeAndAlignment) {
    CacheAligned<int> ca;
    ca.value = 7;
    EXPECT_EQ(ca.value, 7);

    // Alignment must be at least cache line
    EXPECT_GE(alignof(CacheAligned<int>), HARDWARE_CACHE_LINE);
}

}  // namespace
