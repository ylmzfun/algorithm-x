#include "algorithm_x/advanced/link_cut_tree.h"

#include <vector>

#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(LinkCutTree, LinkAndConnectivity) {
    LinkCutTree lct(5);
    EXPECT_FALSE(lct.connected(0, 1));
    lct.link(0, 1);
    EXPECT_TRUE(lct.connected(0, 1));
    lct.link(1, 2);
    lct.link(3, 4);
    EXPECT_TRUE(lct.connected(0, 2));
    EXPECT_FALSE(lct.connected(0, 3));  // 两棵树未连通
    EXPECT_TRUE(lct.connected(3, 4));
    EXPECT_TRUE(lct.connected(2, 2));  // 自身恒连通
}

TEST(LinkCutTree, PathSumOnChain) {
    // 链 0-1-2-3-4，点权 1..5，验证路径和。
    LinkCutTree lct(5);
    lct.link(0, 1);
    lct.link(1, 2);
    lct.link(2, 3);
    lct.link(3, 4);
    for (int i = 0; i < 5; ++i) lct.set_value(i, i + 1);
    EXPECT_EQ(lct.path_query(0, 4), 15);  // 1+2+3+4+5
    EXPECT_EQ(lct.path_query(1, 3), 9);   // 2+3+4
    EXPECT_EQ(lct.path_query(2, 2), 3);   // 单点
    EXPECT_EQ(lct.value(2), 3);
    EXPECT_EQ(lct.value(4), 5);
}

TEST(LinkCutTree, MakerootChangesRoot) {
    // 链 0-1-2-3-4（每次把新点连到前面的点上，根保持为 0），
    // makeroot(4) 后整棵树的根变为 4。
    LinkCutTree lct(5);
    lct.link(1, 0);
    lct.link(2, 1);
    lct.link(3, 2);
    lct.link(4, 3);
    EXPECT_EQ(lct.findroot(0), 0);
    EXPECT_EQ(lct.findroot(4), 0);
    lct.makeroot(4);
    EXPECT_EQ(lct.findroot(0), 4);
    EXPECT_EQ(lct.findroot(2), 4);
    EXPECT_EQ(lct.findroot(4), 4);
    // 换根后路径查询仍然正确。
    for (int i = 0; i < 5; ++i) lct.set_value(i, i + 1);
    EXPECT_EQ(lct.path_query(4, 0), 15);  // 5+4+3+2+1
    EXPECT_EQ(lct.path_query(1, 3), 9);   // 2+3+4
}

TEST(LinkCutTree, CutDisconnects) {
    // 链 0-1-2-3-4，点权 1..5，切断 2-3 后验证连通性与路径和。
    LinkCutTree lct(5);
    lct.link(0, 1);
    lct.link(1, 2);
    lct.link(2, 3);
    lct.link(3, 4);
    for (int i = 0; i < 5; ++i) lct.set_value(i, i + 1);
    lct.cut(2, 3);
    EXPECT_FALSE(lct.connected(2, 3));
    EXPECT_TRUE(lct.connected(1, 2));
    EXPECT_TRUE(lct.connected(3, 4));
    EXPECT_EQ(lct.path_query(1, 2), 5);  // 2+3
    EXPECT_EQ(lct.path_query(3, 4), 9);  // 4+5
    // 重新连接后恢复。
    lct.link(2, 3);
    EXPECT_TRUE(lct.connected(0, 4));
    EXPECT_EQ(lct.path_query(0, 4), 15);
}

TEST(LinkCutTree, PathSumOnStar) {
    // 星形：0 为中心连 1、2、3，验证跨中心路径和。
    LinkCutTree lct(4);
    lct.link(0, 1);
    lct.link(0, 2);
    lct.link(0, 3);
    lct.set_value(0, 10);
    lct.set_value(1, 20);
    lct.set_value(2, 30);
    lct.set_value(3, 40);
    EXPECT_EQ(lct.path_query(1, 2), 60);  // 20+10+30
    EXPECT_EQ(lct.path_query(1, 3), 70);  // 20+10+40
    EXPECT_EQ(lct.path_query(0, 3), 50);  // 10+40
    lct.cut(0, 2);
    EXPECT_FALSE(lct.connected(0, 2));
    EXPECT_TRUE(lct.connected(0, 1));
    EXPECT_TRUE(lct.connected(0, 3));
}
}  // namespace
