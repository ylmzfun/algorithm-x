# 进阶算法（advanced）

本目录（`include/algorithm_x/advanced/`）收录算法进阶与数据结构进阶内容：摊还分析、
CDQ 分治、计算复杂性理论（P/NP）、逆序对计数、Link-Cut Tree 动态树、莫队算法、
在线算法与竞争分析、可持久化线段树、RMQ/LCA（Sparse Table 与倍增法）以及树套树/
分块。多为经典 OI/ACM 结构，部分为教学简化实现（如 cdq.h 为朴素版）。共 10 个头文件，
以下为 10 个条目。

---

### `advanced/amortized.h` — 摊还分析（动态数组扩容）

**用途**：解释"动态数组 push_back 单次最坏 O(n)、但 n 次总开销只有 O(n)"这一看似矛盾的现象，引出均摊分析这一复杂度分析工具。

**原理**：当容量不足时按倍增策略扩容（容量 ×2），扩容那次的开销是复制全部已有元素，但扩容不频繁——总扩容开销为 O(n)（各次扩容复制量 1+2+4+…+n ≈ 2n）。把总开销摊到每次操作上，均摊代价为 O(1)。本实现逐个模拟每次 push_back 的实际代价并返回代价序列，`amortized_average` 计算平均代价验证均摊结论。

**主要 API**：

```cpp
// 模拟 n 次 push_back 每次的实际代价（扩容时 = 复制元素数 + 1，否则 = 1）。
inline std::vector<double> amortized_push_cost(std::size_t n);
// 均摊代价：总代价 / n。
inline double amortized_average(std::size_t n);
```

**复杂度**：时间 O(n)（模拟 n 次操作）/ 空间 O(n)（返回代价数组）。均摊结论：n 次 push_back 总 O(n)、均摊 O(1)。

**使用场景**：
- 理解均摊分析与"平摊"的直观含义
- 对比最坏复杂度与均摊复杂度的差异（如 std::vector、std::deque）
- 学习二进制计数、势能法之前的入门示例

**使用示例**：

```cpp
auto costs = amortized_push_cost(100);   // 扩容时 cost 突增（如 64.0），平时为 1.0
double avg = amortized_average(100);     // 远小于 100，接近常数
```

---

### `advanced/cdq.h` — CDQ 分治（二维矩形计数）

**用途**：离线统计平面上有多少个点落在给定的矩形查询内（二维偏序计数问题）。

**原理**：CDQ 分治的核心思想是把"点-矩形包含"这类偏序关系转化为"点 (x,y) 的 y 维贡献在合并阶段用排序 + 数据结构统计"。标准做法是把矩形查询拆成前缀查询，按 x 排序后在分治合并中统计跨区间的贡献，复杂度 O((n+m) log n)。**注意：本实现为教学简化版，直接朴素双层循环 O(n·m) 求解，未体现 CDQ 的分治过程**，仅用于验证问题定义与结果正确性。

**主要 API**：

```cpp
struct CDQPoint { int x, y; };

struct CDQQuery {
    int x1, y1, x2, y2;        // 矩形（闭区间）
    std::size_t idx;           // 输出下标
};

// 返回每个矩形内的点数（result[query.idx] = 点数）。
inline std::vector<int> cdq_rect_count(
    const std::vector<CDQPoint>& points,
    std::vector<CDQQuery> queries);
```

**复杂度**：时间 O(n·m)（本实现朴素版；标准 CDQ 分治为 O((n+m) log n)）/ 空间 O(m)。

**使用场景**：
- 理解二维偏序 / 矩形计数问题
- 学习 CDQ 分治思想（三维偏序、离线动态问题）的前置
- 几何查询结果正确性的对照验证

**使用示例**：

```cpp
std::vector<CDQPoint> pts = {{0,0}, {2,2}, {5,5}};
std::vector<CDQQuery> queries = {{0, 0, 3, 3, 0}};   // 矩形 [0,3]×[0,3]
auto ans = cdq_rect_count(pts, queries);
// ans[0] == 2（(0,0) 与 (2,2) 落在矩形内）
```

