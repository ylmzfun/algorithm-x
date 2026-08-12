# 算法专题（`algorithm_x/algo/`）

本文档覆盖 `include/algorithm_x/algo/` 下的 14 个头文件，按"算法设计范式 + 具体实现"组织：
回溯、分支限界、减治、分治、贪心、随机化、近似算法、双指针/滑动窗口，以及一组可直接
复用的基础工具（位运算、查找、排序、插值查找、桶排序/三分查找等）。
所有函数位于命名空间 `algorithm_x::algo`，头文件统一以 `#include "algo/xxx.h"` 引入，
均为 header-only 实现（`inline` 或函数模板），无链接依赖。

---

### `algo/approximation.h` — 近似算法（集合覆盖、顶点覆盖）

**用途**：为两类 NP-Hard 组合优化问题（集合覆盖、顶点覆盖）提供多项式时间的近似解，结果有可证明的近似比上界。

**原理**：集合覆盖采用贪心——每轮选择能覆盖"最多当前未覆盖元素"的集合，近似比为 `ln(n) + 1`（n 为全集大小）；顶点覆盖采用最大匹配贪心——反复取一条未覆盖的边并把两个端点都加入覆盖，选出的边构成极大匹配 M，覆盖大小 `2|M| ≤ 2·OPT`，即 2-近似。

**主要 API**：
```cpp
// 集合覆盖：返回选中集合的下标序列（贪心近似比 ln(n)+1）
std::vector<std::size_t> greedy_set_cover(
    const std::vector<std::vector<std::size_t>>& sets, std::size_t universe_size);

// 顶点覆盖：返回覆盖大小（最大匹配贪心，2-近似）
int vertex_cover_approx(const std::vector<std::pair<int, int>>& edges,
                        int num_vertices);
```

**复杂度**：`greedy_set_cover` 最坏 `O(轮数 × Σ|集合|)`（每轮扫描全部集合与元素），空间 `O(全集大小 + 集合数)`；`vertex_cover_approx` 最坏 `O(E²)`（每条边扫描删除所有关联边），空间 `O(E + V)`。

**使用场景**：
- 大规模集合覆盖 / 顶点覆盖问题中，最优解不可行时换取可证明的近似质量。
- 图的最小顶点覆盖、广告投放/传感器部署等覆盖类问题。

**使用示例**：
```cpp
#include "algo/approximation.h"
using namespace algorithm_x::algo;

std::vector<std::vector<std::size_t>> sets = {{0, 1, 2}, {1, 3, 4}, {2, 4}};
auto chosen = greedy_set_cover(sets, 5);          // 返回 {0, 1}，覆盖全集
std::vector<std::pair<int, int>> edges = {{0, 1}, {1, 2}, {2, 3}};
int cover = vertex_cover_approx(edges, 4);        // 覆盖大小 4 ≤ 2·最优(2)
```

---

### `algo/backtracking.h` — 回溯（N 皇后、子集和、排列、子集、组合）

**用途**：提供搜索/枚举类经典题目的模板实现：N 皇后、子集和（存在性与构造）、全排列、幂集、组合数。

**原理**：回溯是"DFS + 剪枝"的穷举：沿递归树逐步扩展部分解，违反约束（如皇后互相攻击、`rem > target`）立即回退撤销上一步选择。`permutations` 借助 `std::next_permutation` 字典序枚举；`subsets` 用 0..2ⁿ-1 的位掩码枚举；`combinations` 用 `start` 参数保证下标严格递增。

**主要 API**：
```cpp
std::vector<std::string> solve_n_queens(int n);          // 返回一块含 n 个 'Q' 的棋盘，无解返回空
bool subset_sum_exists(const std::vector<int>& nums, int target);
std::vector<int> subset_sum_find(const std::vector<int>& nums, int target); // 找到的一个子集
template <typename T> std::vector<std::vector<T>> permutations(std::vector<T> nums);
template <typename T> std::vector<std::vector<T>> subsets(const std::vector<T>& nums);
template <typename T>
void combinations_backtrack(std::size_t start, std::size_t k, std::vector<T>& current,
                            const std::vector<T>& nums, std::vector<std::vector<T>>& result);
template <typename T> std::vector<std::vector<T>> combinations(const std::vector<T>& nums, std::size_t k);
```

