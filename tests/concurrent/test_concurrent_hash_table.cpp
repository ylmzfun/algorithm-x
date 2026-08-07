#include "algorithm_x/concurrent/concurrent_hash_table.h"
#include "gtest/gtest.h"
using namespace algorithm_x::concurrent;
namespace {
TEST(ConcurrentHashTable, InsertFind) {
    ConcurrentHashTable<int,std::string> ht;
    ht.insert(1,"one"); ht.insert(2,"two");
    EXPECT_EQ(*ht.find(1),"one"); EXPECT_EQ(ht.find(3),nullptr);
}
}  // namespace
