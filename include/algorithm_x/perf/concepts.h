#pragma once

#include <concepts>
#include <string>
#include <type_traits>

namespace algorithm_x {
namespace perf {

// ---- Concepts（C++20）----

// 概念：可相加类型（需要支持 a + b）。
template <typename T>
concept Addable = requires(T a, T b) { a + b; };

// 概念：可流式输出类型（需要支持 os << a）。
template <typename T>
concept Printable = requires(std::ostream& os, const T& a) { os << a; };

// ---- SFINAE（enable_if）----

// SFINAE 版：仅接受整型，否则 SFINAE 掉（无匹配重载 → 编译错误提示更友好）。
template <typename T,
          typename = std::enable_if_t<std::is_integral_v<T>>>
inline T twice_sfinae(T x) {
    return x * 2;
}

// ---- requires 子句（C++20）----

// requires 版：仅接受整型。
template <typename T>
    requires std::integral<T>
inline T twice_requires(T x) {
    return x * 2;
}

// 约束与模板头并列的写法。
template <typename T>
    requires Addable<T>
inline T sum(T a, T b) {
    return a + b;
}

// ---- 重载分派（overload resolution with constraints）----

// 整型版本。
template <typename T>
    requires std::integral<T>
inline std::string classify() {
    return "integral";
}

// 浮点版本。
template <typename T>
    requires std::floating_point<T>
inline std::string classify() {
    return "floating_point";
}

// 其余类型（requires 表达式约束）。
template <typename T>
    requires(!std::integral<T> && !std::floating_point<T>)
inline std::string classify() {
    return "other";
}

// ---- 编译期 if（if constexpr + concept）----

// 对整型返回翻倍，对浮点返回平方，其他类型返回 0。
template <typename T>
inline T transform(T x) {
    if constexpr (std::integral<T>) {
        return x * 2;
    } else if constexpr (std::floating_point<T>) {
        return x * x;
    } else {
        return T{};
    }
}

}  // namespace perf
}  // namespace algorithm_x
