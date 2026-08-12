#include <iostream>
#include <string>
#include <utility>

// C/C++ 关键知识示例 —— 值类别（lvalue / rvalue）、移动语义、完美转发。
// 对应 README 第 13 章「C/C++ 关键知识 · 语言核心」。
namespace {

struct Widget {
    std::string name;
    explicit Widget(std::string n) : name(std::move(n)) {}
    Widget(const Widget& other) : name(other.name) { std::cout << "  [copy]\n"; }
    Widget(Widget&& other) noexcept : name(std::move(other.name)) {
        std::cout << "  [move]\n";
    }
};

// 完美转发：arg 保持调用处的值类别（左值 → 左值，右值 → 右值）。
template <typename T>
void relay(T&& arg) {
    Widget w(std::forward<T>(arg));
}

void show(Widget&) { std::cout << "  lvalue overload\n"; }
void show(Widget&&) { std::cout << "  rvalue overload\n"; }

}  // namespace

int main() {
    std::cout << "== 值类别 ==\n";
    Widget a("A");
    show(a);               // 具名变量 → lvalue
    show(Widget("temp"));  // 临时对象 → rvalue（prvalue）
    show(std::move(a));    // std::move → xvalue（也是 rvalue）

    std::cout << "== 移动语义（std::move 后原对象通常被置空）==\n";
    std::string src(100, 'x');
    std::string dst = std::move(src);
    std::cout << "  src.size()=" << src.size() << " dst.size()=" << dst.size() << "\n";

    std::cout << "== 完美转发 ==\n";
    relay(a);              // 左值实参 → 拷贝构造
    relay(Widget("B"));    // 右值实参 → 移动构造
    return 0;
}
