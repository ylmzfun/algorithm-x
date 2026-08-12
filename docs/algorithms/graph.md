# 图论算法（`include/algorithm_x/graph/`）

本文档覆盖图论模块的 **14 个头文件**：连通性（SCC / 割点 / 桥 / 双连通分量）、最短路（Dijkstra / Bellman-Ford / Floyd-Warshall / SPFA / Johnson）、最小生成树（Kruskal / Prim）、网络流（Dinic 最大流 / 最小割 / 最小费用最大流）、二分图匹配（匈牙利 / KM）、以及欧拉路径、哈密顿路径与 2-SAT。

所有 API 均位于 `namespace algorithm_x::graph`，图以邻接表 `std::vector<std::vector<std::size_t>>`（无权图）或 `std::vector<std::vector<std::pair<std::size_t, T>>>`（带权图）表示；`std::size_t` 为顶点编号，`-1`（即 `static_cast<std::size_t>(-1)` / 返回 `long` 时直接是 `-1`）表示「未匹配 / 不存在」。以下条目顺序与头文件清单一致。

---

### `graph/biconnected.h` — 点双连通分量（BCC）
**用途**：将无向图划分为若干个极大点双连通子图（不含割点的极大连通块），用于分析图的健壮性与环结构（如判断每条边是否属于某个环）。
**原理**：基于 Tarjan 深度优先搜索。用 `dfn`（首次访问时间戳）与 `low`（子树内能回溯到的最早时间戳）记录信息；用边栈维护当前路径上的边。当 `low[v] >= dfn[u]` 时，`(u, v)` 子树内的边栈内容恰好构成一个双连通分量，弹出并去重为顶点集合。
**主要 API**：
```cpp
// Tarjan 算法求双连通分量 (Biconnected Components / Blocks).
// 每个分量是一个点集（不含割点的极大双连通子图）。
std::vector<std::vector<std::size_t>>
biconnected_components(const std::vector<std::vector<std::size_t>>& adj);
```
**复杂度**：时间 O(V + E) / 空间 O(V + E)
**使用场景**：图的可靠性与冗余分析；判定每条边是否位于至少一个环中（树边单独构成 BCC）；无向图缩「块」后进行树形 DP。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<std::size_t>> adj(4);
adj[0] = {1}; adj[1] = {0, 2}; adj[2] = {1, 3}; adj[3] = {2};  // 一条链
auto bcc = biconnected_components(adj);   // 树：每条边各是一个 BCC
// bcc.size() == 3，每个分量大小为 2
```

---

### `graph/connectivity.h` — 连通性：Tarjan SCC / 割点 / 桥
**用途**：一次提供三个经典连通性问题：有向图强连通分量（Tarjan）、无向图割点、无向图桥。三者共用同一套 `dfn / low` 思想，是图论连通性分析的基石。
**原理**：Tarjan 算法在 DFS 过程中维护 `dfn` 与 `low`。SCC：`dfn[u] == low[u]` 时弹出栈内节点组成一个分量；割点：`low[v] >= dfn[u]`（根节点需子树数 > 1）；桥：`low[v] > dfn[u]`。其中 `tarjan_scc` 返回的分量编号按 **逆拓扑序** 排列（编号越小越靠拓扑序后面）。
**主要 API**：
```cpp
// ---- Tarjan SCC, O(V+E) ----
// Returns {component_id, component_count}.
// Component IDs are in reverse topological order (lower id = later in topo).
std::pair<std::vector<std::size_t>, std::size_t>
tarjan_scc(const std::vector<std::vector<std::size_t>>& adj);

// ---- Articulation Points (Cut Vertices) ----
std::vector<std::size_t> articulation_points(
    const std::vector<std::vector<std::size_t>>& adj);

// ---- Bridges ----
std::vector<std::pair<std::size_t, std::size_t>> bridges(
    const std::vector<std::vector<std::size_t>>& adj);
