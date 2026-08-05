#include <gtest/gtest.h>

#include <stdexcept>
#include <string>

#include "algorithm_x/ds/lru_cache.h"

using algorithm_x::ds::LRUCache;

TEST(LRUCacheTest, PutAndGet) {
    LRUCache<int, std::string> cache(3);
    cache.put(1, "one");
    cache.put(2, "two");

    EXPECT_EQ(*cache.get(1), "one");
    EXPECT_EQ(*cache.get(2), "two");
    EXPECT_EQ(cache.get(3), nullptr);
}

TEST(LRUCacheTest, EvictionWhenFull) {
    LRUCache<int, int> cache(2);
    cache.put(1, 10);
    cache.put(2, 20);
    cache.put(3, 30);  // evicts key 1 (least recently used)

    EXPECT_EQ(cache.get(1), nullptr);
    EXPECT_EQ(*cache.get(2), 20);
    EXPECT_EQ(*cache.get(3), 30);
    EXPECT_EQ(cache.size(), 2);
}

TEST(LRUCacheTest, GetUpdatesRecency) {
    LRUCache<int, int> cache(2);
    cache.put(1, 10);
    cache.put(2, 20);

    // Access key 1 — it becomes most recently used
    EXPECT_EQ(*cache.get(1), 10);

    cache.put(3, 30);  // should evict key 2, not key 1

    EXPECT_NE(cache.get(1), nullptr);
    EXPECT_EQ(cache.get(2), nullptr);
    EXPECT_EQ(*cache.get(3), 30);
}

TEST(LRUCacheTest, PutUpdatesValueAndRecency) {
    LRUCache<int, int> cache(2);
    cache.put(1, 10);
    cache.put(2, 20);

    // Update key 1 — should NOT evict, value changes
    cache.put(1, 100);

    EXPECT_EQ(*cache.get(1), 100);
    EXPECT_TRUE(cache.contains(2));
    EXPECT_EQ(cache.size(), 2);

    cache.put(3, 30);  // evicts key 2 (key 1 was updated, key 2 is LRU)
    EXPECT_EQ(cache.get(2), nullptr);
    EXPECT_EQ(*cache.get(1), 100);
    EXPECT_EQ(*cache.get(3), 30);
}

TEST(LRUCacheTest, CapacityEnforcement) {
    LRUCache<int, int> cache(3);
    cache.put(1, 1);
    cache.put(2, 2);
    cache.put(3, 3);
    cache.put(4, 4);

    EXPECT_EQ(cache.size(), 3);
    EXPECT_EQ(cache.get(1), nullptr);
}

TEST(LRUCacheTest, Contains) {
    LRUCache<int, int> cache(2);
    cache.put(1, 10);

    EXPECT_TRUE(cache.contains(1));
    EXPECT_FALSE(cache.contains(2));
}

TEST(LRUCacheTest, SizeAndCapacity) {
    LRUCache<int, int> cache(5);
    EXPECT_EQ(cache.capacity(), 5);
    EXPECT_EQ(cache.size(), 0);
    EXPECT_TRUE(cache.empty());

    cache.put(1, 10);
    EXPECT_EQ(cache.size(), 1);
    EXPECT_FALSE(cache.empty());
}

TEST(LRUCacheTest, ZeroCapacityThrows) {
    using IntCache = LRUCache<int, int>;
    EXPECT_THROW(IntCache(0), std::invalid_argument);
}

TEST(LRUCacheTest, FullEvictionOrder) {
    LRUCache<int, int> cache(3);
    cache.put(1, 10);
    cache.put(2, 20);
    cache.put(3, 30);

    // Access order: 3, 2, 1 (1 is LRU)
    cache.get(3);
    cache.get(2);

    cache.put(4, 40);  // evicts 1

    EXPECT_EQ(cache.get(1), nullptr);
    EXPECT_EQ(*cache.get(2), 20);
    EXPECT_EQ(*cache.get(3), 30);
    EXPECT_EQ(*cache.get(4), 40);
}