**复杂度**：`solve_n_queens` 最坏 `O(n!)`，空间 `O(n²)`；`subset_sum_*` 最坏 `O(2ⁿ)`，递归栈 `O(n)`；`permutations` 时间/空间 `O(n·n!)`；`subsets` `O(n·2ⁿ)`；`combinations` `O(C(n,k)·k)`。

**使用场景**：
- N 皇后、数独、图的着色等"约束满足"问题。
- 数据量小（`subsets` 建议 `n ≤ 20`）时的枚举与剪枝搜索。

**使用示例**：
```cpp
#include "algo/backtracking.h"
using namespace algorithm_x::algo;

auto board = solve_n_queens(8);                  // 8 皇后的一组解，无解返回 {}
bool ok = subset_sum_exists({3, 34, 4, 12, 5, 2}, 9);   // true：4+5
auto combs = combinations(std::vector<int>{1, 2, 3, 4}, 2); // 6 个二元组合
```

---

### `algo/bit.h` — 位运算工具集

**用途**：一组与具体类型无关的位操作助手，覆盖奇偶判断、2 的幂、lowbit、popcount、指定位操作与子集枚举。

**原理**：基于补码与位运算恒等式：`x & -x` 提取最低位 1，`x & (x - 1)` 清除最低位 1（Brian Kernighan 计数每轮消去一个 1）；子集枚举用 `0..2ⁿ-1` 掩码。`popcount` 的重载直接用编译器内建 `__builtin_popcount(ll)`。

**主要 API**：
```cpp
template <typename T> bool is_odd(T x);
template <typename T> bool is_power_of_two(T x);
template <typename T> T lowbit(T x);            // x & -x，提取最低位 1
template <typename T> T clear_lowbit(T x);      // x & (x - 1)，清除最低位 1
template <typename T> int popcount_bk(T x);     // Brian Kernighan 逐位计数
inline int popcount(uint32_t x);                // 内建 __builtin_popcount
inline int popcount(uint64_t x);                // 内建 __builtin_popcountll
template <typename T> T set_bit(T x, int k);    // 第 k 位置 1
template <typename T> T clear_bit(T x, int k);  // 第 k 位清 0
template <typename T> T toggle_bit(T x, int k); // 第 k 位取反
template <typename T> bool test_bit(T x, int k);// 测试第 k 位
template <typename Func> void enumerate_subsets(int n, Func f); // 枚举 {0..n-1} 的全部子集掩码
```

**复杂度**：除 `popcount_bk`（`O(位数中 1 的个数)`）与 `enumerate_subsets`（`O(2ⁿ)`）外均为 `O(1)`。

**使用场景**：
- 状态压缩 DP 中提取/设置/枚举状态位（`lowbit`、`enumerate_subsets`）。
- 树状数组（Fenwick）求 `lowbit`、统计二进制中 1 的个数。

**使用示例**：
```cpp
#include "algo/bit.h"
using namespace algorithm_x::algo;

int x = 0b1010;
bool p2 = is_power_of_two(16);        // true
int lb = lowbit(x);                   // 2
int cnt = popcount(0b101101);         // 4
int y = set_bit(x, 3);                // 0b1010 | 8 = 0b1110
enumerate_subsets(3, [](int mask) { /* 依次收到 0,1,2,...,7 */ });
```

---

### `algo/branch_and_bound.h` — 分支限界（0-1 背包）

**用途**：求解 0-1 背包问题的最优值（价值总和），与朴素 DP 结果完全一致，但通过剪枝大幅减少搜索量。

**原理**：把解空间组织成"每件物品取/不取"的搜索树，用优先队列按上界 `bound` 降序扩展节点；节点上界取"剩余物品按价值密度排序后的分数背包"松弛解。当某节点上界不超过当前已知最优 `best` 时整棵子树剪枝，因此结果精确等于 DP。

**主要 API**：
```cpp
int branch_and_bound_knapsack(const std::vector<int>& weights,
                              const std::vector<int>& values,
                              int capacity);
```

**复杂度**：最坏指数级（`O(2ⁿ)` 节点），实际因剪枝通常远低于此；空间 `O(n)`（优先队列 + 排序）。

