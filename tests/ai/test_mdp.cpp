#include "algorithm_x/ai/mdp.h"
#include "gtest/gtest.h"
using namespace algorithm_x::ai;
namespace {
// 2 状态 2 动作，确定性转移：
// 状态 0: 动作 0 → 留在 0 (奖励 0)；动作 1 → 去 1 (奖励 0)
// 状态 1: 动作 0 → 留在 1 (奖励 10)；动作 1 → 去 0 (奖励 0)
std::vector<std::vector<std::tuple<int, double, double>>> make_transitions() {
    std::vector<std::vector<std::tuple<int, double, double>>> t(4);
    t[0 * 2 + 0] = {{0, 1.0, 0.0}};
    t[0 * 2 + 1] = {{1, 1.0, 0.0}};
    t[1 * 2 + 0] = {{1, 1.0, 10.0}};
    t[1 * 2 + 1] = {{0, 1.0, 0.0}};
    return t;
}
TEST(MDP, ValueIteration) {
    auto T = make_transitions();
    auto V = value_iteration(T, 2, 2, 0.9, 1e-6);
    // 状态 1 有自循环奖励 10：V[1] = 10 / (1 - 0.9) = 100
    EXPECT_NEAR(V[1], 100.0, 1.0);
    EXPECT_GT(V[1], V[0]);
}
TEST(MDP, PolicyIteration) {
    auto T = make_transitions();
    auto [V, policy] = policy_iteration(T, 2, 2, 0.9);
    EXPECT_GT(V[1], V[0]);
    // 最优策略：状态 1 应选择留在 1（动作 0）
    EXPECT_EQ(policy[1], 0);
}
}  // namespace
