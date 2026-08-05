#include "algorithm_x/algo/bit.h"

#include <gtest/gtest.h>

#include <cstdint>
#include <set>

namespace ax = algorithm_x::algo;

TEST(BitTest, IsOdd) {
    EXPECT_TRUE(ax::is_odd(1u));
    EXPECT_TRUE(ax::is_odd(7u));
    EXPECT_FALSE(ax::is_odd(0u));
    EXPECT_FALSE(ax::is_odd(2u));
    EXPECT_FALSE(ax::is_odd(100u));
}

TEST(BitTest, IsPowerOfTwo) {
    EXPECT_TRUE(ax::is_power_of_two(1u));
    EXPECT_TRUE(ax::is_power_of_two(2u));
    EXPECT_TRUE(ax::is_power_of_two(4u));
    EXPECT_TRUE(ax::is_power_of_two(8u));
    EXPECT_TRUE(ax::is_power_of_two(1024u));
    EXPECT_TRUE(ax::is_power_of_two(1u << 30));
    EXPECT_FALSE(ax::is_power_of_two(0u));
    EXPECT_FALSE(ax::is_power_of_two(3u));
    EXPECT_FALSE(ax::is_power_of_two(6u));
    EXPECT_FALSE(ax::is_power_of_two(18u));
    EXPECT_FALSE(ax::is_power_of_two((1u << 30) + 1));
}

TEST(BitTest, Lowbit) {
    EXPECT_EQ(ax::lowbit(0u), 0u);
    EXPECT_EQ(ax::lowbit(1u), 1u);
    EXPECT_EQ(ax::lowbit(2u), 2u);
    EXPECT_EQ(ax::lowbit(12u), 4u);   // 0b1100 → 0b0100
    EXPECT_EQ(ax::lowbit(40u), 8u);   // 0b101000 → 0b001000
}

TEST(BitTest, ClearLowbit) {
    EXPECT_EQ(ax::clear_lowbit(0u), 0u);
    EXPECT_EQ(ax::clear_lowbit(0b1010u), 0b1000u);
    EXPECT_EQ(ax::clear_lowbit(0b1111u), 0b1110u);
    EXPECT_EQ(ax::clear_lowbit(0b1100u), 0b1000u);
    // Verify popcount decreases by exactly 1
    unsigned int x = 0xDEADBEEF;
    EXPECT_EQ(ax::popcount_bk(ax::clear_lowbit(x)), ax::popcount_bk(x) - 1);
}

TEST(BitTest, PopcountBK) {
    EXPECT_EQ(ax::popcount_bk(0u), 0);
    EXPECT_EQ(ax::popcount_bk(1u), 1);
    EXPECT_EQ(ax::popcount_bk(0xFFu), 8);
    EXPECT_EQ(ax::popcount_bk(0xFFFFFFFFu), 32);
    EXPECT_EQ(ax::popcount_bk(0xAAAAAAAAu), 16);
}

TEST(BitTest, Popcount) {
    EXPECT_EQ(ax::popcount_bk(static_cast<uint32_t>(0)), 0);
    EXPECT_EQ(ax::popcount_bk(static_cast<uint32_t>(1)), 1);
    EXPECT_EQ(ax::popcount_bk(static_cast<uint32_t>(0xFFFFFFFF)), 32);
    EXPECT_EQ(ax::popcount_bk(static_cast<uint64_t>(0)), 0);
    EXPECT_EQ(ax::popcount_bk(static_cast<uint64_t>(0xFFFFFFFFFFFFFFFFull)), 64);
}

TEST(BitTest, SetBit) {
    EXPECT_EQ(ax::set_bit(0u, 0), 1u);
    EXPECT_EQ(ax::set_bit(0u, 3), 8u);
    EXPECT_EQ(ax::set_bit(5u, 1), 7u);  // 0b101 → 0b111
}

TEST(BitTest, ClearBit) {
    EXPECT_EQ(ax::clear_bit(8u, 3), 0u);
    EXPECT_EQ(ax::clear_bit(7u, 0), 6u);  // 0b111 → 0b110
    EXPECT_EQ(ax::clear_bit(0u, 5), 0u);  // already clear
}

TEST(BitTest, ToggleBit) {
    EXPECT_EQ(ax::toggle_bit(0u, 0), 1u);
    EXPECT_EQ(ax::toggle_bit(1u, 0), 0u);
    EXPECT_EQ(ax::toggle_bit(0b101u, 1), 0b111u);
}

TEST(BitTest, TestBit) {
    EXPECT_TRUE(ax::test_bit(0b1010u, 1));
    EXPECT_FALSE(ax::test_bit(0b1010u, 0));
    EXPECT_TRUE(ax::test_bit(0b1010u, 3));
    EXPECT_FALSE(ax::test_bit(0x80000000u, 30));
    EXPECT_TRUE(ax::test_bit(0x80000000u, 31));
}

TEST(BitTest, EnumerateSubsets) {
    std::set<unsigned int> masks;
    ax::enumerate_subsets(3, [&](unsigned int mask) { masks.insert(mask); });
    EXPECT_EQ(masks.size(), 8u);
    for (unsigned int i = 0; i < 8; ++i) {
        EXPECT_TRUE(masks.count(i)) << "Missing mask " << i;
    }
}
