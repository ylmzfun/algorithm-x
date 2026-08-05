#include "algorithm_x/string/sam.h"
#include <string>
#include "gtest/gtest.h"
using namespace algorithm_x::string;
namespace {
TEST(SAM, Contains) {
    SuffixAutomaton sam; sam.build("hello");
    EXPECT_TRUE(sam.contains("ell"));
    EXPECT_TRUE(sam.contains("hello"));
    EXPECT_FALSE(sam.contains("world"));
}
TEST(SAM, Empty) { SuffixAutomaton sam; sam.build(""); EXPECT_TRUE(sam.contains("")); }
}  // namespace
