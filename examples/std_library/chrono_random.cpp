#include <chrono>
#include <iostream>
#include <random>
#include <vector>

// 核心库示例 —— 计时（<chrono>）与随机数（<random>）。
// 对应 README 第 13 章「核心库 · 时间 / 数值」。
int main() {
    std::cout << "== chrono 高精度计时 ==\n";
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> v(1'000'000);
    long long sum = 0;
    for (int i = 0; i < static_cast<int>(v.size()); ++i) {
        v[static_cast<std::size_t>(i)] = i;
        sum += i;
    }
    auto t1 = std::chrono::steady_clock::now();
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0)
                  .count();
    std::cout << "  sum=" << sum << " 耗时 " << ms << " ms\n";

    std::cout << "== random 引擎与分布（固定种子可复现）==\n";
    std::mt19937 gen(42);
    std::uniform_int_distribution<int> dice(1, 6);
    std::normal_distribution<double> gauss(0.0, 1.0);
    int sixes = 0;
    for (int i = 0; i < 1000; ++i) {
        if (dice(gen) == 6) ++sixes;
    }
    std::cout << "  掷骰子 1000 次得到 6 的次数: " << sixes << "\n";
    std::cout << "  标准正态样本: " << gauss(gen) << "\n";
    return 0;
}