```
**复杂度**：三者均为 时间 O(V + E) / 空间 O(V + E)
**使用场景**：SCC 缩点后处理 DAG 问题（如 2-SAT、可达性）；割点 / 桥用于网络脆弱性分析、判断图是否「点/边连通」。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<std::size_t>> adj = {{1}, {2}, {0}, {}};  // 0→1→2→0, 3 孤立
auto [comp, cnt] = tarjan_scc(adj);       // cnt == 2，comp[0]==comp[1]==comp[2]
auto cuts = articulation_points({{1}, {0, 2, 3}, {1, 3}, {1, 2}}); // {1}：顶点 1 是割点
auto br = bridges({{1, 2}, {0, 2}, {0, 1, 3}, {2}});  // 仅 2-3 是桥
```

---

### `graph/euler.h` — 欧拉路径 / 欧拉回路
**用途**：在无向图中求一条经过每条边恰好一次的路径（欧拉路径）或回路（欧拉回路），用于「一笔画」类问题。
**原理**：Hierholzer 算法。先检查度数条件（奇度顶点数必须为 0 或 2，否则无解），再从奇度顶点（或 0 号点）出发，沿边深度遍历并删除已用边，将无路可走的顶点压入结果栈，最终得到顶点序列；最后校验所有边都被用完（否则图不连通，无解）。
**主要 API**：
```cpp
// 无向图欧拉路径/回路（Hierholzer 算法）。
// 返回路径上的顶点序列，不存在返回空。
std::vector<std::size_t> euler_path(
    std::vector<std::vector<std::size_t>> adj);   // 按值传入，内部会修改
```
**复杂度**：时间 O(E)（均摊；本实现反边删除采用线性扫描，最坏 O(V·E)）/ 空间 O(V + E)
**使用场景**：一笔画问题、字串拼接（把单词首尾字母建模为边）、欧拉回路存在的判定。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<std::size_t>> adj(4);
adj[0] = {1, 3}; adj[1] = {0, 2}; adj[2] = {1, 3}; adj[3] = {0, 2};
auto path = euler_path(adj);      // 存在欧拉回路，path.size() > 0
std::vector<std::vector<std::size_t>> bad(3);
bad[0] = {1}; bad[1] = {0};       // 顶点 2 孤立，图不连通
auto none = euler_path(bad);      // 返回空
```

---

### `graph/hamiltonian.h` — 哈密顿路径（Held-Karp 状态压缩 DP）
**用途**：判定无向/有向图是否存在经过每个顶点恰好一次的路径（哈密顿路径）并输出其一。此为 NP 完全问题，仅适合小规模图（n ≤ 20）。
**原理**：Held-Karp 动态规划：`dp[mask][i]` 表示「恰好经过 `mask` 中所有点且终点为 `i`」的路径是否存在；转移枚举 `j ∉ mask` 且 `adj[i][j]` 有边，`dp[mask|1<<j][j] = true` 并记录前驱 `prev`，最后从全满状态回溯还原路径。
**主要 API**：
```cpp
// 哈密顿路径 — Held-Karp DP O(n² · 2ⁿ)，n ≤ 20。
// adj: 邻接矩阵（true = 有边）。返回顶点序列或空。
std::vector<std::size_t> hamiltonian_path(
    const std::vector<std::vector<bool>>& adj);
```
**复杂度**：时间 O(n² · 2ⁿ) / 空间 O(n · 2ⁿ)
**使用场景**：n ≤ 20 的小规模 NP 完全问题；TSP 的判定子问题（配合最小化可改造为求最小权哈密顿圈）。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<bool>> adj(3, std::vector<bool>(3, false));
adj[0][1] = adj[1][2] = true;      // 0 → 1 → 2
auto p = hamiltonian_path(adj);    // 返回 {0, 1, 2}
```

---

