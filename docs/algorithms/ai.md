# 算法文档：`algorithm_x::ai` — AI 与机器学习模块

本模块（`include/algorithm_x/ai/`，12 个头文件）提供教学级 AI 算法实现，覆盖四大类：**搜索与约束满足**（csp、search、minimax）、**经典机器学习**（ml、naive_bayes、decision_tree、more_ai 中的 PCA/MLP）、**进化计算**（evolution、differential_evolution、more_ai 中的蚁群）与**强化学习**（rl、rl_advanced、mdp）。所有实现均为头文件内联、仅依赖标准库，随机算法统一使用 `std::mt19937` 固定种子 42，结果确定性可复现。每个算法在 `tests/ai/` 下配有单元测试，文档中的 API 签名与源码一致。

---

### `ai/csp.h` — 约束满足问题（CSP）
**用途**：解决经典的约束满足问题——N 皇后解的计数与求解、图 k-着色可满足性判定，是回溯搜索、弧一致性传播与局部搜索（最小冲突）三种 CSP 技术的教学实现。
**原理**：
- **N 皇后计数**：逐行放皇后，用"列 / 主对角线 / 副对角线"三个 bool 数组做 O(1) 冲突检测，冲突即剪枝——等价于每放一个皇后就把其影响位置从后续行可用位置中剔除（前向检查式剪枝）。
- **AC-3 着色**：队列存放弧 (X_i, X_j)，revise 时删除 X_i 域中在 X_j 域无任何可取值的颜色；对无环（树形/森林）约束图，弧一致性即完全判定；对含环图，先在剪枝后的域上做确定性回溯补全，返回真实可满足性。
- **最小冲突**：随机初始放置后，每步从冲突皇后中随机选一个移到冲突最少的列，直至无冲突或达到步数上限。
**主要 API**：
```cpp
// N 皇后解计数（回溯 + 前向检查）：n=1→1, n=4→2, n=5→10, n=8→92
inline std::size_t count_n_queens_forward_checking(int n);

// AC-3 弧一致性 k-着色可满足性判定（edges 为无向邻接边，区域编号 0..num_regions-1）
inline bool ac3_map_coloring(const std::vector<std::pair<int, int>>& edges,
                             int num_regions, int num_colors);

// 最小冲突启发式求解 N 皇后，返回 ans[r]=第 r 行皇后的列号；超步未解返回空 vector
inline std::vector<int> min_conflicts_n_queens(int n, int max_steps = 1000);
```
**复杂度**：N 皇后计数最坏指数级（O(n!) 量级），空间 O(n)；AC-3 时间 O(e·d³)（e=边数，d=颜色数），含环图回溯最坏 O(d^n)，空间 O(n+e)；最小冲突每步 O(n)，总 O(max_steps·n)，实践中对大 n 收敛极快，空间 O(n)。
**使用场景**：
- 验证回溯 + 剪枝与启发式局部搜索的对比（N 皇后）；
- 区域/地图着色可行性判定（如澳大利亚 7 区域、图染色问题）；
- 作为 CSP 理论（弧一致性 vs 完全一致性）的学习示例。
**使用示例**：
```cpp
#include "ai/csp.h"
using namespace algorithm_x::ai;

std::size_t s = count_n_queens_forward_checking(8);          // 92
auto sol = min_conflicts_n_queens(8);                        // 合法放置，确定性（种子 42）
bool ok  = ac3_map_coloring({{0,1},{1,2},{2,0}}, 3, 2);      // 三角形：false（不可 2 着色）
bool ok3 = ac3_map_coloring({{0,1},{1,2},{2,0}}, 3, 3);      // true
```

---

