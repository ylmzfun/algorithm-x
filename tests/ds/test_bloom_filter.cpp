#include "ds/bloom_filter.h"
#include <string>
#include "gtest/gtest.h"
using namespace algorithm_x::ds;
namespace {
TEST(BloomFilter, InsertAndContains) {
    BloomFilter<1000, 3> bf; bf.insert("hello"); bf.insert("world");
    EXPECT_TRUE(bf.contains("hello")); EXPECT_TRUE(bf.contains("world"));
    EXPECT_FALSE(bf.contains("other"));
}
TEST(BloomFilter, MultipleInserts) {
    BloomFilter<10000, 5> bf;
    for (int i = 0; i < 100; ++i) bf.insert(std::to_string(i));
    for (int i = 0; i < 100; ++i) EXPECT_TRUE(bf.contains(std::to_string(i)));
}
}  // namespace
