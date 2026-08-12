# 动态规划模块（algorithm_x/dp）

本模块共 10 个头文件，覆盖经典 DP 模型（背包、LIS、区间 DP、树形 DP、数位 DP、概率 DP、插头 DP）
与常用 DP 优化技术（单调队列优化、数据结构（树状数组）优化、四边形不等式（Knuth）优化、
斜率优化（凸包技巧 CHT）、矩阵快速幂优化）。
全部接口位于 `algorithm_x::dp` 命名空间，多数为 `inline` 函数或模板，引用头文件即可使用。
对应测试见 `tests/dp/test_*.cpp`，本页示例与测试中的真实用法一致。

---

### `dp/advanced_dp.h` — 数位 DP 与树形 DP
**用途**：统计 [1, n] 内所有整数的数位之和（数位 DP）；求无权树的最大独立集大小（树形 DP）。
**原理**：数位 DP 用记忆化 DFS 按位枚举，状态由 (pos, tight, started) 三元组描述——tight 表示当前是否贴合上界、started 表示是否已开始计数（跳过前导零），每个状态同时维护"个数"与"数位和"两个量，对已开始的位累加 d × 子问题个数；树形 DP 对每个节点用 dp[u][0/1] 表示"不选 / 选 u"时的最大独立集，选 u 时子节点只能不选，不选 u 时子节点可选可不选。
**主要 API**：
```cpp
// 数位 DP — 求 [1, n] 所有数字的数位和。
inline int64_t digit_dp_sum(int64_t n);

// 树形 DP — 最大独立集（无权树）。
// adj: 无向邻接表。返回最大独立集大小。
inline int tree_dp_max_independent_set(
    const std::vector<std::vector<std::size_t>>& adj);
```
**复杂度**：`digit_dp_sum` O(log n) 时间（数位个数 × 常数状态）/ O(log n) 空间；`tree_dp_max_independent_set` O(V + E) 时间 / O(V) 空间。
**使用场景**：
- "1 到 n 中满足某数位条件"的计数 / 求和类问题
- 树上选点互不相邻的最大权 / 最大个数问题
**使用示例**：
```cpp
#include "algorithm_x/dp/advanced_dp.h"
using namespace algorithm_x::dp;
int64_t s = digit_dp_sum(9);                       // 45
std::vector<std::vector<std::size_t>> adj(4);
adj[0] = {1}; adj[1] = {0, 2}; adj[2] = {1, 3}; adj[3] = {2};
int mis = tree_dp_max_independent_set(adj);        // 2
```

---

### `dp/common.h` — 经典区间 DP：矩阵链乘法、硬币找零、戳气球
**用途**：矩阵链乘法的最小运算次数、硬币找零的最少硬币数、戳气球的最大得分。
**原理**：矩阵链乘法与戳气球都是区间 DP——按区间长度从小到大枚举 (i, j) 并枚举分割点 k 合并左右子区间（矩阵链取 min，戳气球取 max）；硬币找零是"完全背包"式递推 dp[a] = min(dp[a], dp[a-c] + 1)。
**主要 API**：
```cpp
// 矩阵链乘法：返回最小乘法次数。
// dims[i] 为矩阵 i 的行数，dims[i+1] 为列数。n 个矩阵需要 n+1 维。
inline int matrix_chain_order(const std::vector<int>& dims);

// 硬币找零（最少硬币数）— DP 版本，支持任意硬币系统。
// 返回所需最少硬币数，无解返回 -1。
inline int coin_change_dp(const std::vector<int>& coins, int amount);

// 戳气球（Burst Balloons）— 区间 DP 经典题。
// nums[i] 戳破得分 = nums[left] * nums[i] * nums[right]。
inline int burst_balloons(std::vector<int> nums);
```
**复杂度**：`matrix_chain_order` / `burst_balloons` O(n³) 时间 / O(n²) 空间；`coin_change_dp` O(amount × 硬币种数) 时间 / O(amount) 空间。
**使用场景**：
- 括号化、矩阵链、石子合并等区间合并类问题
- 找零钱（最少硬币）与"最后取走"类区间模型（如 LeetCode 312）
**使用示例**：
```cpp
#include "algorithm_x/dp/common.h"
using namespace algorithm_x::dp;
int c = matrix_chain_order({10, 20, 30, 40, 30});   // 30000
int k = coin_change_dp({1, 2, 5}, 11);              // 3
int s = burst_balloons({3, 1, 5, 8});               // 167
```

---

