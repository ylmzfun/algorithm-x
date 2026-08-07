#include "algorithm_x/algo/external_sort.h"
#include <fstream>
#include "gtest/gtest.h"
using namespace algorithm_x::algo;
namespace {
TEST(ExternalSort, Basic) {
    std::ofstream f("test_in.txt"); for (int x : {5,2,8,1,3}) f << x << "\n"; f.close();
    external_sort("test_in.txt", "test_out.txt", 2);
    std::ifstream in("test_out.txt"); int prev=-999, cur; bool ok=true;
    while(in>>cur){ if(cur<prev) ok=false; prev=cur; }
    EXPECT_TRUE(ok);
}
}  // namespace
