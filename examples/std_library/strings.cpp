#include <iostream>
#include <regex>
#include <sstream>
#include <string>
#include <string_view>

// 核心库示例 —— 字符串与文本处理（<string> / <string_view> / <regex>）。
// 对应 README 第 13 章「核心库 · 字符串」。
int main() {
    std::cout << "== string 拼接 ==\n";
    std::string s = "Hello";
    s += ", ";
    s.append("World");
    s.push_back('!');
    std::cout << "  " << s << " (len=" << s.size() << ")\n";

    std::cout << "== string_view（零拷贝视图）==\n";
    const char* raw = "view me";
    std::string_view sv(raw);  // 不复制数据
    std::cout << "  " << sv.substr(0, 4) << "\n";

    std::cout << "== ostringstream（内存流拼接）==\n";
    std::ostringstream oss;
    oss << "value = " << 42;
    std::cout << "  " << oss.str() << "\n";

    std::cout << "== regex 匹配（捕获组）==\n";
    std::regex re(R"((\d{4})-(\d{2})-(\d{2}))");
    std::smatch m;
    const std::string date = "today is 2026-08-12, ok";
    if (std::regex_search(date, m, re)) {
        std::cout << "  year=" << m[1] << " month=" << m[2] << " day=" << m[3]
                  << "\n";
    }
    return 0;
}
