#pragma once

#include <algorithm>
#include <cstddef>
#include <functional>
#include <stdexcept>
#include <utility>

namespace algorithm_x {
namespace ds {

// AVLTree — 自平衡二叉搜索树（AVL 树）。
// 每个节点维护高度，插入/删除后通过旋转恢复平衡，|balance| ≤ 1。
template <typename T, typename Cmp = std::less<T>>
class AVLTree {
    struct Node {
        T data;
        Node* left = nullptr;
        Node* right = nullptr;
        int height = 1;
        Node(const T& d) : data(d) {}
        Node(T&& d) : data(std::move(d)) {}
    };

public:
    ~AVLTree() { destroy(root_); }

    void insert(const T& value) { root_ = insert_node(root_, value); }

    bool contains(const T& value) const {
        Node* cur = root_;
        while (cur) {
            if (cmp_(value, cur->data)) cur = cur->left;
            else if (cmp_(cur->data, value)) cur = cur->right;
            else return true;
        }
        return false;
    }

    void erase(const T& value) { root_ = erase_node(root_, value); }

    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }

    template <typename Func>
    void inorder(Func f) const { inorder_impl(root_, f); }

private:
    static int height(Node* n) { return n ? n->height : 0; }
    static int balance_factor(Node* n) { return n ? height(n->left) - height(n->right) : 0; }

    static void update_height(Node* n) {
        n->height = 1 + std::max(height(n->left), height(n->right));
    }

    static Node* rotate_right(Node* y) {
        Node* x = y->left;
        Node* t = x->right;
        x->right = y;
        y->left = t;
        update_height(y);
        update_height(x);
        return x;
    }

    static Node* rotate_left(Node* x) {
        Node* y = x->right;
        Node* t = y->left;
        y->left = x;
        x->right = t;
        update_height(x);
        update_height(y);
        return y;
    }

    static Node* balance(Node* n) {
        update_height(n);
        int bf = balance_factor(n);
        // Left heavy
        if (bf > 1) {
            if (balance_factor(n->left) < 0)  // LR
                n->left = rotate_left(n->left);
            return rotate_right(n);  // LL or LR
        }
        // Right heavy
        if (bf < -1) {
            if (balance_factor(n->right) > 0)  // RL
                n->right = rotate_right(n->right);
            return rotate_left(n);  // RR or RL
        }
        return n;
    }

    Node* insert_node(Node* n, const T& value) {
        if (n == nullptr) {
            ++size_;
            return new Node(value);
        }
        if (cmp_(value, n->data))
            n->left = insert_node(n->left, value);
        else if (cmp_(n->data, value))
            n->right = insert_node(n->right, value);
        else
            return n;  // duplicate
        return balance(n);
    }

    Node* erase_node(Node* n, const T& value) {
        if (n == nullptr) return nullptr;
        if (cmp_(value, n->data)) {
            n->left = erase_node(n->left, value);
        } else if (cmp_(n->data, value)) {
            n->right = erase_node(n->right, value);
        } else {
            --size_;
            if (n->left == nullptr || n->right == nullptr) {
                Node* child = n->left ? n->left : n->right;
                delete n;
                return child;
            }
            // Two children: inorder successor
            Node* succ = n->right;
            while (succ->left) succ = succ->left;
            n->data = std::move(succ->data);
            n->right = erase_node(n->right, n->data);
            ++size_;
        }
        return balance(n);
    }

    template <typename Func>
    static void inorder_impl(Node* n, Func f) {
        if (n == nullptr) return;
        inorder_impl(n->left, f);
        f(n->data);
        inorder_impl(n->right, f);
    }

    void destroy(Node* n) {
        if (n) {
            destroy(n->left);
            destroy(n->right);
            delete n;
        }
    }

    Node* root_ = nullptr;
    std::size_t size_ = 0;
    Cmp cmp_;
};

}  // namespace ds
}  // namespace algorithm_x
