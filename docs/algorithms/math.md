# 数学模块（algorithm_x/math）

本模块共 11 个头文件，覆盖数论（素数判定 / 筛法 / 质因数分解 / 扩展欧几里得 / 模逆元 / CRT / 欧拉函数）、
组合数学（卡特兰数 / 二项式系数 / 容斥原理 / 鸽巢原理 / 斯特林数 / 贝尔数 / 母函数）、
线性代数（矩阵乘法 / 矩阵快速幂 / 高斯消元 / 行列式）、快速傅里叶变换（FFT）、
博弈论（Nim 游戏 / SG 函数）与概率统计（期望 / 二项分布）。
全部接口位于 `algorithm_x::math` 命名空间，均为 `inline` 函数或模板，引用头文件即可使用，无需链接额外库。
对应测试见 `tests/math/test_*.cpp`，本页示例与测试中的真实用法一致。

---

### `math/combinatorics.h` — 组合计数：卡特兰数与二项式系数
**用途**：计算卡特兰数 C(n) 与二项式系数 C(n, k)，是组合计数中最常用的两个基础量。
**原理**：卡特兰数按递推式 C(n) = C(n-1) × 2(2n-1) / (n+1) 迭代计算；二项式系数采用乘法公式逐项相乘，并利用对称性 C(n,k) = C(n,n-k) 取较小一侧以降低运算量。
**主要 API**：
```cpp
// 卡特兰数 C(n) = (2n)! / (n! * (n+1)!)
inline int64_t catalan_number(int n);

// 二项式系数 C(n, k) — 乘法公式。
inline int64_t binomial(int n, int k);
```
**复杂度**：`catalan_number` O(n) 时间 / O(1) 空间；`binomial` O(min(k, n-k)) 时间 / O(1) 空间。
**使用场景**：
- 括号匹配方案数、出栈序列数、二叉树形态数等组合计数问题
- 小规模、无需取模的组合数计算
**使用示例**：
```cpp
#include "algorithm_x/math/combinatorics.h"
using namespace algorithm_x::math;
int64_t c = catalan_number(5);   // 42：5 对括号的合法序列数
int64_t b = binomial(5, 2);      // 10
```

---

### `math/fft.h` — 快速傅里叶变换（FFT）与多项式乘法
**用途**：在 O(n log n) 内计算两个多项式的卷积（乘法），是加速大整数乘法、卷积型 DP 与生成函数运算的核心工具。
**原理**：Cooley-Tukey FFT 将 n 次单位根按奇偶分解递归（迭代版按位反转重排 + 蝶形运算），把多项式从系数表示变换到点值表示后逐点相乘，再逆变换回系数表示；`fft_multiply` 将输入补零到 2 的幂后完成"正变换 × 点乘 × 逆变换"并四舍五入取整。
**主要 API**：
```cpp
using cd = std::complex<double>;
const double PI = std::acos(-1.0);

// Cooley-Tukey FFT
inline void fft(std::vector<cd>& a, bool invert);

// 多项式乘法
inline std::vector<int> fft_multiply(const std::vector<int>& a,
                                      const std::vector<int>& b);
```
**复杂度**：`fft` 与 `fft_multiply` 均为 O(n log n) 时间（n 为补零后的 2 的幂）/ O(n) 空间。
**使用场景**：
- 大整数乘法（系数为十进制位）
- 卷积型 DP、生成函数的快速卷积
- 字符串匹配（模式与文本的错位相关）
**使用示例**：
```cpp
#include "algorithm_x/math/fft.h"
using namespace algorithm_x::math;
std::vector<int> a = {1, 2, 1};  // 1 + 2x + x²
std::vector<int> b = {1, 1};     // 1 + x
auto c = fft_multiply(a, b);     // {1, 3, 3, 1}（尾部零会被去除）
```

---

