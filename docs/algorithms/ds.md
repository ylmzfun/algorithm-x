# 数据结构模块（`algorithm_x::ds`）

本模块实现算法竞赛与工程实践中常用的 24 个基础数据结构，全部位于 `namespace algorithm_x::ds` 下，头文件位于 `include/algorithm_x/ds/`，对应测试位于 `tests/ds/test_*.cpp`（gtest，通过 CMake 构建）。覆盖范围：线性结构（动态数组、链表、栈、队列、双端队列）、树结构（二叉搜索树、AVL 树、红黑树、B 树、Trie、线段树、树状数组、并查集）、堆（二叉堆、优先队列、斐波那契堆）、哈希与概率结构（哈希表、布隆过滤器）、图存储（邻接矩阵、邻接表、链式前向星）以及应用型结构（LRU/LFU 缓存、哈夫曼编码、跳表）。本文档按目录顺序逐一说明用途、原理、真实 API、复杂度与使用示例。

---

### `ds/adjacency_matrix.h` — 邻接矩阵

**用途**：用 `V × V` 二维数组存储图，解决稠密图（边数接近 V²）的存储与"两顶点间是否有边、边权多少"的 O(1) 查询问题。

**原理**：`weight_[u][v]` 直接存 `u → v` 的边权（0 表示无边）；`add_edge` 时对无向图同时写入 `(u, v)` 与 `(v, u)` 保证矩阵对称，有向图只写 `(u, v)`。

**主要 API**：

```cpp
class AdjacencyMatrix {
public:
    explicit AdjacencyMatrix(std::size_t vertices, bool directed = false);
    void add_edge(std::size_t u, std::size_t v, int w = 1);
    bool has_edge(std::size_t u, std::size_t v) const;
    int get_weight(std::size_t u, std::size_t v) const;  // 无边返回 0
    std::size_t vertices() const;
};
```

**复杂度**：加边、查边、取权均为 O(1)；空间 O(V²)（按实现，内部为 `vector<vector<int>>`）。

**使用场景**：
- 顶点数较小（如 ≤ 5000）的稠密图，如 Floyd 等需要任意两点最短路的算法
- 需要频繁判断两点之间是否有边/取边权

**使用示例**：

```cpp
AdjacencyMatrix g(4);          // 无向图
g.add_edge(0, 1, 5);
g.add_edge(0, 2, 3);
g.has_edge(1, 0);              // true（无向图对称写入）
int w = g.get_weight(0, 2);    // 3
```

---

### `ds/avl_tree.h` — AVL 树

**用途**：自平衡二叉搜索树，解决普通 BST 在有序插入下退化为链表、操作退化到 O(n) 的问题，保证查找/插入/删除始终 O(log n)。

**原理**：每个节点维护子树高度，插入/删除后从底向上检查平衡因子 `height(left) - height(right)`，当 |bf| > 1 时通过 LL / LR / RR / RL 四种旋转恢复平衡（|balance| ≤ 1）。重复键插入被忽略。

**主要 API**：

```cpp
template <typename T, typename Cmp = std::less<T>>
class AVLTree {
    void insert(const T& value);
    bool contains(const T& value) const;
    void erase(const T& value);
    std::size_t size() const;
    bool empty() const;
    template <typename Func>
    void inorder(Func f) const;       // 中序遍历，升序输出
};
```

**复杂度**：插入/删除/查找 O(log n)；中序遍历 O(n)；空间 O(n)。

**使用场景**：
- 需要始终保证 O(log n) 的平衡 BST，如动态有序集合
- 要求中序遍历即有序序列（如按序输出、求第 k 小）

**使用示例**：

```cpp
AVLTree<int> t;
t.insert(10); t.insert(5); t.insert(15); t.insert(3);
t.contains(5);                    // true
t.erase(5);
t.inorder([](int v) { std::cout << v << ' '; });  // 升序：3 10 15
```

---

### `ds/b_tree.h` — B 树

**用途**：多路平衡搜索树，节点可容纳多个键，解决磁盘/内存块级访问场景下"树高过高导致 IO 次数过多"的问题（数据库与文件系统索引的经典结构）。

**原理**：阶数 `M` 的每个节点最多 `M-1` 个键、`M` 个孩子，最小度数 `T = ceil(M/2)`；插入时自底向上分裂满节点，保持所有叶子同层。本实现为简化版：仅支持 `int` 键，提供插入与查找，无删除。

**主要 API**：

```cpp
template <int M = 5>
class BTree {
    BTree();
    bool search(int key) const;
    void insert(int key);
};
```

**复杂度**：查找/插入 O(log_M n)（即 O(log n)，log 底数为 M）；空间 O(n)。

**使用场景**：
- 理解多路平衡树与磁盘索引的分裂/合并机制
- 大规模有序数据存储（如内存中模拟数据库索引）