### `ai/decision_tree.h` — 决策树（CART + 基尼不纯度）
**用途**：二分类任务的决策树训练与预测，是最基础的监督学习模型。
**原理**：CART（分类回归树）风格——每个内部节点用基尼不纯度（Gini impurity）最小化准则在特征中选出最佳分裂特征，按 `x[f] < 0.5` 二分裂，递归建树；叶子节点存多数类标签。本实现面向教学做了简化：特征是二值的（0/1）、类别是二分类（0/1）、分裂阈值为固定 0.5、最大深度限制防过拟合。
**主要 API**：
```cpp
class DecisionTree {
public:
    DecisionTree(int max_depth = 5);
    ~DecisionTree();
    void fit(const std::vector<std::vector<double>>& X,
             const std::vector<int>& y);
    int predict_single(const std::vector<double>& x) const;
    std::vector<int> predict(const std::vector<std::vector<double>>& X) const;
};
```
**复杂度**：`fit` 时间 O(m·d·max_depth)（m=样本数，d=特征数），`predict` 时间 O(max_depth)；空间 O(节点数)（每个节点动态分配，析构递归释放）。
**使用场景**：
- 学习"递归划分 + 不纯度度量"的决策树原理；
- 二值特征、二分类标签的小规模数据快速建模；
- 作为集成方法（随机森林/GBDT）的对照基准。
**使用示例**：
```cpp
#include "ai/decision_tree.h"
using namespace algorithm_x::ai;

DecisionTree dt(3);                                        // 最大深度 3
dt.fit({{0,0},{0,1},{1,0},{1,1}}, {0,0,0,1});              // 训练
dt.predict_single({1, 1});                                 // 1
auto preds = dt.predict({{0,0},{1,1}});                    // {0, 1}
```

---

### `ai/differential_evolution.h` — 差分进化（DE）
**用途**：求解连续函数的无约束（有边界）全局最小值，属于进化计算中的主流算法。
**原理**：维护 pop_size 个候选解，每代对每个个体随机选三个互异个体 a/b/c，用变异公式 `a + F·(b − c)` 生成差分扰动，再按交叉概率 CR（保证至少一维替换）合成试验个体，与当前个体比较目标函数值、择优保留。参数 F（缩放因子）与 CR（交叉率）控制探索与利用的平衡，边界用 clamp 处理。
**主要 API**：
```cpp
// 最小化 f(x)；返回最优解向量
inline std::vector<double> differential_evolution(
    std::function<double(const std::vector<double>&)> f,
    std::size_t dim,
    const std::vector<double>& lower,
    const std::vector<double>& upper,
    std::size_t pop_size = 50, std::size_t generations = 200,
    double F = 0.8, double CR = 0.9);
```
**复杂度**：时间 O(generations·pop_size·(dim + 单次 f 求值成本))，空间 O(pop_size·dim)。固定种子 42，结果确定可复现。
**使用场景**：
- 无梯度（不可导 / 黑盒）连续优化问题；
- 多峰函数全局寻优的教学实验（如测试中的球面函数 f(x)=x²）；
- 与遗传算法、粒子群对比不同进化策略的收敛行为。
**使用示例**：
```cpp
#include "ai/differential_evolution.h"
using namespace algorithm_x::ai;

auto f = [](const std::vector<double>& x) { return x[0] * x[0]; };
auto r = differential_evolution(f, 1, {-5.0}, {5.0}, 50, 100);
// r[0] ≈ 0.0（逼近最小值点）
```

---

