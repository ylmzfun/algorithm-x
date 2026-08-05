#include "algorithm_x/advanced/rmq_lca.h"

#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::advanced;

namespace {

// ============================================================
// SparseTable
// ============================================================

TEST(SparseTable, SingleElement) {
    SparseTable<int> st({42});
    EXPECT_EQ(st.query(0, 0), 42);
}

TEST(SparseTable, FullRange) {
    std::vector<int> arr = {5, 2, 8, 1, 9, 3};
    SparseTable<int> st(arr);
    EXPECT_EQ(st.query(0, 5), 1);
}

TEST(SparseTable, PartialRange) {
    std::vector<int> arr = {5, 2, 8, 1, 9, 3};
    SparseTable<int> st(arr);
    EXPECT_EQ(st.query(1, 3), 1);  // {2, 8, 1}
    EXPECT_EQ(st.query(0, 2), 2);  // {5, 2, 8}
    EXPECT_EQ(st.query(3, 5), 1);  // {1, 9, 3}
}

TEST(SparseTable, MultipleQueries) {
    std::vector<int> arr = {7, 3, 5, 2, 6, 1, 4};
    SparseTable<int> st(arr);
    EXPECT_EQ(st.query(0, 6), 1);
    EXPECT_EQ(st.query(0, 3), 2);
    EXPECT_EQ(st.query(2, 5), 1);
    EXPECT_EQ(st.query(4, 6), 1);
    EXPECT_EQ(st.query(0, 0), 7);
}

TEST(SparseTable, ConsistentResults) {
    std::vector<int> arr = {10, 20, 15, 5, 25, 30};
    SparseTable<int> st(arr);
    for (std::size_t i = 0; i < arr.size(); ++i) {
        for (std::size_t j = i; j < arr.size(); ++j) {
            int expected = *std::min_element(arr.begin() + static_cast<long>(i),
                                              arr.begin() + static_cast<long>(j) + 1);
            EXPECT_EQ(st.query(i, j), expected);
        }
    }
}

// ============================================================
// LCA
// ============================================================

TEST(LCA, PathGraph) {
    // 0 - 1 - 2
    std::vector<std::vector<std::size_t>> adj(3);
    adj[0].push_back(1);
    adj[1].push_back(0);
    adj[1].push_back(2);
    adj[2].push_back(1);

    LCA lca(adj, 0);
    EXPECT_EQ(lca.query(0, 0), std::size_t{0});
    EXPECT_EQ(lca.query(0, 1), std::size_t{0});
    EXPECT_EQ(lca.query(1, 2), std::size_t{1});
    EXPECT_EQ(lca.query(0, 2), std::size_t{0});
}

TEST(LCA, StarGraph) {
    // 0 (center), leaves: 1, 2, 3
    std::vector<std::vector<std::size_t>> adj(4);
    for (std::size_t i = 1; i < 4; ++i) {
        adj[0].push_back(i);
        adj[i].push_back(0);
    }

    LCA lca(adj, 0);
    EXPECT_EQ(lca.query(1, 2), std::size_t{0});
    EXPECT_EQ(lca.query(1, 3), std::size_t{0});
    EXPECT_EQ(lca.query(2, 3), std::size_t{0});
}

TEST(LCA, DeepTree) {
    //     0
    //    / \
    //   1   2
    //  / \   \
    // 3   4   5
    //         |
    //         6
    std::vector<std::vector<std::size_t>> adj(7);
    adj[0].push_back(1); adj[1].push_back(0);
    adj[0].push_back(2); adj[2].push_back(0);
    adj[1].push_back(3); adj[3].push_back(1);
    adj[1].push_back(4); adj[4].push_back(1);
    adj[2].push_back(5); adj[5].push_back(2);
    adj[5].push_back(6); adj[6].push_back(5);

    LCA lca(adj, 0);
    EXPECT_EQ(lca.query(3, 4), std::size_t{1});
    EXPECT_EQ(lca.query(3, 6), std::size_t{0});
    EXPECT_EQ(lca.query(4, 5), std::size_t{0});
    EXPECT_EQ(lca.query(5, 6), std::size_t{5});
    EXPECT_EQ(lca.query(3, 2), std::size_t{0});
}

TEST(LCA, SingleNode) {
    std::vector<std::vector<std::size_t>> adj(1);
    LCA lca(adj, 0);
    EXPECT_EQ(lca.query(0, 0), std::size_t{0});
}

}  // namespace