### `math/game_theory.h` — 博弈论：Nim 游戏与 SG 函数
**用途**：判断 Nim 取石子游戏的先手胜负，并计算任意公平组合博弈局面的 Sprague-Grundy（SG）值。
**原理**：Nim 游戏先手必胜当且仅当所有堆石子数的异或和不为 0；SG 函数把博弈局面映射到有向图上"可达状态 SG 值的 mex"，多个子游戏组合的 SG 值等于各子游戏 SG 的异或，SG ≠ 0 则必胜。本实现用记忆化 DFS 计算每个状态的 SG 值并返回起点（状态 0）的 SG。
**主要 API**：
```cpp
// Nim 游戏：判断先手是否必胜。
// piles[i] 为第 i 堆石子数。异或和 != 0 则先手必胜。
inline bool nim_win(const std::vector<int>& piles);

// Sprague-Grundy 函数：计算给定局面的 SG 值。
// 输入游戏图 adj[u] = {可到达的状态}。返回起点的 SG 值。
inline int sg_function(const std::vector<std::vector<int>>& adj);
```
**复杂度**：`nim_win` O(n) 时间 / O(1) 空间；`sg_function` O(V² + E) 时间（V 为状态数，每个状态构造 mex 表开销 O(V)）/ O(V) 空间。
**使用场景**：
- Nim 类取石子博弈的胜负判定
- 多子游戏组合的胜负判定（各子游戏 SG 值异或）
- 棋盘走子、图上取石子等公平组合博弈分析
**使用示例**：
```cpp
#include "algorithm_x/math/game_theory.h"
using namespace algorithm_x::math;
bool win  = nim_win({1, 3, 5});   // 异或和 != 0，先手必胜
bool lose = nim_win({1, 1});      // 异或和为 0，先手必败
```

---

### `math/generating_function.h` — 母函数（生成函数）计数
**用途**：计算用若干种"无限供应"的整数重量组合成总重量 s 的方案数（顺序无关的整数拆分）。
**原理**：对单件重量 w 的一类物品，其方案数序列对应几何级数 1 + x^w + x^{2w} + ...；多类物品组合时最终方案数序列 = 各物品母函数逐项相乘（多项式卷积）。本函数从常数多项式 1 出发，对每种重量 w 做一次完全背包式卷积 `ways[s] += ways[s-w]`（s 从小到大遍历，保证同种可重复取），等价于乘上 (1 + x^w + x^{2w} + ...) 并截断到 max_sum 次。
**主要 API**：
```cpp
// 返回 ways[s] = 用给定物品种类组成总重量 s 的方案数（顺序无关，整数拆分的组合版本）。
inline std::vector<int64_t> generating_function_ways(const std::vector<int>& weights, int max_sum);
```
**复杂度**：O(W × max_sum) 时间（W 为物品种类数）/ O(max_sum) 空间。
**使用场景**：
- 整数拆分方案数（组合、顺序无关）
- 完全背包类"凑数"计数问题
- 母函数 / 生成函数思想入门
**使用示例**：
```cpp
#include "algorithm_x/math/generating_function.h"
using namespace algorithm_x::math;
auto ways = generating_function_ways(std::vector<int>{1, 2, 3}, 4);
// ways[4] == 4：1+1+1+1、1+1+2、1+3、2+2
```

---

### `math/linear_algebra.h` — 行列式计算（高斯消元）
**用途**：计算方阵的行列式，奇异矩阵返回 0。
**原理**：高斯消元法，每列先选绝对值最大的主元（部分选主元，提高数值稳定性），行交换时行列式变号，对角线元素连乘即得行列式；选主元时若绝对值小于 eps 判定为奇异矩阵返回 0。
**主要 API**：
```cpp
// 行列式 — 高斯消元法 O(n³)。
// 返回 double，奇异矩阵返回 0。
inline double determinant(std::vector<std::vector<double>> a);
```
**复杂度**：O(n³) 时间 / O(n²) 空间（按值拷贝入参）。
**使用场景**：
- 方阵行列式的数值计算
- 线性代数方程组理论推导（克拉默法则、矩阵可逆性判断）
**使用示例**：
```cpp
#include "algorithm_x/math/linear_algebra.h"
using namespace algorithm_x::math;
std::vector<std::vector<double>> m = {{3, 8}, {4, 6}};
double det = determinant(m);   // -14
```

---

