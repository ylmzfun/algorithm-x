#include "algorithm_x/ai/mdp.h"
#include "gtest/gtest.h"
using namespace algorithm_x::ai;
namespace {
TEST(MDP, ValueIteration) {
    std::vector<std::vector<std::vector<double>>> T(2,std::vector<std::vector<double>>(2,std::vector<double>(2,0)));
    T[0][0][0]=1; T[0][1][1]=1; T[1][0][0]=1; T[1][1][1]=1;
    std::vector<std::vector<double>> R(2,std::vector<double>(2,0));
    R[1][0]=10;
    auto V=value_iteration(T,R,0.9,1e-6);
    EXPECT_GT(V[1],V[0]);
}
}  // namespace
