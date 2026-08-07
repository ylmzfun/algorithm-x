#include "algorithm_x/graph/hamiltonian.h"
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(Hamiltonian, Path) {
    std::vector<std::vector<bool>> adj(3,std::vector<bool>(3,false));
    adj[0][1]=adj[1][2]=true;
    auto p=hamiltonian_path(adj);
    EXPECT_GE(p.size(),2u);
}
}  // namespace
