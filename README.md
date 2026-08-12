# algorithm-rust

> 用 Rust 语言体系系统学习数据结构与算法

## 项目目标

- 掌握 Rust 所有权、借用、生命周期等核心概念在数据结构实现中的应用
- 理解常见数据结构的内部原理并通过 Rust 代码实现
- 掌握经典算法设计思想，能够分析时间/空间复杂度
- 掌握 Rust 工程化实战：std 标准库核心算法、常用第三方库与异步生态的使用
- 为 LeetCode 刷题和系统设计面试打下坚实基础

## 项目结构

```
src/
├── lib.rs                     # 模块入口
├── data_structures/
│   ├── mod.rs
│   ├── array.rs               # 动态数组 / Vector 深入
│   ├── linked_list.rs         # 单链表 / 双链表
│   ├── stack.rs               # 栈
│   ├── queue.rs               # 队列 / 双端队列 / 循环队列
│   ├── hashmap.rs             # 哈希表原理与实现
│   └── heap.rs                # 二叉堆 / 优先队列
├── tree/
│   ├── mod.rs
│   ├── binary_tree.rs         # 二叉树基础与遍历
│   ├── binary_search_tree.rs  # 二叉搜索树
│   ├── avl_tree.rs            # AVL 平衡树
│   └── trie.rs                # 前缀树
├── graph/
│   ├── mod.rs
│   ├── graph.rs               # 图的表示（邻接矩阵 / 邻接表）
│   ├── traversal.rs           # BFS / DFS
│   ├── shortest_path.rs       # Dijkstra / Bellman-Ford / Floyd-Warshall
│   ├── mst.rs                 # 最小生成树 (Prim / Kruskal)
│   └── union_find.rs          # 并查集
├── sort/
│   ├── mod.rs
│   ├── basic.rs               # 冒泡、选择、插入排序
│   ├── advanced.rs            # 归并、快速、堆排序
│   └── linear.rs              # 计数、桶、基数排序
├── search/
│   ├── mod.rs
│   └── binary_search.rs       # 二分搜索及其变体
├── algorithm/
│   ├── mod.rs
│   ├── recursion.rs           # 递归与分治
│   ├── backtracking.rs        # 回溯算法
│   ├── dynamic_programming.rs # 动态规划
│   ├── greedy.rs              # 贪心算法
│   ├── sliding_window.rs      # 滑动窗口 / 双指针
│   └── bit.rs                 # 位运算技巧
├── string/
│   ├── mod.rs
│   └── string_match.rs        # KMP / Rabin-Karp / Boyer-Moore
├── math/
│   ├── mod.rs
│   └── math.rs                # 素数筛、最大公约数、快速幂等
└── rust_engineering/
    ├── mod.rs                # Rust 工程专题
    ├── native/               # Rust 原生：std 核心算法与用法
    │   ├── slice.rs          # 切片 / Vec 核心算法（二分、分区、旋转、窗口）
    │   ├── iterator.rs       # 迭代器核心算法（fold / scan / zip / 自定义迭代器）
    │   ├── collections.rs    # 集合与优先队列（HashMap / BTreeMap / BinaryHeap）
    │   ├── string.rs         # 字符串处理（分割、反转、字符边界安全）
    │   ├── error.rs          # 错误处理模式（Result / ? / 自定义错误）
    │   └── concurrency.rs    # 并发与同步（线程、通道、原子、LazyLock）
    ├── third_party/          # 第三方库核心算法
    │   ├── rayon.rs          # 并行迭代（par_iter / 并行排序 / map-reduce）
    │   ├── itertools.rs      # 迭代器增强（unique / 组合 / group_map / zip_longest）
    │   ├── rand.rs           # 随机数（抽样 / 洗牌 / 随机密码 / 可复现种子）
    │   ├── petgraph.rs       # 图算法（Dijkstra / BFS / MST / 拓扑排序）
    │   ├── num_bigint.rs     # 大整数（阶乘 / 斐波那契 / 模幂）
    │   ├── collections.rs    # indexmap 保序表 / smallvec 栈上小向量
    │   ├── serde.rs          # 序列化（JSON 编解码 / 字段定制）
    │   ├── errors.rs         # anyhow / thiserror 错误处理
    │   ├── regex.rs          # 正则表达式（提取 / 替换 / 捕获）
    │   ├── chrono.rs         # 日期时间（解析 / 格式化 / 日期运算）
    │   └── async_runtime.rs  # tokio / futures 异步（任务 / 通道 / 超时）
    └── tips.rs               # 应用场景与使用技巧（选型速查 / 性能 / 陷阱）
```

## 学习路线

> ✅ 全部 9 个阶段、36 个知识点均已在 `src/` 中实现并附单元测试，可直接跳转到对应源码。
> 运行 `cargo test` 即可验证全部实现。

### 第一阶段：线性数据结构

- [x] **数组与向量** — `Vec` 内部原理、扩容策略、常见遍历模式（`src/data_structures/array.rs`）
- [x] **链表** — `Box` / `Rc<RefCell>` 实现单双向链表，熟悉 Rust 指针抽象（`src/data_structures/linked_list.rs`）
- [x] **栈** — LIFO 结构，括号匹配、后缀表达式求值（`src/data_structures/stack.rs`）
- [x] **队列** — FIFO / 双端队列 / 循环队列（`src/data_structures/queue.rs`）

### 第二阶段：树形结构

- [x] **二叉树** — 前序/中序/后序/层序遍历，递归与迭代实现（`src/tree/binary_tree.rs`）
- [x] **二叉搜索树** — 插入、删除、查找，BST 性质验证（`src/tree/binary_search_tree.rs`）
- [x] **AVL 树** — 四种旋转操作，平衡因子维护（`src/tree/avl_tree.rs`）
- [x] **前缀树 (Trie)** — 字符串前缀匹配、自动补全（`src/tree/trie.rs`）

