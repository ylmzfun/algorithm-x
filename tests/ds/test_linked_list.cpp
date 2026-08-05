#include "algorithm_x/ds/linked_list.h"

#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <utility>

using namespace algorithm_x::ds;

// ============================================================
// SinglyLinkedList
// ============================================================

TEST(SinglyLinkedListTest, DefaultConstruction) {
    SinglyLinkedList<int> list;
    EXPECT_TRUE(list.empty());
    EXPECT_EQ(list.size(), 0u);
}

TEST(SinglyLinkedListTest, PushFront) {
    SinglyLinkedList<int> list;
    list.push_front(3);
    list.push_front(2);
    list.push_front(1);
    EXPECT_EQ(list.size(), 3u);
    EXPECT_FALSE(list.empty());
    EXPECT_EQ(list.front(), 1);
}

TEST(SinglyLinkedListTest, PushBack) {
    SinglyLinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    list.push_back(3);
    EXPECT_EQ(list.size(), 3u);
    EXPECT_EQ(list.front(), 1);
}

TEST(SinglyLinkedListTest, PopFront) {
    SinglyLinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    list.push_back(3);
    list.pop_front();
    EXPECT_EQ(list.size(), 2u);
    EXPECT_EQ(list.front(), 2);
    list.pop_front();
    list.pop_front();
    EXPECT_TRUE(list.empty());
}

TEST(SinglyLinkedListTest, PopFrontOnEmptyThrows) {
    SinglyLinkedList<int> list;
    EXPECT_THROW(list.pop_front(), std::out_of_range);
}

TEST(SinglyLinkedListTest, InsertAfter) {
    SinglyLinkedList<int> list = {1, 3, 4};
    auto* head = list.head();
    list.insert_after(head, 2);
    EXPECT_EQ(list.size(), 4u);
    // list: 1 -> 2 -> 3 -> 4
    auto* cur = list.head();
    EXPECT_EQ(cur->data, 1);
    cur = cur->next;
    EXPECT_EQ(cur->data, 2);
}

TEST(SinglyLinkedListTest, EraseAfter) {
    SinglyLinkedList<int> list = {1, 2, 3};
    auto* head = list.head();
    list.erase_after(head);
    EXPECT_EQ(list.size(), 2u);
    EXPECT_EQ(list.head()->next->data, 3);
}

TEST(SinglyLinkedListTest, Find) {
    SinglyLinkedList<int> list = {10, 20, 30};
    EXPECT_NE(list.find(20), nullptr);
    EXPECT_EQ(list.find(99), nullptr);
}

TEST(SinglyLinkedListTest, Reverse) {
    SinglyLinkedList<int> list = {1, 2, 3, 4};
    list.reverse();
    auto* cur = list.head();
    EXPECT_EQ(cur->data, 4);
    cur = cur->next;
    EXPECT_EQ(cur->data, 3);
    cur = cur->next;
    EXPECT_EQ(cur->data, 2);
    cur = cur->next;
    EXPECT_EQ(cur->data, 1);
}

TEST(SinglyLinkedListTest, FrontOnEmptyThrows) {
    SinglyLinkedList<int> list;
    EXPECT_THROW(list.front(), std::out_of_range);
}

TEST(SinglyLinkedListTest, CopyConstructor) {
    SinglyLinkedList<int> a = {1, 2, 3};
    SinglyLinkedList<int> b(a);
    EXPECT_EQ(b.size(), 3u);
    EXPECT_EQ(b.front(), 1);
    a.pop_front();
    EXPECT_EQ(b.size(), 3u);
}

TEST(SinglyLinkedListTest, CopyAssignment) {
    SinglyLinkedList<int> a = {1, 2, 3};
    SinglyLinkedList<int> b;
    b = a;
    EXPECT_EQ(b.size(), 3u);
    EXPECT_EQ(b.front(), 1);
}

TEST(SinglyLinkedListTest, MoveConstructor) {
    SinglyLinkedList<int> a = {1, 2, 3};
    SinglyLinkedList<int> b(std::move(a));
    EXPECT_EQ(b.size(), 3u);
    EXPECT_EQ(b.front(), 1);
    EXPECT_TRUE(a.empty());
}

TEST(SinglyLinkedListTest, MoveAssignment) {
    SinglyLinkedList<int> a = {1, 2, 3};
    SinglyLinkedList<int> b;
    b = std::move(a);
    EXPECT_EQ(b.size(), 3u);
    EXPECT_TRUE(a.empty());
}

TEST(SinglyLinkedListTest, InitializerList) {
    SinglyLinkedList<std::string> list = {"a", "b", "c"};
    EXPECT_EQ(list.size(), 3u);
    EXPECT_EQ(list.front(), "a");
}

TEST(SinglyLinkedListTest, Clear) {
    SinglyLinkedList<int> list = {1, 2, 3};
    list.clear();
    EXPECT_TRUE(list.empty());
    EXPECT_EQ(list.size(), 0u);
}

