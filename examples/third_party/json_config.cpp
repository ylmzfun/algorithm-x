#include <iostream>
#include <nlohmann/json.hpp>
#include <sstream>
#include <string>

// 第三方库示例 —— nlohmann/json 解析与序列化。
// 依赖：vcpkg install nlohmann-json
using nlohmann::json;

int main() {
    std::cout << "== 构造 JSON（初始化列表）==\n";
    json config = {
        {"name", "server"},
        {"port", 8080},
        {"debug", false},
        {"tags", {"c++", "network"}},
        {"limits", {{"max_conn", 100}, {"timeout_ms", 5000}}},
    };
    std::cout << config.dump(2) << "\n";

    std::cout << "== 读取字段 ==\n";
    std::cout << "  name=" << config["name"].get<std::string>()
              << " port=" << config["port"].get<int>()
              << " tags[0]=" << config["tags"][0].get<std::string>() << "\n";

    std::cout << "== 从字符串解析 ==\n";
    std::istringstream in(R"({"x": [1, 2, 3], "ok": true})");
    json parsed = json::parse(in);
    const int x_sum = parsed["x"][0].get<int>() + parsed["x"][1].get<int>() +
                      parsed["x"][2].get<int>();
    std::cout << "  x 之和=" << x_sum << " ok=" << parsed["ok"].get<bool>() << "\n";

    std::cout << "== 序列化回字符串 ==\n";
    std::string out = json{{"a", 1}, {"b", 2.5}}.dump();
    std::cout << "  " << out << "\n";
    return 0;
}
