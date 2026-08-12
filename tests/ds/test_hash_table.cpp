#include <gtest/gtest.h>

#include <string>

#include "ds/hash_table.h"

using algorithm_x::ds::HashTable;

TEST(HashTableTest, InsertAndFind) {
    HashTable<int, std::string> ht;
    ht.insert(1, "one");
    ht.insert(2, "two");
    ht.insert(3, "three");

    EXPECT_EQ(*ht.find(1), "one");
    EXPECT_EQ(*ht.find(2), "two");
    EXPECT_EQ(*ht.find(3), "three");
    EXPECT_EQ(ht.find(4), nullptr);
    EXPECT_EQ(ht.size(), 3);
}

TEST(HashTableTest, InsertUpdatesExistingKey) {
    HashTable<int, std::string> ht;
    ht.insert(1, "one");
    ht.insert(1, "ONE");

    EXPECT_EQ(*ht.find(1), "ONE");
    EXPECT_EQ(ht.size(), 1);
}

TEST(HashTableTest, EraseExisting) {
    HashTable<int, int> ht;
    ht.insert(10, 100);
    ht.insert(20, 200);

    EXPECT_TRUE(ht.erase(10));
    EXPECT_FALSE(ht.contains(10));
    EXPECT_TRUE(ht.contains(20));
    EXPECT_EQ(ht.size(), 1);
}

TEST(HashTableTest, EraseNonExisting) {
    HashTable<int, int> ht;
    ht.insert(1, 10);

    EXPECT_FALSE(ht.erase(99));
    EXPECT_EQ(ht.size(), 1);
}

TEST(HashTableTest, Contains) {
    HashTable<std::string, int> ht;
    ht.insert("apple", 1);
    ht.insert("banana", 2);

    EXPECT_TRUE(ht.contains("apple"));
    EXPECT_FALSE(ht.contains("cherry"));
}

TEST(HashTableTest, OperatorBracketRead) {
    HashTable<int, int> ht;
    ht.insert(1, 42);

    EXPECT_EQ(ht[1], 42);
}

TEST(HashTableTest, OperatorBracketInsertDefault) {
    HashTable<int, int> ht;

    EXPECT_EQ(ht[1], 0);
    ht[1] = 99;

    EXPECT_EQ(ht[1], 99);
    EXPECT_EQ(ht.size(), 1);
}

TEST(HashTableTest, RehashOnLoad) {
    HashTable<int, int> ht;
    std::size_t initial_buckets = ht.bucket_count();

    // Insert enough to trigger rehash (load_factor > 0.75)
    for (int i = 0; i < 200; ++i) {
        ht.insert(i, i * 10);
    }

    EXPECT_GT(ht.bucket_count(), initial_buckets);
    EXPECT_EQ(ht.size(), 200);

    // Verify all entries survived rehash
    for (int i = 0; i < 200; ++i) {
        EXPECT_EQ(*ht.find(i), i * 10);
    }
}

TEST(HashTableTest, SizeAndEmpty) {
    HashTable<int, int> ht;
    EXPECT_TRUE(ht.empty());
    EXPECT_EQ(ht.size(), 0);

    ht.insert(1, 10);
    EXPECT_FALSE(ht.empty());
    EXPECT_EQ(ht.size(), 1);

    ht.erase(1);
    EXPECT_TRUE(ht.empty());
}

TEST(HashTableTest, StringKeys) {
    HashTable<std::string, int> ht;
    ht.insert("hello", 1);
    ht.insert("world", 2);

    EXPECT_EQ(*ht.find("hello"), 1);
    EXPECT_EQ(*ht.find("world"), 2);
}
