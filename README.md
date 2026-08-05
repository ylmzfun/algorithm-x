# PHP 数据结构与算法实现

一个完整的 PHP 数据结构与算法实现库，包含常用的数据结构和相关算法。

## 📋 目录

- [项目概述](#项目概述)
- [主要特性](#主要特性)
- [数据结构列表](#数据结构列表)
- [算法实现](#算法实现)
- [安装与使用](#安装与使用)
- [示例代码](#示例代码)
- [项目结构](#项目结构)
- [性能特点](#性能特点)
- [实际应用场景](#实际应用场景)
- [扩展功能](#扩展功能)
- [未实现的重要数据结构和算法](#未实现的重要数据结构和算法)
- [优化建议](#优化建议)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [致谢](#致谢)
- [联系方式](#联系方式)

## 🎯 项目概述

本项目实现了计算机科学中常用的数据结构和算法，每个数据结构都包含：
- 完整的方法实现
- 详细的时间复杂度分析
- 丰富的代码注释
- 实际应用场景说明
- 完整的使用示例

## 主要特性

- **完整的数据结构实现**：包含线性、树形、图形、哈希等各类数据结构
- **丰富的算法库**：实现了排序、搜索、图算法、字符串算法、动态规划、贪心算法、回溯算法和数学算法等经典算法
- **标准化接口**：提供统一的接口规范，便于扩展和维护
- **异常处理系统**：完善的异常处理机制，提高代码健壮性
- **工具函数库**：提供常用的辅助函数和性能测试工具
- **完整的测试覆盖**：包含单元测试和集成测试
- **高性能优化**：针对PHP特性进行了性能优化
- **易于使用**：提供清晰的API和详细的文档
- **实际应用场景**：包含真实世界的应用示例
- **教育价值**：适合学习算法和数据结构的完整实现
- **代码质量**：遵循PSR标准，包含完整的错误处理

## 📊 数据结构列表

### 线性数据结构 (Linear)

| 数据结构           | 文件                    | 主要特点                       | 时间复杂度         |
| ------------------ | ----------------------- | ------------------------------ | ------------------ |
| **ArrayList**      | `Linear/ArrayList.php`  | 动态数组，支持随机访问         | 访问O(1), 插入O(n) |
| **LinkedList**     | `Linear/LinkedList.php` | 双向链表，动态内存分配         | 访问O(n), 插入O(1) |
| **Stack**          | `Linear/Stack.php`      | 后进先出(LIFO)，支持表达式求值 | 所有操作O(1)       |
| **Queue**          | `Linear/Queue.php`      | 先进先出(FIFO)，循环数组实现   | 所有操作O(1)       |
| **PriorityQueue**  | `Linear/Queue.php`      | 优先队列，基于最小堆           | 插入/删除O(log n)  |
| **Deque**          | `Linear/Deque.php`      | 双端队列，支持两端操作         | 所有操作O(1)       |
| **MonotonicDeque** | `Linear/Deque.php`      | 单调队列，滑动窗口问题         | 均摊O(1)           |

### 树形数据结构 (Tree)

| 数据结构             | 文件                        | 主要特点                   | 时间复杂度        |
| -------------------- | --------------------------- | -------------------------- | ----------------- |
| **BinaryTree**       | `Tree/BinaryTree.php`       | 二叉树基础实现，多种遍历   | 遍历O(n)          |
| **BinarySearchTree** | `Tree/BinarySearchTree.php` | 二叉搜索树，有序存储       | 平均O(log n)      |
| **Heap**             | `Tree/Heap.php`             | 堆结构，支持最大/最小堆    | 插入/删除O(log n) |
| **MinHeap**          | `Tree/Heap.php`             | 最小堆实现                 | 插入/删除O(log n) |
| **MaxHeap**          | `Tree/Heap.php`             | 最大堆实现                 | 插入/删除O(log n) |
| **IndexedHeap**      | `Tree/Heap.php`             | 索引堆，支持优先级修改     | 修改O(log n)      |
| **AVLTree**          | `Tree/AVLTree.php`          | 自平衡二叉搜索树，严格平衡 | 所有操作O(log n)  |
| **RedBlackTree**     | `Tree/RedBlackTree.php`     | 红黑树，近似平衡           | 所有操作O(log n)  |
| **Treap**            | `Tree/Treap.php`            | 树堆，随机平衡BST          | 期望O(log n)      |
| **BTree**            | `Tree/BTree.php`            | B树，多路平衡搜索树        | 所有操作O(log n)  |
| **BPlusTree**        | `Tree/BPlusTree.php`        | B+树，索引结构标准         | 所有操作O(log n)  |
| **SplayTree**        | `Tree/SplayTree.php`        | 伸展树，自调整BST          | 均摊O(log n)      |

### 图数据结构 (Graph)

| 数据结构          | 文件                      | 主要特点                    | 时间复杂度             |
| ----------------- | ------------------------- | --------------------------- | ---------------------- |
| **Graph**         | `Graph/Graph.php`         | 邻接表实现，支持有向/无向图 | 添加边O(1)             |
| **WeightedGraph** | `Graph/WeightedGraph.php` | 加权图，支持最短路径算法    | Dijkstra O((V+E)log V) |

### 哈希数据结构 (Hash)

| 数据结构                | 文件                      | 主要特点                 | 时间复杂度 |
| ----------------------- | ------------------------- | ------------------------ | ---------- |
| **HashTable**           | `Hash/HashTable.php`      | 哈希表，链式解决冲突     | 平均O(1)   |
| **ConsistentHash**      | `Hash/HashTable.php`      | 一致性哈希，分布式系统   | O(log n)   |
| **BloomFilter**         | `Hash/BloomFilter.php`    | 布隆过滤器，概率数据结构 | O(k)       |
| **CountingBloomFilter** | `Hash/BloomFilter.php`    | 计数布隆过滤器，支持删除 | O(k)       |
| **CuckooHash**          | `Hash/CuckooHash.php`     | 布谷鸟哈希，最坏O(1)查找 | 平均O(1)   |
| **CountMinSketch**      | `Hash/CountMinSketch.php` | 计数最小草图，频率估计   | O(d)       |

### 高级数据结构 (Advanced)

| 数据结构               | 文件                       | 主要特点                     | 时间复杂度    |
| ---------------------- | -------------------------- | ---------------------------- | ------------- |
| **Trie**               | `Advanced/Trie.php`        | 前缀树，字符串检索           | 插入/查找O(m) |
| **CompressedTrie**     | `Advanced/Trie.php`        | 压缩前缀树，节省空间         | 插入/查找O(m) |
| **LRUCache**           | `Advanced/LRUCache.php`    | 最近最少使用缓存             | 所有操作O(1)  |
| **LFUCache**           | `Advanced/LRUCache.php`    | 最少使用频率缓存             | 所有操作O(1)  |
| **TTLCache**           | `Advanced/LRUCache.php`    | 带过期时间的缓存             | 所有操作O(1)  |
| **SkipList**           | `Advanced/SkipList.php`    | 跳表，概率平衡               | 平均O(log n)  |
| **ConcurrentSkipList** | `Advanced/SkipList.php`    | 并发跳表，线程安全           | 平均O(log n)  |
| **UnionFind**          | `Advanced/UnionFind.php`   | 并查集，路径压缩+按秩合并    | 均摊O(α(n))   |
| **FenwickTree**        | `Advanced/FenwickTree.php` | 二叉索引树，前缀和与单点更新 | O(log n)      |
| **SegmentTree**        | `Advanced/SegmentTree.php` | 线段树，区间查询与延迟更新   | O(log n)      |

## 🧮 算法实现

### 📈 排序算法

| 算法     | 时间复杂度 | 空间复杂度 | 稳定性 | 适用场景   |
| -------- | ---------- | ---------- | ------ | ---------- |
| 快速排序 | O(n log n) | O(log n)   | 不稳定 | 通用排序   |
| 归并排序 | O(n log n) | O(n)       | 稳定   | 大数据排序 |
| 堆排序   | O(n log n) | O(1)       | 不稳定 | 内存受限   |
| 插入排序 | O(n²)      | O(1)       | 稳定   | 小数据集   |
| 选择排序 | O(n²)      | O(1)       | 不稳定 | 简单实现   |
| 冒泡排序 | O(n²)      | O(1)       | 稳定   | 教学演示   |
| 计数排序 | O(n+k)     | O(k)       | 稳定   | 整数排序   |
| 基数排序 | O(d(n+k))  | O(n+k)     | 稳定   | 多位数排序 |
| 桶排序   | O(n+k)     | O(n+k)     | 稳定   | 均匀分布   |

### 🔍 搜索算法

| 算法         | 时间复杂度   | 空间复杂度 | 前提条件 | 适用场景     |
| ------------ | ------------ | ---------- | -------- | ------------ |
| 线性搜索     | O(n)         | O(1)       | 无       | 无序数据     |
| 二分搜索     | O(log n)     | O(1)       | 有序     | 有序数据     |
| 插值搜索     | O(log log n) | O(1)       | 均匀分布 | 均匀有序数据 |
| 指数搜索     | O(log n)     | O(1)       | 有序     | 无界搜索     |
| 跳跃搜索     | O(√n)        | O(1)       | 有序     | 大数据集     |
| 三分搜索     | O(log n)     | O(1)       | 单峰函数 | 优化问题     |
| 斐波那契搜索 | O(log n)     | O(1)       | 有序     | 减少比较     |

### 🌐 图算法

| 算法               | 时间复杂度    | 空间复杂度 | 应用场景           |
| ------------------ | ------------- | ---------- | ------------------ |
| 深度优先搜索 (DFS) | O(V+E)        | O(V)       | 路径查找、拓扑排序 |
| 广度优先搜索 (BFS) | O(V+E)        | O(V)       | 最短路径、层次遍历 |
| 拓扑排序           | O(V+E)        | O(V)       | 依赖关系排序       |
| 环检测             | O(V+E)        | O(V)       | 死锁检测           |
| Dijkstra算法       | O((V+E)log V) | O(V)       | 单源最短路径       |
| Floyd-Warshall     | O(V³)         | O(V²)      | 全源最短路径       |
| Bellman-Ford       | O(VE)         | O(V)       | 负权边最短路径     |
| Kruskal算法        | O(E log E)    | O(V)       | 最小生成树         |
| Tarjan算法         | O(V+E)        | O(V)       | 强连通分量         |
| Kosaraju算法       | O(V+E)        | O(V)       | 强连通分量         |
| Prim算法           | O(V²)         | O(V)       | 最小生成树         |
| Edmonds-Karp       | O(V·E²)       | O(V+E)     | 最大流问题         |
| Dinic算法          | O(V²·E)       | O(V+E)     | 最大流问题         |
| 匈牙利算法         | O(V·E)        | O(V+E)     | 二分图最大匹配     |
| 桥检测             | O(V+E)        | O(V)       | 网络脆弱性分析     |
| 割点检测           | O(V+E)        | O(V)       | 网络关键节点       |
| LCA                | O(log n)      | O(n log n) | 最近公共祖先       |
| 最小费用最大流     | O(flow·V·E)   | O(V+E)     | 运输优化问题       |
| 二分图判定         | O(V+E)        | O(V)       | 图着色             |

### 🔤 字符串算法

| 算法           | 时间复杂度 | 空间复杂度 | 应用场景       |
| -------------- | ---------- | ---------- | -------------- |
| KMP算法        | O(n+m)     | O(m)       | 模式匹配       |
| Rabin-Karp     | O(n+m)     | O(1)       | 多模式匹配     |
| Boyer-Moore    | O(n/m)     | O(σ)       | 大文本搜索     |
| 最长公共子序列 | O(nm)      | O(nm)      | 文本比较       |
| 编辑距离       | O(nm)      | O(nm)      | 拼写检查       |
| Manacher算法   | O(n)       | O(n)       | 回文检测       |
| Z算法          | O(n)       | O(n)       | 字符串匹配     |
| 滚动哈希       | O(n)       | O(1)       | 快速字符串比较 |
| Aho-Corasick   | O(n+z)     | O(m)       | 多模式匹配     |
| 后缀自动机     | O(n)       | O(n)       | 子串问题全能   |
| 回文树         | O(n)       | O(n)       | 回文相关问题   |
| 后缀数组       | O(n log n) | O(n)       | 子串索引       |

### 🔄 动态规划算法

| 算法           | 时间复杂度  | 空间复杂度 | 应用场景     |
| -------------- | ----------- | ---------- | ------------ |
| 斐波那契数列   | O(n)        | O(1)       | 数列计算     |
| 最长公共子序列 | O(nm)       | O(nm)      | 序列比较     |
| 编辑距离       | O(nm)       | O(nm)      | 字符串相似度 |
| 0-1背包问题    | O(nW)       | O(nW)      | 资源分配     |
| 最长递增子序列 | O(n²)       | O(n)       | 序列分析     |
| 最大子数组和   | O(n)        | O(1)       | 数组优化     |
| 硬币找零       | O(amount×n) | O(amount)  | 找零问题     |
| 爬楼梯         | O(n)        | O(1)       | 计数问题     |
| 房屋抢劫       | O(n)        | O(1)       | 优化问题     |
| 最小路径和     | O(mn)       | O(mn)      | 路径规划     |
| 完全背包       | O(nW)       | O(W)       | 无限物品分配 |
| 多重背包       | O(nW log C) | O(W)       | 有限物品分配 |
| 分组背包       | O(nW)       | O(W)       | 分组物品选择 |
| 旅行商(TSP)    | O(n²·2^n)   | O(n·2^n)   | 状态压缩DP   |
| 树形DP         | O(n)        | O(n)       | 树结构优化   |
| 数位DP         | O(位数×10)  | O(位数)    | 数字统计     |
| 区间DP         | O(n³)       | O(n²)      | 矩阵链乘法   |

### 🎯 贪心算法

| 算法             | 时间复杂度 | 空间复杂度 | 应用场景 |
| ---------------- | ---------- | ---------- | -------- |
| 活动选择         | O(n log n) | O(1)       | 调度问题 |
| 分数背包         | O(n log n) | O(1)       | 资源分配 |
| 霍夫曼编码       | O(n log n) | O(n)       | 数据压缩 |
| 最小生成树(Prim) | O(V²)      | O(V)       | 网络设计 |
| 跳跃游戏         | O(n)       | O(1)       | 路径问题 |
| 股票买卖         | O(n)       | O(1)       | 投资策略 |
| 加油站问题       | O(n)       | O(1)       | 路径规划 |
| 分发糖果         | O(n)       | O(n)       | 分配问题 |

### 🔙 回溯算法

| 算法      | 时间复杂度 | 空间复杂度 | 应用场景 |
| --------- | ---------- | ---------- | -------- |
| N皇后问题 | O(N!)      | O(N)       | 约束满足 |
| 数独求解  | O(9^(n²))  | O(n²)      | 逻辑推理 |
| 全排列    | O(n!)      | O(n)       | 组合生成 |
| 组合生成  | O(C(n,k))  | O(k)       | 选择问题 |
| 子集生成  | O(2^n)     | O(n)       | 幂集生成 |
| 单词搜索  | O(N×4^L)   | O(L)       | 模式匹配 |
| 括号生成  | O(4^n/√n)  | O(n)       | 序列生成 |
| 迷宫求解  | O(4^(nm))  | O(nm)      | 路径搜索 |

### 🔢 数学算法

| 算法              | 时间复杂度      | 空间复杂度 | 应用场景   |
| ----------------- | --------------- | ---------- | ---------- |
| 欧几里得算法(GCD) | O(log min(a,b)) | O(1)       | 数论计算   |
| 埃拉托斯特尼筛法  | O(n log log n)  | O(n)       | 质数生成   |
| 快速幂            | O(log n)        | O(1)       | 模运算     |
| 扩展欧几里得      | O(log m)        | O(1)       | 模逆元     |
| 组合数计算        | O(k)            | O(1)       | 计数问题   |
| 卡塔兰数          | O(n²)           | O(n)       | 组合计数   |
| 牛顿法求平方根    | O(log n)        | O(1)       | 数值计算   |
| 约瑟夫问题        | O(n)            | O(1)       | 环形淘汰   |
| 几何计算          | O(1)            | O(1)       | 空间分析   |
| 中国剩余定理      | O(n log M)      | O(1)       | 同余方程组 |
| 矩阵快速幂        | O(n³ log k)     | O(n²)      | 线性递推   |
| Nim游戏           | O(n)            | O(1)       | 博弈胜负   |
| SG函数            | O(状态·转移)    | O(状态)    | 组合博弈   |
| 线性同余方程      | O(log m)        | O(1)       | 模方程求解 |
| Miller-Rabin      | O(k log³ n)     | O(1)       | 素性测试   |
| 蒙特卡洛          | O(n)            | O(1)       | 数值估计   |
| 洗牌算法          | O(n)            | O(1)       | 随机排列   |
| QuickSelect       | O(n) 期望       | O(1)       | 第k小元素  |

### 🧠 高级启发式算法

| 算法         | 类型         | 应用场景             |
| ------------ | ------------ | -------------------- |
| 模拟退火     | 元启发式     | 组合优化、布局设计   |
| 遗传算法     | 进化算法     | 特征选择、调度优化   |
| 粒子群优化   | 群智能       | 函数优化、神经网络   |
| 前馈神经网络 | 深度学习基础 | 分类、回归、模式识别 |

## 🚀 安装与使用

### 环境要求

- PHP 8.0 或更高版本
- Composer (用于自动加载)

### 安装步骤

1. 克隆项目：
```bash
git clone <repository-url>
cd php-algorithm
```

2. 安装依赖：
```bash
composer install
```

3. 运行示例：
```bash
php examples/AllDataStructuresDemo.php
```

### 基本使用

```php
<?php
require_once 'vendor/autoload.php';

use DataStructures\Linear\ArrayList;
use DataStructures\Tree\BinarySearchTree;
use DataStructures\Hash\HashTable;

// 使用动态数组
$list = new ArrayList();
$list->add("Hello");
$list->add("World");
echo $list->get(0); // 输出: Hello

// 使用二叉搜索树
$bst = new BinarySearchTree();
$bst->insert(50);
$bst->insert(30);
$bst->insert(70);
echo $bst->search(30) ? "Found" : "Not Found"; // 输出: Found

// 使用哈希表
$hash = new HashTable();
$hash->put("name", "张三");
echo $hash->get("name"); // 输出: 张三
```

## 📝 示例代码

项目提供了丰富的示例代码，位于 `examples/` 目录：

- **`AllDataStructuresDemo.php`** - 完整演示所有数据结构
- **`LinearDataStructuresExample.php`** - 线性数据结构示例
- **`TreeDataStructuresExample.php`** - 树形数据结构示例
- **`GraphDataStructuresExample.php`** - 图数据结构示例
- **`HashAndAdvancedExample.php`** - 哈希和高级数据结构示例

### 运行示例

```bash
# 运行完整演示
php examples/AllDataStructuresDemo.php

# 运行算法演示
php examples/AlgorithmsDemo.php

# 运行综合算法演示
php examples/ComprehensiveAlgorithmsDemo.php

# 运行特定类型的示例
php examples/LinearDataStructuresExample.php
php examples/TreeDataStructuresExample.php
php examples/GraphDataStructuresExample.php
php examples/HashAndAdvancedExample.php

# 运行基础功能测试
php test_basic.php

# 使用Composer脚本
composer demo              # 运行综合算法演示
composer basic-demo        # 运行基本演示
composer algorithms-demo   # 运行算法演示
composer test              # 运行单元测试
composer test-coverage     # 运行测试并生成覆盖率报告
composer test-performance  # 运行性能测试
composer benchmark         # 运行基准测试
composer benchmark-json    # 运行基准测试(JSON输出)
composer generate-help     # 显示代码生成器帮助
composer validate-config   # 验证项目配置
```

## 📁 项目结构

```
php-algorithm/
├── src/                          # 源代码目录
│   ├── Linear/                   # 线性数据结构
│   │   ├── ArrayList.php         # 动态数组
│   │   ├── LinkedList.php        # 链表
│   │   ├── Stack.php             # 栈
│   │   ├── Queue.php             # 队列和优先队列
│   │   └── Deque.php             # 双端队列
│   ├── Tree/                     # 树形数据结构
│   │   ├── BinaryTree.php        # 二叉树
│   │   ├── BinarySearchTree.php  # 二叉搜索树
│   │   ├── Heap.php              # 堆
│   │   ├── AVLTree.php           # AVL平衡树
│   │   ├── RedBlackTree.php      # 红黑树
│   │   ├── BTree.php             # B树
│   │   ├── BPlusTree.php         # B+树
│   │   ├── Treap.php             # 树堆
│   │   └── SplayTree.php         # 伸展树
│   ├── Graph/                    # 图数据结构
│   │   ├── Graph.php             # 图
│   │   └── WeightedGraph.php     # 加权图
│   ├── Hash/                     # 哈希数据结构
│   │   ├── HashTable.php         # 哈希表
│   │   ├── BloomFilter.php       # 布隆过滤器
│   │   ├── CuckooHash.php        # 布谷鸟哈希
│   │   └── CountMinSketch.php    # 计数最小草图
│   ├── Advanced/                 # 高级数据结构
│   │   ├── Trie.php              # 前缀树
│   │   ├── LRUCache.php          # 缓存结构
│   │   ├── SkipList.php          # 跳表
│   │   ├── UnionFind.php         # 并查集
│   │   ├── FenwickTree.php       # 二叉索引树
│   │   └── SegmentTree.php       # 线段树
│   ├── Algorithms/               # 算法实现
│   │   ├── Sorting.php           # 排序算法
│   │   ├── SearchAlgorithms.php  # 搜索算法
│   │   ├── GraphAlgorithms.php   # 图算法
│   │   ├── StringAlgorithms.php  # 字符串算法
│   │   ├── SuffixAutomaton.php   # 后缀自动机
│   │   ├── SuffixArray.php       # 后缀数组
│   │   ├── PalindromicTree.php   # 回文树
│   │   ├── AdvancedAlgorithms.php # 高级启发式算法
│   ├── Interfaces/               # 接口定义
│   │   └── DataStructureInterfaces.php # 数据结构接口
│   ├── Exceptions/               # 异常处理
│   │   └── DataStructureException.php # 数据结构异常
│   └── Utils/                    # 工具类
│       └── Utils.php             # 通用工具函数
├── examples/                     # 示例代码
│   ├── AllDataStructuresDemo.php # 完整演示
│   ├── AlgorithmsDemo.php        # 算法演示
│   ├── LinearDataStructuresExample.php
│   ├── TreeDataStructuresExample.php
│   ├── GraphDataStructuresExample.php
│   └── HashAndAdvancedExample.php
├── test_basic.php                # 基础功能测试
├── composer.json                 # Composer配置
└── README.md                     # 项目说明
```

## ⚡ 性能特点

### 时间复杂度对比

| 操作 | ArrayList | LinkedList | HashTable | BST       | Heap       |
| ---- | --------- | ---------- | --------- | --------- | ---------- |
| 插入 | O(n)      | O(1)       | O(1)*     | O(log n)* | O(log n)   |
| 删除 | O(n)      | O(1)       | O(1)*     | O(log n)* | O(log n)   |
| 查找 | O(1)      | O(n)       | O(1)*     | O(log n)* | O(1)       |
| 遍历 | O(n)      | O(n)       | O(n)      | O(n)      | O(n log n) |

*平均情况下的时间复杂度

### 空间复杂度

- **ArrayList**: O(n) - 连续内存，缓存友好
- **LinkedList**: O(n) - 额外指针开销
- **HashTable**: O(n) - 负载因子影响
- **Tree结构**: O(n) - 递归调用栈
- **Graph**: O(V + E) - 顶点和边的存储

## 🎯 实际应用场景

### 1. Web开发
- **LRU Cache**: 页面缓存、数据库查询缓存
- **HashTable**: 会话存储、配置管理
- **Trie**: 自动补全、搜索建议
- **BloomFilter**: 防止缓存穿透、垃圾邮件过滤

### 2. 系统设计
- **ConsistentHash**: 分布式缓存、负载均衡
- **PriorityQueue**: 任务调度、事件处理
- **Graph**: 社交网络、推荐系统
- **SkipList**: 数据库索引、并发数据结构

### 3. 算法竞赛
- **Stack**: 表达式求值、括号匹配
- **Queue**: BFS遍历、层序处理
- **Heap**: 优先队列、Top K问题
- **BST**: 范围查询、有序操作

## 📋 未实现的重要数据结构和算法

> ✅ 标记项为已实现（自初始版本后新增）

### 数据结构
1. **平衡树结构**：
   - ✅ AVL树
   - ✅ 红黑树
   - ✅ Splay树
   - ✅ Treap树

2. **B树系列**：
   - ✅ B树
   - ✅ B+树
   - B*树

3. **并查集**：
   - ✅ 带路径压缩的并查集
   - ✅ 按秩合并的并查集

4. **线段树**：
   - ✅ 基本线段树
   - ✅ 线段树延迟标记
   - ✅ 线段树区间更新

5. **二叉索引树**（Fenwick Tree）：
   - ✅ 单点更新，区间查询
   - ✅ 区间更新，单点查询
   - ✅ 区间更新，区间查询

6. **后缀树/后缀数组**：
   - 后缀树
   - ✅ 后缀数组
   - ✅ 最长重复子串

7. **其他高级数据结构**：
   - ✅ 布谷鸟哈希
   - ✅ 跳表的更多变体
   - 并发数据结构（如ConcurrentHashMap）
   - ✅ 概率数据结构（Count-Min Sketch）

### 算法
1. **图算法**：
   - ✅ Prim最小生成树算法
   - ✅ 最大流算法（Edmonds-Karp, Dinic）
   - ✅ 最小费用最大流
   - ✅ 二分图匹配（匈牙利算法）
   - ✅ 强连通分量（Kosaraju算法）
   - ✅ 最近公共祖先（LCA）
   - ✅ 桥和割点算法

2. **字符串算法**：
   - ✅ Aho-Corasick自动机
   - ✅ 后缀自动机
   - ✅ 回文树
   - 字典树优化（如双数组Trie）

3. **动态规划**：
   - ✅ 状态压缩动态规划
   - ✅ 树形动态规划
   - ✅ 数位动态规划
   - ✅ 区间动态规划
   - ✅ 背包问题变体（完全背包、多重背包、分组背包）

4. **数学算法**：
   - ✅ 中国剩余定理
   - ✅ 线性同余方程
   - ✅ 矩阵快速幂
   - ✅ 博弈论算法（Nim游戏、SG函数）
   - ✅ 概率算法
   - ✅ 随机化算法

5. **高级算法**：
   - ✅ 模拟退火算法
   - ✅ 遗传算法
   - ✅ 粒子群优化
   - ✅ 神经网络基础算法

## 🚀 优化建议

### 数据结构扩展
1. **实现平衡树结构** ✅：
   - ✅ AVL树、红黑树、Treap、Splay树均已实现
   - B*, 更多变体可继续扩展

2. **实现B树和B+树** ✅：
   - ✅ B树和 B+树已实现，B*树可继续扩展

3. **实现并查集** ✅

4. **实现线段树和二叉索引树** ✅：
   - ✅ 线段树（延迟标记）和 Fenwick树（含区间操作）已实现

### 算法扩展
1. **扩展图算法** ✅

2. **扩展字符串算法** ✅：
   - ✅ Aho-Corasick、后缀自动机、后缀数组、回文树已实现

3. **扩展动态规划** ✅：
   - ✅ 背包变体、状态压缩DP、树形DP、数位DP、区间DP已实现

4. **扩展数学算法** ✅：
   - ✅ CRT、线性同余、矩阵快速幂、博弈论、概率/随机化算法已实现

5. **高级算法** ✅：
   - ✅ 模拟退火、遗传算法、PSO、神经网络基础已实现

### 代码质量优化
1. **增强类型安全**：
   - 利用PHP 8的类型声明，增强代码的类型安全性
   - 实现泛型容器，支持类型约束

2. **优化异常处理**：
   - 定义更具体的异常类型，便于错误定位
   - 提供更详细的错误信息和上下文

3. **增强代码复用**：
   - 提取公共代码到基类或工具类
   - 实现更通用的接口和抽象类

4. **提高代码可读性**：
   - 统一命名规范
   - 增加更详细的注释和文档
   - 优化代码结构，减少嵌套层次

### 性能优化
1. **算法优化**：
   - 针对PHP特性，优化算法实现
   - 减少不必要的内存分配和拷贝
   - 优化递归算法，避免栈溢出

2. **数据结构优化**：
   - 针对不同场景，选择合适的数据结构
   - 优化数据结构的内存使用
   - 实现缓存机制，减少重复计算

3. **并发优化**：
   - 实现线程安全的数据结构
   - 提供无锁数据结构的实现
   - 优化并发访问性能

4. **性能测试**：
   - 增加更全面的性能测试
   - 提供不同规模数据的性能对比
   - 实现性能监控和分析工具

### 文档和测试优化
1. **完善文档**：
   - 提供更详细的API文档
   - 增加算法原理和实现细节的说明
   - 提供更多的使用示例和最佳实践

2. **增强测试**：
   - 增加单元测试覆盖率
   - 实现集成测试
   - 提供边界情况和异常情况的测试

3. **示例代码**：
   - 增加更多的示例代码
   - 提供实际应用场景的示例
   - 实现完整的应用案例

## 🔧 扩展功能

### 自定义比较器

```php
// 自定义对象排序
$heap = new class extends MinHeap {
    protected function compare($a, $b): int {
        return $a->priority <=> $b->priority;
    }
};
```

### 泛型支持

```php
// 类型安全的容器
class TypedArrayList extends ArrayList {
    private string $type;
    
    public function __construct(string $type) {
        parent::__construct();
        $this->type = $type;
    }
    
    public function add($element): void {
        if (!is_a($element, $this->type)) {
            throw new InvalidArgumentException("Element must be of type {$this->type}");
        }
        parent::add($element);
    }
}
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PSR-12 编码标准
- 添加完整的 PHPDoc 注释
- 包含时间复杂度分析
- 提供使用示例
- 编写单元测试

### 提交信息格式

```
type(scope): description

[optional body]

[optional footer]
```

类型：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建过程或辅助工具的变动

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有贡献者的努力
- 参考了经典的数据结构与算法教材
- 借鉴了其他优秀的开源实现

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发起 Discussion
- 邮件联系

---

**Happy Coding! 🚀**