#pragma once

#include <cstddef>
#include <functional>
#include <utility>

namespace algorithm_x {
namespace ds {

// Red-Black Tree. Insert only (erase is complex, skipped for simplicity).
template <typename T, typename Cmp = std::less<T>>
class RedBlackTree {
    enum Color { RED, BLACK };

    struct Node {
        T data;
        Node *left = nullptr, *right = nullptr, *parent = nullptr;
        Color color = RED;
        Node(const T& d) : data(d) {}
    };

public:
    ~RedBlackTree() { destroy(root_); }

    bool insert(const T& value) {
        Node* n = new Node(value);
        if (!bst_insert(n)) { delete n; return false; }
        insert_fixup(n);
        ++size_;
        return true;
    }

    bool contains(const T& value) const {
        Node* cur = root_;
        while (cur) {
            if (cmp_(value, cur->data)) cur = cur->left;
            else if (cmp_(cur->data, value)) cur = cur->right;
            else return true;
        }
        return false;
    }

    template <typename Func>
    void inorder(Func f) const { inorder_impl(root_, f); }

    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    bool bst_insert(Node* n) {
        if (!root_) { root_ = n; root_->color = BLACK; return true; }
        Node* cur = root_;
        while (true) {
            if (cmp_(n->data, cur->data)) {
                if (!cur->left) { cur->left = n; n->parent = cur; return true; }
                cur = cur->left;
            } else if (cmp_(cur->data, n->data)) {
                if (!cur->right) { cur->right = n; n->parent = cur; return true; }
                cur = cur->right;
            } else {
                return false;  // duplicate
            }
        }
    }

    void rotate_left(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        if (y->left) y->left->parent = x;
        y->parent = x->parent;
        if (!x->parent) root_ = y;
        else if (x == x->parent->left) x->parent->left = y;
        else x->parent->right = y;
        y->left = x;
        x->parent = y;
    }

    void rotate_right(Node* y) {
        Node* x = y->left;
        y->left = x->right;
        if (x->right) x->right->parent = y;
        x->parent = y->parent;
        if (!y->parent) root_ = x;
        else if (y == y->parent->left) y->parent->left = x;
        else y->parent->right = x;
        x->right = y;
        y->parent = x;
    }

    void insert_fixup(Node* z) {
        while (z->parent && z->parent->color == RED) {
            Node* gp = z->parent->parent;
            if (z->parent == gp->left) {
                Node* uncle = gp->right;
                if (uncle && uncle->color == RED) {
                    z->parent->color = BLACK;
                    uncle->color = BLACK;
                    gp->color = RED;
                    z = gp;
                } else {
                    if (z == z->parent->right) {
                        z = z->parent;
                        rotate_left(z);
                    }
                    z->parent->color = BLACK;
                    gp->color = RED;
                    rotate_right(gp);
                }
            } else {
                Node* uncle = gp->left;
                if (uncle && uncle->color == RED) {
                    z->parent->color = BLACK;
                    uncle->color = BLACK;
                    gp->color = RED;
                    z = gp;
                } else {
                    if (z == z->parent->left) {
                        z = z->parent;
                        rotate_right(z);
                    }
                    z->parent->color = BLACK;
                    gp->color = RED;
                    rotate_left(gp);
                }
            }
        }
        root_->color = BLACK;
    }

    static void inorder_impl(Node* n, const std::function<void(const T&)>& f) {
        if (!n) return;
        inorder_impl(n->left, f);
        f(n->data);
        inorder_impl(n->right, f);
    }

    void destroy(Node* n) {
        if (!n) return;
        destroy(n->left);
        destroy(n->right);
        delete n;
    }

    Node* root_ = nullptr;
    std::size_t size_ = 0;
    Cmp cmp_;
};

}  // namespace ds
}  // namespace algorithm_x
