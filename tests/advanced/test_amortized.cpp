#include "advanced/amortized.h"
#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(Amortized, PushCost) {
    auto costs=amortized_push_cost(100);
    EXPECT_EQ(costs.size(),100u);
    double avg=0; for(auto c:costs) avg+=c; avg/=100.0;
    EXPECT_LT(avg,3.0);
}
}  // namespace
