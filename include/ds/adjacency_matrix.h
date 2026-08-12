#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace ds {

// AdjacencyMatrix — 邻接矩阵。
// 用 V x V 的二维数组存储边权，add_edge / has_edge / get_weight 均为 O(1)。
// 无向图在 add_edge 时同步写入 (u, v) 与 (v, u)，保证矩阵对称；
// 有向图只写入 (u, v)。
class AdjacencyMatrix {
public:
    explicit AdjacencyMatrix(std::size_t vertices, bool directed = false)
        : weight_(vertices, std::vector<int>(vertices, 0)),
          directed_(directed) {}

    void add_edge(std::size_t u, std::size_t v, int w = 1) {
        weight_[u][v] = w;
        if (!directed_) {
            weight_[v][u] = w;
        }
    }

    bool has_edge(std::size_t u, std::size_t v) const {
        return weight_[u][v] != 0;
    }

    // 无边返回 0。
    int get_weight(std::size_t u, std::size_t v) const {
        return weight_[u][v];
    }

    std::size_t vertices() const { return weight_.size(); }

private:
    std::vector<std::vector<int>> weight_;
    bool directed_;
};

}  // namespace ds
}  // namespace algorithm_x
