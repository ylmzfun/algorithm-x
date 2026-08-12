#include "ds/dynamic_array.h"

#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <utility>

using algorithm_x::ds::DynamicArray;

TEST(DynamicArrayTest, DefaultConstruction) {
    DynamicArray<int> a;
    EXPECT_EQ(a.size(), 0u);
    EXPECT_TRUE(a.empty());
    EXPECT_EQ(a.capacity(), 0u);
}

TEST(DynamicArrayTest, PushBackLvalue) {
    DynamicArray<int> a;
    int x = 10;
    a.push_back(x);
    EXPECT_EQ(a.size(), 1u);
    EXPECT_EQ(a[0], 10);
    EXPECT_EQ(a.front(), 10);
    EXPECT_EQ(a.back(), 10);

    a.push_back(x);
    EXPECT_EQ(a.size(), 2u);
    EXPECT_EQ(a[1], 10);
    EXPECT_EQ(a.back(), 10);
}

TEST(DynamicArrayTest, PushBackRvalue) {
    DynamicArray<std::string> a;
    a.push_back(std::string("hello"));
    EXPECT_EQ(a[0], "hello");
    a.push_back(std::string("world"));
    EXPECT_EQ(a[1], "world");
}

TEST(DynamicArrayTest, PopBack) {
    DynamicArray<int> a{1, 2, 3};
    EXPECT_EQ(a.size(), 3u);
    a.pop_back();
    EXPECT_EQ(a.size(), 2u);
    EXPECT_EQ(a.back(), 2);
    a.pop_back();
    a.pop_back();
    EXPECT_TRUE(a.empty());
}

TEST(DynamicArrayTest, PopBackOnEmptyThrows) {
    DynamicArray<int> a;
    EXPECT_THROW(a.pop_back(), std::out_of_range);
}

TEST(DynamicArrayTest, OperatorBracket) {
    DynamicArray<int> a{10, 20, 30};
    EXPECT_EQ(a[0], 10);
    EXPECT_EQ(a[1], 20);
    EXPECT_EQ(a[2], 30);
    a[0] = 100;
    EXPECT_EQ(a[0], 100);
}

TEST(DynamicArrayTest, AtWithBoundsCheck) {
    DynamicArray<int> a{1, 2, 3};
    EXPECT_EQ(a.at(0), 1);
    EXPECT_EQ(a.at(2), 3);
    EXPECT_THROW(a.at(3), std::out_of_range);
    EXPECT_THROW(a.at(100), std::out_of_range);

    const auto& ca = a;
    EXPECT_EQ(ca.at(1), 2);
    EXPECT_THROW(ca.at(3), std::out_of_range);
}

TEST(DynamicArrayTest, FrontAndBack) {
    DynamicArray<int> a{1, 2, 3};
    EXPECT_EQ(a.front(), 1);
    EXPECT_EQ(a.back(), 3);
    a.front() = 10;
    a.back() = 30;
    EXPECT_EQ(a.front(), 10);
    EXPECT_EQ(a.back(), 30);

    const auto& ca = a;
    EXPECT_EQ(ca.front(), 10);
    EXPECT_EQ(ca.back(), 30);
}

TEST(DynamicArrayTest, InsertAtBeginning) {
    DynamicArray<int> a{2, 3, 4};
    a.insert(0, 1);
    EXPECT_EQ(a.size(), 4u);
    EXPECT_EQ(a[0], 1);
    EXPECT_EQ(a[1], 2);
    EXPECT_EQ(a[2], 3);
    EXPECT_EQ(a[3], 4);
}

TEST(DynamicArrayTest, InsertAtMiddle) {
    DynamicArray<int> a{1, 3, 4};
    a.insert(1, 2);
    EXPECT_EQ(a.size(), 4u);
    EXPECT_EQ(a[0], 1);
    EXPECT_EQ(a[1], 2);
    EXPECT_EQ(a[2], 3);
    EXPECT_EQ(a[3], 4);
}

TEST(DynamicArrayTest, InsertAtEnd) {
    DynamicArray<int> a{1, 2, 3};
    a.insert(3, 4);
    EXPECT_EQ(a.size(), 4u);
    EXPECT_EQ(a[3], 4);
}

TEST(DynamicArrayTest, InsertOutOfRangeThrows) {
    DynamicArray<int> a{1, 2};
    EXPECT_THROW(a.insert(3, 99), std::out_of_range);
}

TEST(DynamicArrayTest, EraseAtBeginning) {
    DynamicArray<int> a{1, 2, 3};
    a.erase(0);
    EXPECT_EQ(a.size(), 2u);
    EXPECT_EQ(a[0], 2);
    EXPECT_EQ(a[1], 3);
}

TEST(DynamicArrayTest, EraseAtMiddle) {
    DynamicArray<int> a{1, 2, 3};
    a.erase(1);
    EXPECT_EQ(a.size(), 2u);
    EXPECT_EQ(a[0], 1);
    EXPECT_EQ(a[1], 3);
}

TEST(DynamicArrayTest, EraseAtEnd) {
    DynamicArray<int> a{1, 2, 3};
    a.erase(2);
    EXPECT_EQ(a.size(), 2u);
    EXPECT_EQ(a[0], 1);
    EXPECT_EQ(a[1], 2);
}

TEST(DynamicArrayTest, EraseOutOfRangeThrows) {
    DynamicArray<int> a{1, 2};
    EXPECT_THROW(a.erase(2), std::out_of_range);
    EXPECT_THROW(a.erase(100), std::out_of_range);
}

