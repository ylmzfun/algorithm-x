# Algorithm X — 多语言算法与数据结构合集

> 同一套算法与数据结构学习体系，用 **9 种语言**分别实现：原理说明 + 可运行代码 + 单元测试。
> 每个语言目录都是**独立可构建、可测试**的工程，根目录只负责索引与统一约定。

- **9** 个语言子项目
- **1100+** 个源码文件（Python 357 · C++ 139 · 头文件 126 · Go 87 · TS 86 · Java 74 · C# 61 · Rust 57 · PHP 55 · Ruby 23）
- 涵盖：基础/进阶数据结构、经典算法、图论、动态规划、数学基础、机器学习与深度学习、工程实践与并发

---

## 子项目总览

| 目录                                 | 语言 / 标准        | 重点内容                                                                | 构建与测试                     |
| ------------------------------------ | ------------------ | ----------------------------------------------------------------------- | ------------------------------ |
| [algorithm-cc](algorithm-cc/)         | C17 / C++20        | 数据结构、经典算法、AI 核心算法、并发、分布式、性能优化                 | CMake + vcpkg + GoogleTest     |
| [algorithm-python](algorithm-python/) | Python 3.9+        | 数据结构 → 算法 → 数学基础 → 机器学习 → 深度学习 → 专项进阶 + LeetCode  | 直接 `python3` 运行，无框架依赖 |
| [algorithm-go](algorithm-go/)         | Go 1.25            | 数据结构 + 标准库/第三方库实战（gin、zap、cobra、viper、gorm）+ 并发与泛型 | `go test ./...`              |
| [algorithm-ts](algorithm-ts/)         | TypeScript 5.7     | 数据结构、基础算法、图算法、动态规划、工程化实践                        | npm + Vitest                   |
| [algorithm-java](algorithm-java/)     | Java 17+           | 数据结构、排序/搜索、递归回溯、DP、图算法、字符串、数学                 | Maven + JUnit 5                |
| [algorithm-csharp](algorithm-csharp/) | C# / .NET 8+       | 6 个 Phase 的学习路线：基础 DS/Algo → 进阶 → 高级专题 → 综合实战        | `dotnet test`                  |
| [algorithm-rust](algorithm-rust/)     | Rust (edition 2024) | 用所有权/借用实现数据结构、图算法，以及 std 与异步工程生态              | Cargo                          |
| [algorithm-php](algorithm-php/)       | PHP 7.4+ / 8.0+    | 线性/树/图/哈希结构、排序搜索、图算法、字符串、DP、贪心、回溯、数学     | Composer + PHPUnit             |
| [algorithm-ruby](algorithm-ruby/)     | Ruby ≥ 2.7         | 11 种核心数据结构 + 6 大算法模块，含复杂度分析与业务场景示例            | minitest + RuboCop             |

---

## 目录结构

```
algorithm-x/
├── .gitignore              # 根级兜底忽略规则（各子目录另有自己的 .gitignore）
├── README.md               # 本文件：仓库总览与统一约定
├── algorithm-cc/           # C / C++
├── algorithm-csharp/       # C#
├── algorithm-go/           # Go
├── algorithm-java/         # Java
├── algorithm-php/          # PHP
├── algorithm-python/       # Python
├── algorithm-ruby/         # Ruby
├── algorithm-rust/         # Rust
└── algorithm-ts/           # TypeScript
```

> 每个子目录内都有独立且更详细的 `README.md`，包含学习路线、模块清单、复杂度分析与示例代码，**建议从对应语言的 README 入手**。

---

## 快速开始

各子项目互不依赖，按需进入对应目录即可。以下命令均在各自目录下执行。

### C / C++ — `algorithm-cc`

前置：GCC 12+ / Clang 16+、CMake 3.20+、vcpkg（fmt、spdlog、nlohmann-json、eigen3、gtest）。

```bash
cd algorithm-cc
cmake --preset release
cmake --build --preset release -j"$(sysctl -n hw.ncpu)"   # Linux 用 -j"$(nproc)"
ctest --preset release

# 一键 CI 流程（配置 → 构建 → 测试）
cmake --workflow --preset ci
```

产物位于 `build/<preset>/`；`debug` 预设启用了 ASan/UBSan。

### Python — `algorithm-python`

前置：Python 3.9+；数学/ML/DL 模块需 `numpy`，部分示例可选 `matplotlib`、`scipy`、`torch`。

```bash
cd algorithm-python
python3 01-data-structures/array/dynamic_array.py    # 运行单个模块

# 运行全部实现文件
find . -name "*.py" -not -name "__init__.py" -not -path "./leetcode/*" -exec python3 {} \;
```

### Go — `algorithm-go`

前置：Go 1.25。

```bash
cd algorithm-go
go test ./...            # 运行全部测试
go run main.go           # 运行入口示例
go vet ./...
```

### TypeScript — `algorithm-ts`

前置：Node.js 18+。

```bash
cd algorithm-ts
npm install
npm test                 # Vitest
npm run typecheck        # tsc --noEmit
```

### Java — `algorithm-java`

前置：JDK 17+、Maven。

```bash
cd algorithm-java
mvn test
```

### C# — `algorithm-csharp`

前置：.NET SDK 8+。

```bash
cd algorithm-csharp
dotnet restore
dotnet build
dotnet test
dotnet test --filter "Category=Sorting"     # 按类别运行
```

### Rust — `algorithm-rust`

前置：Rust 1.85+（edition 2024）。

```bash
cd algorithm-rust
cargo test
```

### PHP — `algorithm-php`

前置：PHP 7.4+（推荐 8.0+）、Composer。

```bash
cd algorithm-php
composer install
composer test            # 等价于 phpunit tests/
```

### Ruby — `algorithm-ruby`

前置：Ruby ≥ 2.7、Bundler。

```bash
cd algorithm-ruby
bundle install
ruby demo.rb                    # 演示脚本
ruby tests/test_runner.rb       # 数据结构测试
ruby tests/algorithms_test.rb   # 算法测试
bundle exec rubocop             # 代码规范检查
```

---

## 仓库约定

1. **子项目隔离**：每个语言目录自带构建配置、`.gitignore` 与文档，可单独克隆/构建/测试；根目录只做索引，不做跨语言统一构建。
2. **忽略规则分层**：各子目录的 `.gitignore` 负责本语言产物；根目录 `.gitignore` 作为跨语言兜底（构建产物、依赖目录、日志、IDE/系统文件、`.env`、`.qwen/`）。
3. **生成物不入库**：`build/`、`target/`、`dist/`、`node_modules/`、`vendor/`、`__pycache__/` 等一律不提交；锁文件（`go.sum`、`Cargo.lock`、`Gemfile.lock`、`package-lock.json`）入库以便复现，`algorithm-php` 按库项目约定忽略 `composer.lock`。
4. **测试先行**：新增实现请附带测试，并在提交前跑通对应语言的测试命令。
5. **提交信息**：遵循 `feat:` / `fix:` / `docs:` / `style:` / `refactor:` / `test:` / `chore:` 约定。
6. **无子模块**：`algorithm-*` 均为普通子目录（未使用 git submodule），克隆即可获得全部代码。

---

## 说明

- 各子项目的许可证与参考资料以其目录内的 `README.md` 为准（`algorithm-ruby` 采用 MIT 许可证）。
- 本仓库定位为**学习与刷题笔记**，实现优先保证可读性与原理清晰，未针对生产环境做极致优化，欢迎按需改造。