**使用场景**：
- 物品数 n 较大、容量 C 也大（DP 的 `O(nC)` 空间不可行）时的 0-1 背包。
- 需要最优解且价值/重量差异悬殊、剪枝高效的问题实例。

**使用示例**：
```cpp
#include "algo/branch_and_bound.h"
using namespace algorithm_x::algo;

int best = branch_and_bound_knapsack({2, 3, 4, 5}, {3, 4, 5, 6}, 5);
// 最优取第 0、1 件：重量 5、价值 7
```

---

### `algo/decrease_conquer.h` — 减治（快速选择、约瑟夫问题）

**用途**：演示"每轮把问题规模减小一部分、只求解子问题"的减治范式，提供第 k 小元素查找与约瑟夫幸存者两个经典实现。

**原理**：`quickselect_kth` 与快排同样做 Lomuto 划分，但只递归进入含第 k 小元素的一侧，另一侧直接丢弃，规模按几何级数衰减；`josephus` 第一轮报数后第 `k-1` 号出列，剩下的人构成规模 `n-1` 的同构子问题，递推式 `j(n) = (j(n-1) + k) % n`，从 1 到 n 迭代。

**主要 API**：
```cpp
// 第 k 小（0 基），k 越界（k >= n）返回 -1
int quickselect_kth(std::vector<int> nums, std::size_t k);
// 幸存者编号（0 基），n <= 0 返回 -1
int josephus(int n, int k);
```

**复杂度**：`quickselect_kth` 期望 `O(n)`、最坏 `O(n²)`，空间 `O(n)`（值传递拷贝）；`josephus` 时间 `O(n)`、空间 `O(1)`。

**使用场景**：
- 不排序直接找第 k 大/小（如中位数、Top-K）。
- 报数出圈类问题（数据规模大、无法模拟圈时）。

**使用示例**：
```cpp
#include "algo/decrease_conquer.h"
using namespace algorithm_x::algo;

int kth = quickselect_kth({3, 1, 4, 1, 5, 9, 2, 6}, 4);  // 第 4 小（0 基）→ 5
int alive = josephus(7, 3);        // 7 人报 3，幸存者编号 3
```

---

### `algo/divide_conquer.h` — 分治（最大子数组、迭代器版快速选择）

**用途**：提供分治范式的两个经典例子：最大子数组和（含 Kadane 线性版与分治版对照）与泛型迭代器版快速选择。

**原理**：`max_subarray_dc` 把区间 `[l, r)` 从中点拆成左右两半，答案取 `max(左半、右半、跨中点的子数组)`，跨中点部分从中点向两边延伸取最大后缀 + 最大前缀；`quickselect` 与快排同构但只处理一侧，且用三数取中选 pivot 抑制退化。Kadane 版 `max_subarray_sum` 是它的线性替代实现。

**主要 API**：
```cpp
template <typename T> T max_subarray_sum(const std::vector<T>& arr);      // Kadane，O(n)
template <typename T> T max_subarray_dc(const std::vector<T>& arr, std::size_t l, std::size_t r);
template <typename T> T max_subarray_dc(const std::vector<T>& arr);       // 整段 [0, size)
template <typename It, typename Cmp = std::less<>>
It quickselect(It first, It last, std::size_t k, Cmp cmp = {});           // 第 k 小，返回迭代器
```

**复杂度**：`max_subarray_sum` 时间 `O(n)`、空间 `O(1)`；`max_subarray_dc` 时间 `O(n log n)`、递归栈 `O(log n)`；`quickselect` 期望 `O(n)`、最坏 `O(n²)`。

**使用场景**：
- 股票最大收益、最大子段和等线性扫描问题（优先用 Kadane 版）。
- 对任意随机访问迭代器区间找第 k 小（泛型，支持自定义比较器）。

**使用示例**：
```cpp
#include "algo/divide_conquer.h"
using namespace algorithm_x::algo;

int s1 = max_subarray_sum(std::vector<int>{-2, 1, -3, 4, -1, 2, 1, -5, 4});  // 6
int s2 = max_subarray_dc(std::vector<int>{-2, 1, -3, 4, -1, 2, 1, -5, 4});   // 6（分治版）
std::vector<int> v{3, 1, 4, 1, 5, 9, 2, 6};
auto it = quickselect(v.begin(), v.end(), 2);        // 指向第 2 小（0 基）元素 2
```

