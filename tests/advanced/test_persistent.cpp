#include "advanced/persistent.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(PersistentSegTree, Basic) {
    PersistentSegmentTree pst({1, 2, 3, 4, 5});
    EXPECT_EQ(pst.query(0, 1, 4), 2 + 3 + 4);
}
TEST(PersistentSegTree, Update) {
    PersistentSegmentTree pst({1, 2, 3});
    int v1 = pst.update(0, 1, 10);
    EXPECT_EQ(pst.query(v1, 0, 3), 14);
}
}  // namespace
