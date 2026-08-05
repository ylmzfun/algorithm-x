#include "algorithm_x/distributed/consistent_hash.h"

#include <set>
#include <string>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::distributed;

namespace {

TEST(ConsistentHash, SingleNode) {
    ConsistentHash ch({"node1"}, 10);
    for (int i = 0; i < 100; ++i) {
        EXPECT_EQ(ch.get_node("key" + std::to_string(i)), "node1");
    }
}

TEST(ConsistentHash, TwoNodesBothUsed) {
    ConsistentHash ch({"nodeA", "nodeB"}, 50);
    std::set<std::string> found;
    for (int i = 0; i < 200; ++i) {
        found.insert(ch.get_node("item" + std::to_string(i)));
    }
    EXPECT_GE(found.size(), 2u);  // both nodes should get some keys
}

TEST(ConsistentHash, AddNode) {
    ConsistentHash ch({"nodeA"}, 30);
    std::size_t before = ch.node_count();
    ch.add_node("nodeB");
    EXPECT_GT(ch.node_count(), before);
}

TEST(ConsistentHash, RemoveNode) {
    ConsistentHash ch({"nodeA", "nodeB"}, 30);
    std::size_t before = ch.node_count();
    ch.remove_node("nodeA");
    EXPECT_LT(ch.node_count(), before);
}

TEST(ConsistentHash, Deterministic) {
    ConsistentHash ch({"X", "Y", "Z"}, 50);
    std::string first = ch.get_node("hello");
    for (int i = 0; i < 50; ++i) {
        EXPECT_EQ(ch.get_node("hello"), first);
    }
}

TEST(ConsistentHash, EmptyRing) {
    ConsistentHash ch({}, 10);
    EXPECT_EQ(ch.get_node("any"), "");
    EXPECT_EQ(ch.node_count(), 0u);
}

}  // namespace
