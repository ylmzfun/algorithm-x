#pragma once

#include <algorithm>
#include <cstddef>
#include <map>
#include <string>
#include <vector>

namespace algorithm_x {
namespace string {

// 后缀自动机 (SAM) — 在线构建，O(n)。
class SuffixAutomaton {
    struct State {
        std::map<char, int> next;
        int link = -1;
        int len = 0;
    };

public:
    void build(const std::string& s) {
        states_.clear();
        states_.reserve(s.size() * 2);
        states_.push_back({});   // state 0 = root
        last_ = 0;

        for (char c : s) extend(c);
    }

    // 判断 t 是否为 s 的子串。
    bool contains(const std::string& t) const {
        int cur = 0;
        for (char c : t) {
            auto it = states_[static_cast<std::size_t>(cur)].next.find(c);
            if (it == states_[static_cast<std::size_t>(cur)].next.end()) {
                return false;
            }
            cur = it->second;
        }
        return true;
    }

    std::size_t state_count() const { return states_.size(); }

private:
    void extend(char c) {
        int cur = static_cast<int>(states_.size());
        states_.push_back({});
        states_[static_cast<std::size_t>(cur)].len =
            states_[static_cast<std::size_t>(last_)].len + 1;

        int p = last_;
        while (p != -1 &&
               states_[static_cast<std::size_t>(p)].next.find(c) ==
                   states_[static_cast<std::size_t>(p)].next.end()) {
            states_[static_cast<std::size_t>(p)].next[c] = cur;
            p = states_[static_cast<std::size_t>(p)].link;
        }

        if (p == -1) {
            states_[static_cast<std::size_t>(cur)].link = 0;
        } else {
            int q = states_[static_cast<std::size_t>(p)].next[c];
            if (states_[static_cast<std::size_t>(p)].len + 1 ==
                states_[static_cast<std::size_t>(q)].len) {
                states_[static_cast<std::size_t>(cur)].link = q;
            } else {
                int clone = static_cast<int>(states_.size());
                states_.push_back(states_[static_cast<std::size_t>(q)]);
                states_[static_cast<std::size_t>(clone)].len =
                    states_[static_cast<std::size_t>(p)].len + 1;
                while (p != -1 &&
                       states_[static_cast<std::size_t>(p)].next[c] == q) {
                    states_[static_cast<std::size_t>(p)].next[c] = clone;
                    p = states_[static_cast<std::size_t>(p)].link;
                }
                states_[static_cast<std::size_t>(q)].link = clone;
                states_[static_cast<std::size_t>(cur)].link = clone;
            }
        }
        last_ = cur;
    }

    std::vector<State> states_;
    int last_ = 0;
};

}  // namespace string
}  // namespace algorithm_x