### `ai/evolution.h` — 遗传算法与粒子群优化
**用途**：提供两种经典进化/群体智能算法——遗传算法（GA）求 f(x) 最大值，粒子群优化（PSO）求 f(x) 最小值，用于连续空间全局优化。
**原理**：
- **GA**：实数编码个体，锦标赛选择两个父代，单点交叉（概率 crossover_rate）后逐维高斯式随机变异（概率 mutate_rate），新种群第 0 位保留精英（当前最优个体），逐代进化使适应度上升；
- **PSO**：每个粒子维护位置、速度、个体最优 pbest 与全局最优 gbest，速度更新公式 `v = w·v + c1·r1·(pbest − x) + c2·r2·(gbest − x)`（惯性权重 w=0.7，学习因子 c1=c2=1.5），位置越界 clamp。
**主要 API**：
```cpp
// 遗传算法求 f(x) 最大值（fitness 越大越好），返回最优解向量
inline std::vector<double> genetic_algorithm(
    std::function<double(const std::vector<double>&)> fitness,
    std::size_t dim,
    const std::vector<double>& lower,
    const std::vector<double>& upper,
    std::size_t pop_size = 100, std::size_t generations = 200,
    double mutate_rate = 0.1, double crossover_rate = 0.8);

// 粒子群优化求 f(x) 最小值，返回全局最优位置
inline std::vector<double> particle_swarm(
    std::function<double(const std::vector<double>&)> f,
    std::size_t dim,
    const std::vector<double>& lower,
    const std::vector<double>& upper,
    std::size_t swarm_size = 50, std::size_t iterations = 200);
```
**复杂度**：GA 时间 O(generations·pop_size·dim)，PSO 时间 O(iterations·swarm_size·dim)，均不含 f 求值成本；空间分别为 O(pop_size·dim)、O(swarm_size·dim)。固定种子 42，确定性可复现。
**使用场景**：
- 高维、不可导连续函数的近似全局寻优；
- 学习"选择-交叉-变异"与"社会学习（个体最优 + 群体最优）"两种范式的对比；
- 算法参数（种群规模、变异率、迭代数）敏感性实验。
**使用示例**：
```cpp
#include "ai/evolution.h"
using namespace algorithm_x::ai;

// GA：求 -(x-5)^2+10 的最大值 → x≈5
auto fitness = [](const std::vector<double>& x) {
    return -std::pow(x[0] - 5.0, 2) + 10.0;
};
auto r = genetic_algorithm(fitness, 1, {-10.0}, {10.0}, 200, 300, 0.05, 0.8);

// PSO：求 x² 的最小值 → x≈0
auto f = [](const std::vector<double>& x) { return x[0] * x[0]; };
auto p = particle_swarm(f, 1, {-10.0}, {10.0}, 100, 300);
```

---

### `ai/mdp.h` — 马尔可夫决策过程（MDP）求解
**用途**：给定已知转移模型的马尔可夫决策过程，求解每个状态的最优值函数 V(s) 与（策略迭代的）最优策略，是强化学习的基础模块。
**原理**：
- **值迭代**：贝尔曼最优性方程 `V(s) = max_a Σ prob·(reward + γ·V(s'))` 同步更新（每个状态取动作最优值），直到相邻两次迭代差值 < epsilon 收敛；
- **策略迭代**：交替执行策略评估（固定当前策略，迭代求解 V(s)，内部最多 1000 轮 / delta < 1e-6 提前退出）与策略改进（每个状态贪心替换为最优动作），直至策略稳定。
**主要 API**：
```cpp
// transitions[u][a] = {next_state, prob, reward} 列表；返回各状态值函数 V
inline std::vector<double> value_iteration(
    const std::vector<std::vector<std::tuple<int, double, double>>>& transitions,
    std::size_t num_states, std::size_t num_actions,
    double gamma = 0.9, double epsilon = 1e-6);

// 策略迭代；返回 {V, policy}，policy[s] 为状态 s 的最优动作
inline std::pair<std::vector<double>, std::vector<int>> policy_iteration(
    const std::vector<std::vector<std::tuple<int, double, double>>>& transitions,
    std::size_t num_states, std::size_t num_actions,
    double gamma = 0.9);
```
**复杂度**：每轮更新 O(S²·A)（遍历转移列表），值迭代轮数取决于 γ 与 ε；策略迭代每轮含策略评估（≤1000 次迭代，各 O(S²·A)）+ 策略改进 O(S²·A)，收敛轮数通常远小于值迭代。空间 O(S + S·A·平均分支)。转移表按 `s*num_actions + a` 索引组织。
**使用场景**：
- 已知环境模型的规划问题（如测试中的 2 状态 2 动作确定性转移）；
- 理解"策略评估 ↔ 策略改进"与"值函数直接收敛"两条经典求解路径；
- 作为后续无模型强化学习（Q-Learning/SARSA）的理论对照。
**使用示例**：
```cpp
#include "ai/mdp.h"
using namespace algorithm_x::ai;

// 2 状态 2 动作：状态 1 自循环奖励 10 ⇒ V[1] = 10/(1-0.9) = 100
std::vector<std::vector<std::tuple<int, double, double>>> t(4);
t[0*2+0] = {{0, 1.0, 0.0}};   t[0*2+1] = {{1, 1.0, 0.0}};
t[1*2+0] = {{1, 1.0, 10.0}};  t[1*2+1] = {{0, 1.0, 0.0}};

auto V = value_iteration(t, 2, 2, 0.9, 1e-6);        // V[1] ≈ 100
auto [V2, policy] = policy_iteration(t, 2, 2, 0.9);  // policy[1] == 0（留在状态 1）
```

