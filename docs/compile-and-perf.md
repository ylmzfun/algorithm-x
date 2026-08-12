# C/C++ 工程与性能笔记

> 对应 README 第 13 章「C/C++ 工程与性能」中标记为未完成/需要文档的条目。
> 本仓库的构建配置见根目录 `CMakeLists.txt` 与 `tests/CMakeLists.txt`。

---

## 1. GCC / Clang 编译选项与优化级别

### 常用优化级别

| 级别 | 含义 | 适用场景 |
| --- | --- | --- |
| `-O0` | 不优化，编译最快，调试信息最准 | Debug |
| `-O1` | 基本优化，编译时间与体积平衡 | 常规构建 |
| `-O2` | 推荐的发布级别：多数局部优化 + 向量化基础 | Release 默认 |
| `-O3` | 更激进：函数内联更多、循环优化更强 | 计算密集（算法/数值） |
| `-Os` | 以体积优先的优化 | 嵌入式 / 体积敏感 |
| `-march=native` | 使用本机 CPU 指令集（AVX2 等） | 只在本机运行的性能测试 |

### 与本仓库搭配的编译命令

```bash
# Debug（本仓库 CMake 已自动开启 -fsanitize=address,undefined）
cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build-debug -j

# Release + 本机指令集
cmake -B build-release -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_CXX_FLAGS="-O3 -march=native"
cmake --build build-release -j
```

### 常用警告与诊断

```bash
-Wall -Wextra -Wpedantic        # 本项目默认开启
-Wshadow                         # 变量遮蔽（本项目曾因此类 bug 踩坑）
-Wconversion -Wsign-conversion   # 隐式类型转换
-Werror                          # 警告即错误（CI 常用）
```

---

## 2. CMake 多目标构建、静态/动态库管理

### 多目标

本仓库的 `tests/CMakeLists.txt` 即为多目标示例：每个模块一个可执行目标
（`test_ds`、`test_algo`、…），各自 `add_test` 注册到 CTest。

```bash
cmake --build build -j                  # 构建全部目标
cmake --build build --target test_dp    # 只构建单个目标
ctest --test-dir build -R dp            # 只运行 dp 套件
```

### 接口库 → 静态库 / 动态库

当前 `algorithm_x` 是 INTERFACE 库（纯头文件，`-fPIC` 无关）。若需打包成库：

```cmake
# 静态库
add_library(algorithm_x STATIC src/algorithm_x.cpp)
target_include_directories(algorithm_x PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

# 动态库（加 -fPIC；Windows 需 __declspec(dllexport)）
add_library(algorithm_x SHARED src/algorithm_x.cpp)
```

要点：

- 头文件-only 库用 `INTERFACE`（零编译成本，依赖方各自实例化模板）；
- 模板多、实例化少 → 静态库；ABI 需要稳定、多进程共享 → 动态库；
- `CMAKE_POSITION_INDEPENDENT_CODE=ON` 可让静态库也能链进动态库。

---

## 3. 预编译头（PCH）与 Unity Build

### PCH（Precompiled Header）

把不变的头（标准库、gtest）预编译，显著减少重复解析时间。

```cmake
target_precompile_headers(test_ds PRIVATE
    <gtest/gtest.h>
    <algorithm>
    <vector>
)
```

注意：

- 每个编译单元用到的 PCH 内容不同时收益打折；大项目常按模块分组；
- 修改 PCH 中任一头文件会导致整组重编译；
- MSVC 与 Clang 支持好；GCC 对 `-include` 相对敏感。

### Unity Build（统一构建 / 分块合并）

把多个 `.cpp` 合并成一个大翻译单元编译，减少头文件重复解析与链接开销
（代价：编译缓存粒度变大、符号冲突面变大）。

CMake 原生支持：

```bash
cmake -B build-unity -DCMAKE_UNITY_BUILD=ON
```

手动分块示例：`unity_1.cpp` 中 `#include "a.cpp" #include "b.cpp"`。

---

## 4. Valgrind / AddressSanitizer 内存检测

### AddressSanitizer（ASan，推荐首选）

本仓库 Debug 构建已默认开启 `-fsanitize=address,undefined`：

```bash
cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug
ctest --test-dir build-debug --output-on-failure   # 任何越界/泄漏会直接报错退出
```

ASan 能捕获：堆越界、栈越界、use-after-free、double free、内存泄漏（LSan）。
比 Valgrind 快 2–20 倍，是 CI 的首选。