---

### `advanced/complexity.h` — 计算复杂性理论（P / NP / NP 完全 / NP 困难）

**用途**：以判定问题为对象，用可运行的小例子直观呈现 P、NP、归约、NP 完全与 NP 困难的定义，帮助理解"P 是否等于 NP"这一核心未解问题。

**概念讲解**：
- **P**：存在多项式时间（O(n^k)）判定算法的问题类。
- **NP**：存在多项式时间"验证器"的问题类——给定实例外加候选解（证书），能在多项式时间内判断其是否合法；显然 P ⊆ NP。
- **归约（A ≤p B）**：存在多项式时间变换 f，使 "x 属于 A" ⇔ "f(x) 属于 B"，即 B 的求解器可求解 A，B 至少与 A 一样难。
- **NP 完全**：属于 NP 且所有 NP 问题都能多项式归约到它，是 NP 中最难的一批；任一 NP 完全问题有多项式算法即得 P = NP。
- **NP 困难**：所有 NP 问题都能多项式归约到它，但本身不要求属于 NP（可为优化问题）；NP 完全 ⊆ NP 困难。
- 关系：P ⊆ NP，NP 完全 = NP 中最难者，NP 困难 ⊇ NP 完全。本头文件只给出教学示例（子集和的指数级判定、多项式验证器、TSP 暴力优化），不提供严格归约证明。

**示例函数**（真实签名）：

```cpp
// 子集和判定问题：能否选出若干个数使和恰为 target。O(2^n) 枚举所有子集。
inline bool subset_sum_brute(const std::vector<int>& nums, int target);
// 子集和的"验证器"：给定候选下标集 indices，验证下标合法、不重复且和为 target。
inline bool subset_sum_verify(const std::vector<int>& nums, int target,
                              const std::vector<int>& indices);
// 旅行商（TSP）NP 困难优化问题：O(n!) 枚举全排列求最小回路（固定从城市 0 出发）。
inline int tsp_brute_force(const std::vector<std::vector<int>>& dist);
```

**复杂度**：subset_sum_brute：时间 O(2^n)、空间 O(1)；subset_sum_verify：时间 O(|indices|)、空间 O(n)（去重数组）；tsp_brute_force：时间 O(n!)、空间 O(n)。三者均只适合极小数据（n ≤ 20 左右 / n ≤ 8）。

**使用场景**：
- 直观感受"指数级暴力"与"多项式验证器"的形态差异
- 理解 P、NP、NP 完全、NP 困难的定义边界
- 作为复杂度理论入门 / 面试复习材料

**使用示例**：

```cpp
std::vector<int> nums = {3, 34, 4, 12, 5, 2};
subset_sum_brute(nums, 9);         // true（4+5）
subset_sum_verify(nums, 9, {2, 4}); // true：下标合法、不重复、和为 9
std::vector<std::vector<int>> dist = {
    {0,10,15,20}, {10,0,35,25}, {15,35,0,30}, {20,25,30,0}};
tsp_brute_force(dist);             // 80：0->1->3->2->0
```

---

### `advanced/inversions.h` — 归并排序求逆序对

**用途**：统计数组中有多少对 (i, j) 满足 i < j 且 a[i] > a[j]（逆序对），这是衡量序列"乱序程度"与冒泡排序交换次数的经典指标。

**原理**：在归并排序的合并过程中，当右半数组的元素先于左半元素被取走时，说明左半剩余的所有元素都比它大，构成逆序对——一次统计 `left.size() - i` 个。归并本身排序正确性不变，逆序数在合并中累计，达到 O(n log n)。

**主要 API**：

```cpp
// 返回 arr 的逆序对数量（任意可比较元素类型，结果可能超过 32 位用 int64_t）。
template <typename T>
int64_t count_inversions(const std::vector<T>& arr);
```

**复杂度**：时间 O(n log n)（归并排序）/ 空间 O(n)（合并辅助数组）。

**使用场景**：
- 逆序对统计（冒泡排序交换次数、Kendall tau 距离）
- 学习"排序过程中顺带统计"的分治技巧
- 比朴素 O(n²) 枚举更快的通用解法

