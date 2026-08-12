#pragma once

#include <cstddef>
#include <random>
#include <vector>

namespace algorithm_x {
namespace ds {

// 跳表 (Skip List) — 期望 O(log n) 插入/查找/删除。
template <typename T>
class SkipList {
    static constexpr int MAX_LEVEL = 16;

    struct Node {
        T data;
        std::vector<Node*> next;
        explicit Node(const T& d, int level) : data(d), next(static_cast<std::size_t>(level), nullptr) {}
    };

public:
    SkipList() : head_(new Node(T{}, MAX_LEVEL)), level_(1), gen_(42) {}

    ~SkipList() {
        Node* cur = head_;
        while (cur) {
            Node* tmp = cur;
            cur = cur->next[0];
            delete tmp;
        }
    }

    bool insert(const T& value) {
        std::vector<Node*> update(static_cast<std::size_t>(MAX_LEVEL), nullptr);
        Node* cur = head_;
        for (int i = level_ - 1; i >= 0; --i) {
            while (cur->next[static_cast<std::size_t>(i)] &&
                   cur->next[static_cast<std::size_t>(i)]->data < value) {
                cur = cur->next[static_cast<std::size_t>(i)];
            }
            update[static_cast<std::size_t>(i)] = cur;
        }
        cur = cur->next[0];

        if (cur && cur->data == value) return false;  // 已存在

        int new_level = random_level();
        if (new_level > level_) {
            for (int i = level_; i < new_level; ++i) {
                update[static_cast<std::size_t>(i)] = head_;
            }
            level_ = new_level;
        }

        Node* node = new Node(value, new_level);
        for (int i = 0; i < new_level; ++i) {
            node->next[static_cast<std::size_t>(i)] =
                update[static_cast<std::size_t>(i)]->next[static_cast<std::size_t>(i)];
            update[static_cast<std::size_t>(i)]->next[static_cast<std::size_t>(i)] = node;
        }
        ++size_;
        return true;
    }

    bool search(const T& value) const {
        Node* cur = head_;
        for (int i = level_ - 1; i >= 0; --i) {
            while (cur->next[static_cast<std::size_t>(i)] &&
                   cur->next[static_cast<std::size_t>(i)]->data < value) {
                cur = cur->next[static_cast<std::size_t>(i)];
            }
        }
        cur = cur->next[0];
        return cur && cur->data == value;
    }

    bool erase(const T& value) {
        std::vector<Node*> update(static_cast<std::size_t>(MAX_LEVEL), nullptr);
        Node* cur = head_;
        for (int i = level_ - 1; i >= 0; --i) {
            while (cur->next[static_cast<std::size_t>(i)] &&
                   cur->next[static_cast<std::size_t>(i)]->data < value) {
                cur = cur->next[static_cast<std::size_t>(i)];
            }
            update[static_cast<std::size_t>(i)] = cur;
        }
        cur = cur->next[0];
        if (!cur || cur->data != value) return false;

        for (int i = 0; i < level_; ++i) {
            if (update[static_cast<std::size_t>(i)]->next[static_cast<std::size_t>(i)] != cur) break;
            update[static_cast<std::size_t>(i)]->next[static_cast<std::size_t>(i)] = cur->next[static_cast<std::size_t>(i)];
        }
        delete cur;
        while (level_ > 1 && head_->next[static_cast<std::size_t>(level_ - 1)] == nullptr) {
            --level_;
        }
        --size_;
        return true;
    }

    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    int random_level() {
        int level = 1;
        std::uniform_real_distribution<double> dis(0.0, 1.0);
        while (dis(gen_) < 0.5 && level < MAX_LEVEL) ++level;
        return level;
    }

    Node* head_;
    int level_;
    std::size_t size_ = 0;
    std::mt19937 gen_;
};

}  // namespace ds
}  // namespace algorithm_x
