#include "algorithm_x/ds/segment_tree.h"

#include <gtest/gtest.h>
#include <vector>

using algorithm_x::ds::SegmentTree;

TEST(SegmentTree, BuildFromVector) {
    SegmentTree<int> st(std::vector<int>{1, 2, 3, 4, 5});
    EXPECT_EQ(st.size(), 5u);
}

TEST(SegmentTree, SingleElementQuery) {
    SegmentTree<int> st(std::vector<int>{7, 3, 9, 2, 1});
    EXPECT_EQ(st.query(0, 1), 7);
    EXPECT_EQ(st.query(2, 3), 9);
    EXPECT_EQ(st.query(4, 5), 1);
}

TEST(SegmentTree, RangeQuery) {
    SegmentTree<int> st(std::vector<int>{1, 2, 3, 4, 5});
    EXPECT_EQ(st.query(0, 5), 15);   // full range
    EXPECT_EQ(st.query(0, 3), 6);     // 1+2+3
    EXPECT_EQ(st.query(1, 4), 9);     // 2+3+4
    EXPECT_EQ(st.query(2, 5), 12);    // 3+4+5
}

TEST(SegmentTree, PointUpdateThenQuery) {
    SegmentTree<int> st(std::vector<int>{1, 2, 3, 4, 5});

    st.update(2, 10);  // {1, 2, 10, 4, 5}
    EXPECT_EQ(st.query(0, 5), 22);
    EXPECT_EQ(st.query(2, 3), 10);
    EXPECT_EQ(st.query(1, 4), 16);  // 2+10+4
}

TEST(SegmentTree, MultipleUpdates) {
    SegmentTree<int> st(std::vector<int>{0, 0, 0, 0, 0});

    st.update(0, 1);
    st.update(1, 2);
    st.update(2, 3);
    st.update(3, 4);
    st.update(4, 5);

    EXPECT_EQ(st.query(0, 5), 15);
    EXPECT_EQ(st.query(0, 3), 6);
    EXPECT_EQ(st.query(3, 5), 9);
}

TEST(SegmentTree, EmptyRange) {
    SegmentTree<int> st(std::vector<int>{1, 2, 3});
    EXPECT_EQ(st.query(1, 1), 0);   // l == r
    EXPECT_EQ(st.query(2, 2), 0);
}

TEST(SegmentTree, LargeArray) {
    std::vector<int> arr(1000, 1);
    SegmentTree<int> st(arr);
    EXPECT_EQ(st.query(0, 1000), 1000);
    EXPECT_EQ(st.query(100, 200), 100);

    st.update(500, 100);
    EXPECT_EQ(st.query(0, 1000), 1000 + 99);  // 999*1 + 100
    EXPECT_EQ(st.query(500, 501), 100);
}

TEST(SegmentTree, AlternatingUpdates) {
    SegmentTree<int> st(std::vector<int>{5, 5, 5, 5});

    st.update(0, 10);
    EXPECT_EQ(st.query(0, 4), 25);  // 10+5+5+5

    st.update(0, 1);
    EXPECT_EQ(st.query(0, 4), 16);  // 1+5+5+5

    st.update(3, 0);
    EXPECT_EQ(st.query(0, 4), 11);  // 1+5+5+0
}