**使用示例**：

```cpp
BTree<3> bt;                 // 阶数为 3 的 B 树
bt.insert(10); bt.insert(20); bt.insert(5);
bt.search(10);               // true
bt.search(99);               // false
```

---

### `ds/binary_heap.h` — 二叉堆

**用途**：完全二叉树形式的堆结构，实现可 O(1) 取最值、O(log n) 插入/删除的优先队列内核，并支持 O(n) 建堆。

**原理**：用 `DynamicArray` 存完全二叉树（父节点下标 i，左右孩子 2i+1、2i+2），`sift_up`/`sift_down` 维护堆序。`Cmp` 控制堆序：`std::less` → 大顶堆，`std::greater` → 小顶堆。

**主要 API**：

```cpp
template <typename T, typename Cmp = std::less<T>>
class BinaryHeap {
    BinaryHeap();
    explicit BinaryHeap(const Cmp& cmp);
    explicit BinaryHeap(const DynamicArray<T>& arr, const Cmp& cmp = Cmp());  // O(n) 建堆
    void push(const T& value);
    void pop();                  // 空堆抛 std::out_of_range
    const T& top() const;
    std::size_t size() const;
    bool empty() const;
};
```

**复杂度**：push / pop O(log n)；top O(1)；由数组建堆 O(n)；空间 O(n)。

**使用场景**：
- 需要"快速取最值 + 动态插入"的场合，如求 Top-K、合并有序序列
- 作为 Dijkstra、Prim 等图算法中的优先队列

**使用示例**：

```cpp
BinaryHeap<int> heap;              // 默认大顶堆
heap.push(3); heap.push(1); heap.push(2);
heap.top();                        // 3
heap.pop();

BinaryHeap<int, std::greater<int>> min_heap;  // 小顶堆
min_heap.push(3); min_heap.top();             // 3 为堆顶（最小）
```

---

### `ds/binary_tree.h` — 二叉搜索树

**用途**：最基础的 BST 实现（不含重复键），提供插入、查找、删除以及四种遍历，是理解树结构与递归/迭代遍历的入门结构。

**原理**：节点 `BinaryTreeNode<T>` 含左右孩子指针；按比较器 `Cmp` 走左/右子树。遍历全部采用迭代实现（`inorder`/`preorder`/`postorder` 用栈，`level_order` 用队列）。删除采用"中序后继"替换的双孩子处理。注意 `erase` 为简化实现，恒返回 `true`。

**主要 API**：

```cpp
template <typename T>
struct BinaryTreeNode {
    T data;
    BinaryTreeNode* left;
    BinaryTreeNode* right;
};

template <typename T, typename Cmp = std::less<T>>
class BinarySearchTree {
    bool insert(const T& value);      // 已存在返回 false
    bool contains(const T& value) const;
    bool erase(const T& value);
    Node* find_min() const;
    Node* find_max() const;
    template <typename Func> void inorder(Func f) const;     // 迭代实现
    template <typename Func> void preorder(Func f) const;
    template <typename Func> void postorder(Func f) const;
    template <typename Func> void level_order(Func f) const;
    Node* root() const;
    std::size_t size() const;
    bool empty() const;
};
```

**复杂度**：查找/插入/删除平均 O(log n)，最坏 O(n)（有序插入时退化为链表，无自平衡）；遍历 O(n)；空间 O(n)。

**使用场景**：
- 学习 BST 机制与三种深度优先遍历的迭代写法
- 数据近乎随机分布、不需要平衡保证的简单有序集合

**使用示例**：

```cpp
BinarySearchTree<int> bst;
bst.insert(5); bst.insert(3); bst.insert(7);
bst.contains(3);               // true
bst.find_min()->data;          // 3
bst.level_order([](int v) { std::cout << v; });   // 层序：5 3 7
```

---

### `ds/bloom_filter.h` — 布隆过滤器

**用途**：概率型集合，用位数组 + 多个哈希函数判断元素"是否存在"，用于内存极省的大规模去重/存在性过滤（如黑名单、缓存穿透防护、爬虫 URL 去重）。

**原理**：插入时把 `HashCount` 个哈希位置 1；查询时只要有一位为 0 即判不存在，全为 1 才判存在。可能出现误报（false positive，本不存在的元素被判存在），但绝不漏报（已插入的元素一定判存在）。

**主要 API**：

```cpp
template <std::size_t Bits = 1024, int HashCount = 3>
class BloomFilter {
    void insert(const std::string& key);
    bool contains(const std::string& key) const;
    void clear();                  // 复位所有位
    std::size_t size() const;      // 当前置 1 的位数
};
```

**复杂度**：插入/查询 O(HashCount)，即常数 O(1)；空间 O(Bits) 位（编译期固定位数组）。

**使用场景**：
- 海量数据存在性预判，允许少量误报（如分布式系统缓存穿透防护）
- 用极小内存做"一定不在"的快速否定过滤