---

### `algo/external_sort.h` — 外部排序

**用途**：模拟经典的外部归并排序：数据量大到内存放不下时，分块排序后多路归并，输出有序结果文件。

**原理**：先整读输入文件到内存；若数据量不超过 `memory_size` 直接 `std::sort` 写出；否则按 `memory_size` 分块排序后各写临时文件，再用小顶堆做 k-way 归并（每轮从堆顶弹出最小元素并从对应文件补充下一个），最后删除临时文件。

**主要 API**：
```cpp
void external_sort(const std::string& input_file,
                   const std::string& output_file,
                   std::size_t memory_size = 1000);
```

**复杂度**：时间 `O(n log n)`（块内排序 + 归并），空间 `O(memory_size + k)`（k 为临时文件数）；输入为空白/换行分隔的整数文本文件。

**使用场景**：
- 教学演示外部归并排序的完整流程（分块 + k 路归并 + 临时文件清理）。
- 理解磁盘友好排序的基本思想（此处是内存模拟，未真正流式读盘）。

**使用示例**：
```cpp
#include "algo/external_sort.h"
using namespace algorithm_x::algo;

// 输入文件每行一个整数；memory_size=2 会强制触发分块+归并路径
external_sort("test_in.txt", "test_out.txt", 2);
// test_out.txt 中为空格分隔的有序整数序列
```

---

### `algo/greedy.h` — 贪心（活动选择、分数背包、硬币找零）

**用途**：提供三个经典贪心算法：最大不重叠区间选择、可分割物品的分数背包、规范硬币体系下的找零。

**原理**：贪心每步做局部最优选择：活动选择按结束时间升序排序，能接上就选（区间调度最优性定理）；分数背包按价值密度 `v/w` 降序尽量取满；硬币找零按面额从大到小除尽（仅对规范体系如 25/10/5/1 正确）。

**主要 API**：
```cpp
// 返回选中的活动下标（内部按结束时间排序）
std::vector<std::size_t> activity_selection(const std::vector<int>& start,
                                            const std::vector<int>& finish);
// 可分割物品的最大总价值
template <typename T>
T fractional_knapsack(const std::vector<T>& weights, const std::vector<T>& values, T capacity);
// 返回每种面额的使用数量；无法找零（amount 不能除尽）返回空 vector
std::vector<int> coin_change_greedy(int amount, const std::vector<int>& coins);
```

**复杂度**：三个函数时间均 `O(n log n)`（排序主导，`coin_change_greedy` 为 `O(m)`，m 为面额数），空间 `O(n)`。

**使用场景**：
- 会议排期、课程表等"区间调度"问题。
- 可拆分货物运输、容量受限下的价值最大化。

**使用示例**：
```cpp
#include "algo/greedy.h"
using namespace algorithm_x::algo;

auto acts = activity_selection({1, 3, 0, 5}, {2, 4, 6, 7});   // 按结束时间选出的活动下标
double best = fractional_knapsack(std::vector<double>{10, 20, 30},
                                  std::vector<double>{60, 100, 120}, 50.0);  // 240
auto coins = coin_change_greedy(93, {25, 10, 5, 1});          // {3, 1, 1, 3}
```

---

### `algo/interpolation_search.h` — 插值查找

**用途**：在已排序数组上按值大小比例估算目标位置，比二分更快地定位目标。

**原理**：假设数组值近似均匀分布，用线性插值公式 `pos = lo + (value - lo_val)/(hi_val - lo_val) × (n-1)` 预测目标下标，据此缩小搜索区间；越界时夹逼到 `[first, last)`。值域很宽的数组上每次区间收缩速度远超二分。

**主要 API**：
```cpp
// 返回第一个匹配元素的迭代器，未找到返回 last
template <typename It, typename T>
It interpolation_search(It first, It last, const T& value);
```

**复杂度**：均匀分布下期望 `O(log log n)`，最坏 `O(n)`（数据分布极不均匀时退化为线性）；空间 `O(1)`。

