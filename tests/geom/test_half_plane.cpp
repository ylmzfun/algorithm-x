#include "geom/half_plane.h"
#include "geom/point.h"
#include "gtest/gtest.h"
using namespace algorithm_x::geom;
namespace {
TEST(HalfPlane, Square) {
    // 四条边围成 [-1,1] × [-1,1] 的正方形
    std::vector<HalfPlane> planes = {
        {1.0, 0.0, -1.0},   // x <= 1
        {-1.0, 0.0, -1.0},  // x >= -1
        {0.0, 1.0, -1.0},   // y <= 1
        {0.0, -1.0, -1.0},  // y >= -1
    };
    auto poly = half_plane_intersection(planes);
    ASSERT_FALSE(poly.empty());
    EXPECT_NEAR(polygon_area(poly), 4.0, 1e-6);
}
TEST(HalfPlane, Triangle) {
    // x >= 0, y >= 0, x + y <= 2 → 三角形面积 2
    std::vector<HalfPlane> planes = {
        {-1.0, 0.0, 0.0},   // x >= 0
        {0.0, -1.0, 0.0},   // y >= 0
        {1.0, 1.0, -2.0},   // x + y <= 2
    };
    auto poly = half_plane_intersection(planes);
    ASSERT_FALSE(poly.empty());
    EXPECT_NEAR(polygon_area(poly), 2.0, 1e-6);
}
TEST(HalfPlane, Empty) {
    // x <= 0 且 x >= 1：无交集
    std::vector<HalfPlane> planes = {
        {1.0, 0.0, 0.0},
        {-1.0, 0.0, 1.0},
    };
    EXPECT_TRUE(half_plane_intersection(planes).empty());
}
TEST(HalfPlane, EmptyInput) {
    EXPECT_TRUE(half_plane_intersection({}).empty());
}
}  // namespace