---

### `ai/minimax.h` — Minimax 与 Alpha-Beta 剪枝
**用途**：零和博弈（井字棋）的完美决策——计算当前局面的最优得分，并配套评估函数与剪枝优化。
**原理**：棋盘用 3×3 向量表示（0=空，1=X 最大方，2=O 最小方）。递归搜索：X 方取子节点得分最大值，O 方取最小值；为使"速胜"优先、"缓败"次之，对终局得分做深度惩罚/补偿（`score ± depth`）。Alpha-Beta 剪枝在搜索中维护上界 alpha、下界 beta，`beta <= alpha` 时剪掉不可能影响结果的子树。
**主要 API**：
```cpp
// 评估：X 胜 +10，O 胜 -10，平局/未终局 0
inline int evaluate_ttt(const std::vector<int>& board);
// 棋盘是否已满
inline bool is_ttt_full(const std::vector<int>& board);
// 纯 Minimax：返回当前局面最优得分
inline int minimax(std::vector<int>& board, int depth, bool is_max);
// Alpha-Beta 剪枝版本
inline int alphabeta(std::vector<int>& board, int depth, int alpha, int beta,
                     bool is_max);
```
**复杂度**：Minimax 时间 O(b^d)（b≈9 分支，d≈9 深度），Alpha-Beta 平均 O(b^(3d/4))、最优序 O(b^(d/2))；空间均 O(d)（递归深度）。井字棋规模下两种算法都能瞬间完成。
**使用场景**：
- 学习零和博弈搜索与剪枝优化，对比两种算法的展开节点数；
- 作为博弈树搜索的入门示例（井字棋）；
- 扩展到其他小棋盘博弈的评估函数设计练习。
**使用示例**：
```cpp
#include "ai/minimax.h"
using namespace algorithm_x::ai;

std::vector<int> board(9, 0);  // 空棋盘
int score = alphabeta(board, 0, -1000, 1000, /*is_max=*/true);
// score >= 0：先手（X）在完美对弈下至少不输
```

---

### `ai/ml.h` — 经典机器学习（KNN / 线性回归 / 逻辑回归 / K-Means）
**用途**：提供四个经典机器学习算法的紧凑实现，覆盖监督学习（分类、回归）与无监督学习（聚类）。
**原理**：
- **KNN**：计算查询点与所有训练样本的欧氏距离平方，取距离最近的 k 个做多数表决（假定标签 0..9）；
- **线性回归**：最小化均方误差，用批量梯度下降（5000 轮、lr=0.01）拟合 `y = w·x + b`（头文件内为简化未用闭式解）；
- **逻辑回归**：sigmoid 输出 + 交叉熵梯度（`pred − y` 恰为 BCE+sigmoid 的梯度形式），2000 轮、lr=0.1 训练二分类；
- **K-Means**：随机选 k 个样本作初始质心（种子 42），交替执行"分配最近质心"与"质心取簇均值"，无点改簇即提前停止。
**主要 API**：
```cpp
// K 近邻分类（多数表决，标签假定 0..9），返回预测标签
inline int knn_classify(const std::vector<std::vector<double>>& train_data,
                        const std::vector<int>& train_labels,
                        const std::vector<double>& query, int k = 3);
// 线性回归 y = w·x + b，返回 {weights, bias}
inline std::pair<std::vector<double>, double>
linear_regression(const std::vector<std::vector<double>>& X,
                  const std::vector<double>& y);
// 逻辑回归二分类（y 为 0/1），返回 {weights, bias}
inline std::pair<std::vector<double>, double>
logistic_regression(const std::vector<std::vector<double>>& X,
                    const std::vector<int>& y);
// K-Means 聚类，返回 {labels, centroids}
inline std::pair<std::vector<int>, std::vector<std::vector<double>>>
kmeans(const std::vector<std::vector<double>>& data, int k,
       int max_iter = 100);
```
**复杂度**：KNN 单次查询 O(m·d + m log m)（m=样本数）；线性/逻辑回归 O(iter·m·d)；K-Means O(iter·m·k·d)。空间分别 O(m)、O(d)、O(d)、O(m + k·d)。
**使用场景**：
- 学习三种主流 ML 范式（懒惰学习 / 梯度下降监督学习 / 迭代聚类）；
- 小规模、低维数据的快速原型实验；
- 对比判别模型（逻辑回归）与实例模型（KNN）的决策边界。
**使用示例**：
```cpp
#include "ai/ml.h"
using namespace algorithm_x::ai;

// KNN
int label = knn_classify({{1,1},{1,2},{2,1},{5,5},{5,6},{6,5}},
                         {0,0,0,1,1,1}, {1.5, 1.5}, 3);        // 0

// 线性回归：y = 2x + 3
auto [w, b] = linear_regression({{1},{2},{3}}, {5,7,9});       // w[0]≈2, b≈3

// K-Means
auto [labels, centroids] = kmeans({{0,0},{0.5,0},{0,0.5},{5,5},{5.5,5},{5,5.5}}, 2);
```

