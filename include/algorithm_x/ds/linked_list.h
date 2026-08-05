#pragma once

#include <cstddef>
#include <initializer_list>
#include <stdexcept>
#include <utility>

namespace algorithm_x {
namespace ds {

template <typename T>
class SinglyLinkedList {
    struct Node {
        T data;
        Node* next = nullptr;
        Node(const T& d) : data(d) {}
        Node(T&& d) : data(std::move(d)) {}
    };

public:
    SinglyLinkedList() = default;

    SinglyLinkedList(std::initializer_list<T> init) {
        for (auto it = init.end(); it != init.begin();) {
            --it;
            push_front(*it);
        }
    }

    ~SinglyLinkedList() { clear(); }

    SinglyLinkedList(const SinglyLinkedList& other) { copy_from(other); }

    SinglyLinkedList& operator=(const SinglyLinkedList& other) {
        if (this != &other) {
            clear();
            copy_from(other);
        }
        return *this;
    }

    SinglyLinkedList(SinglyLinkedList&& other) noexcept
        : head_(other.head_), tail_(other.tail_), size_(other.size_) {
        other.head_ = nullptr;
        other.tail_ = nullptr;
        other.size_ = 0;
    }

    SinglyLinkedList& operator=(SinglyLinkedList&& other) noexcept {
        if (this != &other) {
            clear();
            head_ = other.head_;
            tail_ = other.tail_;
            size_ = other.size_;
            other.head_ = nullptr;
            other.tail_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }

    void push_front(const T& value) {
        auto* node = new Node(value);
        node->next = head_;
        head_ = node;
        if (tail_ == nullptr) {
            tail_ = node;
        }
        ++size_;
    }

    void push_back(const T& value) {
        auto* node = new Node(value);
        if (tail_) {
            tail_->next = node;
        } else {
            head_ = node;
        }
        tail_ = node;
        ++size_;
    }

    void pop_front() {
        if (head_ == nullptr) {
            throw std::out_of_range("SinglyLinkedList::pop_front: empty list");
        }
        Node* tmp = head_;
        head_ = head_->next;
        if (head_ == nullptr) {
            tail_ = nullptr;
        }
        delete tmp;
        --size_;
    }

    void insert_after(Node* prev, const T& value) {
        auto* node = new Node(value);
        node->next = prev->next;
        prev->next = node;
        if (prev == tail_) {
            tail_ = node;
        }
        ++size_;
    }

    void erase_after(Node* prev) {
        if (prev == nullptr || prev->next == nullptr) return;
        Node* tmp = prev->next;
        prev->next = tmp->next;
        if (tmp == tail_) {
            tail_ = prev;
        }
        delete tmp;
        --size_;
    }

    Node* find(const T& value) {
        Node* cur = head_;
        while (cur) {
            if (cur->data == value) return cur;
            cur = cur->next;
        }
        return nullptr;
    }

    void reverse() {
        Node* prev = nullptr;
        Node* cur = head_;
        tail_ = head_;
        while (cur) {
            Node* next = cur->next;
            cur->next = prev;
            prev = cur;
            cur = next;
        }
        head_ = prev;
    }

    void clear() {
        while (head_) {
            Node* tmp = head_;
            head_ = head_->next;
            delete tmp;
        }
        tail_ = nullptr;
        size_ = 0;
    }

    T& front() {
        if (head_ == nullptr) {
            throw std::out_of_range("SinglyLinkedList::front: empty list");
        }
        return head_->data;
    }

    const T& front() const {
        if (head_ == nullptr) {
            throw std::out_of_range("SinglyLinkedList::front: empty list");
        }
        return head_->data;
    }

    Node* head() { return head_; }
    const Node* head() const { return head_; }
    Node* tail() { return tail_; }
    const Node* tail() const { return tail_; }
    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    void copy_from(const SinglyLinkedList& other) {
        Node* cur = other.head_;
        while (cur) {
            push_back(cur->data);
            cur = cur->next;
        }
    }

    Node* head_ = nullptr;
    Node* tail_ = nullptr;
    std::size_t size_ = 0;
};

template <typename T>
class DoublyLinkedList {
    struct Node {
        T data;
        Node* prev = nullptr;
        Node* next = nullptr;
        Node(const T& d) : data(d) {}
        Node(T&& d) : data(std::move(d)) {}
    };

public:
    DoublyLinkedList() = default;