### `dp/ds_opt_dp.h` — 树状数组优化递增子序列 DP
**用途**：求带权严格递增子序列的最大和（最大和递增子序列），以及最长递增子序列（LIS）的方案数。
**原理**：把形如 dp[i] = w[i] + max{dp[j] | j < i 且 values[j] < values[i]} 的转移中"已处理且值更小"的状态按值域压缩排名组织进树状数组（Fenwick）：前缀查询 [1, rank-1] 的最优值 O(log n)、单点更新 O(log n)，按输入顺序处理天然满足 j < i，只查严格更小值域 [1, rank-1] 保证严格递增。LIS 方案数版本在树状数组节点上聚合 (最长长度, 方案数) 二元组，长度相同时累加计数；若前缀长度为 0，说明当前值只能作为长度为 1 的新 LIS 起点。
**主要 API**：
```cpp
// 最大和递增子序列（严格递增）— O(n log n)。
// dp[i] = weights[i] + max{dp[j] | j < i 且 values[j] < values[i]}。
inline int64_t max_sum_increasing_subsequence(const std::vector<int>& values, const std::vector<int>& weights);

// 最长递增子序列的方案数 — O(n log n)。
inline int64_t lis_count(const std::vector<int>& values);
```
**复杂度**：均为 O(n log n) 时间 / O(n) 空间。
**使用场景**：
- 带权 LIS（最大和递增子序列，含负权时可跳过，结果 ≥ 0）
- 统计最长递增子序列的方案数
**使用示例**：
```cpp
#include "algorithm_x/dp/ds_opt_dp.h"
using namespace algorithm_x::dp;
int64_t s = max_sum_increasing_subsequence({1, 2, 3, 4}, {1, 2, 3, 4});  // 10
int64_t c = lis_count({2, 1, 3});   // 2：最长递增子序列 1-3 与 2-3
```

---

### `dp/knapsack.h` — 背包问题全家桶
**用途**：0-1 背包（每件最多一次）、0-1 背包带回溯选品、完全背包（每件无限次）、多重背包（每件有数量上限）。
**原理**：滚动数组按容量倒序遍历实现 0-1 背包（防止同一件被重复选取），正序遍历实现完全背包；多重背包用二进制拆分把 count 件物品拆成 O(log count) 个 1、2、4、... 的等价 0-1 物品组再套 0-1 背包；带回溯版本保存完整二维表，结束后从右下角反向比较 dp[i][j] 与 dp[i-1][j] 恢复选中下标。
**主要 API**：
```cpp
// 0-1 背包：每件物品最多选一次。
// 返回最大价值。weights 和 values 长度相同。
inline int knapsack_01(const std::vector<int>& weights,
                        const std::vector<int>& values, int capacity);

// 0-1 背包（带回溯）：返回 {最大价值, 选中物品的下标}。
inline std::pair<int, std::vector<std::size_t>>
knapsack_01_with_items(const std::vector<int>& weights,
                        const std::vector<int>& values, int capacity);

// 完全背包：每件物品可选无限次。
inline int knapsack_complete(const std::vector<int>& weights,
                              const std::vector<int>& values, int capacity);

// 多重背包（二进制拆分优化）：每件物品有 count 个。
inline int knapsack_multiple(const std::vector<int>& weights,
                              const std::vector<int>& values,
                              const std::vector<int>& counts, int capacity);
```
**复杂度**：`knapsack_01` / `knapsack_complete` O(n·capacity) 时间 / O(capacity) 空间；`knapsack_01_with_items` O(n·capacity) 时间 / O(n·capacity) 空间；`knapsack_multiple` O(capacity·Σ log counts[i]) 时间 / O(capacity) 空间。
**使用场景**：
- 资源分配、预算选择类最优化问题
- 需要输出具体选品方案时使用带回溯版本
**使用示例**：
```cpp
#include "algorithm_x/dp/knapsack.h"
using namespace algorithm_x::dp;
int v01 = knapsack_01({10, 20, 30}, {60, 100, 120}, 50);   // 220
auto [val, items] = knapsack_01_with_items({10, 20, 30}, {60, 100, 120}, 50);
int vc = knapsack_complete({1, 2}, {1, 3}, 4);              // 6
int vm = knapsack_multiple({1}, {1}, {3}, 4);               // 3
```

---

