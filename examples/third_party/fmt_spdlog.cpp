#include <fmt/core.h>
#include <fmt/ranges.h>
#include <spdlog/spdlog.h>
#include <vector>

// 第三方库示例 —— fmt 格式化 + spdlog 日志。
// 依赖：vcpkg install fmt spdlog
int main() {
    // fmt：类型安全、可读的格式化（std::format 的前身）
    fmt::print("== fmt ==\n");
    fmt::print("  {0} + {1} = {2}\n", 2, 3, 5);
    fmt::print("  hex: {:#x}, 右对齐: {:>8}\n", 255, "hi");

    std::vector<int> v{1, 2, 3};
    fmt::print("  vector: {}\n", v);  // 需要 <fmt/ranges.h>

    // spdlog：多级日志（默认输出到 stderr）
    spdlog::info("== spdlog ==");
    spdlog::info("user {} scored {}", "alice", 90);
    spdlog::warn("disk usage {:.1f}%", 87.3);
    spdlog::error("failed to open file: {}", "config.ini");
    return 0;
}