**使用示例**：

```cpp
BloomFilter<1000, 3> bf;
bf.insert("hello");
bf.contains("hello");     // true（已插入，绝不漏报）
bf.contains("world");     // 大概率 false，小概率误报 true
```

---

### `ds/dynamic_array.h` — 动态数组

**用途**：手写 std::vector 的简化版，解决定长数组无法动态扩容的问题，同时保证随机访问 O(1) 与末尾操作均摊 O(1)。

**原理**：内部持有 `T*` 数组与 `size_`/`capacity_`；容量不足时翻倍扩容（`ensure_capacity`，初始 4，翻倍，必要时直接扩到所需大小）并迁移元素。是本模块 Stack / PriorityQueue / BinaryHeap 等结构的底层容器。

**主要 API**：

```cpp
template <typename T>
class DynamicArray {
    DynamicArray();
    DynamicArray(std::initializer_list<T> init);
    DynamicArray(const DynamicArray& other);                 // 拷贝
    DynamicArray(DynamicArray&& other) noexcept;            // 移动
    void push_back(const T& value);
    void push_back(T&& value);
    void pop_back();                     // 空数组抛 std::out_of_range
    void insert(std::size_t index, const T& value);
    void erase(std::size_t index);
    void reserve(std::size_t new_capacity);
    void clear();
    T& operator[](std::size_t index);    // 无越界检查
    T& at(std::size_t index);            // 越界抛异常
    T& front(); T& back();
    T* data();
    std::size_t size() const;
    std::size_t capacity() const;
    bool empty() const;
    T* begin(); T* end();                // 支持范围 for
};
```

**复杂度**：push_back / pop_back 均摊 O(1)（翻倍扩容，每次扩容 O(n) 但次数对数级）；随机访问 O(1)；中间 insert / erase O(n)；空间 O(n)。

**使用场景**：
- 需要连续内存 + 随机访问 + 动态增长的通用容器
- 作为其他数据结构的底层存储

**使用示例**：

```cpp
DynamicArray<int> arr{1, 2, 3};
arr.push_back(4);            // 1 2 3 4
arr.insert(1, 9);            // 1 9 2 3 4
arr.erase(0);                // 9 2 3 4
arr.at(1);                   // 2（带越界检查）
for (int v : arr) { /* 范围 for 可用 */ }
```

---

### `ds/fenwick_tree.h` — 树状数组（Fenwick Tree / BIT）

**用途**：支持"单点修改 + 前缀和/区间和查询"的高效数据结构，解决多次点更新与区间求和的动态问题，常用于竞赛中的前缀统计。

**原理**：数组下标按 `lowbit(i) = i & (~i + 1)` 组织覆盖区间，每个位置存一段区间的和；更新时沿 `i += lowbit(i)` 向上传播，查询时沿 `i -= lowbit(i)` 累加。由数组可 O(n) 建树。

**主要 API**：

```cpp
template <typename T>
class FenwickTree {
    explicit FenwickTree(std::size_t n);                  // 全 0 建树
    explicit FenwickTree(const std::vector<T>& arr);      // 由数组 O(n) 建树
    void add(std::size_t idx, const T& delta);            // 位置 idx（0-indexed）加 delta
    T sum(std::size_t idx) const;                         // 前缀和 sum[0..idx]
    T range_sum(std::size_t l, std::size_t r) const;      // 区间和 sum[l..r]
    std::size_t size() const;
};
```

**复杂度**：单点加、前缀和、区间和均 O(log n)；建树 O(n)；空间 O(n)。

**使用场景**：
- 动态数组的区间求和（配合差分可做区间加、单点查）
- 求逆序对（边插入边查前缀和）、维护前缀频次等竞赛题目

**使用示例**：

```cpp
FenwickTree<int> bit(std::vector<int>{1, 3, 5, 7});
bit.add(1, 2);               // arr[1] 变为 5
bit.sum(2);                  // 前缀和 arr[0..2] = 1 + 5 + 5 = 11
bit.range_sum(1, 3);         // arr[1..3] = 5 + 5 + 7 = 17
```

---

### `ds/fibonacci_heap.h` — 斐波那契堆

**用途**：以均摊 O(1) 的插入代价著称的堆结构，适合插入极多、删除较少且对 push 性能敏感的场合（如 Dijkstra / Prim 等需要大量 push 的图算法；配合 decrease-key 可进一步优化）。

**原理**：由多棵无序二项树构成的"松弛堆"：push 只把新节点并入根链表（O(1)），pop 才做 `consolidate` 合并同度数树（均摊 O(log n)）。根链表为环形双向链表，节点含 `degree` 与 `marked` 标记（本实现为最小堆语义，未提供 decrease-key）。

**主要 API**：