**使用场景**：
- 值近似均匀分布的已排序大数组（如连续编号的 ID 表）。
- 二分查找的分布感知优化替代。

**使用示例**：
```cpp
#include "algo/interpolation_search.h"
using namespace algorithm_x::algo;

std::vector<int> v{1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
auto it = interpolation_search(v.begin(), v.end(), 13);   // 指向 13
bool found = it != v.end();
```

---

### `algo/more_algo.h` — 杂项（桶排序、三分查找）

**用途**：提供两个独立实用算法：整数桶排序与单峰函数最小值三分查找。

**原理**：`bucket_sort` 对整数按 `value - min_val` 直接落入同一下标桶（计数即有序），再顺序回填，本质是"值域桶"；`ternary_search` 对 U 形（凸）函数把区间三等分，比较 `f(m1)` 与 `f(m2)` 舍掉不可能是最小值点的一段，区间按 `2/3` 比例收缩。

**主要 API**：
```cpp
// 桶排序：仅限整数类型，原地排序 [first, last)
template <typename It> void bucket_sort(It first, It last);
// 三分查找：在 [l, r] 上找凸函数 f 的最小值点，eps 为收敛阈值
template <typename T, typename F>
T ternary_search(T l, T r, F f, const T eps = T{0});
```

**复杂度**：`bucket_sort` 时间 `O(n + k)`（k = max - min + 1）、空间 `O(n + k)`；`ternary_search` 迭代 `O(log((r-l)/eps))` 轮、空间 `O(1)`。

**使用场景**：
- 值域紧凑（max-min 小）的整数排序，特别是重复值多的场景。
- 二分不适用（函数不单调）时的凸函数极值搜索（抛物线、二次代价函数）。

**使用示例**：
```cpp
#include "algo/more_algo.h"
using namespace algorithm_x::algo;

std::vector<int> v{5, 2, 8, 1, 3, 2, 9};
bucket_sort(v.begin(), v.end());               // v 升序
double m = ternary_search(0.0, 10.0,
                          [](double x) { return (x - 3.0) * (x - 3.0); },
                          1e-9);               // ≈ 3.0（极小值点）
```

---

### `algo/randomized.h` — 随机化算法（洗牌、随机快速选择、蒙特卡洛、蓄水池抽样）

**用途**：收集四个随机化基础算法：Fisher-Yates 均匀洗牌、随机 pivot 的快速选择、蒙特卡洛估算 π、流式蓄水池抽样。

**原理**：`shuffle` 从后往前每个位置 `i` 与 `[0, i]` 内随机位置交换，保证每种排列等概率；`randomized_quickselect` 随机选 pivot 使第 k 小期望 `O(n)` 且无需三数取中；`monte_carlo_pi` 在单位正方形内均匀撒点统计落入单位圆的占比 ×4；`reservoir_sample` 前 k 个直接入池，之后第 i 个元素以 `k/(i+1)` 概率替换池中随机一项。

**主要 API**：
```cpp
template <typename It> void shuffle(It first, It last);   // Fisher-Yates
template <typename It, typename Cmp = std::less<>>
It randomized_quickselect(It first, It last, std::size_t k, Cmp cmp = {});
inline double monte_carlo_pi(long long samples);
template <typename It>
std::vector<typename std::iterator_traits<It>::value_type>
reservoir_sample(It first, It last, std::size_t k);
```

**复杂度**：`shuffle` `O(n)`；`randomized_quickselect` 期望 `O(n)`、最坏 `O(n²)`；`monte_carlo_pi` `O(samples)`；`reservoir_sample` 时间 `O(n)`、空间 `O(k)`。

**使用场景**：
- 打乱数据（洗牌）、流式数据中不放回地均匀抽样（日志、传感器流）。
- 无三数取中时仍需稳定 `O(n)` 期望的第 k 小查询；π 的统计模拟教学。

**使用示例**：
```cpp
#include "algo/randomized.h"
using namespace algorithm_x::algo;

std::vector<int> v{1, 2, 3, 4, 5};
shuffle(v.begin(), v.end());                     // 随机重排
auto it = randomized_quickselect(v.begin(), v.end(), 2);   // 第 2 小（0 基）
double pi = monte_carlo_pi(1'000'000);          // ≈ 3.14
auto sample = reservoir_sample(v.begin(), v.end(), 3);     // 均匀抽 3 个
```

