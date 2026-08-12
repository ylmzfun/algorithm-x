#include "distributed/consensus.h"

#include "gtest/gtest.h"

using namespace algorithm_x::distributed;

namespace {

TEST(Paxos, AchievesConsensus) {
    Paxos p(3);
    EXPECT_TRUE(p.propose(1, 7));
    EXPECT_EQ(p.chosen_value(), 7);
    EXPECT_EQ(p.num_acceptors(), 3u);
}

// 对已共识的值重新提案（更高提案号）：多数派已接受 7，
// 新提案必须采纳 7，共识结果保持不变。
TEST(Paxos, HigherProposalAdoptsChosenValue) {
    Paxos p(3);
    EXPECT_TRUE(p.propose(1, 7));
    EXPECT_TRUE(p.propose(2, 8));
    EXPECT_EQ(p.chosen_value(), 7);
}

// 相同提案号不高于已承诺号，无法获得承诺。
TEST(Paxos, StaleProposalRejected) {
    Paxos p(3);
    EXPECT_TRUE(p.propose(1, 7));
    EXPECT_FALSE(p.propose(1, 9));
    EXPECT_EQ(p.chosen_value(), 7);
}

// 单接受者无法构成多数派，不能达成共识。
TEST(Paxos, SingleAcceptorNoConsensus) {
    Paxos p(1);
    EXPECT_FALSE(p.propose(1, 5));
    EXPECT_EQ(p.chosen_value(), -1);
}

}  // namespace