---

### `ai/more_ai.h` — 进阶 AI（蚁群 TSP / PCA / 两层 MLP）
**用途**：聚合三个进阶算法——蚁群算法解 TSP、主成分分析（PCA）降维、两层 MLP 神经网络二分类。
**原理**：
- **ACO**：信息素矩阵初始为 1，每只蚂蚁按"信息素^α × 启发式(1/d)^β"轮盘赌选下一城；走完按 Q/len 在路径上增强信息素，每代全局乘 (1−ρ) 挥发；α=1, β=2, ρ=0.5, Q=100；
- **PCA**：中心化 → 协方差矩阵（除以 n−1）→ 幂迭代逐个求前 k 个主成分，用特征值收缩（残差矩阵减去该成分）保证各成分正交；
- **SimpleMLP**：输入层→隐藏层（ReLU）→输出层（Sigmoid），损失为 BCE，按"输出层 → 隐藏层"逐层反传梯度（epochs、lr 可调），权重用正态分布（σ=0.1，种子 42）初始化。
**主要 API**：
```cpp
// 蚁群算法解 TSP，dist 为 n×n 距离矩阵，返回最优路径（顶点排列）
inline std::vector<int> aco_tsp(const std::vector<std::vector<double>>& dist,
                                int num_ants = 20, int iterations = 100);
// PCA 降维到 k 维，返回 k 个主成分向量（每个长度为 d）
inline std::vector<std::vector<double>> pca(
    const std::vector<std::vector<double>>& data, int k);
// 两层 MLP（ReLU 隐层 + Sigmoid 输出），二分类
class SimpleMLP {
public:
    SimpleMLP(int input_dim, int hidden_dim = 8);
    double predict(const std::vector<double>& x) const;  // 输出 (0,1) 概率
    void fit(const std::vector<std::vector<double>>& X,
             const std::vector<int>& y,
             int epochs = 500, double lr = 0.1);
};
```
**复杂度**：ACO O(iter·ants·n²)；PCA 协方差 O(m·d²)、幂迭代 O(k·iter·d²)；MLP `fit` O(epochs·m·(d·h))。ACO 与 PCA 均确定性（种子 42）。
**使用场景**：
- 组合优化（TSP）的群体智能解法与路径可视化；
- 高维数据可视化前的降维预处理；
- 手工实现反向传播理解神经网络训练（如测试中的 XOR 问题）。
**使用示例**：
```cpp
#include "ai/more_ai.h"
using namespace algorithm_x::ai;

auto tour = aco_tsp({{0,10,15},{10,0,20},{15,20,0}}, 20, 100);   // 3 城 TSP
auto comps = pca({{1.0,2.0},{2.0,3.0},{3.0,4.0}}, 1);            // 1 个 2 维主成分

SimpleMLP mlp(2, 4);                                             // XOR
mlp.fit({{0,0},{0,1},{1,0},{1,1}}, {0,1,1,0}, 2000);
mlp.predict({1, 1});                                             // ≈ 0
```