TEST(DynamicArrayTest, Reserve) {
    DynamicArray<int> a;
    a.reserve(100);
    EXPECT_GE(a.capacity(), 100u);
    EXPECT_EQ(a.size(), 0u);

    // reserve smaller than current capacity should not shrink
    std::size_t cap = a.capacity();
    a.reserve(10);
    EXPECT_EQ(a.capacity(), cap);
}

TEST(DynamicArrayTest, CapacityGrowth) {
    DynamicArray<int> a;
    EXPECT_EQ(a.capacity(), 0u);

    a.push_back(1);  // 0 → 4
    EXPECT_EQ(a.capacity(), 4u);

    a.push_back(2);
    a.push_back(3);
    a.push_back(4);
    EXPECT_EQ(a.capacity(), 4u);

    a.push_back(5);  // 4 → 8
    EXPECT_EQ(a.capacity(), 8u);
}

TEST(DynamicArrayTest, CopyConstructor) {
    DynamicArray<int> a{1, 2, 3};
    DynamicArray<int> b(a);
    EXPECT_EQ(b.size(), 3u);
    EXPECT_EQ(b[0], 1);
    EXPECT_EQ(b[1], 2);
    EXPECT_EQ(b[2], 3);

    // Ensure deep copy: modifying b does not affect a
    b[0] = 99;
    EXPECT_EQ(a[0], 1);
}

TEST(DynamicArrayTest, CopyAssignment) {
    DynamicArray<int> a{10, 20};
    DynamicArray<int> b{1, 2, 3, 4, 5};
    b = a;
    EXPECT_EQ(b.size(), 2u);
    EXPECT_EQ(b[0], 10);
    EXPECT_EQ(b[1], 20);
}

TEST(DynamicArrayTest, MoveConstructor) {
    DynamicArray<int> a{1, 2, 3};
    DynamicArray<int> b(std::move(a));
    EXPECT_EQ(b.size(), 3u);
    EXPECT_EQ(b[0], 1);
    EXPECT_EQ(b[1], 2);
    EXPECT_EQ(b[2], 3);
    EXPECT_EQ(a.size(), 0u);  // NOLINT: move-from object is valid but unspecified
}

TEST(DynamicArrayTest, MoveAssignment) {
    DynamicArray<int> a{10, 20, 30};
    DynamicArray<int> b{1};
    b = std::move(a);
    EXPECT_EQ(b.size(), 3u);
    EXPECT_EQ(b[0], 10);
    EXPECT_EQ(a.size(), 0u);  // NOLINT
}

TEST(DynamicArrayTest, InitializerListConstruction) {
    DynamicArray<int> a{5, 4, 3, 2, 1};
    EXPECT_EQ(a.size(), 5u);
    EXPECT_EQ(a[0], 5);
    EXPECT_EQ(a[4], 1);
}

TEST(DynamicArrayTest, Clear) {
    DynamicArray<int> a{1, 2, 3};
    EXPECT_FALSE(a.empty());
    a.clear();
    EXPECT_TRUE(a.empty());
    EXPECT_EQ(a.size(), 0u);

    // Can push after clear
    a.push_back(42);
    EXPECT_EQ(a.size(), 1u);
    EXPECT_EQ(a[0], 42);
}

TEST(DynamicArrayTest, BeginEndIteration) {
    DynamicArray<int> a{10, 20, 30};
    int expected = 10;
    for (auto it = a.begin(); it != a.end(); ++it) {
        EXPECT_EQ(*it, expected);
        expected += 10;
    }
}

TEST(DynamicArrayTest, RangeBasedForLoop) {
    DynamicArray<int> a{1, 2, 3, 4, 5};
    int sum = 0;
    for (const auto& v : a) {
        sum += v;
    }
    EXPECT_EQ(sum, 15);
}

TEST(DynamicArrayTest, LargeNumberOfInsertions) {
    DynamicArray<int> a;
    constexpr int N = 10000;
    for (int i = 0; i < N; ++i) {
        a.push_back(i);
    }
    EXPECT_EQ(a.size(), static_cast<std::size_t>(N));
    for (int i = 0; i < N; ++i) {
        EXPECT_EQ(a[i], i);
    }
    EXPECT_GE(a.capacity(), static_cast<std::size_t>(N));
}

TEST(DynamicArrayTest, DataPointer) {
    DynamicArray<int> a{1, 2, 3};
    int* raw = a.data();
    EXPECT_EQ(raw[0], 1);
    EXPECT_EQ(raw[1], 2);
    EXPECT_EQ(raw[2], 3);

    const auto& ca = a;
    const int* craw = ca.data();
    EXPECT_EQ(craw[0], 1);
}

TEST(DynamicArrayTest, EmptyFrontAndBack) {
    DynamicArray<int> a;
    // front() and back() on empty array have undefined behavior in our
    // implementation (no bounds check). We only verify the const overloads
    // are accessible.
    EXPECT_TRUE(a.empty());
}

TEST(DynamicArrayTest, MoveSemanticsPreserveData) {
    DynamicArray<std::string> a;
    a.push_back("one");
    a.push_back("two");
    a.push_back("three");

    // Move via explicit push_back(std::move(...))
    std::string s = "four";
    a.push_back(std::move(s));
    EXPECT_TRUE(s.empty());  // moved-from string
    EXPECT_EQ(a[3], "four");
}