---

### `algo/search.h` — 查找（线性 / 二分全家桶）

**用途**：提供对任意随机访问迭代器区间生效的查找函数：线性查找、精确二分、lower_bound 与 upper_bound。

**原理**：二分族基于经典的半开区间 `[first, last)` 收缩：`lower_bound` 返回第一个 `≥ value` 的位置，`upper_bound` 返回第一个 `> value` 的位置，`binary_search_range` 在 `lower_bound` 基础上再验证 `!cmp(value, *it)` 判定存在性；均支持自定义比较器 `Cmp`。

**主要 API**：
```cpp
template <typename It, typename T>
It linear_search(It first, It last, const T& value);        // 线性，O(n)
template <typename It, typename T, typename Cmp = std::less<>>
It binary_search_range(It first, It last, const T& value, Cmp cmp = {});
template <typename It, typename T, typename Cmp = std::less<>>
It lower_bound(It first, It last, const T& value, Cmp cmp = {});
template <typename It, typename T, typename Cmp = std::less<>>
It upper_bound(It first, It last, const T& value, Cmp cmp = {});
```

**复杂度**：`linear_search` 时间 `O(n)`；二分三个函数时间均 `O(log n)`；空间均 `O(1)`。

**使用场景**：
- 有序容器上的精确查找与"第一个满足条件的位置"查询。
- 自定义比较语义的二分（如对结构体数组按字段查找、求插入位置）。

**使用示例**：
```cpp
#include "algo/search.h"
using namespace algorithm_x::algo;

std::vector<int> v{1, 3, 3, 5, 7, 9};
auto a = lower_bound(v.begin(), v.end(), 3);     // 第一个 3
auto b = upper_bound(v.begin(), v.end(), 3);     // 第一个 5 的位置
auto f = binary_search_range(v.begin(), v.end(), 5);   // 指向 5
```

---

### `algo/sort.h` — 排序全集（O(n²) / O(n log n) / 非比较排序）

**用途**：教学用完整排序实现：三个 `O(n²)` 基础排序、三个 `O(n log n)` 比较排序、两个整数专用非比较排序，全部支持自定义比较器（非比较排序除外）。

**原理**：冒泡带"早停"优化（记录最后一次交换位置）；选择每轮挑最小放前面；插入把元素前移到正确位置（近有序时近线性）；归并递归分半后线性归并（需 `O(n)` 辅助）；快排用三数取中 pivot + Lomuto 划分原地完成；堆排自底向上建堆后反复交换堆顶到尾部并 `sift_down`；计数排序按值域计数回填；基数排序按十进制位 LSD 逐位稳定排序。

**主要 API**：
```cpp
template <typename It, typename Cmp = std::less<>>
void bubble_sort(It first, It last, Cmp cmp = {});
template <typename It, typename Cmp = std::less<>>
void selection_sort(It first, It last, Cmp cmp = {});
template <typename It, typename Cmp = std::less<>>
void insertion_sort(It first, It last, Cmp cmp = {});
template <typename It, typename Cmp = std::less<>>
void merge_sort(It first, It last, Cmp cmp = {});
template <typename It, typename Cmp = std::less<>>
void quick_sort(It first, It last, Cmp cmp = {});
template <typename It, typename Cmp = std::less<>>
void heap_sort(It first, It last, Cmp cmp = {});
template <typename It> void counting_sort(It first, It last);   // 仅整数
template <typename It> void radix_sort(It first, It last);      // 仅非负整数，基 10
```

**复杂度**：冒泡/选择/插入最坏 `O(n²)`（插入近有序 `O(n)`），空间 `O(1)`；归并 `O(n log n)`、空间 `O(n)`；快排平均 `O(n log n)`、最坏 `O(n²)`、空间 `O(log n)` 栈；堆排 `O(n log n)`、空间 `O(1)`；计数排序 `O(n + k)`（k = max-min+1）、空间 `O(k)`；基数排序 `O(d·n)`（d 为最大数位数）、空间 `O(n)`。

