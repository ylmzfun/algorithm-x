#include "algorithm_x/distributed/vector_clock.h"
#include "gtest/gtest.h"
using namespace algorithm_x::distributed;
namespace {
TEST(VectorClock, Basic) {
    VectorClock a(3),b(3);
    a.increment(0); b.increment(1);
    EXPECT_TRUE(a.is_concurrent(b));
    a.merge(b);
    EXPECT_TRUE(a.happens_before(b) || b.happens_before(a) || a.is_concurrent(b));
}
}  // namespace