```cpp
template <typename T, typename Cmp = std::less<T>>
class FibonacciHeap {
    void push(const T& value);
    const T& top() const;         // 空堆抛 std::out_of_range
    void pop();
    std::size_t size() const;
    bool empty() const;
};
```

**复杂度**：push 均摊 O(1)；top O(1)；pop 均摊 O(log n)；空间 O(n)（按实现注释）。

**使用场景**：
- push 操作远多于 pop 的场景（大量元素进入堆、只有少数被取走）
- 理解"懒删除 + 合并分摊"的堆优化思想

**使用示例**：

```cpp
FibonacciHeap<int> fh;
fh.push(5); fh.push(3); fh.push(8);
fh.top();        // 3（最小堆堆顶）
fh.pop();
fh.top();        // 5
```

---

### `ds/forward_star.h` — 链式前向星

**用途**：用紧凑静态数组存储图的邻接关系，解决 vector 邻接表内存碎片/缓存局部性差的问题，是竞赛中最常用的高效图存储（尤其带权图）。

**原理**：`head_[u]` 指向 u 的第一条出边编号，`next_[i]` 指向与边 i 同起点的下一条边，`to_[i]`/`weight_[i]` 存终点与边权。`add_edge` 头插法 O(1)；`neighbors(u)` 按插入顺序返回全部出边（内部先逆序再反转还原）。

**主要 API**：

```cpp
class ForwardStar {
    ForwardStar(std::size_t vertices, std::size_t max_edges);
    void add_edge(std::size_t u, std::size_t v, int w = 1);   // 头插法 O(1)
    std::vector<std::pair<std::size_t, int>> neighbors(std::size_t u) const;  // 按插入顺序
    std::size_t edge_count() const;
};
```

**复杂度**：加边 O(1)；枚举 u 的出边 O(deg(u))；空间 O(V + E)（预先 reserve 边容量）。

**使用场景**：
- 大规模带权图的存储与遍历（Dijkstra、SPFA、网络流等）
- 需要缓存友好、常数小的邻接表场景

**使用示例**：

```cpp
ForwardStar fs(4, 10);
fs.add_edge(0, 1, 5);
fs.add_edge(0, 2, 3);
for (auto [v, w] : fs.neighbors(0)) {  // 依次 (1,5), (2,3)，按插入顺序
    /* 处理出边 */
}
fs.edge_count();   // 2
```

---

### `ds/graph.h` — 图的邻接表

**用途**：通用图容器，用 vector 邻接表存储有向/无向图（顶点 0..V-1），并内置 DFS、BFS 遍历与 Kahn 拓扑排序。

**原理**：`adj_[u]` 存 u 的所有邻居；无向图 `add_edge` 时对称插入。DFS 用显式栈（反向压栈以匹配递归序），BFS 用队列，拓扑排序统计入度后反复取出入度为 0 的顶点，存在环时返回空 vector。

**主要 API**：

```cpp
class Graph {
    explicit Graph(std::size_t vertices, bool directed = false);
    void add_edge(std::size_t u, std::size_t v);
    template <typename Func>
    void dfs(std::size_t start, Func f) const;      // 深度优先，每访问一顶点回调 f
    template <typename Func>
    void bfs(std::size_t start, Func f) const;      // 广度优先
    std::vector<std::size_t> topological_sort() const;  // Kahn 算法，有环返回空
    std::size_t vertices() const;
    bool is_directed() const;
    const std::vector<std::size_t>& neighbors(std::size_t u) const;
};
```

**复杂度**：DFS / BFS O(V + E)；拓扑排序 O(V + E)；空间 O(V + E)。

**使用场景**：
- 图的存储与遍历基础题（连通分量、可达性）
- 有向无环图的拓扑排序（任务依赖、课程表问题）

**使用示例**：

```cpp
Graph g(5, true);                  // 有向图
g.add_edge(0, 1); g.add_edge(0, 2);
g.add_edge(1, 3); g.add_edge(2, 3);
auto order = g.topological_sort(); // {0, 1, 2, 3} 一类合法拓扑序
g.bfs(0, [](std::size_t u) { /* 访问顶点 u */ });
```

---

### `ds/hash_table.h` — 哈希表

**用途**：键值对容器，解决"按 key 快速定位 value"问题，平均 O(1) 的插入/删除/查找，是本模块 LRU/LFU 缓存的基石。

**原理**：拉链法（separate chaining）：`bucket_count` 个桶，每个桶存 `std::list<std::pair<K, V>>`；`hash(key) % bucket_count` 定位桶。负载因子超过 0.75 时桶数翻倍 rehash。`insert` 遇相同 key 更新值，`operator[]` 在 key 不存在时插入默认值。

**主要 API**：