### `graph/johnson.h` — Johnson 全源最短路径
**用途**：求有向带权图所有点对之间的最短路径；支持负权边（但图中不得有负环），比裸跑 n 次 Bellman-Ford 更快。
**原理**：先加一个虚拟源点，用 Bellman-Ford 求势函数 `h[v]`，再对每条边做重赋权 `w' = w + h[u] - h[v]`（保证非负且最短路径不变），最后对每个顶点跑一次 Dijkstra，并将结果还原 `dist = d - h[s] + h[v]`。
**主要 API**：
```cpp
// Johnson 全源最短路径 O(V² log V + VE)。
// 支持负权边，无负环。返回 dist[i][j]。
template <typename T>
std::vector<std::vector<T>> johnson(
    const std::vector<std::vector<std::pair<std::size_t, T>>>& adj);
```
**复杂度**：时间 O(V² log V + V·E) / 空间 O(V²)
**使用场景**：稀疏图（E 远小于 V²）且带负权边的全源最短路；竞赛中比 Floyd-Warshall 更快的大图全源最短路。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<std::pair<std::size_t, int>>> adj(3);
adj[0] = {{1, 2}}; adj[1] = {{2, -1}}; adj[2] = {{0, 4}};   // 含负权边、无负环
auto dist = johnson(adj);   // dist[0][2] == 1（0→1→2）
```

---

### `graph/km.h` — KM 算法（二分图最大权完美匹配）
**用途**：求二分图（左右各 n 个点，完全带权）的权值总和最大的完美匹配。常用于指派 / 分配问题。
**原理**：维护顶标 `labelL / labelR` 使恒有 `labelL[u] + labelR[v] >= cost[u][v]`，相等子图上的匹配不断通过增广路扩展；找不到增广路时按最小松弛量 `d = min slack` 调整顶标，保证相等子图规模单调增长，最终得到最优匹配（DFS 增广 + 松弛优化，O(n³)）。
**主要 API**：
```cpp
// KM 算法 — O(n³) 最大权二分图完美匹配。
// cost: n×n 矩阵，cost[i][j] 为左部 i 到右部 j 的权重（整数）。
// Returns {matchL, total_cost}, matchL[i] = 匹配的右部编号。
std::pair<std::vector<int>, int>
km_algorithm(const std::vector<std::vector<int>>& cost);
```
**复杂度**：时间 O(n³) / 空间 O(n²)
**使用场景**：任务指派（n 个任务分配给 n 个人使总收益最大）；求最大权匹配（求最小权时可将权值取负）。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<int>> cost = {{3, 2}, {4, 1}};
auto [match, total] = km_algorithm(cost);   // total == 6：0→1(2) + 1→0(4)
```

---

### `graph/kosaraju.h` — Kosaraju 强连通分量
**用途**：求有向图的强连通分量（SCC），与 `connectivity.h` 中的 `tarjan_scc` 功能等价但采用两遍 DFS 思路。
**原理**：第一遍 DFS 在原图上记录顶点出栈序；构造反向图；第二遍 DFS 按出栈序逆序在反图上遍历，每次 DFS 到达的点集即一个 SCC。反图上天然保证每个 SCC 收缩后形成 DAG。
**主要 API**：
```cpp
// Kosaraju 强连通分量 — O(V+E)。
// 返回 {comp, comp_cnt}，comp[u] 为 u 所属分量编号。
std::pair<std::vector<std::size_t>, std::size_t>
kosaraju_scc(const std::vector<std::vector<std::size_t>>& adj);
```
**复杂度**：时间 O(V + E) / 空间 O(V + E)
**使用场景**：需要显式构造反图的 SCC 问题；SCC 缩点后做拓扑排序 / 可达性统计；作为理解「两遍 DFS」范式的教学实现。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<std::size_t>> adj(4);
adj[0] = {1}; adj[1] = {2}; adj[2] = {0}; adj[3] = {};   // SCC：{0,1,2} 与 {3}
auto [comp, cnt] = kosaraju_scc(adj);   // cnt == 2
```

---

### `graph/min_cost_flow.h` — 最小费用最大流
**用途**：在带容量、带单位费用的网络（类 `MinCostMaxFlow` 实例）中求从源点 `s` 到汇点 `t` 的最大流，且在该最大流量下总费用最小。
**原理**：Successive Shortest Path（连续最短路增广）：每次用「势能 + Dijkstra」在当前残量网络中找费用最小的增广路（势能消除负权边，避免负环影响），沿路增广并累计费用，直到无可增广路。边以 `(u, v, cap, cost)` 形式添加，自动附带反向边 `(v, u, 0, -cost)`。
**主要 API**：
```cpp
class MinCostMaxFlow {
public:
    MinCostMaxFlow(std::size_t n);
    void add_edge(std::size_t u, std::size_t v, int cap, int cost);
    // Returns {max_flow, min_cost}.
    std::pair<int, int> solve(std::size_t s, std::size_t t);
};
```
**复杂度**：时间 O(F · E log V)（F 为最大流量，每次增广一次 Dijkstra）/ 空间 O(V + E)
**使用场景**：带成本的运输 / 分配问题（如最小费用运输、任务调度）；最大流 + 单位费用求最短路变体。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
MinCostMaxFlow mcmf(2);
mcmf.add_edge(0, 1, 5, 2);                 // u, v, cap, cost
auto [flow, cost] = mcmf.solve(0, 1);      // flow == 5, cost == 10
```

