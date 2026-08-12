#include "string/string_match.h"

#include <string>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::string;

namespace {

// ============================================================
// KMP
// ============================================================

TEST(KmpSearch, BasicMatch) {
    auto pos = kmp_search("ababc", "ab");
    std::vector<std::size_t> expected = {0, 2};
    EXPECT_EQ(pos, expected);
}

TEST(KmpSearch, NotFound) {
    auto pos = kmp_search("abcdef", "xyz");
    EXPECT_TRUE(pos.empty());
}

TEST(KmpSearch, PatternLargerThanText) {
    auto pos = kmp_search("ab", "abcdef");
    EXPECT_TRUE(pos.empty());
}

TEST(KmpSearch, EmptyPattern) {
    auto pos = kmp_search("abcdef", "");
    EXPECT_TRUE(pos.empty());
}

TEST(KmpSearch, EmptyTextEmptyPattern) {
    auto pos = kmp_search("", "");
    EXPECT_TRUE(pos.empty());
}

TEST(KmpSearch, OverlappingMatches) {
    auto pos = kmp_search("aaaaa", "aa");
    std::vector<std::size_t> expected = {0, 1, 2, 3};
    EXPECT_EQ(pos, expected);
}

TEST(KmpSearch, SingleCharMatch) {
    auto pos = kmp_search("abcabc", "b");
    std::vector<std::size_t> expected = {1, 4};
    EXPECT_EQ(pos, expected);
}

TEST(KmpSearch, FullMatch) {
    auto pos = kmp_search("hello", "hello");
    std::vector<std::size_t> expected = {0};
    EXPECT_EQ(pos, expected);
}

// ============================================================
// Rabin-Karp
// ============================================================

TEST(RabinKarp, BasicMatch) {
    auto pos = rabin_karp("ababc", "ab");
    std::vector<std::size_t> expected = {0, 2};
    EXPECT_EQ(pos, expected);
}

TEST(RabinKarp, NotFound) {
    auto pos = rabin_karp("abcdef", "xyz");
    EXPECT_TRUE(pos.empty());
}

TEST(RabinKarp, PatternLargerThanText) {
    auto pos = rabin_karp("ab", "abcdef");
    EXPECT_TRUE(pos.empty());
}

TEST(RabinKarp, EmptyPattern) {
    auto pos = rabin_karp("abcdef", "");
    EXPECT_TRUE(pos.empty());
}

TEST(RabinKarp, OverlappingMatches) {
    auto pos = rabin_karp("aaaaa", "aa");
    std::vector<std::size_t> expected = {0, 1, 2, 3};
    EXPECT_EQ(pos, expected);
}

TEST(RabinKarp, FullMatch) {
    auto pos = rabin_karp("hello", "hello");
    std::vector<std::size_t> expected = {0};
    EXPECT_EQ(pos, expected);
}

TEST(RabinKarp, HashCollisionResistant) {
    // Verify no false positives on a longer string
    std::string text = "abcabdabexyz";
    auto pos = rabin_karp(text, "abe");
    std::vector<std::size_t> expected = {6};
    EXPECT_EQ(pos, expected);
}

// ============================================================
// Z-function
// ============================================================

TEST(ZFunction, AllSameChars) {
    auto z = z_function("aaaaa");
    std::vector<std::size_t> expected = {0, 4, 3, 2, 1};
    EXPECT_EQ(z, expected);
}

TEST(ZFunction, AlternatingPattern) {
    auto z = z_function("abacaba");
    std::vector<std::size_t> expected = {0, 0, 1, 0, 3, 0, 1};
    EXPECT_EQ(z, expected);
}

TEST(ZFunction, SingleChar) {
    auto z = z_function("a");
    std::vector<std::size_t> expected = {0};
    EXPECT_EQ(z, expected);
}

TEST(ZFunction, EmptyString) {
    auto z = z_function("");
    EXPECT_TRUE(z.empty());
}

TEST(ZFunction, NoPrefixMatch) {
    auto z = z_function("abcdef");
    std::vector<std::size_t> expected = {0, 0, 0, 0, 0, 0};
    EXPECT_EQ(z, expected);
}

}  // namespace
