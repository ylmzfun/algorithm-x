#pragma once

#include <cmath>
#include <cstddef>
#include <functional>
#include <stdexcept>
#include <vector>

namespace algorithm_x {
namespace ds {

// Fibonacci Heap — min-heap with amortized O(1) push, O(log n) pop.
template <typename T, typename Cmp = std::less<T>>
class FibonacciHeap {
    struct Node {
        T data;
        Node *parent = nullptr, *child = nullptr;
        Node *left = this, *right = this;  // circular doubly-linked
        std::size_t degree = 0;
        bool marked = false;
        Node(const T& d) : data(d) {}
    };

public:
    ~FibonacciHeap() { destroy(root_); }

    void push(const T& value) {
        Node* n = new Node(value);
        root_ = merge_lists(root_, n);
        if (!min_ || cmp_(n->data, min_->data)) min_ = n;
        ++size_;
    }

    const T& top() const {
        if (!min_) throw std::out_of_range("FibonacciHeap::top: empty");
        return min_->data;
    }

    void pop() {
        if (!min_) throw std::out_of_range("FibonacciHeap::pop: empty");
        Node* old_min = min_;
        // Promote children to root list
        if (old_min->child) {
            Node* child = old_min->child;
            // Break circular link of children
            Node* cur = child;
            do {
                cur->parent = nullptr;
                cur = cur->right;
            } while (cur != child);
            root_ = merge_lists(root_, child);
        }
        // Remove min from root list
        remove_from_list(old_min);
        if (old_min == old_min->right) {
            root_ = nullptr;
            min_ = nullptr;
        } else {
            min_ = old_min->right;
            consolidate();
        }
        delete old_min;
        --size_;
    }

    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    Node* merge_lists(Node* a, Node* b) {
        if (!a) return b;
        if (!b) return a;
        Node* a_right = a->right;
        a->right = b;
        b->left = a;
        a_right->left = b->right;
        b->right->right = a_right;
        return a;
    }

    void remove_from_list(Node* n) {
        n->left->right = n->right;
        n->right->left = n->left;
    }

    void consolidate() {
        std::size_t max_degree = static_cast<std::size_t>(std::log2(size_)) + 2;
        std::vector<Node*> degree_table(max_degree + 1, nullptr);

        // Collect all roots
        std::vector<Node*> roots;
        if (root_) {
            Node* cur = root_;
            do {
                roots.push_back(cur);
                cur = cur->right;
            } while (cur != root_);
        }

        for (Node* w : roots) {
            Node* x = w;
            std::size_t d = x->degree;
            while (degree_table[d]) {
                Node* y = degree_table[d];
                if (cmp_(y->data, x->data)) std::swap(x, y);
                link(y, x);
                degree_table[d] = nullptr;
                ++d;
            }
            degree_table[d] = x;
        }

        min_ = nullptr;
        root_ = nullptr;
        for (Node* n : degree_table) {
            if (n) {
                n->left = n->right = n;  // isolate
                root_ = merge_lists(root_, n);
                if (!min_ || cmp_(n->data, min_->data)) min_ = n;
            }
        }
    }

    void link(Node* y, Node* x) {
        remove_from_list(y);
        y->parent = x;
        y->left = y->right = y;
        x->child = merge_lists(x->child, y);
        ++x->degree;
        y->marked = false;
    }

    void destroy(Node* n) {
        if (!n) return;
        Node* cur = n;
        do {
            Node* next = cur->right;
            destroy(cur->child);
            delete cur;
            cur = next;
        } while (cur != n);
    }

    Node* root_ = nullptr;
    Node* min_ = nullptr;
    std::size_t size_ = 0;
    Cmp cmp_;
};

}  // namespace ds
}  // namespace algorithm_x