### Valgrind（Linux；macOS 需特殊处理）

```bash
valgrind --leak-check=full --error-exitcode=1 ./tests/test_ds
valgrind --tool=helgrind ./tests/test_concurrent   # 竞态检测
```

macOS 上 Valgrind 支持不完整（Xcode/新系统上易失效），可改用：
`-fsanitize=thread`（TSan）检测数据竞争。

---

## 5. 性能分析：perf / gprof / 火焰图

### gprof（编译期插桩，最简单）

```bash
g++ -pg -O2 -o app main.cpp && ./app && gprof ./app gmon.out
```

缺点：插桩影响结果、只统计函数粒度。适合快速定位热点函数。

### perf（Linux，采样式，低开销）

```bash
perf stat ./app                 # 概要：IPC、cache miss、分支预测
perf record -g ./app            # 采集调用栈
perf report                     # 交互式热点
```

生成火焰图（Brendan Gregg 工具集）：

```bash
perf record -g ./app
perf script > out.perf
# https://github.com/brendangregg/FlameGraph
./stackcollapse-perf.pl out.perf > out.folded
./flamegraph.pl out.folded > flame.svg
```

### macOS 替代

macOS 无 `perf`，可用：

```bash
# 采样（10 秒）
sample ./tests/test_dp 10 -file profile.txt
# Instruments 的 Time Profiler（GUI）
```

### 内存/分配分析

```bash
# macOS
leaks ./tests/test_ds
# Linux
valgrind --tool=massif ./app     # 堆内存随时间曲线
```

---

## 6. 编译器优化技巧（内联、循环展开、常量折叠）

### 内联（Inlining）

```cpp
// 显式建议（编译器可忽略）
inline int f(int x) { return x * 2; }

// 强制内联（谨慎，可能导致代码膨胀）
__attribute__((always_inline)) inline int g(int x) { return x * 2; }

// 禁止内联（便于调试 / 减少 I-cache 压力）
__attribute__((noinline)) int h(int x);
```

要点：内联省去调用开销、开启跨语句优化；但过度内联增大代码体积、
损害指令缓存。热点小函数内联收益最大。

### 循环展开（Loop Unrolling）

```cpp
// 编译器通常自动展开小常数循环；#pragma 可提示
#pragma clang loop unroll(4)
for (int i = 0; i < n; ++i) { acc += a[i]; }

// 手写展开 4 路（减少分支与依赖链）
for (int i = 0; i + 3 < n; i += 4) {
    s0 += a[i]; s1 += a[i + 1]; s2 += a[i + 2]; s3 += a[i + 3];
}
```

注意：展开增加寄存器压力；现代编译器在 `-O2`/`-O3` 下大多能自行判断，
手写展开通常只对极内层循环有意义。

### 常量折叠 / 常量传播

```cpp
constexpr double PI = 3.14159265358979;   // 编译期常量
constexpr int factorial(int n) {          // constexpr 函数在编译期求值
    return n <= 1 ? 1 : n * factorial(n - 1);
}
static_assert(factorial(5) == 120);
```

`-O2` 以上编译器会做常量传播（如 `x = 2 * 3` 直接折叠为 6）、
死代码消除、分支预测（见 `perf/cache.h` 的 `LIKELY/UNLIKELY`）。

### 分支预测

```cpp
#include "algorithm_x/perf/cache.h"
if (UNLIKELY(err != 0)) { handle_error(); }   // 冷路径标记
```

### 实践建议

1. 先 `-O2` 编译并分析（gprof / perf / sample）再动手优化；
2. 优化前用 `-O0` 保留可读性，优化只针对热点（80/20 法则）；
3. 每步优化后用测试 + benchmark 验证，避免"负优化"；
4. 优先选择算法/数据结构层面的改进，编译器技巧是最后手段。

---

## 快速参考命令表

| 目的 | 命令 |
| --- | --- |
| Debug + 全部 sanitizer | `cmake -B build-debug -DCMAKE_BUILD_TYPE=Debug && ctest --test-dir build-debug` |
| Release 构建 | `cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j` |
| Unity Build | `cmake -B build-unity -DCMAKE_UNITY_BUILD=ON` |
| 单模块测试 | `ctest --test-dir build -R 'dp\|math'` |
| 泄漏检查（Linux） | `valgrind --leak-check=full ./tests/test_ds` |
| 热点分析（Linux） | `perf record -g ./tests/test_graph && perf report` |
| 热点分析（macOS） | `sample ./tests/test_graph 10` |