**使用场景**：
- 学习各排序算法结构与稳定性差异（教学对照）。
- 整数数据且值域/位数可控时的非比较排序（计数、基数）。

**使用示例**：
```cpp
#include "algo/sort.h"
using namespace algorithm_x::algo;

std::vector<int> a{5, 2, 8, 1, 3}, b{5, 2, 8, 1, 3}, c{5, 2, 8, 1, 3};
merge_sort(a.begin(), a.end());
quick_sort(b.begin(), b.end());
counting_sort(c.begin(), c.end());     // 三个数组都变 {1, 2, 3, 5, 8}
```

---

### `algo/two_pointers.h` — 双指针 / 滑动窗口 / 前缀和

**用途**：集合三类高频区间技巧：相向双指针（有序两数之和、去重）、滑动窗口（定长最大和、最短达标子数组）、以及一维/二维前缀和与差分数组类。

**原理**：`two_sum_sorted` 左右指针根据 `sum` 与 target 的大小关系单向收缩；`remove_duplicates` 快慢指针原地压缩重复；`max_sum_fixed_window` 每步加右减左维持定长窗；`min_subarray_len` 右指针扩张、左指针收缩的变长窗；`PrefixSum(2D)` 预计算矩形区域和以 `O(1)` 查询；`DifferenceArray` 对区间 `[l, r]` 做 `O(1)` 的 `diff[l]+=v, diff[r+1]-=v` 后前缀还原。

**主要 API**：
```cpp
template <typename T> std::pair<long, long> two_sum_sorted(const std::vector<T>& arr, const T& target);
template <typename T> std::size_t remove_duplicates(std::vector<T>& arr);   // 返回去重后长度
template <typename T> T max_sum_fixed_window(const std::vector<T>& arr, std::size_t k);
template <typename T> std::size_t min_subarray_len(const std::vector<T>& arr, const T& target);

template <typename T> class PrefixSum {          // query(l, r) = sum(arr[l..r))，半开区间
    explicit PrefixSum(const std::vector<T>& arr);
    T query(std::size_t l, std::size_t r) const;
};
template <typename T> class PrefixSum2D {        // query(r1,c1,r2,c2) = 子矩阵和 [r1..r2)×[c1..c2)
    explicit PrefixSum2D(const std::vector<std::vector<T>>& mat);
    T query(std::size_t r1, std::size_t c1, std::size_t r2, std::size_t c2) const;
};
template <typename T> class DifferenceArray {    // O(1) 区间加、O(n) 还原
    explicit DifferenceArray(const std::vector<T>& arr);
    void add(std::size_t l, std::size_t r, const T& val);
    std::vector<T> restore() const;
};
```

**复杂度**：`two_sum_sorted`/`remove_duplicates`/`max_sum_fixed_window`/`min_subarray_len` 均时间 `O(n)`、空间 `O(1)`；`PrefixSum`/`PrefixSum2D` 预处理 `O(n)` / `O(rows·cols)`、查询 `O(1)`；`DifferenceArray` 预处理 `O(n)`、add `O(1)`、restore `O(n)`。

**使用场景**：
- 有序数组两数之和、去重、定长窗口最值、最短/最长满足条件子数组。
- 大量区间和/子矩阵和查询（前缀和）、多次区间批量加值（差分数组）。

**使用示例**：
```cpp
#include "algo/two_pointers.h"
using namespace algorithm_x::algo;

auto pr = two_sum_sorted(std::vector<int>{1, 2, 4, 7, 11}, 9);      // {1, 4}：arr[1]+arr[4]
int best = max_sum_fixed_window(std::vector<int>{2, 3, -1, 4, 1}, 3);  // 窗口和最大 6
size_t len = min_subarray_len(std::vector<int>{2, 3, 1, 2, 4, 3}, 7);  // 最短长度 2
PrefixSum<int> ps(std::vector<int>{1, 2, 3, 4});
int s = ps.query(1, 3);                             // arr[1]+arr[2] = 5
DifferenceArray<int> da(std::vector<int>{0, 0, 0, 0, 0});
da.add(1, 3, 5);                                    // [1,3] 各加 5
auto arr = da.restore();                            // {0, 5, 5, 5, 0}
```
