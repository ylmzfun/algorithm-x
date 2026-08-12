#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

// 核心库示例 —— 标准库算法（<algorithm> / <numeric>）。
// 对应 README 第 13 章「核心库 · 算法」。
int main() {
    std::vector<int> v{5, 2, 8, 1, 6, 3};

    std::sort(v.begin(), v.end());
    std::cout << "== sort: ";
    for (int x : v) std::cout << x << ' ';
    std::cout << "\n";

    auto it = std::lower_bound(v.begin(), v.end(), 4);  // 第一个 >= 4 的位置
    std::cout << "== lower_bound(4) 下标: " << std::distance(v.begin(), it) << "\n";

    std::cout << "== accumulate 求和: " << std::accumulate(v.begin(), v.end(), 0)
              << "\n";

    auto is_even = [](int x) { return x % 2 == 0; };
    std::cout << "== count_if(偶数): "
              << std::count_if(v.begin(), v.end(), is_even) << "\n";
    std::cout << "== all_of(>0): "
              << std::all_of(v.begin(), v.end(), [](int x) { return x > 0; })
              << "\n";

    std::vector<int> sq(v.size());
    std::transform(v.begin(), v.end(), sq.begin(), [](int x) { return x * x; });
    std::cout << "== transform 平方: ";
    for (int x : sq) std::cout << x << ' ';
    std::cout << "\n";

    std::reverse(v.begin(), v.end());
    std::cout << "== reverse 后首元素: " << v.front() << "\n";
    return 0;
}
