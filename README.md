# algorithm-rust

> 用 Rust 语言体系系统学习数据结构与算法

## 项目目标

- 掌握 Rust 所有权、借用、生命周期等核心概念在数据结构实现中的应用
- 理解常见数据结构的内部原理并通过 Rust 代码实现
- 掌握经典算法设计思想，能够分析时间/空间复杂度
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
└── math/
    ├── mod.rs
    └── math.rs                # 素数筛、最大公约数、快速幂等
```

## 学习路线

### 第一阶段：线性数据结构（3-5 天）

- [ ] **数组与向量** — `Vec` 内部原理、扩容策略、常见遍历模式
- [ ] **链表** — `Box` / `Rc<RefCell>` 实现单双向链表，熟悉 Rust 指针抽象
- [ ] **栈** — LIFO 结构，表达式求值、括号匹配等经典应用
- [ ] **队列** — FIFO / 双端队列 / 循环队列

### 第二阶段：树形结构（4-6 天）

- [ ] **二叉树** — 前序/中序/后序/层序遍历，递归与迭代实现
- [ ] **二叉搜索树** — 插入、删除、查找，BST 性质验证
- [ ] **AVL 树** — 四种旋转操作，平衡因子维护
- [ ] **前缀树 (Trie)** — 字符串前缀匹配、自动补全

### 第三阶段：堆与哈希表（2-3 天）

- [ ] **二叉堆** — 上浮/下沉操作，用 `Vec` 实现最小堆/最大堆
- [ ] **优先队列** — `BinaryHeap` 源码阅读，自定义比较器
- [ ] **哈希表** — 开放寻址法 vs 拉链法，哈希函数设计

### 第四阶段：排序与搜索（3-4 天）

- [ ] **基础排序** — 冒泡、选择、插入排序
- [ ] **高级排序** — 归并排序、快速排序、堆排序
- [ ] **线性排序** — 计数排序、桶排序、基数排序
- [ ] **二分搜索** — 标准二分、查找边界、旋转数组搜索

### 第五阶段：图论（5-7 天）

- [ ] **图的表示** — 邻接矩阵 vs 邻接表，有向/无向/加权图
- [ ] **图的遍历** — BFS（最短路径）、DFS（连通分量、环检测）
- [ ] **最短路径** — Dijkstra、Bellman-Ford、Floyd-Warshall
- [ ] **最小生成树** — Prim 算法、Kruskal 算法（配合并查集）
- [ ] **拓扑排序** — Kahn 算法 / DFS 后序遍历
- [ ] **并查集** — 路径压缩 + 按秩合并

### 第六阶段：核心算法思想（7-10 天）

- [ ] **递归与分治** — 汉诺塔、快速幂、归并排序思想
- [ ] **回溯算法** — 全排列、N 皇后、子集、组合总和
- [ ] **贪心算法** — 区间调度、哈夫曼编码、跳跃游戏
- [ ] **动态规划** — 背包系列、最长子序列、打家劫舍、编辑距离
- [ ] **滑动窗口 / 双指针** — 无重复字符子串、接雨水、链表快慢指针

### 第七阶段：字符串与数学（3-4 天）

- [ ] **字符串匹配** — KMP 算法、Rabin-Karp、Boyer-Moore
- [ ] **数学基础** — 埃拉托色尼筛、快速幂、欧几里得算法

### 第八阶段：位运算与技巧（2-3 天）

- [ ] **位运算** — 与/或/异或操作，状态压缩，布隆过滤器基础

## Rust 特色关注点

每个实现会重点标注以下 Rust 语言特性：

| 特性 | 应用场景 |
|------|---------|
| `Box<T>` | 链表节点、树节点的堆分配 |
| `Rc<RefCell<T>>` | 多重所有权的图节点 |
| `Option<T>` | 空指针安全的替代方案 |
| 泛型 + Trait Bound | 通用数据结构的类型约束 |
| 迭代器模式 | 自定义 `Iterator` 实现遍历 |
| `unsafe` 块 | 何时需要、何时避免 |
| `derive` 宏 | `Debug` / `Clone` / `PartialEq` 自动实现 |

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
