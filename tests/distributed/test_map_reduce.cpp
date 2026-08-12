#include "distributed/map_reduce.h"

#include <map>
#include <string>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::distributed;

namespace {

TEST(MapReduce, WordCount) {
    std::map<std::string, int> counts = word_count({"hello world", "hello algorithm"});
    EXPECT_EQ(counts.size(), 3u);
    EXPECT_EQ(counts["hello"], 2);
    EXPECT_EQ(counts["world"], 1);
    EXPECT_EQ(counts["algorithm"], 1);
}

// map 阶段产出 (x, x*x)，shuffle 按 key 分组，reduce 累加。
// 输入 {2,2,2} 映射为三个 (2,4)，同 key 的 value 累加为 4+4+4=12（即平方和）。
TEST(MapReduce, SumOfSquares) {
    std::vector<int> input{2, 2, 2};
    auto result = map_reduce<int, int, int>(
        input,
        [](const int& x) {
            return std::vector<std::pair<int, int>>{{x, x * x}};
        },
        [](const int& acc, const int& v) { return acc + v; });
    EXPECT_EQ(result.size(), 1u);
    EXPECT_EQ(result.at(2), 12);
}

TEST(MapReduce, EmptyInput) {
    auto result = map_reduce<int, int, int>(
        std::vector<int>{},
        [](const int&) { return std::vector<std::pair<int, int>>{}; },
        [](const int& acc, const int& v) { return acc + v; });
    EXPECT_TRUE(result.empty());
    EXPECT_TRUE(word_count({}).empty());
}

}  // namespace
