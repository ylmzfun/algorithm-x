#include "ai/rl_advanced.h"
#include "gtest/gtest.h"
using namespace algorithm_x::ai;
namespace {
TEST(SARSA, Train) {
    std::vector<std::vector<int>> grid={{0,0},{0,2}};
    SARSA agent(grid,0.1,0.9,0.1);
    agent.train(500);
    auto path=agent.get_path(0,0);
    EXPECT_GT(path.size(),0u);
}
}  // namespace
