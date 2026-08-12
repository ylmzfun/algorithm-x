#include <Eigen/Dense>
#include <fmt/core.h>
#include <iostream>
#include <nlohmann/json.hpp>
#include <spdlog/spdlog.h>
#include <string>

// 综合使用案例 —— JSON 配置 + 日志 + Eigen 数值求解，链路串起来。
// 依赖：vcpkg install fmt spdlog nlohmann-json eigen3
using nlohmann::json;

int main() {
    // 1) JSON 配置（模拟从文件读入）
    json cfg = {
        {"matrix", {{3, 1}, {1, 2}}},
        {"rhs", {9, 8}},
        {"solver", "colPivHouseholderQr"},
    };
    spdlog::info("加载配置: solver={}", cfg["solver"].get<std::string>());

    // 2) 从 JSON 构造矩阵 / 向量
    Eigen::MatrixXd A(2, 2);
    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            A(i, j) = cfg["matrix"][i][j].get<double>();
        }
    }
    Eigen::VectorXd b(2);
    for (int i = 0; i < 2; ++i) {
        b(i) = cfg["rhs"][i].get<double>();
    }

    // 3) Eigen 求解线性方程组
    Eigen::VectorXd x = A.colPivHouseholderQr().solve(b);
    spdlog::info("解得 x = [{:.2f}, {:.2f}]", x(0), x(1));

    // 4) 结果回写 JSON 并用 fmt 打印
    json result;
    result["x"] = {x(0), x(1)};
    result["residual"] = (A * x - b).norm();
    fmt::print("结果: {}\n", result.dump());
    return 0;
}
