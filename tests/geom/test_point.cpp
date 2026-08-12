#include "geom/point.h"

#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::geom;

TEST(PointOps, Addition) {
    Point a{1, 2}, b{3, 4};
    Point c = a + b;
    EXPECT_DOUBLE_EQ(c.x, 4);
    EXPECT_DOUBLE_EQ(c.y, 6);
}

TEST(PointOps, Subtraction) {
    Point a{5, 7}, b{2, 3};
    Point c = a - b;
    EXPECT_DOUBLE_EQ(c.x, 3);
    EXPECT_DOUBLE_EQ(c.y, 4);
}

TEST(PointOps, ScalarMultiply) {
    Point a{2, 3};
    Point c = a * 2;
    EXPECT_DOUBLE_EQ(c.x, 4);
    EXPECT_DOUBLE_EQ(c.y, 6);
}

TEST(PointOps, DotProduct) {
    Point a{1, 2}, b{3, 4};
    EXPECT_DOUBLE_EQ(a * b, 11);
}

TEST(PointOps, Equality) {
    EXPECT_TRUE((Point{1, 2} == Point{1, 2}));
    EXPECT_FALSE((Point{1, 2} == Point{1, 3}));
}

TEST(CrossProduct, Perpendicular) {
    EXPECT_DOUBLE_EQ(cross({1, 0}, {0, 1}), 1);
    EXPECT_DOUBLE_EQ(cross({0, 1}, {1, 0}), -1);
}

TEST(CrossProduct, Parallel) {
    EXPECT_DOUBLE_EQ(cross({2, 3}, {4, 6}), 0);
    EXPECT_DOUBLE_EQ(cross({1, 0}, {3, 0}), 0);
}

TEST(Distance, Euclidean) {
    EXPECT_DOUBLE_EQ(dist({0, 0}, {3, 4}), 5);
}

TEST(Distance, SamePoint) {
    EXPECT_DOUBLE_EQ(dist({7, 7}, {7, 7}), 0);
}

TEST(DistanceSquared, Basic) {
    EXPECT_DOUBLE_EQ(dist2({0, 0}, {3, 4}), 25);
}

TEST(PolygonArea, Square) {
    std::vector<Point> sq = {{0, 0}, {2, 0}, {2, 2}, {0, 2}};
    EXPECT_DOUBLE_EQ(polygon_area(sq), 4);
}

TEST(PolygonArea, Triangle) {
    std::vector<Point> tri = {{0, 0}, {3, 0}, {0, 4}};
    EXPECT_DOUBLE_EQ(polygon_area(tri), 6);
}

TEST(PolygonArea, ClockwiseOrder) {
    std::vector<Point> cw = {{0, 0}, {0, 2}, {2, 2}, {2, 0}};
    EXPECT_NEAR(polygon_area(cw), -4, 1e-9);
}

TEST(OnSegment, Middle) {
    EXPECT_TRUE(on_segment({0, 0}, {4, 0}, {2, 0}));
}

TEST(OnSegment, Endpoint) {
    EXPECT_TRUE(on_segment({0, 0}, {4, 0}, {4, 0}));
}

TEST(OnSegment, Outside) {
    EXPECT_FALSE(on_segment({0, 0}, {4, 0}, {5, 0}));
    EXPECT_FALSE(on_segment({0, 0}, {4, 0}, {2, 1}));
}

TEST(Orient, CCW) {
    EXPECT_GT(orient({0, 0}, {1, 0}, {0, 1}), 0);
}

TEST(Orient, CW) {
    EXPECT_LT(orient({0, 0}, {1, 0}, {0, -1}), 0);
}

TEST(Orient, Collinear) {
    EXPECT_DOUBLE_EQ(orient({0, 0}, {1, 0}, {2, 0}), 0);
}
