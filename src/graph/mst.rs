/// 最小生成树 (MST)
///
/// - Prim 算法：从节点扩展，类似 Dijkstra，O((V+E) log V)
/// - Kruskal 算法：按边排序 + 并查集，O(E log E)
///
/// 注：Kruskal 实现在 `union_find.rs` 中，此处展示 Prim。

use std::cmp::Reverse;
use std::collections::BinaryHeap;

/// Prim 算法求最小生成树总权重
///
/// 从一个起始节点开始，每次选择连接已选集合和未选集合的最小权重边。
pub fn prim_mst(graph: &[Vec<(usize, i32)>]) -> i32 {
    let n = graph.len();
    if n == 0 {
        return 0;
    }

    let mut visited = vec![false; n];
    let mut total_weight = 0;
    let mut heap = BinaryHeap::new();

    // 从节点 0 开始
    visited[0] = true;
    for &(v, w) in &graph[0] {
        heap.push(Reverse((w, v)));
    }

    let mut edges_selected = 0;

    while let Some(Reverse((w, v))) = heap.pop() {
        if visited[v] {
            continue;
        }
        visited[v] = true;
        total_weight += w;
        edges_selected += 1;

        if edges_selected == n - 1 {
            break;
        }

        for &(next, weight) in &graph[v] {
            if !visited[next] {
                heap.push(Reverse((weight, next)));
            }
        }
    }

    total_weight
}

/// Prim 算法返回具体的 MST 边集
pub fn prim_mst_edges(graph: &[Vec<(usize, i32)>]) -> Vec<(usize, usize, i32)> {
    let n = graph.len();
    if n == 0 {
        return vec![];
    }

    let mut visited = vec![false; n];
    let mut edges = Vec::new();
    // heap: (weight, from, to)
    let mut heap = BinaryHeap::new();

    visited[0] = true;
    for &(v, w) in &graph[0] {
        heap.push(Reverse((w, 0, v)));
    }

    while let Some(Reverse((w, from, to))) = heap.pop() {
        if visited[to] {
            continue;
        }
        visited[to] = true;
        edges.push((from, to, w));

        if edges.len() == n - 1 {
            break;
        }

        for &(next, weight) in &graph[to] {
            if !visited[next] {
                heap.push(Reverse((weight, to, next)));
            }
        }
    }
    edges
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_prim_mst() {
        // 图:
        //     1
        //  0 -- 1
        //  | \  |
        // 4|  \3| 2
        //  |   \|
        //  2 -- 3
        //     1
        let graph = vec![
            vec![(1, 1), (2, 4), (3, 3)],   // node 0
            vec![(0, 1), (3, 2)],            // node 1
            vec![(0, 4), (3, 1)],            // node 2
            vec![(0, 3), (1, 2), (2, 1)],    // node 3
        ];
        let total = prim_mst(&graph);
        assert_eq!(total, 4); // edges: (0,1,1), (1,3,2), (3,2,1)
    }

    #[test]
    fn test_prim_mst_edges() {
        let graph = vec![
            vec![(1, 1), (2, 4), (3, 3)],
            vec![(0, 1), (3, 2)],
            vec![(0, 4), (3, 1)],
            vec![(0, 3), (1, 2), (2, 1)],
        ];
        let edges = prim_mst_edges(&graph);
        assert_eq!(edges.len(), 3);
        let total: i32 = edges.iter().map(|(_, _, w)| w).sum();
        assert_eq!(total, 4);
    }
}