    DoublyLinkedList(std::initializer_list<T> init) {
        for (auto it = init.end(); it != init.begin();) {
            --it;
            push_front(*it);
        }
    }

    ~DoublyLinkedList() { clear(); }

    DoublyLinkedList(const DoublyLinkedList& other) { copy_from(other); }

    DoublyLinkedList& operator=(const DoublyLinkedList& other) {
        if (this != &other) {
            clear();
            copy_from(other);
        }
        return *this;
    }

    DoublyLinkedList(DoublyLinkedList&& other) noexcept
        : head_(other.head_), tail_(other.tail_), size_(other.size_) {
        other.head_ = nullptr;
        other.tail_ = nullptr;
        other.size_ = 0;
    }

    DoublyLinkedList& operator=(DoublyLinkedList&& other) noexcept {
        if (this != &other) {
            clear();
            head_ = other.head_;
            tail_ = other.tail_;
            size_ = other.size_;
            other.head_ = nullptr;
            other.tail_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }

    void push_front(const T& value) {
        auto* node = new Node(value);
        node->next = head_;
        if (head_) {
            head_->prev = node;
        } else {
            tail_ = node;
        }
        head_ = node;
        ++size_;
    }

    void push_back(const T& value) {
        auto* node = new Node(value);
        node->prev = tail_;
        if (tail_) {
            tail_->next = node;
        } else {
            head_ = node;
        }
        tail_ = node;
        ++size_;
    }

    void pop_front() {
        if (head_ == nullptr) {
            throw std::out_of_range("DoublyLinkedList::pop_front: empty list");
        }
        Node* tmp = head_;
        head_ = head_->next;
        if (head_) {
            head_->prev = nullptr;
        } else {
            tail_ = nullptr;
        }
        delete tmp;
        --size_;
    }

    void pop_back() {
        if (tail_ == nullptr) {
            throw std::out_of_range("DoublyLinkedList::pop_back: empty list");
        }
        Node* tmp = tail_;
        tail_ = tail_->prev;
        if (tail_) {
            tail_->next = nullptr;
        } else {
            head_ = nullptr;
        }
        delete tmp;
        --size_;
    }

    void insert_before(Node* node, const T& value) {
        auto* n = new Node(value);
        n->next = node;
        n->prev = node->prev;
        if (node->prev) {
            node->prev->next = n;
        } else {
            head_ = n;
        }
        node->prev = n;
        ++size_;
    }

    void insert_after(Node* node, const T& value) {
        auto* n = new Node(value);
        n->prev = node;
        n->next = node->next;
        if (node->next) {
            node->next->prev = n;
        } else {
            tail_ = n;
        }
        node->next = n;
        ++size_;
    }

    void erase(Node* node) {
        if (node->prev) {
            node->prev->next = node->next;
        } else {
            head_ = node->next;
        }
        if (node->next) {
            node->next->prev = node->prev;
        } else {
            tail_ = node->prev;
        }
        delete node;
        --size_;
    }

    void clear() {
        while (head_) {
            Node* tmp = head_;
            head_ = head_->next;
            delete tmp;
        }
        tail_ = nullptr;
        size_ = 0;
    }

    T& front() {
        if (head_ == nullptr) {
            throw std::out_of_range("DoublyLinkedList::front: empty list");
        }
        return head_->data;
    }

    const T& front() const {
        if (head_ == nullptr) {
            throw std::out_of_range("DoublyLinkedList::front: empty list");
        }
        return head_->data;
    }

    T& back() {
        if (tail_ == nullptr) {
            throw std::out_of_range("DoublyLinkedList::back: empty list");
        }
        return tail_->data;
    }

    const T& back() const {
        if (tail_ == nullptr) {
            throw std::out_of_range("DoublyLinkedList::back: empty list");
        }
        return tail_->data;
    }

    Node* head() { return head_; }
    const Node* head() const { return head_; }
    Node* tail() { return tail_; }
    const Node* tail() const { return tail_; }
    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    void copy_from(const DoublyLinkedList& other) {
        Node* cur = other.head_;
        while (cur) {
            push_back(cur->data);
            cur = cur->next;
        }
    }

    Node* head_ = nullptr;
    Node* tail_ = nullptr;
    std::size_t size_ = 0;
};

}  // namespace ds
}  // namespace algorithm_x
