# 算法与数据结构 — Java 实现

[![Java](https://img.shields.io/badge/Java-17%2B-ED8B00)](https://openjdk.org/)
[![Tests](https://img.shields.io/badge/tests-150%20passed-brightgreen)]()
[![Topics](https://img.shields.io/badge/topics-41-blue)]()

用 Java 从零实现的算法与数据结构大全，42 个实现文件，32 个测试文件，150 个用例，`mvn test` 一键验证。

---

## 快速开始

```bash
# 前置条件：Java 17+ 和 Maven
git clone <repo-url>
cd algorithm-java
mvn test      # 139 个用例全部通过 ✅
```

---

## 项目结构

```
algorithm-java/
├── README.md
├── pom.xml
└── src/
    ├── main/java/com/algorithmx/
    │   │
    │   ├── foundation/
    │   │   ├── sort/Sorting.java                 # 十大排序
    │   │   ├── search/BinarySearch.java          # 二分查找
    │   │   ├── array/ArrayTechniques.java        # 数组技巧
    │   │   └── recursion/Recursion.java          # 递归专题
    │   │
    │   ├── datastructure/
    │   │   ├── list/
    │   │   │   ├── SinglyLinkedList.java         # 单向链表
    │   │   │   └── DoublyLinkedList.java         # 双向链表
    │   │   ├── queue/StacksAndQueues.java        # 栈、队列、单调栈、单调队列
    │   │   ├── heap/MaxHeap.java                 # 二叉堆
    │   │   ├── hash/CustomHashMap.java           # 手写 HashMap
    │   │   ├── tree/
    │   │   │   ├── BinaryTree.java               # 二叉树遍历 + 树形 DP
    │   │   │   ├── BST.java                      # BST + AVL 平衡树
    │   │   │   └── MorrisTraversal.java          # O(1) 空间中序遍历
    │   │   ├── graph/Graph.java                  # 图表示、遍历、拓扑排序
    │   │   ├── trie/Trie.java                    # 前缀树
    │   │   ├── unionfind/UnionFind.java          # 并查集
    │   │   ├── cache/
    │   │   │   ├── LRUCache.java                 # LRU（含手写双向链表版）
    │   │   │   └── LFUCache.java                 # LFU
    │   │   ├── fenwick/FenwickTree.java          # 树状数组（BIT）
    │   │   ├── segment/SegmentTree.java          # 线段树（惰性标记）
    │   │   ├── sparsetable/SparseTable.java      # 稀疏表 RMQ — O(1) 区间最值
    │   │   ├── skiplist/SkipList.java            # 跳表
    │   │   ├── bloom/BloomFilter.java            # 布隆过滤器
    │   │   └── design/DesignProblems.java        # 设计题
    │   │
    │   ├── algorithm/
    │   │   ├── dp/DynamicProgramming.java        # 动态规划
    │   │   ├── backtracking/Backtracking.java    # 回溯
    │   │   ├── greedy/Greedy.java                # 贪心
    │   │   ├── randomized/Randomized.java        # Fisher-Yates / 蓄水池抽样 / QuickSelect
    │   │   ├── graph/
    │   │   │   ├── GraphAlgorithms.java          # Dijkstra / Kruskal / Prim
    │   │   │   ├── ShortestPath.java             # Bellman-Ford / Floyd / SPFA
    │   │   │   └── AdvancedGraph.java            # Tarjan SCC / Edmonds-Karp 最大流
    │   │   ├── search/AStar.java                 # A* 寻路
    │   │   ├── expression/ExpressionEval.java    # 表达式求值 + 逆波兰
    │   │   └── string/
    │   │       ├── KMP.java                      # KMP
    │   │       ├── StringMatching.java           # Rabin-Karp / Manacher
    │   │       └── ZAlgorithm.java               # Z Algorithm
    │   │
    │   └── technique/
    │       ├── bit/BitManipulation.java          # 位运算 + BitMap
    │       ├── math/NumberTheory.java            # 数论
    │       ├── image/ImageProcessing.java        # 图像处理
    │       └── ml/                               # AI/ML 算法
    │           ├── LinearAlgebra.java            #     线性代数基础
    │           ├── MLAlgorithms.java             #     梯度下降 / 线性回归 / 逻辑回归 / 感知机
    │           ├── MLClassifiers.java            #     K-Means / KNN / 朴素贝叶斯
    │           └── MLAdvanced.java               #     决策树 CART / PCA 降维
    │
    └── test/java/com/algorithmx/                 # 32 个测试文件 / 150 个用例
```

---

## 完整大纲

### 第一阶段：基础

| #   | 主题       | 核心算法                                   | 文件                    |
| --- | ---------- | ------------------------------------------ | ----------------------- |
| 1   | 复杂度分析 | 大 O、最好/最坏/平均                       | —                       |
| 2   | 数组       | 双指针、前缀和、差分、滑动窗口             | `foundation/array/`     |
| 3   | 链表       | 单/双向链表、反转、快慢指针、LRU           | `datastructure/list/`   |
| 4   | 栈与队列   | 单调栈、单调队列、最小栈、循环队列         | `datastructure/queue/`  |
| 5   | 递归       | 阶乘、斐波那契（记忆化）、汉诺塔、括号生成 | `foundation/recursion/` |

### 第二阶段：核心数据结构

| #   | 主题   | 核心算法                            | 文件                   |
| --- | ------ | ----------------------------------- | ---------------------- |
| 6   | 哈希表 | 链地址法、自动扩容                  | `datastructure/hash/`  |
| 7   | 堆     | 二叉堆（上浮/下沉）                 | `datastructure/heap/`  |
| 8   | 树     | 前/中/后序、层序、深度、直径        | `datastructure/tree/`  |
| 9   | BST    | BST 增删查、AVL 旋转（LL/RR/LR/RL） | `datastructure/tree/`  |
| 10  | 图     | 邻接表、DFS/BFS、连通分量、拓扑排序 | `datastructure/graph/` |

### 第三阶段：核心排序与搜索

| #   | 主题     | 核心算法                                               | 文件                 |
| --- | -------- | ------------------------------------------------------ | -------------------- |
| 11  | 十大排序 | 冒泡、选择、插入、希尔、归并、快速、堆、计数、桶、基数 | `foundation/sort/`   |
| 12  | 二分查找 | 精确查找、左右边界、旋转数组                           | `foundation/search/` |

### 第四阶段：算法思想

| #   | 主题     | 核心算法                                                               | 文件                      |
| --- | -------- | ---------------------------------------------------------------------- | ------------------------- |
| 13  | 贪心     | 区间调度、跳跃游戏、分糖果、加油站                                     | `algorithm/greedy/`       |
| 14  | 动态规划 | 0-1/完全/多重背包、LIS、LCS、编辑距离、区间 DP、状压 DP（TSP）、Kadane | `algorithm/dp/`           |
| 15  | 回溯     | 排列、组合、子集、N 皇后、数独                                         | `algorithm/backtracking/` |

### 第五阶段：图论

| #   | 主题       | 核心算法                                     | 文件                       |
| --- | ---------- | -------------------------------------------- | -------------------------- |
| 16  | 最短路径   | Dijkstra、Bellman-Ford、Floyd-Warshall、SPFA | `algorithm/graph/`         |
| 17  | 最小生成树 | Prim、Kruskal                                | `algorithm/graph/`         |
| 18  | 并查集     | 路径压缩 + 按秩合并                          | `datastructure/unionfind/` |
| 19  | 强连通分量 | Tarjan SCC                                   | `algorithm/graph/`         |
| 20  | 最大流     | Edmonds-Karp（BFS）                          | `algorithm/graph/`         |

### 第六阶段：高级数据结构与算法

| #   | 主题              | 核心算法                                    | 文件                                |
| --- | ----------------- | ------------------------------------------- | ----------------------------------- |
| 21  | Trie              | 插入、搜索、前缀匹配                        | `datastructure/trie/`               |
| 22  | 线段树 & 树状数组 | BIT 单点/区间、线段树区间更新 + 惰性标记    | `datastructure/fenwick/` `segment/` |
| 23  | 稀疏表            | RMQ — O(1) 区间最小值查询                   | `datastructure/sparsetable/`        |
| 24  | 字符串算法        | KMP、Rabin-Karp、Manacher、Z Algorithm      | `algorithm/string/`                 |
| 25  | 跳表              | 概率型 O(log n) 增删查                      | `datastructure/skiplist/`           |
| 26  | 布隆过滤器        | 概率型集合，空间高效                        | `datastructure/bloom/`              |
| 27  | 位运算            | 基础运算、BitMap                            | `technique/bit/`                    |
| 28  | 设计题            | LRU、LFU、Twitter、排行榜、中位数、循环队列 | `datastructure/cache/` `design/`    |

### 第七阶段：专题突破

| #   | 主题              | 核心算法                                                                            | 文件                    |
| --- | ----------------- | ----------------------------------------------------------------------------------- | ----------------------- |
| 29  | 双指针 & 滑动窗口 | 同向/相向双指针、固定/可变窗口                                                      | `foundation/array/`     |
| 30  | 单调栈 & 单调队列 | 下一个更大元素、滑动窗口最大值                                                      | `datastructure/queue/`  |
| 31  | 数学 & 数论       | GCD、LCM、扩展欧几里得、快速幂/矩阵快速幂、埃氏筛/欧拉筛、进制转换、大数运算        | `technique/math/`       |
| 32  | Morris 遍历       | O(1) 空间树遍历                                                                     | `datastructure/tree/`   |
| 33  | 随机化算法        | Fisher-Yates 洗牌、蓄水池抽样、QuickSelect                                          | `algorithm/randomized/` |
| 34  | A* 寻路           | 启发式搜索（曼哈顿距离）                                                            | `algorithm/search/`     |
| 35  | 表达式求值        | 中缀计算器、逆波兰求值、中缀 → 后缀                                                 | `algorithm/expression/` |
| 36  | 图像算法          | 翻转、旋转、卷积（模糊/锐化/Sobel）、直方图均衡、形态学（膨胀/腐蚀）、泛洪填充、RLE | `technique/image/`      |
| 37  | 综合实战          | 多算法融合 + LeetCode 高频题                                                        | 练习篇                  |

### 第八阶段：AI / ML 经典算法

| #   | 主题         | 核心算法                                                       | 文件            |
| --- | ------------ | -------------------------------------------------------------- | --------------- |
| 38  | 线性代数基础 | 向量/矩阵运算、Gauss-Jordan 消元、幂迭代                       | `technique/ml/` |
| 39  | 回归与优化   | 批量/随机梯度下降、线性回归（最小二乘法+GD）、逻辑回归、感知机 | `technique/ml/` |
| 40  | 分类与聚类   | K-Means、KNN、朴素贝叶斯（高斯）                               | `technique/ml/` |
| 41  | 决策树 & PCA | CART 分类树（Gini 纯度）、PCA 降维（幂迭代）                   | `technique/ml/` |

---

## 运行

```bash
mvn test                        # 全部 150 个测试
mvn test -Dtest=SortingTest     # 单个测试类
mvn test -Dtest=AStarTest#withObstacles  # 单个测试方法
```

## 学习建议

1. 按阶段顺序推进，每完成一个知识点搭配 LeetCode 3-5 题
2. 先看注释理解思路，再运行测试验证
3. Debug 单步跟踪关键算法，加深理解
4. 看完代码后尝试不参考原文自己重写
