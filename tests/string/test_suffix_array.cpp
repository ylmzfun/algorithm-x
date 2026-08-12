#include "string/suffix_array.h"
#include <string>
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::string;
namespace {
TEST(SuffixArray, Banana) {
    SuffixArray sa("banana");
    auto arr = sa.sa();
    EXPECT_EQ(arr.size(), 6u);
}
TEST(SuffixArray, LCP) {
    SuffixArray sa("banana");
    auto l = sa.lcp();
    EXPECT_EQ(l.size(), 6u);
}
TEST(SuffixArray, Empty) { SuffixArray sa(""); EXPECT_EQ(sa.sa().size(), 0u); }
}  // namespace
