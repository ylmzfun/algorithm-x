#include "algorithm_x/advanced/cdq.h"
#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(CDQ, RectCount) {
    std::vector<CDQPoint> pts = {{0,0},{2,2},{5,5}};
    std::vector<CDQQuery> queries = {{0,0,3,3,0}};
    auto ans=cdq_rect_count(pts, queries);
    EXPECT_EQ(ans.size(),1u);
}
}  // namespace