```cpp
template <typename K, typename V, typename Hash = std::hash<K>>
class HashTable {
    explicit HashTable(std::size_t bucket_count = 16);
    void insert(const K& key, const V& value);   // 已存在则更新
    bool erase(const K& key);
    V* find(const K& key);                       // 未命中返回 nullptr
    const V* find(const K& key) const;
    bool contains(const K& key) const;
    V& operator[](const K& key);                 // 不存在时插入 V{}
    std::size_t size() const;
    bool empty() const;
    std::size_t bucket_count() const;
};
```

**复杂度**：插入/删除/查找平均 O(1)（负载因子 ≤ 0.75 时），最坏 O(n)；rehash 均摊 O(1)/元素；空间 O(n)。

**使用场景**：
- 键值映射、去重、频次统计
- 缓存、索引等一切需要 O(1) 查找的场景

**使用示例**：

```cpp
HashTable<std::string, int> ht;
ht.insert("apple", 3);
ht["banana"] = 5;
*ht.find("apple");        // 3
ht.contains("banana");    // true
ht.erase("apple");
```

---

### `ds/huffman.h` — 哈夫曼编码

**用途**：根据字符频率生成最优前缀码，实现无歧义的文本压缩（高频字符短码、低频字符长码）。

**原理**：统计文本中字符频率，用小顶堆反复合并两个最小频率节点构建哈夫曼树；左子树记 '0'、右子树记 '1' 得到编码表。前缀码性质保证解码无歧义。`decode` 处理了单字符特例（整串编码为单个字符）。

**主要 API**：

```cpp
class HuffmanCoding {
    void build(const std::string& text);             // 统计频率并建树、生成编码表
    std::string encode(const std::string& text) const;   // 编码为 '0'/'1' 串
    std::string decode(const std::string& bits) const;   // 解码还原文本
    const std::map<char, std::string>& codes() const;    // 字符 → 编码映射
};
```

**复杂度**：build O(n + k log k)（n 为文本长度，k 为不同字符数）；encode / decode O(输出长度)；空间 O(k)。

**使用场景**：
- 文本压缩（如 ZIP 中 DEFLATE 的前置步骤）
- 学习贪心策略与最优前缀码的构造

**使用示例**：

```cpp
HuffmanCoding hc;
hc.build("aababcabcd");
auto bits = hc.encode("aababcabcd");
auto text = hc.decode(bits);    // 还原为 "aababcabcd"
auto& table = hc.codes();       // 各字符的最优前缀码
```

---

### `ds/lfu_cache.h` — LFU 缓存

**用途**：最不经常使用（Least Frequently Used）缓存：容量满时淘汰"使用频率最低"的项，同频率项按 LRU（最久未用）淘汰。

**原理**：`freq_map_`（频率 → 该频率的 Entry 双向链表，链表头为最近使用）+ `key_map_`（key → 迭代器）实现 O(1) get/put；`min_freq_` 记录当前最小频率用于快速定位淘汰项。get 命中后频率 +1 并移入上一级链表。

**主要 API**：

```cpp
template <typename K, typename V>
class LFUCache {
    explicit LFUCache(std::size_t capacity);   // capacity 为 0 抛 std::invalid_argument
    V* get(const K& key);                      // 命中返回 value 指针（并提升频率），未命中返回 nullptr
    void put(const K& key, const V& value);    // 满时淘汰最不常用项
    std::size_t size() const;
    std::size_t capacity() const;
};
```

**复杂度**：get / put 均摊 O(1)；空间 O(capacity)。

**使用场景**：
- 访问频次比访问新鲜度更能反映"接下来会用"的缓存场景（如热点数据缓存）
- 数据库缓存淘汰策略（Redis 的 allkeys-lfu 等）

**使用示例**：

```cpp
LFUCache<int, int> c(2);
c.put(1, 1); c.put(2, 2);
c.get(1);                  // key=1 频率 1→2
c.put(3, 3);               // 满：淘汰频率最低（为 1）的 key=2
c.get(2);                  // nullptr
c.get(1);                  // 1
```

---

### `ds/linked_list.h` — 链表（单链表 / 双向链表）

**用途**：提供 `SinglyLinkedList` 与 `DoublyLinkedList` 两种链式结构，解决频繁头部/尾部插入删除（O(1)）且不搬移元素的场景，双向链表额外支持 O(1) 尾部删除与双向遍历。

**原理**：节点以指针链接，`head_`/`tail_` 维护首尾。单链表带尾指针使 push_back 为 O(1)，支持 `insert_after`/`erase_after`（需先 find 定位）与原地 `reverse`；双向链表支持 `insert_before`/`insert_after`/`erase(node)` 任意位置 O(1) 增删。

**主要 API**：

