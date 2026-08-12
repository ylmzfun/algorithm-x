#include "string/aho_corasick.h"

#include <string>
#include <utility>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::string;

namespace {

TEST(AhoCorasick, SinglePattern) {
    AhoCorasick ac;
    int pid = ac.insert("he");
    ac.build();
    auto matches = ac.search("hello");
    ASSERT_EQ(matches.size(), 1u);
    EXPECT_EQ(matches[0].first, pid);
    EXPECT_EQ(matches[0].second, 0u);
}

TEST(AhoCorasick, MultiplePatterns) {
    AhoCorasick ac;
    int she = ac.insert("she");
    int he = ac.insert("he");
    int his = ac.insert("his");
    int hers = ac.insert("hers");
    ac.build();
    auto matches = ac.search("ushers");

    ASSERT_EQ(matches.size(), 3u);
    EXPECT_EQ(matches[0].first, she);
    EXPECT_EQ(matches[0].second, 1u);
    EXPECT_EQ(matches[1].first, he);
    EXPECT_EQ(matches[1].second, 2u);
    EXPECT_EQ(matches[2].first, hers);
    EXPECT_EQ(matches[2].second, 2u);
}

TEST(AhoCorasick, OverlappingPatterns) {
    AhoCorasick ac;
    int a = ac.insert("a");
    int aa = ac.insert("aa");
    int aaa = ac.insert("aaa");
    ac.build();
    auto matches = ac.search("aaaa");

    ASSERT_EQ(matches.size(), 9u);

    int a_count = 0, aa_count = 0, aaa_count = 0;
    for (auto& [pid, pos] : matches) {
        if (pid == a) ++a_count;
        else if (pid == aa) ++aa_count;
        else if (pid == aaa) ++aaa_count;
    }
    EXPECT_EQ(a_count, 4);
    EXPECT_EQ(aa_count, 3);
    EXPECT_EQ(aaa_count, 2);
}

TEST(AhoCorasick, NoMatch) {
    AhoCorasick ac;
    ac.insert("xyz");
    ac.build();
    auto matches = ac.search("abcdef");
    EXPECT_TRUE(matches.empty());
}

TEST(AhoCorasick, EmptyText) {
    AhoCorasick ac;
    ac.insert("a");
    ac.build();
    auto matches = ac.search("");
    EXPECT_TRUE(matches.empty());
}

TEST(AhoCorasick, AdjacentMatches) {
    AhoCorasick ac;
    int ab = ac.insert("ab");
    int bc = ac.insert("bc");
    ac.build();
    auto matches = ac.search("abc");
    ASSERT_EQ(matches.size(), 2u);
    EXPECT_EQ(matches[0].first, ab);
    EXPECT_EQ(matches[0].second, 0u);
    EXPECT_EQ(matches[1].first, bc);
    EXPECT_EQ(matches[1].second, 1u);
}

}  // namespace
