#include "algorithm_x/concurrent/dining.h"
#include <thread>
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::concurrent;
namespace {
TEST(Dining, NoDeadlock) {
    DiningPhilosophers dp;
    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i) threads.emplace_back([&dp, i]() { dp.philosopher(i); });
    for (auto& t : threads) t.join();
    SUCCEED();
}
}  // namespace
