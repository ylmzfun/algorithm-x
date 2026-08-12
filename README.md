# Algorithm X — 算法学习大纲（C/C++）

> 基于 **C/C++** 的算法学习仓库，系统覆盖数据结构、经典算法、AI 核心算法及进阶专题。
> 每个模块包含原理说明 + 可运行的 C/C++ 实现。

---

## 开发环境

| 项目     | 说明                 |
| -------- | -------------------- |
| 语言标准 | C17 / C++20          |
| 编译器   | GCC 12+ / Clang 16+  |
| 构建工具 | CMake 3.20+          |
| 测试框架 | Google Test（gtest） |
| 包管理   | vcpkg / Conan        |

### 快速开始

```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
ctest --output-on-failure
```

---

## 代码风格

本项目遵循统一的 C++ 编码规范：

| 规则       | 说明                                                                         |
| ---------- | ---------------------------------------------------------------------------- |
| 头文件防护 | `#pragma once`                                                               |
| 缩进       | 4 空格                                                                       |
| 大括号     | K&R 风格（左括号同行）                                                       |
| 命名       | 类型 `PascalCase`，函数 `snake_case`，模板参数 `T`/`It`/`Cmp`                |
| 注释       | 仅使用 `//`，不使用 `/* */`                                                  |
| 分区标记   | `// ---- Section Name ----`                                                  |
| 命名空间   | `algorithm_x::{module}`。测试文件用 `using namespace algorithm_x::{module};` |
| 递归       | 禁止使用 `std::function` 做递归；使用 Y-combinator 或 `auto` 自引用模式      |
| 返回空     | 统一使用 `return {};`                                                        |
| 头文件包含 | 先标准库（按字母序），空行分隔，再本仓库头文件                               |

---

## 目录

