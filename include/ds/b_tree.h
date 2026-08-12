#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace ds {

// B-Tree (order M, minimum degree t = ceil(M/2)).
// Simple implementation: insert + search, int keys only.
template <int M = 5>
class BTree {
    static constexpr int T = (M + 1) / 2;  // minimum degree

    struct Node {
        std::vector<int> keys;
        std::vector<Node*> children;
        bool leaf = true;

        Node(bool is_leaf = true) : leaf(is_leaf) {}
    };

public:
    BTree() : root_(new Node()) {}

    bool search(int key) const { return search_impl(root_, key); }

    void insert(int key) {
        Node* r = root_;
        if (static_cast<int>(r->keys.size()) == M - 1) {
            Node* s = new Node(false);
            s->children.push_back(r);
            split_child(s, 0);
            root_ = s;
            insert_nonfull(s, key);
        } else {
            insert_nonfull(r, key);
        }
    }

    ~BTree() { destroy(root_); }

private:
    bool search_impl(Node* node, int key) const {
        auto it = std::lower_bound(node->keys.begin(), node->keys.end(), key);
        if (it != node->keys.end() && *it == key) return true;
        if (node->leaf) return false;
        std::size_t i = static_cast<std::size_t>(it - node->keys.begin());
        return search_impl(node->children[i], key);
    }

    void split_child(Node* parent, std::size_t idx) {
        Node* child = parent->children[idx];
        Node* new_node = new Node(child->leaf);

        // Move half keys to new_node
        int mid = T - 1;
        for (int i = mid + 1; i < static_cast<int>(child->keys.size()); ++i) {
            new_node->keys.push_back(child->keys[static_cast<std::size_t>(i)]);
        }
        if (!child->leaf) {
            for (int i = mid + 1; i < static_cast<int>(child->children.size()); ++i) {
                new_node->children.push_back(
                    child->children[static_cast<std::size_t>(i)]);
            }
            child->children.resize(static_cast<std::size_t>(mid + 1));
        }

        // Insert middle key into parent
        parent->keys.insert(
            parent->keys.begin() + static_cast<long>(idx), child->keys[static_cast<std::size_t>(mid)]);
        parent->children.insert(
            parent->children.begin() + static_cast<long>(idx) + 1, new_node);

        child->keys.resize(static_cast<std::size_t>(mid));
    }

    void insert_nonfull(Node* node, int key) {
        int i = static_cast<int>(node->keys.size()) - 1;
        if (node->leaf) {
            node->keys.push_back(key);
            while (i >= 0 && node->keys[static_cast<std::size_t>(i)] > key) {
                node->keys[static_cast<std::size_t>(i + 1)] = node->keys[static_cast<std::size_t>(i)];
                --i;
            }
            node->keys[static_cast<std::size_t>(i + 1)] = key;
        } else {
            while (i >= 0 && node->keys[static_cast<std::size_t>(i)] > key) --i;
            ++i;
            if (static_cast<int>(node->children[static_cast<std::size_t>(i)]->keys.size()) == M - 1) {
                split_child(node, static_cast<std::size_t>(i));
                if (key > node->keys[static_cast<std::size_t>(i)]) ++i;
            }
            insert_nonfull(node->children[static_cast<std::size_t>(i)], key);
        }
    }

    void destroy(Node* n) {
        if (!n) return;
        for (auto* c : n->children) destroy(c);
        delete n;
    }

    Node* root_;
};

}  // namespace ds
}  // namespace algorithm_x
