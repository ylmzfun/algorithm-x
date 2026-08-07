#pragma once

#include <atomic>
#include <cstddef>

namespace algorithm_x {
namespace concurrent {

// Lock-free stack using Treiber's algorithm (CAS on head pointer).
template <typename T>
class LockFreeStack {
    struct Node {
        T data;
        Node* next;
        Node(const T& d) : data(d), next(nullptr) {}
    };

public:
    LockFreeStack() : head_(nullptr) {}

    ~LockFreeStack() {
        while (Node* n = head_.load(std::memory_order_relaxed)) {
            head_.store(n->next, std::memory_order_relaxed);
            delete n;
        }
    }

    // Disable copy.
    LockFreeStack(const LockFreeStack&) = delete;
    LockFreeStack& operator=(const LockFreeStack&) = delete;

    void push(const T& value) {
        Node* n = new Node(value);
        n->next = head_.load(std::memory_order_relaxed);
        while (!head_.compare_exchange_weak(n->next, n,
               std::memory_order_release, std::memory_order_relaxed)) {}
    }

    bool pop(T& result) {
        Node* n = head_.load(std::memory_order_relaxed);
        while (n) {
            if (head_.compare_exchange_weak(n, n->next,
                    std::memory_order_acquire, std::memory_order_relaxed)) {
                result = n->data;
                delete n;
                return true;
            }
        }
        return false;
    }

    bool empty() const {
        return head_.load(std::memory_order_relaxed) == nullptr;
    }

private:
    std::atomic<Node*> head_;
};

}  // namespace concurrent
}  // namespace algorithm_x
