#include "algorithm_x/geom/intersection.h"

#include <algorithm>
#include <cmath>
#include <random>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::geom;

TEST(SegmentIntersect, CrossingX) {
    Point a{0, 0}, b{2, 2};
    Point c{0, 2}, d{2, 0};
    EXPECT_TRUE(segment_intersect(a, b, c, d));
}

TEST(SegmentIntersect, ParallelNonOverlapping) {
    Point a{0, 0}, b{2, 0};
    Point c{0, 2}, d{2, 2};
    EXPECT_FALSE(segment_intersect(a, b, c, d));
}

TEST(SegmentIntersect, TJunction) {
    Point a{0, 0}, b{2, 0};
    Point c{1, 0}, d{1, 2};
    EXPECT_TRUE(segment_intersect(a, b, c, d));
}

TEST(SegmentIntersect, CollinearOverlapping) {
    Point a{0, 0}, b{3, 0};
    Point c{1, 0}, d{4, 0};
    EXPECT_TRUE(segment_intersect(a, b, c, d));
}

TEST(SegmentIntersect, CollinearNonOverlapping) {
    Point a{0, 0}, b{1, 0};
    Point c{2, 0}, d{3, 0};
    EXPECT_FALSE(segment_intersect(a, b, c, d));
}

TEST(SegmentIntersect, EndpointTouch) {
    Point a{0, 0}, b{2, 2};
    Point c{2, 2}, d{3, 1};
    EXPECT_TRUE(segment_intersect(a, b, c, d));
}

TEST(SegmentIntersect, NoIntersection) {
    Point a{0, 0}, b{1, 1};
    Point c{2, 0}, d{3, 1};
    EXPECT_FALSE(segment_intersect(a, b, c, d));
}

TEST(ClosestPair, SimpleFourPoints) {
    std::vector<Point> pts = {{0, 0}, {1, 0}, {10, 10}, {11, 10}};
    double d = closest_pair(pts);
    EXPECT_NEAR(d, 1.0, 1e-9);
}

TEST(ClosestPair, DuplicatePoints) {
    std::vector<Point> pts = {{0, 0}, {1, 1}, {1, 1}, {3, 3}};
    double d = closest_pair(pts);
    EXPECT_NEAR(d, 0.0, 1e-9);
}

TEST(ClosestPair, TwoPoints) {
    std::vector<Point> pts = {{0, 0}, {3, 4}};
    double d = closest_pair(pts);
    EXPECT_NEAR(d, 5.0, 1e-9);
}

TEST(ClosestPair, LargeRandom) {
    std::mt19937 gen(42);
    std::uniform_real_distribution<double> udist(-1000.0, 1000.0);
    std::vector<Point> pts(100);
    for (auto& p : pts) {
        p = {udist(gen), udist(gen)};
    }

    double d = closest_pair(pts);

    // Brute-force verify
    double brute_min = std::numeric_limits<double>::max();
    for (std::size_t i = 0; i < pts.size(); ++i) {
        for (std::size_t j = i + 1; j < pts.size(); ++j) {
            brute_min = std::min(brute_min, dist(pts[i], pts[j]));
        }
    }
    EXPECT_NEAR(d, brute_min, 1e-9);
}
