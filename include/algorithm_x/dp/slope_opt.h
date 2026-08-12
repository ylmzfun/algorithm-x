#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <vector>

namespace algorithm_x {
namespace dp {

// Convex Hull Trick (CHT) for DP optimization.
// Supports adding lines y = mx + b and querying minimum value at x.
// Assumes slopes are added in decreasing order (monotonic).
// For maximum queries, negate slopes and intercepts.
template <typename T>
class ConvexHullTrick {
    struct Line {
        T m, b;
        // Intersection x-coordinate with previous line
        double intersect_x(const Line& other) const {
            return static_cast<double>(other.b - b) /
                   static_cast<double>(m - other.m);
        }
    };

public:
    // Add line y = mx + b. Slopes must be added in decreasing order.
    void add_line(T m, T b) {
        Line line{m, b};
        while (hull_.size() >= 2) {
            auto& l1 = hull_[hull_.size() - 2];
            auto& l2 = hull_.back();
            if (l2.intersect_x(l1) >= line.intersect_x(l2)) {
                hull_.pop_back();
            } else {
                break;
            }
        }
        hull_.push_back(line);
    }

    // Query minimum y at given x. Queries must be in increasing order.
    T query(T x) {
        if (hull_.empty()) return std::numeric_limits<T>::max();
        while (ptr_ + 1 < hull_.size()) {
            auto& l1 = hull_[ptr_];
            auto& l2 = hull_[ptr_ + 1];
            if (l1.m * x + l1.b > l2.m * x + l2.b) {
                ++ptr_;
            } else {
                break;
            }
        }
        return hull_[ptr_].m * x + hull_[ptr_].b;
    }

    void clear() {
        hull_.clear();
        ptr_ = 0;
    }

private:
    std::vector<Line> hull_;
    std::size_t ptr_ = 0;
};

}  // namespace dp
}  // namespace algorithm_x