### `dp/lis.h` — 最长递增子序列与最大子数组和
**用途**：求严格递增子序列（LIS）的长度与具体序列内容，以及最大子数组和。
**原理**：耐心排序（Patience Sorting）维护递增的 tails 数组，用 lower_bound 找到第一个不小于当前值的位置并替换，tails 长度即 LIS 长度；`lis_sequence` 额外记录每个下标的长度位与前驱，结束后从最长尾部下标沿前驱链还原序列；最大子数组和用 Kadane 算法线性扫描，cur = max(x, cur + x)。
**主要 API**：
```cpp
// 最长递增子序列长度 — O(n log n) 耐心排序。
template <typename T>
std::size_t lis_length(const std::vector<T>& nums);

// 最长递增子序列具体内容 — O(n log n)。
template <typename T>
std::vector<T> lis_sequence(const std::vector<T>& nums);

// 最大子数组和 — Kadane O(n)。
template <typename T>
T max_subarray_sum(const std::vector<T>& arr);
```
**复杂度**：`lis_length` / `lis_sequence` O(n log n) 时间 / O(n) 空间；`max_subarray_sum` O(n) 时间 / O(1) 空间。
**使用场景**：
- 最长递增子序列长度 / 构造（模板类，适用于任意可比较类型）
- 最大子段和（Kadane）
**使用示例**：
```cpp
#include "algorithm_x/dp/lis.h"
using namespace algorithm_x::dp;
auto len = lis_length(std::vector<int>{10, 9, 2, 5, 3, 7, 101, 18});  // 4
auto seq = lis_sequence(std::vector<int>{0, 1, 0, 3, 2, 3});          // {0, 1, 2, 3}
int m = max_subarray_sum(std::vector<int>{-2, 1, -3, 4, -1, 2, 1, -5, 4});  // 6
```

---

### `dp/optimization.h` — 单调队列：滑动窗口最值
**用途**：求定长滑动窗口内的最大 / 最小值，是形如 dp[i] = max_{j∈[i-k, i-1]} dp[j] + ... 的单调队列优化 DP 的基础工具。
**原理**：用双端队列维护窗口内"下标单调、值单调"的候选序列：新元素入队前弹出队尾所有不优于它的元素（求最大值时值 ≤ 当前值的全部弹出），队头下标越出窗口则弹出，队头即为当前窗口最值。
**主要 API**：
```cpp
// 单调队列优化 — 滑动窗口最大值 O(n)。
// 用于 DP 中形如 dp[i] = max_{j∈[i-k, i-1]} dp[j] + ... 的转移。
// 返回每个位置对应窗口内的最大值。
template <typename T>
std::vector<T> sliding_window_max(const std::vector<T>& arr, std::size_t k);

// 滑动窗口最小值。
template <typename T>
std::vector<T> sliding_window_min(const std::vector<T>& arr, std::size_t k);
```
**复杂度**：O(n) 时间（每个下标入队出队各一次，均摊 O(1)）/ O(k) 空间。
**使用场景**：
- 定长滑动窗口最大 / 最小值
- 形如 dp[i] = 窗口内最值 + 常数的 DP 转移加速
**使用示例**：
```cpp
#include "algorithm_x/dp/optimization.h"
using namespace algorithm_x::dp;
auto mx = sliding_window_max(std::vector<int>{1, 3, -1, -3, 5, 3, 6, 7}, 3);
// {3, 3, 5, 5, 6, 7}
auto mn = sliding_window_min(std::vector<int>{1, 3, -1, -3, 5, 3, 6, 7}, 3);
```

---

### `dp/plug_dp.h` — 插头 DP（轮廓线 DP）：骨牌覆盖计数
**用途**：统计用 1×2 骨牌完全覆盖 rows×cols 棋盘的总方案数。
**原理**：按行优先逐格推进扫描，用 cols 位二进制掩码记录"轮廓线"上各列的占用情况：对已处理的列，bit 为 1 表示该列被本行竖放骨牌占住并延伸到下一行；对未处理的列，bit 为 1 表示当前格已被上方竖放或本行左侧横放的骨牌占住。处理完当前格后该位含义自动从"本行已占"切换为"下一行已占"，从而跨行传递。转移分三种：该位已置位则清位（当前格已被覆盖）；空闲可竖放（置位当前位）或横放（置位下一位，要求下一位空闲且不越界）；全部格子处理完后轮廓线必须为空（mask == 0）。
**主要 API**：
```cpp
// 插头 DP / 轮廓线 DP — 1×2 骨牌完全覆盖 rows×cols 棋盘的方案数。
inline int64_t domino_tilings(int rows, int cols);
```
**复杂度**：O(rows × cols × 2^cols) 时间 / O(2^cols) 空间。
**使用场景**：
- 棋盘覆盖计数（多米诺骨牌、L 形等网格铺砖）
- 轮廓线状态压缩 DP 入门（滚动状态逐格转移）
**使用示例**：
```cpp
#include "algorithm_x/dp/plug_dp.h"
using namespace algorithm_x::dp;
int64_t t1 = domino_tilings(2, 3);   // 3
int64_t t2 = domino_tilings(4, 4);   // 36
int64_t t3 = domino_tilings(3, 3);   // 0（面积奇数，无法完全覆盖）
```

---

