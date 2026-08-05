#pragma once

#include <cstddef>
#include <queue>
#include <stack>
#include <vector>

namespace algorithm_x {
namespace ds {

// Graph — 有向/无向图的邻接表存储，顶点从 0 到 V-1 编号。
// // 提供遍历方法：dfs / bfs / topological_sort。
class Graph {
public:
    explicit Graph(std::size_t vertices, bool directed = false)
        : V_(vertices), directed_(directed), adj_(vertices) {}

    void add_edge(std::size_t u, std::size_t v) {
        adj_[u].push_back(v);
        if (!directed_) {
            adj_[v].push_back(u);
        }
    }

    // DFS — 给定起点的深度优先遍历，对每个访问的顶点回调 f
    template <typename Func>
    void dfs(std::size_t start, Func f) const {
        std::vector<bool> visited(V_, false);
        std::stack<std::size_t> stk;
        stk.push(start);
        while (!stk.empty()) {
            std::size_t u = stk.top();
            stk.pop();
            if (visited[u]) continue;
            visited[u] = true;
            f(u);
            // reverse push to match recursive DFS order
            for (auto it = adj_[u].rbegin(); it != adj_[u].rend(); ++it) {
                if (!visited[*it]) stk.push(*it);
            }
        }
    }

    // BFS — 给定起点的广度优先遍历
    template <typename Func>
    void bfs(std::size_t start, Func f) const {
        std::vector<bool> visited(V_, false);
        std::queue<std::size_t> q;
        q.push(start);
        visited[start] = true;
        while (!q.empty()) {
            std::size_t u = q.front();
            q.pop();
            f(u);
            for (std::size_t v : adj_[u]) {
                if (!visited[v]) {
                    visited[v] = true;
                    q.push(v);
                }
            }
        }
    }

    // 拓扑排序（Kahn 算法），仅有向图有效。存在环时返回空 vector。
    std::vector<std::size_t> topological_sort() const {
        std::vector<int> indegree(V_, 0);
        for (std::size_t u = 0; u < V_; ++u) {
            for (std::size_t v : adj_[u]) {
                ++indegree[v];
            }
        }
        std::queue<std::size_t> q;
        for (std::size_t u = 0; u < V_; ++u) {
            if (indegree[u] == 0) q.push(u);
        }
        std::vector<std::size_t> result;
        while (!q.empty()) {
            std::size_t u = q.front();
            q.pop();
            result.push_back(u);
            for (std::size_t v : adj_[u]) {
                if (--indegree[v] == 0) q.push(v);
            }
        }
        if (result.size() != V_) return {};  // cycle detected
        return result;
    }

    std::size_t vertices() const { return V_; }
    bool is_directed() const { return directed_; }
    const std::vector<std::size_t>& neighbors(std::size_t u) const { return adj_[u]; }

private:
    std::size_t V_;
    bool directed_;
    std::vector<std::vector<std::size_t>> adj_;
};

}  // namespace ds
}  // namespace algorithm_x
