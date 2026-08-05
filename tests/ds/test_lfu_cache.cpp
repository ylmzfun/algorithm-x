#include "algorithm_x/ds/lfu_cache.h"
#include "gtest/gtest.h"
using namespace algorithm_x::ds;
namespace {
TEST(LFUCache, PutGet) { LFUCache<int,int> c(2); c.put(1,10); EXPECT_EQ(*c.get(1),10); }
TEST(LFUCache, Eviction) { LFUCache<int,int> c(2); c.put(1,1); c.put(2,2); c.get(1); c.put(3,3); EXPECT_FALSE(c.get(2)); EXPECT_TRUE(c.get(1)); }
TEST(LFUCache, Capacity) { LFUCache<int,int> c(3); EXPECT_EQ(c.capacity(), 3u); }
}  // namespace
