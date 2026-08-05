#include "algorithm_x/string/edit_distance.h"

#include <string>

#include "gtest/gtest.h"

using namespace algorithm_x::string;

namespace {

TEST(EditDistance, KittenToSitting) {
    EXPECT_EQ(edit_distance("kitten", "sitting"), 3);
}

TEST(EditDistance, SameString) {
    EXPECT_EQ(edit_distance("abc", "abc"), 0);
}

TEST(EditDistance, DeleteAll) {
    EXPECT_EQ(edit_distance("a", ""), 1);
}

TEST(EditDistance, EmptyToEmpty) {
    EXPECT_EQ(edit_distance("", ""), 0);
}

TEST(EditDistance, AllDifferent) {
    EXPECT_EQ(edit_distance("abc", "def"), 3);
}

TEST(EditDistance, IntentionToExecution) {
    EXPECT_EQ(edit_distance("intention", "execution"), 5);
}

TEST(LcsLength, Subsequence) {
    EXPECT_EQ(lcs_length("abcde", "ace"), 3);
}

TEST(LcsLength, SameString) {
    EXPECT_EQ(lcs_length("abc", "abc"), 3);
}

TEST(LcsLength, NoCommon) {
    EXPECT_EQ(lcs_length("abc", "def"), 0);
}

TEST(LcsLength, OneEmpty) {
    EXPECT_EQ(lcs_length("", "abc"), 0);
    EXPECT_EQ(lcs_length("abc", ""), 0);
}

TEST(LcsLength, Another) {
    EXPECT_EQ(lcs_length("abcdef", "acf"), 3);
}

TEST(LcsString, Classic) {
    std::string s = lcs_string("abcde", "ace");
    // s should be a subsequence of both
    EXPECT_EQ(s.size(), 3u);
    // Verify it matches lcs_length
    EXPECT_EQ(s.size(), static_cast<std::size_t>(lcs_length("abcde", "ace")));
}

TEST(LcsString, AGTAB_GTAB) {
    std::string s = lcs_string("AGGTAB", "GXTXAYB");
    EXPECT_EQ(s, "GTAB");
}

TEST(LcsString, Empty) {
    EXPECT_TRUE(lcs_string("", "abc").empty());
    EXPECT_TRUE(lcs_string("abc", "").empty());
}

TEST(LcsString, Same) {
    EXPECT_EQ(lcs_string("hello", "hello"), "hello");
}

}  // namespace