---

### `ai/naive_bayes.h` — 高斯朴素贝叶斯分类器
**用途**：基于贝叶斯定理 + 特征条件独立假设的生成式二分类器，适合连续特征（高斯分布假设）的快速分类。
**原理**：`fit` 阶段对每个类别统计各维特征的均值与（无偏修正的）方差以及类先验 `prior[c]`；`predict` 阶段用高斯概率密度取对数计算 `log P(c) + Σ log P(x_j|c)`（对数化避免下溢），取后验最大者为预测类。方差用 max(·, 1e-9) 保底防止除零。
**主要 API**：
```cpp
// 高斯特征、二分类（标签 0/1）
class NaiveBayes {
public:
    void fit(const std::vector<std::vector<double>>& X,
             const std::vector<int>& y);
    int predict_single(const std::vector<double>& x) const;
    std::vector<int> predict(const std::vector<std::vector<double>>& X) const;
};
```
**复杂度**：`fit` 时间 O(m·d)、`predict_single` 时间 O(d)（m=样本数，d=特征数）；空间 O(d)（每类均值/方差向量）。训练是单遍统计，非常快。
**使用场景**：
- 高维但特征近似独立的分类任务（如文本分类的特征独立假设）；
- 对比生成式（朴素贝叶斯）与判别式（逻辑回归）分类器的效果差异；
- 需要可解释、训练极快的基线分类器。
**使用示例**：
```cpp
#include "ai/naive_bayes.h"
using namespace algorithm_x::ai;

NaiveBayes nb;
nb.fit({{1.0,2.0},{2.0,3.0},{5.0,6.0},{6.0,7.0}}, {0,0,1,1});
nb.predict_single({1.5, 2.5});   // 0（靠近类 0 的样本）
nb.predict_single({5.5, 6.5});   // 1
```

---

### `ai/rl.h` — Q-Learning（网格世界）
**用途**：无模型强化学习的入门算法——在网格世界中训练智能体，学会从任意起点走到目标格子的策略。
**原理**：Q 表按 `(state, action)` 存于 `std::map`，state 由 `r*cols+c` 编码，动作 4 方向（0 上 / 1 右 / 2 下 / 3 左）。每轮从随机非障碍非目标格子出发，ε-贪心选动作（探索率 epsilon），执行一步（撞障碍/边界原地不动），奖励"每步 −0.1、到达目标 +10"，用离策略更新 `Q ← Q + α·(reward + γ·max_a Q(s',a) − Q)`。
**主要 API**：
```cpp
// grid: 0=通路, 1=障碍, 2=目标
class QLearning {
public:
    QLearning(const std::vector<std::vector<int>>& grid,
              double alpha = 0.1, double gamma = 0.9, double epsilon = 0.1);
    void train(int episodes = 1000);
    int best_action(int state) const;              // 0 上 / 1 右 / 2 下 / 3 左
    std::vector<std::pair<int, int>> get_path(int start_r, int start_c) const;
    int rows() const;
    int cols() const;
};
```
**复杂度**：`train` 时间 O(episodes·(steps·(4 + log|Q|)))，每步要查 Q 表（std::map，O(log|Q|)）；`get_path` O(rows·cols)。空间 O(状态数×4)。训练确定性（种子 42）。
**使用场景**：
- 理解时间差分（TD）与离策略（off-policy）学习；
- 小规模网格路径规划教学（迷宫寻路）；
- 作为比较 SARSA（在策略）与 Q-Learning 差异的基础。
**使用示例**：
```cpp
#include "ai/rl.h"
using namespace algorithm_x::ai;

QLearning agent({{0,0,0},{0,0,0},{0,0,2}}, 0.1, 0.9, 0.1);  // 3x3 网格，右下角为目标
agent.train(500);
auto path = agent.get_path(0, 0);   // 从 (0,0) 到目标的路径点序列
agent.best_action(0);               // 起始格的最优动作
```

---