### 第三阶段：堆与哈希表

- [x] **二叉堆** — 上浮/下沉操作，用 `Vec` 实现最小堆/最大堆（`src/data_structures/heap.rs`）
- [x] **优先队列** — `BinaryHeap` 自定义比较器与 Top-K 工程用法（`src/data_structures/heap.rs`、`src/rust_engineering/native/collections.rs`）；源码阅读见 [BinaryHeap 文档](https://doc.rust-lang.org/std/collections/struct.BinaryHeap.html)
- [x] **哈希表** — 拉链法与开放寻址法两种实现，哈希函数设计（`src/data_structures/hashmap.rs`）

### 第四阶段：排序与搜索

- [x] **基础排序** — 冒泡、选择、插入排序（`src/sort/basic.rs`）
- [x] **高级排序** — 归并排序、快速排序、堆排序（`src/sort/advanced.rs`）
- [x] **线性排序** — 计数排序、桶排序、基数排序（`src/sort/linear.rs`）
- [x] **二分搜索** — 标准二分、查找边界、旋转数组搜索（`src/search/binary_search.rs`）

### 第五阶段：图论

- [x] **图的表示** — 邻接矩阵 vs 邻接表，有向/无向/加权图（`src/graph/graph.rs`）
- [x] **图的遍历** — BFS（最短路径）、DFS（连通分量、环检测）（`src/graph/traversal.rs`）
- [x] **最短路径** — Dijkstra、Bellman-Ford、Floyd-Warshall（`src/graph/shortest_path.rs`）
- [x] **最小生成树** — Prim 算法、Kruskal 算法（配合并查集）（`src/graph/mst.rs`）
- [x] **拓扑排序** — Kahn 算法（BFS），返回 None 表示有环（`src/graph/traversal.rs`）
- [x] **并查集** — 路径压缩 + 按秩合并（`src/graph/union_find.rs`）

### 第六阶段：核心算法思想

- [x] **递归与分治** — 汉诺塔、快速幂、归并排序思想（`src/algorithm/recursion.rs`）
- [x] **回溯算法** — 全排列、N 皇后、子集、组合总和（`src/algorithm/backtracking.rs`）
- [x] **贪心算法** — 区间调度、哈夫曼编码、跳跃游戏（`src/algorithm/greedy.rs`）
- [x] **动态规划** — 背包系列、最长子序列、打家劫舍、编辑距离（`src/algorithm/dynamic_programming.rs`）
- [x] **滑动窗口 / 双指针** — 无重复字符子串、接雨水、链表快慢指针（`src/algorithm/sliding_window.rs`）

### 第七阶段：字符串与数学

- [x] **字符串匹配** — KMP、Rabin-Karp、Boyer-Moore（`src/string/string_match.rs`）
- [x] **数学基础** — 埃拉托色尼筛、快速幂、欧几里得算法（`src/math/math.rs`）

### 第八阶段：位运算与技巧

- [x] **位运算** — 与/或/异或操作、汉明重量、2 的幂、位运算加法（`src/algorithm/bit.rs`）
- [ ] **拓展：状态压缩与布隆过滤器** — 依赖位运算技巧，后续补充

### 第九阶段：Rust 工程专题（持续学习）

- [x] **std 核心算法** — 切片二分/分区/旋转、迭代器组合、集合与堆的工程用法（`src/rust_engineering/native/slice.rs`、`iterator.rs`、`collections.rs`）
- [x] **字符串与错误处理** — 字符边界安全、Result 组合子、自定义错误类型（`src/rust_engineering/native/string.rs`、`error.rs`）
- [x] **并发与同步** — 线程/通道/原子操作/LazyLock（`src/rust_engineering/native/concurrency.rs`）
- [x] **第三方算法库** — rayon 并行、itertools 迭代器增强、petgraph 图算法、num-bigint 大整数（`src/rust_engineering/third_party/`）
- [x] **工程常用库** — serde 序列化、anyhow/thiserror 错误处理、regex、chrono（`src/rust_engineering/third_party/`）
- [x] **异步生态** — tokio 任务与通道、futures 组合子（`src/rust_engineering/third_party/async_runtime.rs`）
- [x] **实战技巧** — 场景选型、性能优化、内存与所有权技巧、常见陷阱（`src/rust_engineering/tips.rs`）

## Rust 特色关注点

每个实现会重点标注以下 Rust 语言特性：

| 特性               | 应用场景                                 |
| ------------------ | ---------------------------------------- |
| `Box<T>`           | 链表节点、树节点的堆分配                 |
| `Rc<RefCell<T>>`   | 多重所有权的图节点                       |
| `Option<T>`        | 空指针安全的替代方案                     |
| 泛型 + Trait Bound | 通用数据结构的类型约束                   |
| 迭代器模式         | 自定义 `Iterator` 实现遍历               |
| `unsafe` 块        | 何时需要、何时避免                       |
| `derive` 宏        | `Debug` / `Clone` / `PartialEq` 自动实现 |

## 运行测试

```bash
cargo test                    # 运行所有测试
cargo test -- --nocapture     # 显示 print 输出
cargo test <test_name>        # 运行单个测试
cargo clippy                  # 代码风格检查
cargo fmt                     # 代码格式化
```

## 参考资源

- 《算法导论》(CLRS)
- 《算法 (第四版)》— Robert Sedgewick
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/) — 涵盖 unsafe Rust 和高级数据结构
- [LeetCode](https://leetcode.cn/) — 在线刷题平台
- [Learn Rust With Entirely Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/)