### `math/matrix.h` — 矩阵乘法、矩阵快速幂、斐波那契与高斯消元
**用途**：提供矩阵乘法、矩阵快速幂、基于矩阵快速幂的斐波那契数列，以及解线性方程组的高斯消元。
**原理**：矩阵乘法按 i-k-j 循环实现（跳过零元减少无效运算）；矩阵快速幂用二进制分解（倍增）把 n 次乘法压缩为 O(log n) 次矩阵乘法；斐波那契使用转移矩阵 [[1,1],[1,0]] 的 (n-1) 次幂取左上角；高斯消元用"选主元 + 逐行消元（Gauss-Jordan 风格）"解 Ax = b，无解 / 无穷解返回空向量。
**主要 API**：
```cpp
// 矩阵乘法 — C = A × B, A 为 n×m，B 为 m×p。返回 n×p 矩阵。
template <typename T>
std::vector<std::vector<T>> matrix_mul(
    const std::vector<std::vector<T>>& A,
    const std::vector<std::vector<T>>& B);

// 矩阵快速幂 — A^n，A 为方阵。
template <typename T>
std::vector<std::vector<T>> matrix_pow(std::vector<std::vector<T>> A,
                                        int64_t n);

// 斐波那契数列第 n 项（矩阵快速幂 O(log n)）。
// fib(0)=0, fib(1)=1。
template <typename T>
T fibonacci(int64_t n);

// 高斯消元 — 解 Ax = b，返回解的向量。无解 / 无穷解返回空。
// A 为 n×n 方阵，b 为 n×1，使用 double。
inline std::vector<double> gaussian_elimination(
    std::vector<std::vector<double>> A, std::vector<double> b);
```
**复杂度**：`matrix_mul` O(n·m·p) 时间 / O(n·p) 空间；`matrix_pow` O(sz³·log n) 时间 / O(sz²) 空间；`fibonacci` O(log n) 时间 / O(1) 额外空间；`gaussian_elimination` O(n³) 时间 / O(n²) 空间。
**使用场景**：
- 线性递推加速（斐波那契、常系数线性递推）
- 线性方程组求解、图论中路径计数（邻接矩阵幂）
**使用示例**：
```cpp
#include "algorithm_x/math/matrix.h"
using namespace algorithm_x::math;
int64_t fib = fibonacci<int64_t>(50);          // 12586269025
auto R = matrix_pow(std::vector<std::vector<int>>{{1, 1}, {1, 0}}, 5);
auto x = gaussian_elimination(
    std::vector<std::vector<double>>{{2, 1, -1}, {-3, -1, 2}, {-2, 1, 2}},
    std::vector<double>{8, -11, -3});          // {2, 3, -1}
```

---

### `math/modint.h` — 数论基础：扩展欧几里得、逆元、快速幂、CRT、欧拉函数
**用途**：提供模算术与初等数论的一组基础工具：解 ax + by = gcd(a,b)、求模逆元、快速幂取模、中国剩余定理、欧拉函数。
**原理**：扩展欧几里得递归回溯同时得到 gcd 与一组贝祖系数；模逆元即 a·x ≡ 1 (mod m) 的解（要求 a 与 m 互质）；快速幂用二进制分解在 O(log n) 次乘方内完成；CRT 用 M_i = M/m_i 及其模 m_i 的逆元把多个同余式合并为最小非负解；欧拉函数按质因子使用公式 φ(n) = n·Π(1 - 1/p)。
**主要 API**：
```cpp
// 扩展欧几里得算法 — 解 ax + by = gcd(a, b)。
// 返回 {gcd, x, y}。
inline std::tuple<int64_t, int64_t, int64_t>
extended_gcd(int64_t a, int64_t b);

// 最大公约数。
inline int64_t gcd_ext(int64_t a, int64_t b);

// 模逆元 — a^(-1) mod m，要求 gcd(a, m) = 1。
inline int64_t mod_inverse(int64_t a, int64_t m);

// 快速幂 — a^n % mod。
inline int64_t fast_pow(int64_t a, int64_t n, int64_t mod);

// 中国剩余定理 (CRT)。
// 求解 x ≡ r[i] (mod m[i])，其中所有 m[i] 两两互质。
inline int64_t crt(const std::vector<int64_t>& r,
                    const std::vector<int64_t>& m);

// 欧拉函数 φ(n) — O(√n)。
inline int64_t euler_phi(int64_t n);
```
**复杂度**：`extended_gcd` / `gcd_ext` / `mod_inverse` O(log min(a, m)) 时间 / O(log n) 递归栈；`fast_pow` O(log n) 时间 / O(1) 空间；`crt` O(k·log m) 时间（k 个同余式）/ O(1) 额外空间；`euler_phi` O(√n) 时间 / O(1) 空间。
**使用场景**：
- 模意义下的除法（组合数取模、有理数取模）
- 大指数取模（快速幂）
- 一次同余方程组求解（CRT，模数两两互质）
- 与模数互质的数计数（欧拉函数）
**使用示例**：
```cpp
#include "algorithm_x/math/modint.h"
using namespace algorithm_x::math;
auto [g, x, y] = extended_gcd(30, 12);     // g = 6，且 30x + 12y = 6
int64_t inv = mod_inverse(3, 7);           // 5
int64_t p   = fast_pow(2, 10, 1000);       // 24
int64_t r   = crt({2, 3, 2}, {3, 5, 7});   // 23
int64_t phi = euler_phi(12);               // 4
```

