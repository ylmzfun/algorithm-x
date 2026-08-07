#include "algorithm_x/string/min_representation.h"
#include <string>
#include "gtest/gtest.h"
using namespace algorithm_x::string;
namespace {
TEST(MinRep, Basic) { EXPECT_EQ(min_representation("bca"), "abc"); }
TEST(MinRep, AlreadyMin) { EXPECT_EQ(min_representation("abc"), "abc"); }
TEST(MinRep, AllSame) { EXPECT_EQ(min_representation("aaa"), "aaa"); }
}  // namespace
