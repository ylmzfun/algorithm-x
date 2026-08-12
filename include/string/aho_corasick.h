#pragma once

#include <array>
#include <cstddef>
#include <queue>
#include <string>
#include <vector>

namespace algorithm_x {
namespace string {

// Aho-Corasick automaton for multi-pattern matching, O(n + total_matches).
// Supports lowercase a-z only.
class AhoCorasick {
    static constexpr int ALPHABET = 26;

    struct Node {
        std::array<int, ALPHABET> next{};
        int fail = 0;
        std::vector<int> output;
        Node() { next.fill(-1); }
    };

public:
    AhoCorasick() { nodes_.emplace_back(); }

    // Add a pattern; returns its id (0-based).
    int insert(const std::string& pattern) {
        int u = 0;
        for (char c : pattern) {
            int idx = c - 'a';
            if (nodes_[static_cast<std::size_t>(u)].next[idx] == -1) {
                nodes_[static_cast<std::size_t>(u)].next[idx] =
                    static_cast<int>(nodes_.size());
                nodes_.emplace_back();
            }
            u = nodes_[static_cast<std::size_t>(u)].next[idx];
        }
        int id = static_cast<int>(patterns_.size());
        patterns_.push_back(pattern);
        nodes_[static_cast<std::size_t>(u)].output.push_back(id);
        return id;
    }

    // Build failure links (must be called after all patterns inserted).
    void build() {
        std::queue<int> q;
        auto& root = nodes_[0];
        for (int& nxt : root.next) {
            if (nxt != -1) {
                nodes_[static_cast<std::size_t>(nxt)].fail = 0;
                q.push(nxt);
            } else {
                nxt = 0;
            }
        }

        while (!q.empty()) {
            int u = q.front();
            q.pop();
            auto& node = nodes_[static_cast<std::size_t>(u)];

            // merge output from fail chain
            int f = node.fail;
            auto& fail_output = nodes_[static_cast<std::size_t>(f)].output;
            node.output.insert(node.output.end(), fail_output.begin(),
                               fail_output.end());

            for (int c = 0; c < ALPHABET; ++c) {
                int v = node.next[c];
                if (v != -1) {
                    nodes_[static_cast<std::size_t>(v)].fail =
                        nodes_[static_cast<std::size_t>(node.fail)].next[c];
                    q.push(v);
                } else {
                    node.next[c] =
                        nodes_[static_cast<std::size_t>(node.fail)].next[c];
                }
            }
        }
    }

    // Search text; returns vector of {pattern_id, start_position}.
    std::vector<std::pair<int, std::size_t>> search(
        const std::string& text) {
        std::vector<std::pair<int, std::size_t>> result;
        int u = 0;
        for (std::size_t i = 0; i < text.size(); ++i) {
            int idx = text[i] - 'a';
            u = nodes_[static_cast<std::size_t>(u)].next[idx];
            for (int pid : nodes_[static_cast<std::size_t>(u)].output) {
                std::size_t start =
                    i + 1 - patterns_[static_cast<std::size_t>(pid)].size();
                result.emplace_back(pid, start);
            }
        }
        return result;
    }

private:
    std::vector<Node> nodes_;
    std::vector<std::string> patterns_;
};

}  // namespace string
}  // namespace algorithm_x