### `ai/rl_advanced.h` — SARSA（在策略 TD 控制）
**用途**：Q-Learning 的"在策略（on-policy）"对照实现——同样解决网格世界寻路，但更新时使用实际执行的下一步动作。
**原理**：状态-动作对用 `(r, c, a)` 自定义 Key 哈希存于 `unordered_map`。每轮随机起点（避开障碍与目标），ε-贪心选出动作 a，执行后获得 `(s', a')` 并立即用同一策略选出 a'，按 SARSA 更新 `Q(s,a) ← Q(s,a) + α·(reward + γ·Q(s',a') − Q(s,a))`；到达目标奖励 +100、其余步 −1。与 Q-Learning 用 max 不同，SARSA 用实际动作 a' 的 Q 值，策略更保守。
**主要 API**：
```cpp
// grid: 0=通路, 1=障碍, 2=目标
class SARSA {
public:
    SARSA(const std::vector<std::vector<int>>& grid,
          double alpha = 0.1, double gamma = 0.9, double epsilon = 0.1);
    void train(int episodes);
    std::vector<std::pair<int, int>> get_path(int start_r, int start_c) const;
};
```
**复杂度**：`train` 时间 O(episodes·steps)，Q 表为 `unordered_map` 均摊 O(1) 访问；`get_path` O(rows·cols)。空间 O(状态数×4)。训练确定性（`std::mt19937` 种子 42）。
**使用场景**：
- 对比 SARSA（在策略、更稳）与 Q-Learning（离策略、更激进）在带"危险"奖励环境中的表现差异；
- 学习 TD(0) 控制在策略版本的更新公式；
- 简单机器人导航教学。
**使用示例**：
```cpp
#include "ai/rl_advanced.h"
using namespace algorithm_x::ai;

SARSA agent({{0,0},{0,2}}, 0.1, 0.9, 0.1);   // 2x2 网格，右下角为目标
agent.train(500);
auto path = agent.get_path(0, 0);            // 从 (0,0) 出发的路径
```

---

### `ai/search.h` — A* 搜索与模拟退火
**用途**：提供两种经典搜索/优化算法——A* 网格路径规划（启发式图搜索）与模拟退火（连续函数全局最小化）。
**原理**：
- **A\***：开放表用按 f = g + h 排序的小顶堆，g 为起点步数、h 为到目标的曼哈顿距离（可采纳启发），四方向扩展；到达目标时经 `came_from` 反推重建路径，无解返回空；
- **模拟退火**：当前解 x 用正态分布扰动生成邻域（邻域宽度随温度收缩），`delta < 0` 或按 `exp(−delta/temp)` 概率接受较差解，温度每步 ×0.999 冷却，记录历史最优。
**主要 API**：
```cpp
// 网格位置（提供 std::hash 特化，可直接用于 unordered_map/set）
struct GridPos {
    int r, c;
    bool operator==(const GridPos& o) const { return r == o.r && c == o.c; }
};

// A* 网格路径规划（grid: 0=通路, 1=障碍），返回起点到终点的路径点序列，无解返回空
inline std::vector<GridPos> astar(const std::vector<std::vector<int>>& grid,
                                  GridPos start, GridPos goal);

// 模拟退火求 f(x) 在 [lo, hi] 上的最小值（连续一维）
inline double simulated_annealing(std::function<double(double)> f,
                                  double lo, double hi,
                                  int iterations = 10000);
```
**复杂度**：A* 时间 O(V log V)（V=rows·cols 节点，四方向边），空间 O(V)；模拟退火 O(iterations)。两者均为确定性（种子 42，A* 无随机）。
**使用场景**：
- 网格地图最短路径规划（含障碍绕行）；
- 学习启发式搜索中"可采纳启发 + 优先队列"的组合；
- 一维连续函数全局寻优的退火演示（对比爬山法的局部最优问题）。
**使用示例**：
```cpp
#include "ai/search.h"
using namespace algorithm_x::ai;

auto path = astar({{0,0,0},{0,1,0},{0,0,0}}, {0,0}, {2,2});  // 绕过中心障碍
// path.front() == {0,0}, path.back() == {2,2}

double x = simulated_annealing([](double v) { return v * v; }, -5.0, 5.0, 20000);
// x ≈ 0.0（最小值点）
```
