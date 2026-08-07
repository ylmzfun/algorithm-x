#include "algorithm_x/distributed/distributed_lock.h"
#include "gtest/gtest.h"
using namespace algorithm_x::distributed;
namespace {
TEST(DistLock, AcquireRelease) {
    DistributedLock lock(2);
    EXPECT_TRUE(lock.acquire(0));
    EXPECT_FALSE(lock.acquire(0));
    lock.release(0);
    EXPECT_TRUE(lock.acquire(0));
}
}  // namespace
