# 更新日志

本项目的版本与 git tag 一一对应。

## [1.3.0] - 2026-08-12

### 新增
- `docs/algorithms/`：全量中文算法参考手册，覆盖全部 126 个头文件
  （用途 / 原理 / 真实 API 签名 / 复杂度 / 使用场景 / 使用示例）
- 构建现代化：
  - `CMakePresets.json`：debug / release 预设（vcpkg toolchain，`build/<preset>/` 输出）
  - `cmake/AlgorithmX.cmake`：统一的警告与 gtest 套件注册助手
  - 安装 / 导出规则：支持 `find_package(algorithm_x)`（`cmake --install`）
  - 构建选项：`BUILD_TESTS` / `BUILD_EXAMPLES` / `ALGORITHM_X_ENABLE_SANITIZERS`
  - 测试注册升级为 `gtest_discover_tests`（CTest 粒度到单个用例）
- 工程规范文件：`.clang-format` / `.clang-tidy` / `.editorconfig`
- CI：`.github/workflows/ci.yml`（Ubuntu / macOS × 构建 / 测试 / 安装冒烟）

### 变更
- 依赖统一由 vcpkg 管理：fmt / spdlog / nlohmann-json / eigen3 / gtest
- `project()` 版本号同步为 1.3.0

## [1.2.0] - 2026-08-12

### 新增
- `examples/`：13 个可运行示例（关键知识 / 标准库 / 第三方库 / 综合案例）
- `docs/compile-and-perf.md`：工程与性能笔记

### 变更
- 依赖管理切换为 vcpkg（`CMAKE_TOOLCHAIN_FILE`）

## [1.1.0] - 2026-08-12

### 新增
- 补齐学习大纲全部 27 个未实现专题：邻接矩阵、链式前向星、分支限界、减治法、
  近似算法、母函数、插头 DP、数据结构优化 DP、CSP（回溯 / AC-3 / 最小冲突）、
  RCU、Paxos、2PC、MapReduce、CRDT、LCT、树套树与分块、计算理论、在线算法、
  SFINAE 与 concepts 等
- 126 个头文件 / 823 个测试全部通过（Release 与 ASan/UBSan）

### 修复
- 差分进化 RNG 变量遮蔽、SARSA 缺头文件与 `step()` 遮蔽、
  `vector<atomic<bool>>` 不可拷贝、CHT 文档契约、MDP API 不符等潜伏 bug

## [1.0.1] - 2026-08-12

### 修复
- 接入 6 个从未编译的测试文件；补齐 5 个缺测头文件的测试
- 修正 README 勾选状态与统计数字

## [1.0.0] - 2026-08-12

### 新增
- 首个完整版本：12 个模块、47 个头文件、601 个测试
