#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace distributed {

// 两阶段提交（2PC）教学实现。
//
// 协议流程：
//   阶段一（准备/投票）：协调者向所有参与者发送"准备"请求；
//     参与者各自投票（赞成则进入 PREPARED 状态），并把结果返回协调者。
//   阶段二（决定）：若全部赞成，协调者广播"提交"，所有参与者提交（COMMITTED）；
//     若任一反对，协调者广播"中止"，所有参与者回滚（ABORTED）。
//
// 局限（与真实系统一致）：
//   - 阻塞问题：若协调者在阶段二之前故障，参与者会一直等待决定而阻塞，
//     因此 2PC 是阻塞协议，无法在协调者故障时自动恢复；
//   - 单点故障：协调者故障会使整个事务悬而未决；
//   - 本模拟假设消息同步可靠，未模拟参与者故障与超时。
class TwoPhaseCommit {
public:
    // 参与者状态：0=INITIAL, 1=PREPARED, 2=COMMITTED, 3=ABORTED。
    enum State {
        kInitial = 0,
        kPrepared = 1,
        kCommitted = 2,
        kAborted = 3,
    };

    explicit TwoPhaseCommit(std::size_t num_participants)
        : states_(num_participants, kInitial) {}

    // 执行一轮两阶段提交。participant_votes[i] 为第 i 个参与者的投票
    // （true=赞成，false=反对）。若票数少于参与者数量，缺失的投票视为反对，
    // 保证不会在信息不全时提交。
    bool commit(const std::vector<bool>& participant_votes) {
        // 阶段一：准备。赞成者进入 PREPARED，反对者保持 INITIAL。
        bool all_yes = true;
        for (std::size_t i = 0; i < states_.size(); ++i) {
            bool vote = i < participant_votes.size() && participant_votes[i];
            if (vote) {
                states_[i] = kPrepared;
            } else {
                all_yes = false;
            }
        }

        // 阶段二：决定。全部赞成则提交，否则中止（回滚）。
        State final_state = all_yes ? kCommitted : kAborted;
        for (std::size_t i = 0; i < states_.size(); ++i) {
            states_[i] = final_state;
        }
        return all_yes;
    }

    // 返回第 i 个参与者的状态；越界访问返回 INITIAL。
    int participant_state(std::size_t i) const {
        return i < states_.size() ? static_cast<int>(states_[i]) : kInitial;
    }

    std::size_t num_participants() const { return states_.size(); }

private:
    std::vector<State> states_;
};

}  // namespace distributed
}  // namespace algorithm_x
