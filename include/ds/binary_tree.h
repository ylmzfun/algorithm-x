#pragma once

#include <algorithm>
#include <cstddef>
#include <functional>
#include <queue>
#include <stack>
#include <stdexcept>
#include <utility>

namespace algorithm_x {
namespace ds {

template <typename T>
struct BinaryTreeNode {
    T data;
    BinaryTreeNode* left = nullptr;
    BinaryTreeNode* right = nullptr;

    BinaryTreeNode(const T& d) : data(d) {}
    BinaryTreeNode(T&& d) : data(std::move(d)) {}
};

// BinarySearchTree — 不含重复键的二叉搜索树。
template <typename T, typename Cmp = std::less<T>>
class BinarySearchTree {
public:
    using Node = BinaryTreeNode<T>;

    ~BinarySearchTree() { destroy(root_); }

    // 插入，已存在则返回 false
    bool insert(const T& value) {
        if (root_ == nullptr) {
            root_ = new Node(value);
            ++size_;
            return true;
        }
        Node* cur = root_;
        while (true) {
            if (cmp_(value, cur->data)) {
                if (cur->left == nullptr) {
                    cur->left = new Node(value);
                    ++size_;
                    return true;
                }
                cur = cur->left;
            } else if (cmp_(cur->data, value)) {
                if (cur->right == nullptr) {
                    cur->right = new Node(value);
                    ++size_;
                    return true;
                }
                cur = cur->right;
            } else {
                return false;  // duplicate
            }
        }
    }

    bool contains(const T& value) const {
        Node* cur = root_;
        while (cur) {
            if (cmp_(value, cur->data)) {
                cur = cur->left;
            } else if (cmp_(cur->data, value)) {
                cur = cur->right;
            } else {
                return true;
            }
        }
        return false;
    }

    bool erase(const T& value) {
        root_ = erase_node(root_, value);
        return true;  // simplified: always returns true
    }

    Node* find_min() const {
        if (root_ == nullptr) return nullptr;
        Node* cur = root_;
        while (cur->left) cur = cur->left;
        return cur;
    }

    Node* find_max() const {
        if (root_ == nullptr) return nullptr;
        Node* cur = root_;
        while (cur->right) cur = cur->right;
        return cur;
    }

    // ---- traversals (iterative) ----
    template <typename Func>
    void inorder(Func f) const {
        std::stack<Node*> stk;
        Node* cur = root_;
        while (cur || !stk.empty()) {
            while (cur) {
                stk.push(cur);
                cur = cur->left;
            }
            cur = stk.top();
            stk.pop();
            f(cur->data);
            cur = cur->right;
        }
    }

    template <typename Func>
    void preorder(Func f) const {
        if (root_ == nullptr) return;
        std::stack<Node*> stk;
        stk.push(root_);
        while (!stk.empty()) {
            Node* cur = stk.top();
            stk.pop();
            f(cur->data);
            if (cur->right) stk.push(cur->right);
            if (cur->left) stk.push(cur->left);
        }
    }

    template <typename Func>
    void postorder(Func f) const {
        if (root_ == nullptr) return;
        std::stack<Node*> stk;
        Node* cur = root_;
        Node* last_visited = nullptr;
        while (cur || !stk.empty()) {
            while (cur) {
                stk.push(cur);
                cur = cur->left;
            }
            Node* top = stk.top();
            if (top->right == nullptr || top->right == last_visited) {
                f(top->data);
                last_visited = top;
                stk.pop();
            } else {
                cur = top->right;
            }
        }
    }

    template <typename Func>
    void level_order(Func f) const {
        if (root_ == nullptr) return;
        std::queue<Node*> q;
        q.push(root_);
        while (!q.empty()) {
            Node* cur = q.front();
            q.pop();
            f(cur->data);
            if (cur->left) q.push(cur->left);
            if (cur->right) q.push(cur->right);
        }
    }

    Node* root() const { return root_; }
    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    Node* erase_node(Node* node, const T& value) {
        if (node == nullptr) return nullptr;
        if (cmp_(value, node->data)) {
            node->left = erase_node(node->left, value);
        } else if (cmp_(node->data, value)) {
            node->right = erase_node(node->right, value);
        } else {
            --size_;
            if (node->left == nullptr) {
                Node* right = node->right;
                delete node;
                return right;
            }
            if (node->right == nullptr) {
                Node* left = node->left;
                delete node;
                return left;
            }
            // Two children: replace with inorder successor
            Node* succ = node->right;
            while (succ->left) succ = succ->left;
            node->data = std::move(succ->data);
            node->right = erase_node(node->right, node->data);
            ++size_;  // compensate — erase_node decremented it
        }
        return node;
    }

    void destroy(Node* node) {
        if (node) {
            destroy(node->left);
            destroy(node->right);
            delete node;
        }
    }

    Node* root_ = nullptr;
    std::size_t size_ = 0;
    Cmp cmp_;
};

}  // namespace ds
}  // namespace algorithm_x
