#include <algorithm>
#include <concepts>
#include <format>
#include <iostream>
#include <map>
#include <ranges>
#include <span>
#include <string>
#include <vector>

// C/C++ 关键知识示例 —— 现代 C++ 特性（C++20：concepts / ranges / span /
// format / 结构化绑定 / if constexpr）。
// 对应 README 第 13 章「C/C++ 关键知识 · 现代 C++ 特性速查」。
namespace {

template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

// 约束模板：只接受数值类型。
template <Numeric T>
T twice(T x) {
    return x * 2;
}

}  // namespace

int main() {
    std::cout << "== concepts 约束 ==\n";
    std::cout << "  twice(21)=" << twice(21) << " twice(2.5)=" << twice(2.5) << "\n";

    std::cout << "== ranges 管道（filter → transform）==\n";
    std::vector<int> v{5, 2, 8, 1, 6};
    auto even_squares =
        v | std::views::filter([](int x) { return x % 2 == 0; })
          | std::views::transform([](int x) { return x * x; });
    for (int x : even_squares) std::cout << "  " << x;
    std::cout << "\n";

    std::cout << "== std::format ==\n";
    std::cout << "  " << std::format("{} + {} = {}", 2, 3, 2 + 3) << "\n";

    std::cout << "== span（连续内存零拷贝视图）==\n";
    auto sum = [](std::span<const int> s) {
        int acc = 0;
        for (int x : s) acc += x;
        return acc;
    };
    std::cout << "  sum=" << sum(v) << "\n";

    std::cout << "== 结构化绑定 ==\n";
    auto [n, word] = std::pair<int, std::string>{1, "one"};
    std::cout << "  " << n << " -> " << word << "\n";
    std::map<std::string, int> scores{{"alice", 90}, {"bob", 85}};
    for (const auto& [name, score] : scores) {
        std::cout << "  " << name << ":" << score << "\n";
    }

    std::cout << "== if constexpr（编译期分支）==\n";
    auto classify = []<typename T>(T) {
        if constexpr (std::integral<T>) {
            return std::string("integral");
        } else if constexpr (std::floating_point<T>) {
            return std::string("floating_point");
        } else {
            return std::string("other");
        }
    };
    std::cout << "  int -> " << classify(1) << ", double -> " << classify(1.0)
              << ", string -> " << classify(std::string{}) << "\n";
    return 0;
}