**使用示例**：

```cpp
std::vector<int> arr = {2, 3, 8, 6, 1};
count_inversions(arr);    // 5：{2,1},{3,1},{8,6},{8,1},{6,1}
```

---

### `advanced/link_cut_tree.h` — Link-Cut Tree（动态树）

**用途**：在森林（可动态加边、删边、换根的树集合）上 O(log n) 维护路径信息——本实现聚合"路径点权和"。

**原理**：把每棵树剖成"虚实链"，每条实链用一棵 Splay 维护（中序遍历恰为链上从上到下的顺序），虚链只保留父指针。`access(x)` 把树根到 x 的整条路径变为一条实链并令 x 为链根（一切操作的基础）；`makeroot(x)` 在 access 后打翻转懒标记完成换根；`link`/`cut` 借助 makeroot 与 access 拼接/断开路径；路径查询经 `makeroot(x)+access(y)` 后取 y 的子树聚合值。翻转只交换左右子树，不破坏"和"聚合。

**主要 API**：

```cpp
class LinkCutTree {
public:
    explicit LinkCutTree(int n);          // n 个孤立点，编号 0..n-1，点权初值 0
    void set_value(int x, long long v);   // 把 x 的点权设为 v
    long long value(int x) const;         // 查询 x 的点权
    bool connected(int x, int y) const;   // x 与 y 是否连通
    void makeroot(int x) const;           // 把 x 所在树的根换为 x
    int findroot(int x) const;            // 求 x 所在代表树的根
    void link(int x, int y);              // 连接 x、y（要求原本不连通）
    void cut(int x, int y);               // 断开边 x-y（要求直接相连）
    long long path_query(int x, int y);   // 查询 x 到 y 路径上的点权和
};
```

**复杂度**：单次操作均摊 O(log n)（access/makeroot/link/cut/path_query 等）；空间 O(n)。

**使用场景**：
- 动态森林上的路径查询（加边删边、换根）
- 动态树相关 OI 题（如动态 MST、动态连通性问题）
- 学习 Splay + 虚实链剖分的组合数据结构

**使用示例**：

```cpp
LinkCutTree lct(5);
lct.link(0, 1); lct.link(1, 2);            // 建链 0-1-2
for (int i = 0; i < 3; ++i) lct.set_value(i, i + 1);
lct.path_query(0, 2);                      // 6（1+2+3）
lct.makeroot(2);                           // 换根为 2
lct.cut(0, 1);                             // 断开边 0-1
lct.connected(0, 2);                       // false
```

---

### `advanced/mo_algorithm.h` — 莫队算法

**用途**：离线处理大量区间查询（本实现为"区间内不同元素个数"），把朴素 O(n) 每次的查询优化到整体接近 O((n+m)√n)。

**原理**：把查询按"左端点所在块"分块排序（块内再按右端点排序，奇偶块交替升/降序——奇偶优化减少指针来回），然后用双指针滑动窗口维护当前区间的答案：每次移动端点只做 O(1) 的 add/remove（维护频率数组与 distinct 计数）。端点移动总量被排序限制在 O((n+m)√n)，从而摊薄每个查询的开销。

**主要 API**：

```cpp
struct MoQuery { std::size_t l, r, idx; };   // 闭区间 [l, r] 与输出下标

// arr：原数组；queries：查询列表。返回每个查询区间内不同元素的个数。
inline std::vector<int> mo_algorithm(const std::vector<int>& arr,
                                     std::vector<MoQuery> queries);
```

**复杂度**：时间 O((n+m)√n)（排序 O(m log m)；端点总移动量 O(n√n + m√n)）/ 空间 O(n+m)。单次查询均摊约 O(√n)。

**使用场景**：
- 大量"区间统计"类离线查询（众数、不同元素数、出现次数等）
- 无法用线段树直接维护的复杂区间信息
- 学习离线排序 + 双指针滑窗的优化范式

**使用示例**：