---

### `math/prime.h` — 素数判定、筛法与质因数分解
**用途**：提供素性测试（试除 / Miller-Rabin）、素数筛（埃氏筛 / 线性筛）与大数质因数分解（Pollard-Rho）。
**原理**：试除法只检查到 √n；Miller-Rabin 将 n-1 分解为 d·2^s 后对确定性底数集合做二次探测，配合防溢出的龟速乘 `mul_mod`，在 int64_t 范围内确定无误判；埃氏筛从 p² 开始逐倍剔除合数；线性筛（欧拉筛）保证每个合数被其最小质因子恰好筛掉一次，并顺带记录最小质因子；Pollard-Rho 用伪随机函数 f(v) = v² + 1 (mod n) 与 Floyd 判圈找出非平凡因子，递归配合 Miller-Rabin 完成分解。
**主要 API**：
```cpp
// 试除法判定素数 — O(√n)。
inline bool is_prime_trial(int64_t n);

// 龟速乘（防溢出）— a*b % mod。
inline int64_t mul_mod(int64_t a, int64_t b, int64_t mod);

// 快速幂（乘法用 mul_mod）— a^n % mod。
inline int64_t pow_mod(int64_t a, int64_t n, int64_t mod);

// Miller-Rabin 素数判定（确定性，适用于 int64_t 范围）。
inline bool is_prime_miller_rabin(int64_t n);

// 埃氏筛 — 返回 [0, n] 的素数表 O(n log log n)。
inline std::vector<bool> sieve_bool(std::size_t n);

// 线性筛（欧拉筛）— 同时计算每个数的最小质因子 O(n)。
// 返回 {is_prime, min_prime_factor}。
inline std::pair<std::vector<bool>, std::vector<std::size_t>>
linear_sieve(std::size_t n);

// 最大公约数（迭代版）。
inline int64_t gcd(int64_t a, int64_t b);

// Pollard-Rho 质因数分解 — O(n^(1/4)) 期望。
inline int64_t pollard_rho(int64_t n);

// 递归分解（内部使用，入口见 prime_factors）。
inline void factorize(int64_t n, std::vector<int64_t>& factors);

// 质因数分解（入口函数）。先去掉小因子，再用 Pollard-Rho。
inline std::vector<int64_t> prime_factors(int64_t n);
```
**复杂度**：`is_prime_trial` O(√n)；`mul_mod` / `pow_mod` O(log n)；`is_prime_miller_rabin` O(log³ n)（7 个确定性底数）；`sieve_bool` O(n log log n) 时间 / O(n) 空间；`linear_sieve` O(n) 时间 / O(n) 空间；`gcd` O(log min(a,b))；`pollard_rho` / `prime_factors` 期望 O(n^{1/4})（配合 Miller-Rabin 判定）。
**使用场景**：
- 1e18 以内的素性判定（确定性 Miller-Rabin）
- 区间素数表与最小质因子预处理（线性筛）
- 大整数质因数分解
**使用示例**：
```cpp
#include "algorithm_x/math/prime.h"
using namespace algorithm_x::math;
bool ok = is_prime_miller_rabin(999983);    // true
auto [is_prime, min_p] = linear_sieve(30);  // 素数表 + 最小质因子
auto f = prime_factors(12);                 // {2, 2, 3}
```

---

