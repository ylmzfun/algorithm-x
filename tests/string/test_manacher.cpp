#include "string/manacher.h"

#include <string>

#include "gtest/gtest.h"

using namespace algorithm_x::string;

namespace {

TEST(LongestPalindrome, Babad) {
    auto res = longest_palindrome("babad");
    EXPECT_TRUE(res == "bab" || res == "aba");
    EXPECT_EQ(res.size(), 3u);
}

TEST(LongestPalindrome, Cbbd) {
    EXPECT_EQ(longest_palindrome("cbbd"), "bb");
}

TEST(LongestPalindrome, SingleChar) {
    EXPECT_EQ(longest_palindrome("a"), "a");
}

TEST(LongestPalindrome, Empty) {
    EXPECT_EQ(longest_palindrome(""), "");
}

TEST(LongestPalindrome, AllSame) {
    EXPECT_EQ(longest_palindrome("aaaa"), "aaaa");
}

TEST(LongestPalindrome, NoPalindrome) {
    std::string res = longest_palindrome("abcd");
    EXPECT_EQ(res.size(), 1u);
    EXPECT_TRUE(res == "a" || res == "b" || res == "c" || res == "d");
}

TEST(LongestPalindrome, FullWord) {
    EXPECT_EQ(longest_palindrome("racecar"), "racecar");
}

TEST(LongestPalindrome, PalindromeAtStart) {
    auto res = longest_palindrome("abacdfgdcaba");
    EXPECT_EQ(res, "aba");
}

}  // namespace