```cpp
std::vector<int> arr = {1, 1, 2, 2, 3};
std::vector<MoQuery> qs = {{0, 1, 0}, {0, 4, 2}};
auto ans = mo_algorithm(arr, qs);
// ans[0] == 1（{1,1}），ans[1] == 3（{1,1,2,2,3}）
```

---

### `advanced/online_algorithm.h` — 在线算法与竞争分析

**用途**：研究"输入逐步到达、必须当下做不可撤销决定、无法预知未来"的在线问题，并用竞争比度量在线策略相对离线最优的损失。

**原理**：竞争分析比较在线代价与离线最优（能预知全部输入）代价：若任意输入下 cost_online ≤ c·cost_offline + d，则称 c-竞争比。滑雪板租赁问题：每天租 1 元或一次性买 buy_cost 元，最优确定型策略"先租到第 buy_cost-1 天、第 buy_cost 天买"的竞争比恰为 2。move-to-front（MTF）列表查找：找到元素后移到队首，是静态列表查找问题的 2k-1 竞争比算法。

**主要 API**：

```cpp
// 滑雪板租赁：返回策略总花费 = min(days, buy_cost-1) + (days >= buy_cost ? buy_cost : 0)。
inline int ski_rental_cost(int buy_cost, int days);
// MTF 在线列表查找：返回处理全部请求的总查找代价（代价 = 位置 + 1，找到即移到队首）。
inline int move_to_front_search(const std::vector<int>& requests, int list_size);
```

**复杂度**：ski_rental_cost：时间 O(1)、空间 O(1)。move_to_front_search：时间 O(|requests| · list_size)（线性查找 + 平移）、空间 O(list_size)。

**使用场景**：
- 学习在线算法与竞争比分析（ski rental、caching、MTF）
- 理解"不可撤销决定"与离线最优的差距量化
- 缓存替换、自组织列表等实际启发式的理论依据

**使用示例**：

```cpp
ski_rental_cost(7, 10);                 // 13：租 6 天 + 买 7（< 2*OPT）
move_to_front_search({1, 2, 1, 3}, 3);  // 8：代价序列 1+2+2+3
```

---

### `advanced/persistent.h` — 可持久化线段树（主席树）

**用途**：支持"回退到历史版本"查询的线段树——每次单点更新生成一个新版本，旧版本仍可查询（多版本区间求和）。

**原理**：更新时只复制从根到被改叶子的 O(log n) 个节点（路径复制，path copying），其余子树直接复用旧版本节点，新根加入版本数组。任意两个版本共享大量节点，查询沿对应版本的根下钻即可。总节点数 = 初始 O(n) + 每次更新 O(log n)。

**主要 API**：

```cpp
class PersistentSegmentTree {
public:
    explicit PersistentSegmentTree(const std::vector<int>& arr);  // 版本 0
    int update(int ver, std::size_t pos, int val);  // 基于版本 ver 单点赋值，返回新版本号
    int query(int ver, std::size_t l, std::size_t r) const;  // 版本 ver 的 [l, r) 区间和
    int version_count() const;                        // 版本总数
};
```

**复杂度**：构建 O(n)；update/query 时间 O(log n)、空间 O(log n)（每版本新节点）；总空间 O(n + m log n)（m 次更新）。

**使用场景**：
- 区间第 k 大（经典主席树应用）、历史版本回溯
- 可持久化数据结构教学（路径复制思想）
- 离线可回滚的区间统计问题

**使用示例**：

```cpp
PersistentSegmentTree pst({1, 2, 3});
int v1 = pst.update(0, 1, 10);      // 版本 1：{1,10,3}
pst.query(0, 0, 3);                 // 6，旧版本仍可查
pst.query(v1, 0, 3);                // 14，新版本区间和
pst.version_count();                // 2
```

---

### `advanced/rmq_lca.h` — RMQ 与 LCA（Sparse Table 与倍增法）

**用途**：静态区间最值查询（RMQ）与树上最近公共祖先（LCA）两个高频基础问题：前者 O(n log n) 建表 O(1) 查询，后者 O(n log n) 预处理 O(log n) 查询。

