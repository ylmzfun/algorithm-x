#include "algorithm_x/math/principles.h"
#include "gtest/gtest.h"
using namespace algorithm_x::math;
namespace {
TEST(InclusionExclusion, ThreeSets) {
    // |A|=3, |B|=4, |C|=5, |A∩B|=1, |A∩C|=2, |B∩C|=1, |A∩B∩C|=0
    std::vector<int64_t> intersections = {0, 3, 4, 1, 5, 2, 1, 0};
    EXPECT_EQ(inclusion_exclusion(intersections), 8);
}
TEST(InclusionExclusion, OverlappingSets) {
    // 集合 {1,2,3} 与 {2,3} 的并大小为 3
    std::vector<int64_t> intersections = {0, 3, 2, 2};
    EXPECT_EQ(inclusion_exclusion(intersections), 3);
}
TEST(Pigeonhole, Basic) {
    EXPECT_TRUE(pigeonhole(5, 3));
    EXPECT_FALSE(pigeonhole(3, 5));
    EXPECT_FALSE(pigeonhole(3, 3));
}
TEST(Pigeonhole, MaxMin) {
    EXPECT_EQ(pigeonhole_max_min(10, 3), 4);
    EXPECT_EQ(pigeonhole_max_min(9, 3), 3);
    EXPECT_EQ(pigeonhole_max_min(5, 0), 5);
}
}  // namespace