```cpp
template <typename T>
class SinglyLinkedList {
    void push_front(const T& value);  void push_back(const T& value);
    void pop_front();
    void insert_after(Node* prev, const T& value);
    void erase_after(Node* prev);
    Node* find(const T& value);
    void reverse();                   // 原地反转
    void clear();
    T& front();
    Node* head();  Node* tail();
    std::size_t size() const;  bool empty() const;
};

template <typename T>
class DoublyLinkedList {
    void push_front(const T& value);  void push_back(const T& value);
    void pop_front();  void pop_back();
    void insert_before(Node* node, const T& value);
    void insert_after(Node* node, const T& value);
    void erase(Node* node);
    void clear();
    T& front();  T& back();
    Node* head();  Node* tail();
    std::size_t size() const;  bool empty() const;
};
```

**复杂度**：头/尾操作 O(1)；已知位置（节点指针）插入/删除 O(1)；按值查找 O(n)；空间 O(n)。

**使用场景**：
- 需要大量头尾增删的队列/栈底层
- 已知节点位置时 O(1) 增删（如 LRU 淘汰、哈希表桶）

**使用示例**：

```cpp
SinglyLinkedList<int> sl{1, 2, 3};
sl.push_front(0);            // 0 1 2 3
sl.reverse();                // 3 2 1 0
sl.front();                  // 3

DoublyLinkedList<int> dl;
dl.push_back(1);  dl.push_front(0);   // 0 1
dl.pop_back();                         // 0
```

---

### `ds/lru_cache.h` — LRU 缓存

**用途**：最近最少使用（Least Recently Used）缓存：容量满时淘汰"最久未被访问"的项，是操作系统页面置换与常见缓存框架的经典策略。

**原理**：哈希表（key → 迭代器）+ 双向链表（`std::list<pair<K,V>>`）组合：链表头为最近使用、链表尾为最久未用；get/put 命中时 `splice` 移到头部 O(1)，淘汰时弹出尾部 O(1)。

**主要 API**：

```cpp
template <typename K, typename V>
class LRUCache {
    explicit LRUCache(std::size_t capacity);   // capacity 为 0 抛 std::invalid_argument
    V* get(const K& key);                      // 命中返回 value 指针并移到最近使用，未命中返回 nullptr
    void put(const K& key, const V& value);
    bool contains(const K& key) const;
    std::size_t size() const;
    std::size_t capacity() const;
    bool empty() const;
};
```

**复杂度**：get / put O(1)；空间 O(capacity)。

**使用场景**：
- 通用缓存淘汰（浏览器、CPU 缓存、本地缓存库）
- 竞赛中"设计 LRU Cache"类题目

**使用示例**：

```cpp
LRUCache<int, std::string> cache(3);
cache.put(1, "one");  cache.put(2, "two");  cache.put(3, "three");
cache.get(1);                     // "one"，key=1 变为最近使用
cache.put(4, "four");             // 满：淘汰最久未用的 key=2
cache.get(2);                     // nullptr
cache.contains(1);                // true
```

---

### `ds/priority_queue.h` — 优先队列

**用途**：二叉堆实现的优先队列，支持 O(log n) 插入与取走最值，默认大顶堆，是 Dijkstra、堆排序等算法的基础工具。

**原理**：与 `BinaryHeap` 同构的 sift_up / sift_down 实现，底层容器为 `DynamicArray`。模板参数 `Cmp` 控制堆序：`std::less<T>` → 大顶堆，`std::greater<T>` → 小顶堆。

**主要 API**：

```cpp
template <typename T, typename Cmp = std::less<T>>
class PriorityQueue {
    PriorityQueue();
    explicit PriorityQueue(const Cmp& cmp);
    void push(const T& value);
    void push(T&& value);
    void pop();                       // 空队列抛 std::out_of_range
    const T& top() const;
    std::size_t size() const;
    bool empty() const;
};
```

**复杂度**：push / pop O(log n)；top O(1)；空间 O(n)。

**使用场景**：
- 动态维护极值（数据流中的最大/最小值）
- Dijkstra 最短路、Prim 最小生成树、堆排序

**使用示例**：

```cpp
PriorityQueue<int> pq;               // 默认大顶堆
pq.push(3); pq.push(1); pq.push(2);
pq.top();                            // 3
pq.pop();

PriorityQueue<int, std::greater<int>> min_pq;  // 小顶堆
min_pq.push(3); min_pq.top();                  // 3（最小）
```

---

### `ds/queue.h` — 队列 / 双端队列（Deque）

**用途**：提供 FIFO 的 `Queue` 与两端均可增删的 `Deque`（循环缓冲实现），解决 BFS、滑动窗口等需要顺序处理或双端访问的问题。

**原理**：`Queue` 基于 `DoublyLinkedList`（push_back + pop_front）。`Deque` 用环形缓冲数组：`head_`/`tail_` 游标取模移动，容量不足时翻倍扩容并重排到 0 起始；`operator[]` 按队首偏移随机访问。

**主要 API**：