1. [数据结构](#1-数据结构)
2. [基础算法](#2-基础算法)
3. [算法设计范式](#3-算法设计范式)
4. [图论算法](#4-图论算法)
5. [字符串算法](#5-字符串算法)
6. [数学与数论](#6-数学与数论)
7. [计算几何](#7-计算几何)
8. [动态规划专题](#8-动态规划专题)
9. [AI / ML 核心算法](#9-ai--ml-核心算法)
10. [并发与多线程](#10-并发与多线程)
11. [分布式算法](#11-分布式算法)
12. [进阶专题](#12-进阶专题)
13. [C/C++ 工程与性能](#13-cc-工程与性能)

---

## 1. 数据结构

### 线性结构
- [x] 数组与动态数组（ArrayList / Vector）
- [x] 链表：单向、双向链表
- [x] 循环链表
- [x] 栈与单调栈
- [x] 队列、双端队列、单调队列、优先队列（堆）

### 树形结构
- [x] 二叉树、二叉搜索树（BST）
- [x] 平衡二叉树：AVL 树
- [x] 红黑树
- [x] 堆：二叉堆
- [x] 堆：斐波那契堆、配对堆
- [x] B 树 / B+ 树（数据库索引）
- [x] 线段树（区间查询与更新）
- [x] 树状数组（Fenwick Tree）
- [x] 字典树（Trie）
- [x] 并查集（Union-Find / DSU）
- [x] 跳表（Skip List）
- [x] 哈夫曼树

### 哈希与集合
- [x] 哈希表（开放寻址 / 拉链法）
- [x] 布隆过滤器
- [x] LRU 缓存
- [x] LFU 缓存
- [x] 一致性哈希

### 图存储
- [x] 邻接矩阵
- [x] 邻接表
- [x] 链式前向星

---

## 2. 基础算法

### 排序
- [x] O(n²)：冒泡、选择、插入
- [x] O(n log n)：归并、快速、堆排序
- [x] 非比较排序：计数、基数、桶排序
- [x] 外部排序、TimSort

### 查找
- [x] 线性查找
- [x] 二分查找及其变体（lower_bound / upper_bound）
- [x] 三分查找
- [x] 插值查找、指数查找

### 双指针与滑动窗口
- [x] 快慢指针、对撞指针
- [x] 定长 / 变长滑动窗口

### 前缀和与差分
- [x] 一维 / 二维前缀和
- [x] 差分数组

### 位运算
- [x] 常见位操作技巧
- [x] 状态压缩
- [x] 布赖恩·克尼根算法（Brian Kernighan）

---

## 3. 算法设计范式

- [x] 分治法（Divide and Conquer）
- [x] 贪心算法（Greedy）
- [x] 回溯法（Backtracking）
- [x] 分支限界（Branch and Bound）
- [x] 减治法（Decrease and Conquer）
- [x] 随机化算法（Randomized Algorithms）
- [x] 近似算法

---

## 4. 图论算法

### 图遍历
- [x] DFS（深度优先搜索）
- [x] BFS（广度优先搜索）
- [x] 拓扑排序（Kahn / DFS 实现）

### 最短路径
- [x] Dijkstra
- [x] Bellman-Ford
- [x] SPFA
- [x] Floyd-Warshall
- [x] A* 搜索
- [x] Johnson 全源最短路径

### 最小生成树
- [x] Prim
- [x] Kruskal

### 连通性
- [x] 强连通分量（Tarjan / Kosaraju）
- [x] 割点与桥
- [x] 双连通分量
- [x] 2-SAT 问题

### 网络流
- [x] 最大流：Ford-Fulkerson、Edmonds-Karp、Dinic
- [x] 最小割
- [x] 费用流（最小费用最大流）
- [x] 二分图最大匹配（匈牙利算法 / 最大流）
- [x] KM 算法（带权二分图最优匹配）

### 其他
- [x] 欧拉路径 / 回路
- [x] 哈密顿路径（NP 完全）

---

## 5. 字符串算法

- [x] 字符串哈希（Rabin-Karp）
- [x] KMP（Knuth-Morris-Pratt）
- [x] Boyer-Moore
- [x] Z 算法
- [x] Manacher（最长回文子串）
- [x] AC 自动机（Aho-Corasick）
- [x] 后缀数组（Suffix Array）
- [x] 后缀自动机（SAM）
- [x] 最小表示法
- [x] 编辑距离（Levenshtein Distance）

---

## 6. 数学与数论

### 基础数论
- [x] 素数判定（试除法 / Miller-Rabin）
- [x] 筛法（埃氏筛 / 线性筛）
- [x] 质因数分解（Pollard-Rho）
- [x] 最大公约数（欧几里得 / 扩展欧几里得）
- [x] 乘法逆元
- [x] 中国剩余定理（CRT）
- [x] 欧拉函数

### 组合数学
- [x] 排列组合
- [x] 容斥原理
- [x] 鸽巢原理
- [x] 卡特兰数（Catalan Number）
- [x] 斯特林数、贝尔数

### 线性代数
- [x] 矩阵乘法
- [x] 矩阵快速幂
- [x] 高斯消元
- [x] 行列式

### 其他数学
- [x] 快速幂 / 龟速乘
- [x] 博弈论（SG 函数、Nim 游戏）
- [x] 概率与期望
- [x] 快速傅里叶变换（FFT / NTT）
- [x] 母函数（生成函数）

---

## 7. 计算几何

- [x] 点、向量基本运算（叉积、点积）
- [x] 线段相交判定
- [x] 多边形面积
- [x] 凸包（Graham Scan / Andrew）
- [x] 旋转卡壳
- [x] 最近点对
- [x] 扫描线算法
- [x] 半平面交

---

## 8. 动态规划专题

### 经典 DP 模型
- [x] 背包问题（0-1 / 完全 / 多重 / 分组）
- [x] 最长公共子序列（LCS）
- [x] 最长递增子序列（LIS）O(n log n)
- [x] 区间 DP
- [x] 树形 DP
- [x] 数位 DP
- [x] 状态压缩 DP
- [x] 概率 DP
- [x] 插头 DP（轮廓线 DP）

### DP 优化
- [x] 单调队列优化
- [x] 斜率优化
- [x] 四边形不等式优化
- [x] 矩阵快速幂优化（倍增 DP）
- [x] 数据结构优化（线段树 / 树状数组上 DP）

---

## 9. AI 核心算法（C/C++ 实现）

> 本章聚焦可直接用 C/C++ 从零实现的 AI 算法，不依赖 Python 生态。

### 搜索算法
- [x] 无信息搜索：BFS、DFS、迭代加深（IDDFS）
- [x] 启发式搜索：A*、IDA*、双向 BFS
- [x] 局部搜索：爬山法、模拟退火、禁忌搜索
- [x] 博弈搜索：Minimax、Alpha-Beta 剪枝、蒙特卡洛树搜索（MCTS）

### 约束满足问题（CSP）
- [x] 回溯搜索 + 约束传播
- [x] AC-3 算法
- [x] 最小冲突启发式

### 进化与元启发式算法
- [x] 遗传算法（GA）
- [x] 粒子群优化（PSO）
- [x] 蚁群算法（ACO）
- [x] 差分进化（DE）
- [x] 模拟退火（SA）

### 经典 ML 算法（从零实现）
- [x] K 近邻（KNN）
- [x] 线性回归（正规方程 / 梯度下降）
- [x] 逻辑回归 + 交叉熵损失
- [x] 朴素贝叶斯分类器
- [x] 决策树（ID3 / CART）
- [x] K-Means 聚类
- [x] PCA（特征值分解）
- [x] 感知机 → 多层感知机（MLP）+ 反向传播

### 强化学习
- [x] 马尔可夫决策过程（MDP）
- [x] 价值迭代 / 策略迭代
- [x] Q-Learning（表格法）
- [x] SARSA

### C++ ML 库（进阶，可选依赖）
| 库                                      | 用途                              |
| --------------------------------------- | --------------------------------- |
| [mlpack](https://www.mlpack.org)        | 通用机器学习（SVM、随机森林、NN） |
| [libtorch](https://pytorch.org/cppdocs) | PyTorch C++ 前端                  |
| [ONNX Runtime](https://onnxruntime.ai)  | 模型推理                          |
| [dlib](http://dlib.net)                 | ML 算法 + 计算机视觉              |
| [Eigen](https://eigen.tuxfamily.org)    | 线性代数（矩阵运算基础库）        |

---

## 10. 并发与多线程

> C/C++ 的强项领域，覆盖从原子操作到并发模式。

### 基础原语
- [x] `std::thread` / `pthread` 线程管理
- [x] `std::mutex` / `std::shared_mutex` 互斥锁
- [x] `std::condition_variable` 条件变量
- [x] `std::atomic` 原子操作与内存序（memory order）
- [x] `std::future` / `std::promise` / `std::async`

### 并发数据结构
- [x] 无锁队列（Lock-Free Queue）
- [x] 无锁栈（Lock-Free Stack）
- [x] 读写锁（Read-Write Lock）
- [x] 并发哈希表
- [x] 线程安全单例（Double-Checked Locking）

### 经典并发问题
- [x] 生产者-消费者模型
- [x] 读者-写者问题
- [x] 哲学家就餐问题
- [x] 线程池（Thread Pool）实现

### 同步模式
- [x] 信号量（Semaphore）
- [x] 屏障（Barrier / Latch）
- [x] Read-Copy-Update（RCU）
- [x] CAS（Compare-And-Swap）编程

---

## 11. 分布式算法

- [x] 共识算法：Paxos / Raft
- [x] 分布式一致性：两阶段提交（2PC）
- [x] 一致性哈希
- [x] Gossip 协议
- [x] MapReduce 模型
- [x] 分布式锁
- [x] 向量时钟（Vector Clock）
- [x] CRDT（无冲突复制数据类型）

---

## 12. 进阶专题

- [x] 计算理论：P / NP / NP 完全 / NP 困难
- [x] 在线算法与竞争分析
- [x] 摊还分析
- [x] 莫队算法（Mo's Algorithm）
- [x] CDQ 分治
- [x] LCT（Link-Cut Tree）
- [x] 主席树（可持久化线段树）
- [x] 树套树与分块
- [x] 稀疏表（Sparse Table / RMQ）
- [x] LCA（最近公共祖先）—— 倍增 / Tarjan / 欧拉序 + ST 表
- [x] 逆序对、偏序问题

---

## 13. C/C++ 工程与性能

> 编译选项、CMake 多目标、PCH/Unity Build、内存检测、性能分析的完整命令与
> 配置示例见 [docs/compile-and-perf.md](docs/compile-and-perf.md)。

### 编译与构建
- [x] GCC / Clang 编译选项与优化级别（-O2 / -O3 / -march=native）
- [x] CMake 多目标构建、静态/动态库管理
- [x] 预编译头（PCH）与 Unity Build
- [x] Address / Undefined / Thread Sanitizer

### 内存管理
- [x] RAII 与智能指针（`unique_ptr` / `shared_ptr`）
- [x] 自定义 Allocator（内存池 / 对象池 / slab）
- [x] 内存对齐与缓存行（cache line）优化
- [x] Valgrind / AddressSanitizer 内存检测

### 性能优化
- [x] 性能分析：perf / gprof /火焰图
- [x] SIMD 向量化（SSE / AVX 内联汇编 + intrinsics）
- [x] 缓存友好数据结构（AoS vs SoA）
- [x] 分支预测优化（`likely` / `unlikely`）
- [x] 编译器优化技巧（内联、循环展开、常量折叠）

### 模板与泛型
- [x] 模板元编程（TMP）基础
- [x] SFINAE 与 `concepts`（C++20）
- [x] `constexpr` 编译期计算
- [x] 类型萃取（type traits）

---

## 参考资源

### 书籍
- 《算法导论》（CLRS）—— 算法圣经
- 《算法》（Sedgewick）—— C 语言实现
- 《算法竞赛入门经典》（刘汝佳）—— C++ 竞赛实战
- 《C++ Concurrency in Action》（Anthony Williams）
- 《Effective Modern C++》（Scott Meyers）
- 《Computer Systems: A Programmer's Perspective》（CS:APP）

### 在线平台
- [LeetCode](https://leetcode.cn)
- [Luogu](https://www.luogu.com.cn)
- [Codeforces](https://codeforces.com)
- [AtCoder](https://atcoder.jp)

---

## 实现进度

| #        | 模块                | 目录           | 头文件         | 测试          | 状态 |
| -------- | ------------------- | -------------- | -------------- | ------------- | ---- |
| 1        | 数据结构            | `ds/`          | 24             | 206           | ✅    |
| 2-3      | 基础算法 + 设计范式 | `algo/`        | 14             | 205           | ✅    |
| 4        | 图论                | `graph/`       | 14             | 60            | ✅    |
| 5        | 字符串              | `string/`      | 8              | 61            | ✅    |
| 6        | 数学数论            | `math/`        | 11             | 62            | ✅    |
| 7        | 计算几何            | `geom/`        | 5              | 43            | ✅    |
| 8        | 动态规划            | `dp/`          | 10             | 55            | ✅    |
| 9        | AI / ML             | `ai/`          | 12             | 37            | ✅    |
| 10       | 并发                | `concurrent/`  | 7              | 23            | ✅    |
| 11       | 分布式              | `distributed/` | 8              | 26            | ✅    |
| 12       | 进阶专题            | `advanced/`    | 10             | 29            | ✅    |
| 13       | C++ 工程            | `perf/`        | 3              | 16            | ✅    |
| **合计** |                     | **12 模块**    | **126 头文件** | **823 tests** |      |

```
include/algorithm_x/
├── ds/          (24) 数据结构
├── algo/        (14) 基础算法
├── graph/       (14) 图论
├── string/      (8)  字符串
├── math/        (11) 数学
├── geom/        (5)  计算几何
├── dp/          (10) 动态规划
├── ai/          (12) AI/ML
├── concurrent/  (7)  并发
├── distributed/ (8)  分布式
├── advanced/    (10) 进阶
└── perf/        (3)  C++ 工程
```

> 持续更新中。每个章节的详细笔记和 C/C++ 代码实现位于对应子目录。
