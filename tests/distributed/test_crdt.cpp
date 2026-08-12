#include "distributed/crdt.h"

#include <cstdint>
#include <string>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::distributed;

namespace {

TEST(GCounter, MergeSumsReplicas) {
    GCounter a(2), b(2);
    a.increment(0, 3);
    a.increment(1, 1);
    b.increment(1, 2);
    a.merge(b);
    b.merge(a);
    // 副本 0：max(3, 0)=3；副本 1：max(1, 2)=2；总和 5。
    EXPECT_EQ(a.value(), 5);
    EXPECT_EQ(b.value(), 5);
    EXPECT_EQ(a.local(0), 3);
    EXPECT_EQ(a.local(1), 2);
}

TEST(GCounter, MergeIsIdempotent) {
    GCounter a(2), b(2);
    a.increment(0);
    b.increment(1, 6);
    a.merge(b);
    int64_t v1 = a.value();
    a.merge(b);  // 重复合并结果不变
    a.merge(b);
    EXPECT_EQ(a.value(), v1);
    EXPECT_EQ(a.value(), 7);
}

TEST(GCounter, DefaultDeltaIsOne) {
    GCounter g(3);
    g.increment(1);
    EXPECT_EQ(g.local(1), 1);
    EXPECT_EQ(g.value(), 1);
}

TEST(ORSet, BasicAddContains) {
    ORSet s;
    s.add("a");
    s.add("b");
    EXPECT_TRUE(s.contains("a"));
    EXPECT_TRUE(s.contains("b"));
    EXPECT_EQ(s.elements().size(), 2u);
}

// 场景一：A 添加 x，B 删除 x，merge 后 x 不存在。
TEST(ORSet, RemoveWinsSequential) {
    ORSet a, b;
    a.add("x");
    b.remove("x");  // B 从未见过 x 的 add 标签 → 记录元素级墓碑
    a.merge(b);
    b.merge(a);
    EXPECT_FALSE(a.contains("x"));
    EXPECT_FALSE(b.contains("x"));
    EXPECT_TRUE(a.elements().empty());
    EXPECT_TRUE(b.elements().empty());
}

// 场景二：A 添加 x、B 也添加 x，A 删除自己的 x 后 merge，x 仍存在
// （B 的 add 标签仍然存活）。
TEST(ORSet, ConcurrentAddSurvivesRemove) {
    ORSet a, b;
    a.add("x");
    b.add("x");
    a.remove("x");  // A 只删除自己 add 的标签
    a.merge(b);
    b.merge(a);
    EXPECT_TRUE(a.contains("x"));
    EXPECT_TRUE(b.contains("x"));
    EXPECT_EQ(a.elements().size(), 1u);
    EXPECT_EQ(a.elements()[0], "x");
}

}  // namespace