### `dp/probability_dp.h` — 概率 DP
**用途**：计算公平硬币 n 次投掷恰好 k 次正面的概率，以及一维对称随机游走 n 步后到达指定位置的概率。
**原理**：滚动数组递推 dp[j] = 0.5·dp[j] + 0.5·dp[j-1]（本轮仍反面 / 上轮为正面再加一次正面），dp[0] 每轮乘 0.5；一维随机游走第 n 步到达位置 pos 等价于 n 次投掷中正面数恰好为 (n+pos)/2，因此直接复用 `coin_toss_probability`。
**主要 API**：
```cpp
// 掷硬币概率 — DP[i][j] = i 次投掷恰好 j 次正面的概率（公平硬币 p=0.5）。
inline double coin_toss_probability(int n, int k);

// 随机游走 — 从 0 出发，n 步后到达位置 pos 的概率。
inline double random_walk_probability(int n, int pos);
```
**复杂度**：O(n·k) 时间 / O(k) 空间。
**使用场景**：
- 独立重复试验的恰好发生次数概率
- 随机游走、赌徒破产类期望问题
**使用示例**：
```cpp
#include "algorithm_x/dp/probability_dp.h"
using namespace algorithm_x::dp;
double p1 = coin_toss_probability(2, 1);    // 0.5
double p2 = coin_toss_probability(2, 2);    // 0.25
```
注意：`random_walk_probability` 依赖 `coin_toss_probability`，要求 n 与 pos 奇偶性一致（即 n+pos 为偶数）结果才有意义，否则 (n+pos)/2 的整数除法会截断。

---

### `dp/quadrangle.h` — 四边形不等式（Knuth）优化：最优二叉搜索树
**用途**：给定各键的访问频率，构造期望检索代价最小的二叉搜索树。
**原理**：区间 DP 状态 dp[i][j] 表示键区间 [i, j] 的最小代价，分割点枚举所有 k；Knuth 优化利用最优分割点的决策单调性，把 k 的枚举范围从 [i, j] 收窄到 [opt[i][j-1], opt[i+1][j]]，使总复杂度从 O(n³) 降为 O(n²)。
**主要 API**：
```cpp
// 最优二叉搜索树 (Optimal BST) — Knuth 优化 O(n²)。
// freq[i]: 键 i 的访问频率 (0-indexed)。
inline int optimal_bst(const std::vector<int>& freq);
```
**复杂度**：O(n²) 时间 / O(n²) 空间。
**使用场景**：
- 最优二叉搜索树构造（数据库索引、字典查询优化）
- 满足四边形不等式 / 决策单调性的区间 DP 优化
**使用示例**：
```cpp
#include "algorithm_x/dp/quadrangle.h"
using namespace algorithm_x::dp;
int cost = optimal_bst({34, 50});   // 最小期望检索代价 ≥ 84
```

---

### `dp/slope_opt.h` — 斜率优化：凸包技巧（Convex Hull Trick）
**用途**：维护若干直线 y = m·x + b，支持插入直线与按 x 查询最小函数值，用于形如 dp[i] = min_j(dp[j] + m_j·x_i + b_j) 的斜率优化 DP。
**原理**：当下凸包上相邻直线的交点横坐标单调递增时，各直线按斜率排序后只需比较相邻交点即可维护凸包（交点倒转时弹出栈顶直线）；查询 x 单调递增时指针只向右移动，均摊 O(1)。取最大值时可将斜率与截距取负转化为最小值问题。
**主要 API**：
```cpp
// Convex Hull Trick (CHT) for DP optimization.
// Supports adding lines y = mx + b and querying minimum value at x.
// Assumes slopes are added in decreasing order (monotonic).
// For maximum queries, negate slopes and intercepts.
template <typename T>
class ConvexHullTrick {
public:
    // Add line y = mx + b. Slopes must be added in decreasing order.
    void add_line(T m, T b);

    // Query minimum y at given x. Queries must be in increasing order.
    T query(T x);

    void clear();
};
```
**复杂度**：`add_line` 均摊 O(1)（每条直线至多被弹出一次）、`query` 均摊 O(1)（指针单调右移）、`clear` O(1)；空间 O(n)（直线条数）。
**使用场景**：
- 斜率优化 DP（如"玩具装箱"类问题；求最大值时对斜率、截距取负）
- 平面直线族的最小值查询类几何问题
**使用示例**：
```cpp
#include "algorithm_x/dp/slope_opt.h"
using namespace algorithm_x::dp;
ConvexHullTrick<long long> cht;
cht.add_line(1, 0);    // y = x
cht.add_line(0, 5);    // y = 5
cht.add_line(-1, 10);  // y = -x + 10
long long v = cht.query(5);   // min{5, 5, 5} = 5
```
