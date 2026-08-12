#include "string/boyer_moore.h"
#include <string>
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::string;
namespace {
TEST(BoyerMoore, Found) { EXPECT_EQ(boyer_moore_search("hello world", "world"), std::vector<std::size_t>{6}); }
TEST(BoyerMoore, Multiple) { EXPECT_EQ(boyer_moore_search("aaa", "aa"), std::vector<std::size_t>({0, 1})); }
TEST(BoyerMoore, NotFound) { EXPECT_TRUE(boyer_moore_search("abc", "xyz").empty()); }
TEST(BoyerMoore, EmptyPattern) { EXPECT_TRUE(boyer_moore_search("abc", "").empty()); }
}  // namespace
