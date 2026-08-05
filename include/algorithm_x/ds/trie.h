#pragma once

#include <array>
#include <cstddef>
#include <string>

namespace algorithm_x {
namespace ds {

// Trie — 小写字母字典树（26 叉）。
// 支持 insert / search / starts_with。
// // 调用示例：
//   Trie trie;
//   trie.insert("hello");
//   trie.search("hello");
// true
//   trie.starts_with("hel");  // true
class Trie {
    static constexpr int ALPHABET = 26;

    struct Node {
        std::array<Node*, ALPHABET> children{};
        bool is_end = false;
    };

public:
    Trie() : root_(new Node()) {}

    ~Trie() { destroy(root_); }

    void insert(const std::string& word) {
        Node* cur = root_;
        for (char ch : word) {
            int idx = ch - 'a';
            if (cur->children[idx] == nullptr) {
                cur->children[idx] = new Node();
            }
            cur = cur->children[idx];
        }
        cur->is_end = true;
    }

    bool search(const std::string& word) const {
        Node* n = find_node(word);
        return n != nullptr && n->is_end;
    }

    bool starts_with(const std::string& prefix) const {
        return find_node(prefix) != nullptr;
    }

private:
    Node* find_node(const std::string& s) const {
        Node* cur = root_;
        for (char ch : s) {
            int idx = ch - 'a';
            if (cur->children[idx] == nullptr) return nullptr;
            cur = cur->children[idx];
        }
        return cur;
    }

    void destroy(Node* n) {
        if (n == nullptr) return;
        for (auto* child : n->children) {
            destroy(child);
        }
        delete n;
    }

    Node* root_;
};

}  // namespace ds
}  // namespace algorithm_x
