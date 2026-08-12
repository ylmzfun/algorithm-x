#include "geom/convex_hull.h"

#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::geom;

namespace {

TEST(ConvexHull, Square) {
    std::vector<Point> pts = {{0, 0}, {2, 0}, {2, 2}, {0, 2}};
    auto hull = convex_hull(pts);
    EXPECT_EQ(hull.size(), 4u);
}

TEST(ConvexHull, SquareWithInterior) {
    std::vector<Point> pts = {{0, 0}, {2, 0}, {2, 2}, {1, 1}, {0, 2}};
    auto hull = convex_hull(pts);
    EXPECT_EQ(hull.size(), 4u);
}

TEST(ConvexHull, Triangle) {
    std::vector<Point> pts = {{0, 0}, {3, 0}, {1, 2}};
    auto hull = convex_hull(pts);
    EXPECT_EQ(hull.size(), 3u);
}

TEST(ConvexHull, Collinear) {
    std::vector<Point> pts = {{0, 0}, {1, 1}, {2, 2}, {3, 3}};
    auto hull = convex_hull(pts);
    EXPECT_GE(hull.size(), 2u);
    EXPECT_LE(hull.size(), 2u);
}

TEST(ConvexHull, SinglePoint) {
    std::vector<Point> pts = {{5, 3}};
    auto hull = convex_hull(pts);
    EXPECT_EQ(hull.size(), 1u);
}

TEST(ConvexHull, TwoPoints) {
    std::vector<Point> pts = {{0, 0}, {1, 1}};
    auto hull = convex_hull(pts);
    EXPECT_EQ(hull.size(), 2u);
}

TEST(ConvexHull, HullIsConvex) {
    std::vector<Point> pts = {
        {0, 0}, {3, 1}, {2, 3}, {5, 4}, {1, 5}, {4, 2}, {2, 2},
    };
    auto hull = convex_hull(pts);
    ASSERT_GE(hull.size(), 3u);

    std::size_t n = hull.size();
    bool all_positive = true;
    bool all_negative = true;
    for (std::size_t i = 0; i < n; ++i) {
        double o = orient(hull[i], hull[(i + 1) % n], hull[(i + 2) % n]);
        if (o > 1e-9) all_negative = false;
        if (o < -1e-9) all_positive = false;
    }
    EXPECT_TRUE(all_positive || all_negative);
}

}  // namespace
