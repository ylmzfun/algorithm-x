#include "ds/trie.h"

#include <gtest/gtest.h>

using algorithm_x::ds::Trie;

TEST(TrieTest, InsertAndSearchSingleWord) {
    Trie trie;
    trie.insert("hello");
    EXPECT_TRUE(trie.search("hello"));
    EXPECT_FALSE(trie.search("hell"));
    EXPECT_FALSE(trie.search("helloo"));
}

TEST(TrieTest, InsertMultipleWordsWithSharedPrefix) {
    Trie trie;
    trie.insert("app");
    trie.insert("apple");
    trie.insert("apply");

    EXPECT_TRUE(trie.search("app"));
    EXPECT_TRUE(trie.search("apple"));
    EXPECT_TRUE(trie.search("apply"));
    EXPECT_FALSE(trie.search("appl"));
}

TEST(TrieTest, SearchNonExistentWord) {
    Trie trie;
    trie.insert("cat");
    EXPECT_FALSE(trie.search("dog"));
    EXPECT_FALSE(trie.search("cats"));
    EXPECT_FALSE(trie.search("ca"));
}

TEST(TrieTest, StartsWithFullWord) {
    Trie trie;
    trie.insert("algorithm");
    EXPECT_TRUE(trie.starts_with("algo"));
    EXPECT_TRUE(trie.starts_with("algorithm"));
    EXPECT_FALSE(trie.starts_with("algorithms"));
}

TEST(TrieTest, StartsWithPrefix) {
    Trie trie;
    trie.insert("prefix");
    EXPECT_TRUE(trie.starts_with("pre"));
    EXPECT_TRUE(trie.starts_with("prefix"));
    EXPECT_TRUE(trie.starts_with("pref"));
    EXPECT_FALSE(trie.starts_with("prefiy"));
}

TEST(TrieTest, StartsWithNonExistent) {
    Trie trie;
    trie.insert("hello");
    EXPECT_FALSE(trie.starts_with("x"));
    EXPECT_FALSE(trie.starts_with("hellx"));
}

TEST(TrieTest, EmptyString) {
    Trie trie;
    trie.insert("");
    EXPECT_TRUE(trie.search(""));
    EXPECT_TRUE(trie.starts_with(""));
}