**原理**：Sparse Table 用倍增思想预处理所有长度为 2^j 的区间最小值，查询 [l, r] 用两个可重叠的 2^k 区间取 min（k = ⌊log₂(len)⌋）。LCA 用倍增表 up[u][j] = u 向上 2^j 步的祖先：先提升较深节点到同深度，再从高到低跳"祖先不同的最大步"，最后父节点即 LCA。

**主要 API**：

```cpp
// Sparse Table：静态 RMQ。
template <typename T>
class SparseTable {
public:
    explicit SparseTable(const std::vector<T>& arr);
    T query(std::size_t l, std::size_t r) const;   // 闭区间 [l, r] 最小值
    std::size_t size() const;
};

// LCA：倍增法，树以无向邻接表给出。
class LCA {
public:
    LCA(const std::vector<std::vector<std::size_t>>& adj, std::size_t root = 0);
    std::size_t query(std::size_t u, std::size_t v) const;   // u、v 的最近公共祖先
};
```

**复杂度**：SparseTable：建表 O(n log n)、查询 O(1)、空间 O(n log n)。LCA：预处理 O(n log n)、查询 O(log n)、空间 O(n log n)。

**使用场景**：
- 静态数组海量区间最值查询（不可修改数据）
- 树上路径问题（距离、树上差分）的基础预处理
- 与 Tarjan、欧拉序转 RMQ 等方法对比学习

**使用示例**：

```cpp
SparseTable<int> st({5, 2, 8, 1, 9, 3});
st.query(1, 3);                      // 1（{2,8,1} 的最小值）

std::vector<std::vector<std::size_t>> adj(7);  // 建树后：
LCA lca(adj, 0);
lca.query(3, 4);                     // 节点 3、4 的最近公共祖先
```

---

### `advanced/tree_in_tree.h` — 树套树与分块（SqrtDecomp 与 FenwickOfSets）

**用途**：以空间换时间解决两类结构化查询：分块处理"单点改 + 区间和"，树套树处理"前缀中 ≤ x 的个数"（静态二维偏序计数）。

**原理**：分块（SqrtDecomp）把数组切成约 √n 大小的块并预计算块和：区间求和时完整块直接取块和、两端零散部分逐个累加（O(√n)），单点修改只更新所在块（O(1)）。树套树（FenwickOfSets）外层为树状数组、内层每个 BIT 节点保存其覆盖区间内所有元素排序后的值：查询把前缀拆成 O(log n) 个 BIT 节点，每个节点上 upper_bound 二分计数，单次 O(log²n)。

**主要 API**：

```cpp
// 分块：单点修改 + 区间和。
class SqrtDecomp {
public:
    explicit SqrtDecomp(const std::vector<int64_t>& data);
    void point_update(std::size_t pos, int64_t delta);   // data[pos] += delta
    int64_t range_sum(std::size_t l, std::size_t r) const;  // 闭区间 [l, r] 和
};

// Fenwick 套有序集合：静态数组上前 r+1 个元素中 ≤ x 的个数。
class FenwickOfSets {
public:
    explicit FenwickOfSets(const std::vector<int>& values);
    std::size_t count_less_equal(std::size_t r, int x) const;
};
```

**复杂度**：SqrtDecomp：建 O(n)、单点改 O(1)、区间查询 O(√n)、空间 O(n)。FenwickOfSets：建 O(n log n)（每个元素沿 lowbit 上传并排序）、查询 O(log²n)、空间 O(n log n)。

**使用场景**：
- 分块：带修改的区间求和（代码量小、常数小）
- 树套树：二维偏序计数、静态区间排名类问题
- 对比"分块 vs 树套树"的复杂度取舍（√n 对 log²n）

**使用示例**：

```cpp
SqrtDecomp sd({1,2,3,4,5,6,7,8,9,10});
sd.point_update(3, 10);              // data[3]: 4 → 14
sd.range_sum(2, 5);                  // 3+14+5+6 = 28

FenwickOfSets fos({1, 5, 2, 4, 3});
fos.count_less_equal(4, 3);          // 3（{1,2,3} ≤ 3）
```