```cpp
template <typename T>
class Queue {
    void push(const T& value);  void push(T&& value);
    void pop();                 // 空队列抛 std::out_of_range
    T& front();  T& back();
    std::size_t size() const;  bool empty() const;
};

template <typename T>
class Deque {
    void push_front(const T& value);  void push_back(const T& value);
    void pop_front();  void pop_back();
    T& front();  T& back();
    T& operator[](std::size_t i);     // i=0 为队首
    std::size_t size() const;  bool empty() const;
};
```

**复杂度**：Queue 的 push / pop O(1)；Deque 两端 push / pop 均摊 O(1)（扩容 O(n)）、随机访问 O(1)；空间 O(n)。

**使用场景**：
- BFS 层序遍历、消息队列
- 双端访问场景（如单调队列求滑动窗口最值）

**使用示例**：

```cpp
Queue<int> q;
q.push(1); q.push(2);
q.front();       // 1
q.pop();         // 出队 1

Deque<int> dq;
dq.push_back(2); dq.push_front(1);   // 1 2
dq[0];           // 1
dq.back();       // 2
dq.pop_front();  // 2
```

---

### `ds/red_black_tree.h` — 红黑树

**用途**：自平衡 BST 的另一种经典实现（C++ std::map 内部结构），通过红黑染色规则保证插入/查找 O(log n)。本实现只提供插入与查找（删除较复杂，未实现）。

**原理**：每个节点着色（红/黑），满足五条红黑性质（根黑、红节点子必黑、任一路径黑节点数相同等）；插入后按叔节点颜色分情况做变色与左/右旋转修复（`insert_fixup`），保证任意根到叶路径长度差不超过 2 倍。

**主要 API**：

```cpp
template <typename T, typename Cmp = std::less<T>>
class RedBlackTree {
    bool insert(const T& value);      // 重复键返回 false
    bool contains(const T& value) const;
    template <typename Func>
    void inorder(Func f) const;       // 中序遍历（递归实现）
    std::size_t size() const;
    bool empty() const;
};
```

**复杂度**：插入/查找 O(log n)；中序遍历 O(n)；空间 O(n)。

**使用场景**：
- 需要严格 O(log n) 且偏爱红黑树场景（如实现有序关联容器）
- 学习"变色 + 旋转"修复插入的平衡算法

**使用示例**：

```cpp
RedBlackTree<int> rbt;
rbt.insert(7); rbt.insert(3); rbt.insert(18);
rbt.contains(3);       // true
rbt.inorder([](int v) { std::cout << v << ' '; });   // 3 7 18
rbt.insert(3);         // false，重复键拒绝
```

---

### `ds/segment_tree.h` — 线段树

**用途**：区间查询 + 单点更新的经典树形结构，支持 O(log n) 的区间求和与单点修改，本实现为求和线段树（注释说明可扩展为 min/max/gcd 等）。

**原理**：用大小为 4n 的数组存完全二叉树：节点 `node` 覆盖区间 `[tl, tr)`，叶子存单点值，内部节点存两孩子之和。`update` 递归下推到叶子后回溯重算；`query` 按区间覆盖情况合并左右子区间的结果，区间采用左闭右开 `[l, r)`。

**主要 API**：

```cpp
template <typename T>
class SegmentTree {
    SegmentTree();
    explicit SegmentTree(const std::vector<T>& arr);   // 建树
    void update(std::size_t idx, const T& value);      // 单点赋值为 value
    T query(std::size_t l, std::size_t r) const;       // 区间和 [l, r)（左闭右开）
    std::size_t size() const;
};
```

**复杂度**：建树 O(n)；单点更新 O(log n)；区间查询 O(log n)；空间 O(4n)。

**使用场景**：
- 数组在单点修改与区间求和间交替的"动态静态区间和"问题
- 扩展为区间最值、区间 gcd 等（需自行改合并操作）

**使用示例**：

```cpp
SegmentTree<int> st({1, 3, 5, 7, 9});
st.query(1, 3);          // 15（arr[1..3) = 3 + 5 + 7）
st.update(2, 10);        // arr[2] = 10
st.query(1, 3);          // 20（3 + 10 + 7）
```

---

### `ds/skip_list.h` — 跳表

**用途**：基于多层链表的概率型有序结构，以期望 O(log n) 实现插入/查找/删除，无需旋转即可保持平衡，是 Redis 有序集合 ZSET 的底层结构。

**原理**：节点按随机层数（`random_level`：每次 1/2 概率升层，最大 16 层）插入多层链表中；查找从最高层开始"逐层下降"，跳过大量中间节点。随机化保证期望树高 O(log n)。

**主要 API**：

```cpp
template <typename T>
class SkipList {
    bool insert(const T& value);     // 已存在返回 false
    bool search(const T& value) const;
    bool erase(const T& value);
    std::size_t size() const;
    bool empty() const;
};
```