---

### `graph/min_cut.h` — 最小割（Dinic 实现）
**用途**：求有向带容量网络的最小 s-t 割（一组边，删除后 s、t 不连通，容量和最小），同时给出割的 S 侧顶点集合。
**原理**：由最大流最小割定理，最小割容量 = 最大流值。先用 Dinic 求出最大流，再在残量网络上从源点 BFS，可达的顶点构成 S 侧，S 侧到 T 侧的割边集合即最小割（本实现返回 S 侧顶点集合）。
**主要 API**：
```cpp
// Min-Cut via Dinic. Returns {max_flow_value, S_side_vertices}.
// S_side[u] = true if vertex u is reachable from src in residual graph.
std::pair<int, std::vector<bool>>
min_cut(std::vector<std::vector<int>>& capacity, std::size_t src, std::size_t sink);
```
**复杂度**：时间 O(V² · E)（Dinic 一般上界，实际通常远快）/ 空间 O(V²)（输入容量矩阵）+ O(V + E)
**使用场景**：图割问题（如图像分割、闭合子图最大权问题）；需要同时输出割边 / S 侧集合而非仅最大流值。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<int>> cap = {{0, 10, 0}, {0, 0, 5}, {0, 0, 0}};
auto [flow, side] = min_cut(cap, 0, 2);   // flow == 5，side = {true, true, false}
```

---

### `graph/mst.h` — 最小生成树（Kruskal / Prim）
**用途**：求无向带权连通图的最小生成树（MST）——连接所有顶点且总边权最小的树。提供两种经典实现供选择。
**原理**：Kruskal 按边权升序排序，用并查集（含路径压缩）贪心加入不成环的边，直至选出 n-1 条；Prim 从 0 号点出发，每次选择「已入树集合」连向未入树顶点的最小权边扩展（本实现为 O(V²) 朴素版，`min_edge` 数组维护最近距离）。
**主要 API**：
```cpp
struct Edge {
    std::size_t u;
    std::size_t v;
    int w;
};

// ---- Kruskal (edge-list, O(E log E)) ----
// Returns {mst_edges, total_weight}.
std::pair<std::vector<Edge>, int> kruskal(std::vector<Edge> edges,
                                          std::size_t n);

// ---- Prim (adjacency-list, O(V^2)) ----
// Returns total MST weight; -1 if graph is disconnected.
int prim(const std::vector<std::vector<std::pair<std::size_t, int>>>& adj);
```
**复杂度**：Kruskal 时间 O(E log E) / 空间 O(V)；Prim 时间 O(V²) / 空间 O(V)
**使用场景**：Kruskal 适合边集较小的稀疏图且天然带「第 k 小生成树」等扩展；Prim 朴素版适合稠密图（E 接近 V²）或需要输出 MST 总权值的场景。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<Edge> edges = {{0, 1, 2}, {0, 3, 6}, {1, 2, 3}, {1, 3, 1}, {1, 4, 5}, {2, 4, 4}};
auto [mst, total] = kruskal(edges, 5);     // total == 10，mst.size() == 4
std::vector<std::vector<std::pair<std::size_t, int>>> adj(5);
for (auto& e : edges) { adj[e.u].emplace_back(e.v, e.w); adj[e.v].emplace_back(e.u, e.w); }
int t2 = prim(adj);                        // t2 == 10；图不连通时返回 -1
```

