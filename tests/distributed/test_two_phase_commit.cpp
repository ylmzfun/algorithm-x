#include "algorithm_x/distributed/two_phase_commit.h"

#include "gtest/gtest.h"

using namespace algorithm_x::distributed;

namespace {

TEST(TwoPhaseCommit, AllVoteYes) {
    TwoPhaseCommit tpc(3);
    EXPECT_TRUE(tpc.commit({true, true, true}));
    EXPECT_EQ(tpc.participant_state(0), TwoPhaseCommit::kCommitted);
    EXPECT_EQ(tpc.participant_state(1), TwoPhaseCommit::kCommitted);
    EXPECT_EQ(tpc.participant_state(2), TwoPhaseCommit::kCommitted);
}

// 任一参与者反对 → 全部回滚。
TEST(TwoPhaseCommit, OneVoteNoAbortsAll) {
    TwoPhaseCommit tpc(3);
    EXPECT_FALSE(tpc.commit({true, false, true}));
    EXPECT_EQ(tpc.participant_state(0), TwoPhaseCommit::kAborted);
    EXPECT_EQ(tpc.participant_state(1), TwoPhaseCommit::kAborted);
    EXPECT_EQ(tpc.participant_state(2), TwoPhaseCommit::kAborted);
}

// 状态枚举与数值约定：0=INITIAL, 1=PREPARED, 2=COMMITTED, 3=ABORTED。
TEST(TwoPhaseCommit, StateEnumValues) {
    TwoPhaseCommit tpc(2);
    EXPECT_EQ(TwoPhaseCommit::kInitial, 0);
    EXPECT_EQ(TwoPhaseCommit::kPrepared, 1);
    EXPECT_EQ(TwoPhaseCommit::kCommitted, 2);
    EXPECT_EQ(TwoPhaseCommit::kAborted, 3);
    EXPECT_EQ(tpc.participant_state(0), TwoPhaseCommit::kInitial);
    EXPECT_EQ(tpc.participant_state(1), TwoPhaseCommit::kInitial);
}

// 票数不足（缺失投票视为反对）→ 中止。
TEST(TwoPhaseCommit, MissingVoteAborts) {
    TwoPhaseCommit tpc(3);
    EXPECT_FALSE(tpc.commit({true}));
    EXPECT_EQ(tpc.participant_state(0), TwoPhaseCommit::kAborted);
    EXPECT_EQ(tpc.participant_state(2), TwoPhaseCommit::kAborted);
}

}  // namespace