**复杂度**：插入/查找/删除期望 O(log n)（最坏 O(n)）；空间 O(n)（按实现，MAX_LEVEL = 16，随机种子固定为 42）。

**使用场景**：
- 需要有序集合 + 范围检索语义的场合（Redis ZSET 同类问题）
- 相比平衡树编码更简单、且天然支持并发改造的有序结构

**使用示例**：

```cpp
SkipList<int> sl;
sl.insert(3); sl.insert(1); sl.insert(2);
sl.search(2);        // true
sl.search(5);        // false
sl.erase(3);
sl.size();           // 2
```

---

### `ds/stack.h` — 栈 / 单调栈

**用途**：提供 LIFO 的 `Stack` 与维护单调性的 `MonotonicStack`（如求"下一个更大元素"），是括号匹配、表达式求值、直方图最大矩形等问题的基石。

**原理**：`Stack` 基于 `DynamicArray`，push/pop 均走尾部。`MonotonicStack` 在 push 时先把所有违反单调性的栈顶元素弹出（`Cmp = std::less` → 自底向上严格递增，`std::greater` → 严格递减），并返回弹出个数。

**主要 API**：

```cpp
template <typename T>
class Stack {
    void push(const T& value);  void push(T&& value);
    void pop();                 // 空栈抛 std::out_of_range
    T& top();  const T& top() const;
    std::size_t size() const;  bool empty() const;
};

template <typename T, typename Cmp = std::less<T>>
class MonotonicStack {
    std::size_t push(const T& value);  // 返回为维持单调性弹出的元素个数
    void pop();
    T& top();
    std::size_t size() const;  bool empty() const;
};
```

**复杂度**：所有操作 O(1)（单调栈每个元素至多入栈/出栈一次，整体均摊 O(n)）；空间 O(n)。

**使用场景**：
- DFS 显式栈、括号匹配、逆波兰表达式求值
- 单调栈求"下一个更大/更小元素"、最大矩形面积等经典题

**使用示例**：

```cpp
Stack<int> s;
s.push(1); s.push(2);
s.top();       // 2
s.pop();

MonotonicStack<int> ms;        // 严格递增（默认 std::less）
ms.push(1); ms.push(3);
ms.push(2);                    // 弹出 3（返回 1），栈变为 1 2
```

---

### `ds/trie.h` — 字典树（Trie）

**用途**：面向字符串前缀的多叉树，支持 O(len) 的插入、精确查找与前缀匹配，是自动补全、词频统计、敏感词过滤的基础。

**原理**：26 叉树（仅小写字母），每个节点 `children[26]` 指向下一字符，`is_end` 标记单词结束；从根沿字符依次下走即可完成插入与查询，共享公共前缀。

**主要 API**：

```cpp
class Trie {
    void insert(const std::string& word);
    bool search(const std::string& word) const;      // 精确匹配（须为完整单词）
    bool starts_with(const std::string& prefix) const;  // 前缀匹配
};
```

**复杂度**：insert / search / starts_with 均为 O(len)；空间 O(字符总数 × 26)（按实现，小写字母 26 叉）。

**使用场景**：
- 大量字符串的公共前缀统计、自动补全/拼写检查
- 词频统计、基于前缀的检索类竞赛题

**使用示例**：

```cpp
Trie trie;
trie.insert("hello");
trie.search("hello");        // true
trie.starts_with("hel");     // true
trie.search("hel");          // false（"hel" 不是完整单词）
```

---

### `ds/union_find.h` — 并查集（Union-Find / DSU）

**用途**：维护不相交集合的"合并 + 查询连通性"问题，如判断两点是否连通、统计连通分量数、Kruskal 最小生成树的边去重。

**原理**：每个集合是一棵以代表元为根的树（`parent_` 数组）；`find` 递归带路径压缩，`unite` 按秩（`rank_`）合并，小树挂到大树下。两者结合使单次操作均摊 O(α(n))（反阿克曼函数，可视作常数）。

**主要 API**：

```cpp
class UnionFind {
    explicit UnionFind(std::size_t n);        // 0..n-1 各自成集合
    std::size_t find(std::size_t x);          // 路径压缩
    void unite(std::size_t x, std::size_t y); // 按秩合并
    bool connected(std::size_t x, std::size_t y);
    std::size_t count() const;                // 连通分量个数
    std::size_t size() const;                 // 元素总数
};
```

**复杂度**：find / unite / connected 均摊 O(α(n))；空间 O(n)。

**使用场景**：
- 图的连通性判定、动态加边后查询两点连通
- Kruskal 最小生成树、冗余连接、朋友圈等经典题目

**使用示例**：

```cpp
UnionFind uf(5);
uf.unite(0, 2);
uf.unite(2, 4);
uf.connected(0, 4);      // true
uf.connected(0, 1);      // false
uf.count();              // 3（{0,2,4}、{1}、{3}）
```