---

### `graph/network_flow.h` — 最大流与二分图匹配（Dinic / 匈牙利）
**用途**：提供 Dinic 最大流（含类封装）与二分图最大匹配（DFS 增广路 / 匈牙利）两个常用网络流工具。最大流用于容量网络中的流量最大化，匹配用于二分图配对问题。
**原理**：Dinic 通过 BFS 分层（level graph）+ DFS 多路增广（当前弧优化 `iter`）反复推进，直到无法增广；`add_edge` 同时插入容量为 0 的反向边。`bipartite_matching` 对每个左部点做 DFS 增广，能「抢」到已匹配右部点时通过递归重新匹配来实现最大匹配，O(V·E)。
**主要 API**：
```cpp
// ---- Dinic Max Flow ----
// Usage:
//   DinicGraph g(V);
//   g.add_edge(u, v, cap);
//   int max_flow = g.max_flow(src, sink);
class DinicGraph {
public:
    struct Edge {
        std::size_t to, rev;
        int cap;
    };
    explicit DinicGraph(std::size_t n);
    void add_edge(std::size_t u, std::size_t v, int cap);
    int max_flow(std::size_t s, std::size_t t);
};

// ---- Bipartite Matching (Hungarian / DFS augmenting path), O(VE) ----
// Returns matchL[u] = v, or -1 if unmatched.
std::vector<long> bipartite_matching(
    std::size_t L, std::size_t R,
    const std::vector<std::vector<std::size_t>>& adj);
```
**复杂度**：Dinic 时间 O(V² · E)（一般上界，单位容量图上为 O(E√V)）/ 空间 O(V + E)；二分图匹配 时间 O(V·E) / 空间 O(L + R)
**使用场景**：最大流（食堂配餐、最大不相交路径等）；二分图最大匹配（课程分配、棋盘覆盖、最小点覆盖的转化）。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
DinicGraph g(3);
g.add_edge(0, 1, 10); g.add_edge(1, 2, 10);
int mf = g.max_flow(0, 2);                    // mf == 10
auto match = bipartite_matching(2, 2, {{0, 1}, {0, 1}});  // 完美匹配，两个 -1 之外的都非 -1
```

---

### `graph/shortest_path.h` — 最短路径（Dijkstra / Bellman-Ford / Floyd-Warshall 聚合头）
**用途**：聚合三种最短路算法：单源非负权（Dijkstra）、单源可负权并检测负环（Bellman-Ford）、全源（Floyd-Warshall），按图的性质选择合适算法。
**原理**：Dijkstra 用优先队列每次取当前距离最小的未确定点松弛邻边；Bellman-Ford 对全部边做 n-1 轮松弛，第 n 轮仍能松弛即存在负环；Floyd-Warshall 以 k 为中间点三重循环松弛 `dist[i][j]`，结束后 `dist[i][i] < 0` 即存在负环。
**主要 API**：
```cpp
// Dijkstra — non-negative single-source shortest path, O((V+E) log V).
template <typename T>
std::vector<T> dijkstra(
    const std::vector<std::vector<std::pair<std::size_t, T>>>& adj,
    std::size_t src);

// Bellman-Ford — handles negative edge weights, O(VE).
template <typename T>
std::pair<std::vector<T>, bool> bellman_ford(
    const std::vector<std::tuple<std::size_t, std::size_t, T>>& edges,
    std::size_t n, std::size_t src);

// Floyd-Warshall — all-pairs shortest path, O(V^3).
template <typename T>
std::pair<std::vector<std::vector<T>>, bool> floyd_warshall(
    std::vector<std::vector<T>> dist);
