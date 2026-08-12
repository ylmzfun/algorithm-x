#include "geom/sweep_line.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::geom;
namespace {
TEST(SweepLine, RectArea) {
    std::vector<Rect> rects = {{0, 0, 2, 2}};
    EXPECT_NEAR(rectangle_union_area(rects), 4.0, 1e-9);
}
TEST(SweepLine, TwoOverlapping) {
    std::vector<Rect> rects = {{0, 0, 2, 2}, {1, 1, 3, 3}};
    EXPECT_NEAR(rectangle_union_area(rects), 7.0, 1e-9);
}
}  // namespace