### `math/principles.h` — 容斥原理与鸽巢原理
**用途**：计算多个集合并集的大小（容斥原理）；判定鸽巢原理成立与否并给出"最满盒子"的最小件数。
**原理**：容斥原理 |A₁∪...∪Aₙ| = Σ|单个集合| − Σ|两两交集| + Σ|三交集| − ...，本实现中 `intersections[i]` 存放下标 i 的二进制位对应交集的大小，按二进制位数奇偶决定加减；鸽巢原理：n 件物品放入 m 个盒子，n > m 时必有盒子至少 2 件；推广版本为 ceil(n/m)。
**主要 API**：
```cpp
// Inclusion-Exclusion Principle: compute union size of n sets.
// intersections[i] = size of intersection of sets indexed by the bits set in i.
// 返回 |A ∪ B ∪ C|。
inline int64_t inclusion_exclusion(const std::vector<int64_t>& intersections);

// Pigeonhole Principle: returns true if placing n items into m boxes
// guarantees at least one box has >1 item.
inline bool pigeonhole(int64_t n, int64_t m);

// Pigeonhole — generalized: minimum number of items in the fullest box.
inline int64_t pigeonhole_max_min(int64_t n, int64_t m);
```
**复杂度**：`inclusion_exclusion` O(2^k) 时间（k 为集合数）/ O(1) 额外空间；`pigeonhole` 与 `pigeonhole_max_min` O(1)。
**使用场景**：
- 计算多个集合的并集大小（去重计数）
- 存在性证明与构造题（鸽巢原理）
**使用示例**：
```cpp
#include "algorithm_x/math/principles.h"
using namespace algorithm_x::math;
// |A|=3, |B|=4, |C|=5，两两交集 1, 2, 1，三交集 0 → 并集大小 8
int64_t u  = inclusion_exclusion({0, 3, 4, 1, 5, 2, 1, 0});
bool g     = pigeonhole(5, 3);              // true
int64_t mx = pigeonhole_max_min(10, 3);     // 4
```

---

### `math/probability.h` — 概率统计：期望与二项分布
**用途**：计算离散随机变量的期望值与二项分布概率。
**原理**：期望按定义 E[X] = Σ p_i·x_i 直接累加；二项分布概率 P(X = k) = C(n,k)·p^k·(1-p)^{n-k}，其中组合系数用 double 乘法公式计算以避免整数溢出。
**主要 API**：
```cpp
// Expected value of a discrete random variable.
// E[X] = sum(p_i * x_i)
inline double expected_value(const std::vector<double>& probs,
                              const std::vector<double>& values);

// Binomial coefficient C(n,k) — helper for binomial probability.
inline double binomial_coeff_double(int n, int k);

// Binomial probability: P(X = k) = C(n,k) * p^k * (1-p)^(n-k)
inline double binomial_probability(int n, int k, double p);
```
**复杂度**：`expected_value` O(n) 时间；`binomial_coeff_double` / `binomial_probability` O(k) 时间；空间均为 O(1)。
**使用场景**：
- 期望类题目的直接计算
- 伯努利试验 / 二项分布概率计算
**使用示例**：
```cpp
#include "algorithm_x/math/probability.h"
using namespace algorithm_x::math;
double ev = expected_value({0.5, 0.5}, {2.0, 4.0});  // 3.0
double pb = binomial_probability(10, 5, 0.5);        // 252 / 1024
```

---

### `math/stirling.h` — 斯特林数与贝尔数
**用途**：计算第一类（无符号）斯特林数、第二类斯特林数与贝尔数，覆盖轮换排列、集合划分与划分方案总数三类组合计数。
**原理**：第一类（无符号）斯特林数 s(n,k) 表示 n 个元素排成 k 个轮换的方案数，递推 s(n,k) = s(n-1,k-1) + (n-1)·s(n-1,k)；第二类斯特林数 S(n,k) 表示 n 个元素分成 k 个非空子集的方案数，递推 S(n,k) = S(n-1,k-1) + k·S(n-1,k)；贝尔数 B(n) = Σₖ S(n,k) 表示 n 个元素所有划分方案总数。
**主要 API**：
```cpp
// Stirling numbers of the first kind (unsigned): s(n,k) = number of
// permutations of n elements with exactly k cycles.
inline int64_t stirling_first(int n, int k);

// Stirling numbers of the second kind: S(n,k) = number of ways to partition
// a set of n elements into k non-empty subsets.
inline int64_t stirling_second(int n, int k);

// Bell number B(n): total number of ways to partition a set of n elements.
inline int64_t bell_number(int n);
```
**复杂度**：`stirling_first` / `stirling_second` O(n·k) 时间 / O(n·k) 空间；`bell_number` 最坏 O(n⁴) 时间（内部逐次调用 `stirling_second`）/ O(n²) 峰值空间。
**使用场景**：
- 圆桌排列 / 轮换计数（第一类）
- 集合划分计数（第二类）
- 划分方案总数（贝尔数）
**使用示例**：
```cpp
#include "algorithm_x/math/stirling.h"
using namespace algorithm_x::math;
int64_t s1 = stirling_first(5, 2);    // 50
int64_t s2 = stirling_second(5, 3);   // 25
int64_t b  = bell_number(5);          // 52
```
