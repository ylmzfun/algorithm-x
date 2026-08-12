#pragma once

#include <cstddef>
#include <functional>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace distributed {

// MapReduce 教学框架 —— Map → Shuffle → Reduce 三个阶段。
//
//   Map    ：对每个输入元素调用 map_fn，产出若干 (Key, Value) 对；
//   Shuffle：按 Key 对所有 (Key, Value) 对分组；
//   Reduce ：对每个 Key 的 value 列表调用 reduce_fn 合并为一个 Value。
//
// 简化说明：
//   - 单机顺序执行，未模拟分布式并行、分区与容错；
//   - reduce_fn 采用签名 Value(const Value& acc, const Value& v)：
//     以组内首元素为初值，从左到右两两折叠；
//   - shuffle 直接用 std::map 完成（Key 需满足严格弱序）。
template <typename In, typename Key, typename Value, typename ReduceFunc>
std::map<Key, Value> map_reduce(
    const std::vector<In>& input,
    std::function<std::vector<std::pair<Key, Value>>(const In&)> map_fn,
    ReduceFunc reduce_fn) {
    // Map 阶段：对每个输入元素产出 (Key, Value) 对。
    std::vector<std::pair<Key, Value>> pairs;
    for (const In& item : input) {
        std::vector<std::pair<Key, Value>> mapped = map_fn(item);
        pairs.insert(pairs.end(), mapped.begin(), mapped.end());
    }

    // Shuffle 阶段：按 Key 分组。
    std::map<Key, std::vector<Value>> groups;
    for (const auto& pair : pairs) {
        groups[pair.first].push_back(pair.second);
    }

    // Reduce 阶段：对每个 Key 合并 values。
    std::map<Key, Value> result;
    for (const auto& group : groups) {
        if (group.second.empty()) continue;
        Value acc = group.second.front();
        for (std::size_t i = 1; i < group.second.size(); ++i) {
            acc = reduce_fn(acc, group.second[i]);
        }
        result[group.first] = acc;
    }
    return result;
}

// 便捷函数：按空格分词统计单词出现次数。
inline std::map<std::string, int> word_count(const std::vector<std::string>& texts) {
    std::vector<std::string> words;
    for (const std::string& text : texts) {
        std::istringstream iss(text);
        std::string word;
        while (iss >> word) {
            words.push_back(word);
        }
    }
    return map_reduce<std::string, std::string, int>(
        words,
        [](const std::string& w) {
            return std::vector<std::pair<std::string, int>>{{w, 1}};
        },
        [](const int& acc, const int& v) { return acc + v; });
}

}  // namespace distributed
}  // namespace algorithm_x