```
**复杂度**：Dijkstra 时间 O((V+E) log V) / 空间 O(V)；Bellman-Ford 时间 O(V·E) / 空间 O(V)；Floyd-Warshall 时间 O(V³) / 空间 O(V²)
**使用场景**：Dijkstra 用于非负权大图单源最短路；Bellman-Ford 用于存在负权边（或需检测负环）的场景；Floyd-Warshall 用于 n ≤ 500 的全源最短路 / 传递闭包。注意：不可达顶点距离为 `INF`，输入 `dist[i][i]` 应为 0、无边处为 `INF`。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<std::pair<std::size_t, int>>> adj(5);
adj[0] = {{1, 1}, {3, 4}}; adj[1] = {{0, 1}, {2, 2}, {4, 3}};
auto d = dijkstra(adj, 0);                    // d[2] == 3
std::vector<std::tuple<std::size_t, std::size_t, int>> es = {{0, 1, 4}, {0, 2, 5}, {1, 2, -3}};
auto [dist, neg] = bellman_ford(es, 3, 0);    // dist[2] == 1，neg == false
```

---

### `graph/spfa.h` — SPFA 最短路（队列版 Bellman-Ford）
**用途**：带负权边的单源最短路，并能检测从源点可达的负环；通常比裸 Bellman-Ford 快，适合竞赛中「负权 + 稀疏图」场景。
**原理**：只在距离被更新的顶点入队（队列版 Bellman-Ford）。每出队一个顶点就松弛其邻边；记录每个顶点的入队次数 `cnt`，当某点入队超过 n 次（`cnt[v] > n`）时判定存在负环，立即返回 `{dist, true}`。
**主要 API**：
```cpp
// SPFA — Shortest Path Faster Algorithm (queue-based Bellman-Ford).
// Returns {distances, has_negative_cycle}.
template <typename T>
std::pair<std::vector<T>, bool>
spfa(const std::vector<std::vector<std::pair<std::size_t, T>>>& adj,
     std::size_t src);
```
**复杂度**：时间 平均 O(E)、最坏 O(V·E) / 空间 O(V)
**使用场景**：负权边的单源最短路；检测源点可达负环（此时最短路不存在）；图论建模中边的权值随状态变化的变体。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
std::vector<std::vector<std::pair<std::size_t, int>>> adj(4);
adj[0] = {{1, 1}, {2, 4}}; adj[1] = {{2, 2}, {3, 5}}; adj[2] = {{3, 1}};
auto [d, neg] = spfa(adj, 0);   // d[3] == 4，neg == false
adj = {{{1, 1}}, {{2, -1}}, {{0, -1}}};
bool has = spfa(adj, 0).second; // has == true（存在负环 0→1→2→0）
```

---

### `graph/two_sat.h` — 2-SAT 可满足性判定
**用途**：判定由形如「(u OR v)」（可带取反）的二元子句组成的布尔公式是否可满足，并给出一组可行赋值。
**原理**：每个变量拆成两个点（真 / 假），子句 `(u OR v)` 转化为两条蕴含边 `¬u → v` 与 `¬v → u`；用 Tarjan SCC 求强连通分量，若某变量的真、假两点同属一个分量则不可满足；否则按分量编号比较（Tarjan 编号为逆拓扑序）确定赋值：`comp[2i] > comp[2i+1]` 时变量为真。
**主要 API**：
```cpp
// 2-SAT solver using Tarjan SCC.
// n variables. add_clause(u, u_neg, v, v_neg):
//   u_neg=true means NOT u. So (u OR v) = add_clause(u, false, v, false).
// Returns assignment (index by variable) or empty if unsatisfiable.
class TwoSAT {
public:
    explicit TwoSAT(std::size_t n);
    void add_clause(std::size_t u, bool u_neg,
                    std::size_t v, bool v_neg);
    std::vector<bool> solve();
};
```
**复杂度**：时间 O(V + E)（V = 2n 个节点）/ 空间 O(V + E)
**使用场景**：互斥约束类问题（安排 / 染色 / 选课）；任何可转化为二元布尔约束的判定问题。
**使用示例**：
```cpp
using namespace algorithm_x::graph;
TwoSAT ts(2);
ts.add_clause(0, false, 1, true);    // (x0 OR ¬x1)
auto assign = ts.solve();            // 非空即可满足
TwoSAT bad(1);
bad.add_clause(0, false, 0, false);  // (x0) 与 (¬x0)
bad.add_clause(0, true, 0, true);    // 同时要求 x0 与 ¬x0：不可满足
EXPECT_TRUE(bad.solve().empty());    // 返回空向量
```
