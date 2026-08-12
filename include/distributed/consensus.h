#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace distributed {

// Paxos 教学模拟 —— 单值共识，同步消息、无网络故障。
//
// 两阶段协议：
//   阶段一 prepare（准备）：提议者携带提案号 n 向所有接受者广播。
//     接受者若 n 大于自己已承诺的最大提案号，则承诺（此后不再接受更小的提案号），
//     并返回自己已接受的值（若有）。
//   阶段二 accept（接受）：提议者收集多数派承诺。若承诺者中有人已接受过值，
//     则必须采纳其中提案号最高的那个值（保证一致性）；否则使用自己提议的值。
//     随后向该多数派广播 accept(n, v)，多数派接受即达成共识。
//
// 多数派原理：任意两个多数派必有交集，因此不可能有两个不同的值同时被选中，
// 这保证了共识的唯一性。
//
// 与真实 Paxos 的差异（教学简化）：
//   - 只解决单值共识（真实系统通过提案实例序列解决多值问题）；
//   - 同步消息、无网络分区/消息丢失/节点故障；
//   - 接受者只承诺、不会"忘记"承诺，提案号必须严格递增使用。
class Paxos {
public:
    explicit Paxos(std::size_t num_acceptors)
        : promised_(num_acceptors, 0),
          accepted_number_(num_acceptors, 0),
          accepted_value_(num_acceptors, -1),
          chosen_value_(-1) {}

    // 执行一轮 prepare + accept。达成共识返回 true，否则返回 false。
    bool propose(std::size_t proposal_id, int value) {
        // 教学简化：单接受者无法构成多数派，不具备共识意义，直接失败。
        if (num_acceptors() < 2) return false;

        // 阶段一：prepare —— 向所有接受者广播提案号。
        std::vector<std::size_t> promised;  // 本轮做出承诺的接受者
        bool have_accepted = false;         // 承诺者中是否有人已接受过值
        std::size_t highest_number = 0;     // 承诺者中已接受值的最高提案号
        int highest_value = -1;
        for (std::size_t i = 0; i < num_acceptors(); ++i) {
            if (proposal_id > promised_[i]) {
                promised_[i] = proposal_id;  // 承诺
                promised.push_back(i);
                // 该接受者返回已接受的值，记录其中提案号最高的。
                if (accepted_number_[i] > 0 &&
                    (!have_accepted || accepted_number_[i] > highest_number)) {
                    have_accepted = true;
                    highest_number = accepted_number_[i];
                    highest_value = accepted_value_[i];
                }
            }
        }
        // 未获得多数派承诺，本轮失败。
        if (promised.size() < majority()) return false;

        // 阶段二：accept —— 有已接受的值则必须采纳（保证一致性），否则用自己的值。
        int final_value = have_accepted ? highest_value : value;
        for (std::size_t i : promised) {
            accepted_number_[i] = proposal_id;
            accepted_value_[i] = final_value;
        }
        // 已承诺的接受者都会接受（它们已承诺该提案号），构成多数派 → 共识达成。
        chosen_value_ = final_value;
        return true;
    }

    // 被选中的值；未达成共识时返回 -1。
    int chosen_value() const { return chosen_value_; }

    std::size_t num_acceptors() const { return promised_.size(); }

private:
    // 多数派：超过半数的接受者。
    std::size_t majority() const { return num_acceptors() / 2 + 1; }

    std::vector<std::size_t> promised_;         // 每个接受者已承诺的最大提案号
    std::vector<std::size_t> accepted_number_;  // 每个接受者已接受的提案号
    std::vector<int> accepted_value_;           // 每个接受者已接受的值
    int chosen_value_;                          // 已选中的值，-1 表示未达成
};

}  // namespace distributed
}  // namespace algorithm_x
