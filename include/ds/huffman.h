#pragma once

#include <cstddef>
#include <map>
#include <queue>
#include <string>
#include <vector>

namespace algorithm_x {
namespace ds {

// 哈夫曼编码 — 根据输入文本生成最优前缀码。
class HuffmanCoding {
    struct Node {
        char ch;
        int freq;
        Node* left = nullptr;
        Node* right = nullptr;
        Node(char c, int f) : ch(c), freq(f) {}
        Node(int f, Node* l, Node* r) : ch('\0'), freq(f), left(l), right(r) {}
    };

public:
    // 根据输入文本构建哈夫曼树并生成编码表。
    void build(const std::string& text) {
        // 统计频率
        std::map<char, int> freq_map;
        for (char c : text) ++freq_map[c];

        // 最小堆
        auto cmp = [](Node* a, Node* b) { return a->freq > b->freq; };
        std::priority_queue<Node*, std::vector<Node*>, decltype(cmp)> pq(cmp);
        for (auto& [ch, freq] : freq_map) {
            pq.push(new Node(ch, freq));
        }

        while (pq.size() > 1) {
            Node* l = pq.top(); pq.pop();
            Node* r = pq.top(); pq.pop();
            pq.push(new Node(l->freq + r->freq, l, r));
        }

        root_ = pq.empty() ? nullptr : pq.top();

        // 生成编码表
        codes_.clear();
        if (root_) build_codes(root_, "");
    }

    // 编码文本。
    std::string encode(const std::string& text) const {
        std::string result;
        for (char c : text) {
            auto it = codes_.find(c);
            if (it != codes_.end()) result += it->second;
        }
        return result;
    }

    // 解码比特串。
    std::string decode(const std::string& bits) const {
        if (!root_) return "";
        // 单字符特例
        if (root_->left == nullptr && root_->right == nullptr) {
            return std::string(bits.size(), root_->ch);
        }
        std::string result;
        Node* cur = root_;
        for (char bit : bits) {
            cur = (bit == '0') ? cur->left : cur->right;
            if (!cur) break;  // 无效比特
            if (cur->left == nullptr && cur->right == nullptr) {
                result += cur->ch;
                cur = root_;
            }
        }
        return result;
    }

    // 字符 → 编码映射。
    const std::map<char, std::string>& codes() const { return codes_; }

    ~HuffmanCoding() { destroy(root_); }

private:
    void build_codes(Node* node, const std::string& prefix) {
        if (node->left == nullptr && node->right == nullptr) {
            codes_[node->ch] = prefix.empty() ? "0" : prefix;
            return;
        }
        if (node->left) build_codes(node->left, prefix + "0");
        if (node->right) build_codes(node->right, prefix + "1");
    }

    void destroy(Node* node) {
        if (node) {
            destroy(node->left);
            destroy(node->right);
            delete node;
        }
    }

    Node* root_ = nullptr;
    std::map<char, std::string> codes_;
};

}  // namespace ds
}  // namespace algorithm_x
