#include "algorithm_x/distributed/gossip.h"
#include "gtest/gtest.h"
using namespace algorithm_x::distributed;
namespace {
TEST(Gossip, Spreads) {
    int rounds=gossip_protocol(10,2);
    EXPECT_GT(rounds,0);
}
}  // namespace
