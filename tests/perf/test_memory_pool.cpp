#include "perf/memory_pool.h"
#include "gtest/gtest.h"
using namespace algorithm_x::perf;
namespace {
TEST(MemoryPool, AllocFree) {
    MemoryPool<64,10> pool;
    void* p=pool.allocate(); EXPECT_NE(p,nullptr);
    pool.deallocate(p); SUCCEED();
}
}  // namespace
