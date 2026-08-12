#include "algorithm_x/algo/approximation.h"

#include <algorithm>
#include <bit>
#include <cstddef>
#include <utility>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::algo;

namespace {

// 暴力枚举所有顶点子集求最优顶点覆盖大小，作为 2-近似的下界基准。
int brute_force_vertex_cover_opt(const std::vector<std::pair<int, int>>& edges,
                                 int num_vertices) {
    int best = num_vertices + 1;
    for (int mask = 0; mask < (1 << num_vertices); ++mask) {
        bool covers = true;
        for (const auto& [u, v] : edges) {
            if ((mask & (1 << u)) == 0 && (mask & (1 << v)) == 0) {
                covers = false;
                break;
            }
        }
        if (covers) {
            best = std::min(best, std::popcount(static_cast<unsigned>(mask)));
        }
    }
    return best;
}

// 按与 vertex_cover_approx 相同的贪心规则重建覆盖集合（用于验证确实覆盖所有边）。
int rebuild_greedy_cover(const std::vector<std::pair<int, int>>& edges,
                         int num_vertices, std::vector<char>* in_cover_out) {
    std::vector<char> removed(edges.size(), 0);
    std::vector<char>& in_cover = *in_cover_out;
    in_cover.assign(static_cast<std::size_t>(num_vertices), 0);
    int size = 0;
    for (std::size_t i = 0; i < edges.size(); ++i) {
        if (removed[i]) {
            continue;
        }
        const int u = edges[i].first;
        const int v = edges[i].second;
        if (!in_cover[static_cast<std::size_t>(u)]) {
            in_cover[static_cast<std::size_t>(u)] = 1;
            ++size;
        }
        if (!in_cover[static_cast<std::size_t>(v)]) {
            in_cover[static_cast<std::size_t>(v)] = 1;
            ++size;
        }
        for (std::size_t j = 0; j < edges.size(); ++j) {
            if (removed[j]) {
                continue;
            }
            const int a = edges[j].first;
            const int b = edges[j].second;
            if (a == u || b == u || a == v || b == v) {
                removed[j] = 1;
            }
        }
    }
    return size;
}

TEST(GreedySetCover, CoversWholeUniverse) {
    const std::vector<std::vector<std::size_t>> sets = {
        {0, 1, 2}, {1, 3, 4}, {2, 4}
    };
    const std::size_t universe = 5;
    const auto chosen = greedy_set_cover(sets, universe);
    ASSERT_EQ(chosen.size(), 2u);
    EXPECT_EQ(chosen[0], 0u);
    EXPECT_EQ(chosen[1], 1u);
    std::vector<bool> covered(universe, false);
    for (const std::size_t s : chosen) {
        for (const std::size_t e : sets[s]) {
            covered[e] = true;
        }
    }
    for (std::size_t i = 0; i < universe; ++i) {
        EXPECT_TRUE(covered[i]);  // 选中的集合覆盖全部元素
    }
}

TEST(GreedySetCover, UncoveredElementStillTerminates) {
    const std::vector<std::vector<std::size_t>> sets = {{0, 1}, {2}};
    const std::size_t universe = 4;  // 元素 3 不被任何集合覆盖
    const auto chosen = greedy_set_cover(sets, universe);
    ASSERT_EQ(chosen.size(), 2u);
    std::vector<bool> covered(universe, false);
    for (const std::size_t s : chosen) {
        for (const std::size_t e : sets[s]) {
            covered[e] = true;
        }
    }
    EXPECT_TRUE(covered[0]);
    EXPECT_TRUE(covered[1]);
    EXPECT_TRUE(covered[2]);
    EXPECT_FALSE(covered[3]);  // 无法覆盖的元素由调用方自行判断
}

TEST(GreedySetCover, DuplicateSetsPickedOnePerRound) {
    // 两个完全相同的集合：每轮只选一个（平局取小下标），全集覆盖后即终止
    const std::vector<std::vector<std::size_t>> sets = {{0, 1}, {0, 1}, {2}};
    const auto chosen = greedy_set_cover(sets, 3);
    ASSERT_EQ(chosen.size(), 2u);
    EXPECT_EQ(chosen[0], 0u);
    EXPECT_EQ(chosen[1], 2u);
    std::vector<bool> covered(3, false);
    for (const std::size_t s : chosen) {
        for (const std::size_t e : sets[s]) {
            covered[e] = true;
        }
    }
    EXPECT_TRUE(covered[0]);
    EXPECT_TRUE(covered[1]);
    EXPECT_TRUE(covered[2]);
}

TEST(GreedySetCover, EmptySets) {
    const std::vector<std::vector<std::size_t>> sets;
    EXPECT_TRUE(greedy_set_cover(sets, 3).empty());
    EXPECT_TRUE(greedy_set_cover(sets, 0).empty());
}

TEST(VertexCoverApprox, PathOfFour) {
    // 路径 0-1-2-3：贪心取 (0,1) 与 (2,3)，覆盖大小 4；最优为 {1,2}，大小 2
    const std::vector<std::pair<int, int>> edges = {{0, 1}, {1, 2}, {2, 3}};
    EXPECT_EQ(vertex_cover_approx(edges, 4), 4);
    EXPECT_LE(vertex_cover_approx(edges, 4), 2 * brute_force_vertex_cover_opt(edges, 4));
}

TEST(VertexCoverApprox, StarGraph) {
    // 星形图：贪心取 (0,1) 后所有边都被删除，覆盖大小 2；最优为 {0}，大小 1
    const std::vector<std::pair<int, int>> edges = {{0, 1}, {0, 2}, {0, 3}};
    EXPECT_EQ(vertex_cover_approx(edges, 4), 2);
    EXPECT_LE(vertex_cover_approx(edges, 4), 2 * brute_force_vertex_cover_opt(edges, 4));
}

TEST(VertexCoverApprox, Triangle) {
    // 三角形：贪心取 (0,1) 后所有边都被删除，覆盖大小 2；最优也是 2
    const std::vector<std::pair<int, int>> edges = {{0, 1}, {1, 2}, {0, 2}};
    EXPECT_EQ(vertex_cover_approx(edges, 3), 2);
    EXPECT_EQ(brute_force_vertex_cover_opt(edges, 3), 2);
}

TEST(VertexCoverApprox, WithinTwoOptOnSmallGraphs) {
    // 最优覆盖为 {1,2,4}（大小 3），贪心覆盖全部 6 个顶点（大小 6），6 <= 2*3
    const std::vector<std::pair<int, int>> edges = {
        {0, 1}, {0, 2}, {1, 2}, {2, 3}, {3, 4}, {4, 5}
    };
    const int opt = brute_force_vertex_cover_opt(edges, 6);
    const int got = vertex_cover_approx(edges, 6);
    EXPECT_EQ(opt, 3);
    EXPECT_EQ(got, 6);
    EXPECT_GE(got, opt);
    EXPECT_LE(got, 2 * opt);
}

TEST(VertexCoverApprox, ReconstructedCoverCoversAllEdges) {
    const std::vector<std::pair<int, int>> edges = {
        {0, 1}, {0, 2}, {1, 2}, {2, 3}, {3, 4}, {4, 5}
    };
    const int got = vertex_cover_approx(edges, 6);
    std::vector<char> in_cover;
    const int rebuilt = rebuild_greedy_cover(edges, 6, &in_cover);
    EXPECT_EQ(rebuilt, got);
    for (const auto& [u, v] : edges) {
        EXPECT_TRUE(in_cover[static_cast<std::size_t>(u)] ||
                    in_cover[static_cast<std::size_t>(v)]);
    }
}

TEST(VertexCoverApprox, EmptyEdges) {
    const std::vector<std::pair<int, int>> edges;
    EXPECT_EQ(vertex_cover_approx(edges, 4), 0);
}

}  // namespace