TEST(SinglyLinkedListTest, LargePush) {
    SinglyLinkedList<int> list;
    for (int i = 0; i < 10000; ++i) {
        list.push_back(i);
    }
    EXPECT_EQ(list.size(), 10000u);
}

// ============================================================
// DoublyLinkedList
// ============================================================

TEST(DoublyLinkedListTest, PushFrontAndBack) {
    DoublyLinkedList<int> list;
    list.push_front(2);
    list.push_front(1);
    list.push_back(3);
    EXPECT_EQ(list.front(), 1);
    EXPECT_EQ(list.back(), 3);
    EXPECT_EQ(list.size(), 3u);
}

TEST(DoublyLinkedListTest, PopFrontAndBack) {
    DoublyLinkedList<int> list = {1, 2, 3, 4};
    list.pop_front();
    EXPECT_EQ(list.front(), 2);
    list.pop_back();
    EXPECT_EQ(list.back(), 3);
    EXPECT_EQ(list.size(), 2u);
    list.pop_front();
    list.pop_front();
    EXPECT_TRUE(list.empty());
}

TEST(DoublyLinkedListTest, PopFrontOnEmptyThrows) {
    DoublyLinkedList<int> list;
    EXPECT_THROW(list.pop_front(), std::out_of_range);
}

TEST(DoublyLinkedListTest, PopBackOnEmptyThrows) {
    DoublyLinkedList<int> list;
    EXPECT_THROW(list.pop_back(), std::out_of_range);
}

TEST(DoublyLinkedListTest, InsertBefore) {
    DoublyLinkedList<int> list = {1, 3};
    auto* tail = list.tail();
    list.insert_before(tail, 2);
    // list: 1 <-> 2 <-> 3
    EXPECT_EQ(list.size(), 3u);
    EXPECT_EQ(list.head()->next->data, 2);
    EXPECT_EQ(list.tail()->prev->data, 2);
}

TEST(DoublyLinkedListTest, InsertAfter) {
    DoublyLinkedList<int> list = {1, 3};
    auto* head = list.head();
    list.insert_after(head, 2);
    EXPECT_EQ(list.size(), 3u);
    EXPECT_EQ(list.head()->next->data, 2);
}

TEST(DoublyLinkedListTest, Erase) {
    DoublyLinkedList<int> list = {1, 2, 3};
    list.erase(list.head()->next);
    EXPECT_EQ(list.size(), 2u);
    EXPECT_EQ(list.front(), 1);
    EXPECT_EQ(list.back(), 3);
    list.erase(list.head());
    EXPECT_EQ(list.size(), 1u);
    EXPECT_EQ(list.front(), 3);
    list.erase(list.head());
    EXPECT_TRUE(list.empty());
}

TEST(DoublyLinkedListTest, BidirectionalTraversal) {
    DoublyLinkedList<int> list = {1, 2, 3};
    // Forward
    const auto* cur = list.head();
    EXPECT_EQ(cur->data, 1);
    cur = cur->next;
    EXPECT_EQ(cur->data, 2);
    cur = cur->next;
    EXPECT_EQ(cur->data, 3);
    // Backward
    cur = list.tail();
    EXPECT_EQ(cur->data, 3);
    cur = cur->prev;
    EXPECT_EQ(cur->data, 2);
    cur = cur->prev;
    EXPECT_EQ(cur->data, 1);
}

TEST(DoublyLinkedListTest, CopyConstructor) {
    DoublyLinkedList<int> a = {1, 2, 3};
    DoublyLinkedList<int> b(a);
    EXPECT_EQ(b.size(), 3u);
    EXPECT_EQ(b.front(), 1);
    EXPECT_EQ(b.back(), 3);
    a.pop_front();
    EXPECT_EQ(b.size(), 3u);
}

TEST(DoublyLinkedListTest, CopyAssignment) {
    DoublyLinkedList<int> a = {1, 2, 3};
    DoublyLinkedList<int> b;
    b = a;
    EXPECT_EQ(b.size(), 3u);
    EXPECT_EQ(b.front(), 1);
}

TEST(DoublyLinkedListTest, MoveConstructor) {
    DoublyLinkedList<int> a = {1, 2, 3};
    DoublyLinkedList<int> b(std::move(a));
    EXPECT_EQ(b.size(), 3u);
    EXPECT_TRUE(a.empty());
}

TEST(DoublyLinkedListTest, MoveAssignment) {
    DoublyLinkedList<int> a = {1, 2, 3};
    DoublyLinkedList<int> b;
    b = std::move(a);
    EXPECT_EQ(b.size(), 3u);
    EXPECT_TRUE(a.empty());
}

TEST(DoublyLinkedListTest, Clear) {
    DoublyLinkedList<int> list = {1, 2, 3};
    list.clear();
    EXPECT_TRUE(list.empty());
    list.push_back(42);
    EXPECT_EQ(list.front(), 42);
}
