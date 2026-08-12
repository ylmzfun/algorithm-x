//! petgraph 图算法
//!
//! 覆盖主题：Dijkstra 最短路、BFS 可达计数、最小生成树、
//! 有向环检测、拓扑排序、连通分量。
//!
//! 典型场景：路由/导航（最短路）、依赖解析（拓扑排序）、
//! 网络连通性分析；用 `GraphMap` 时节点可直接用字符串，代码最简洁。

use petgraph::graphmap::{DiGraphMap, UnGraphMap};

/// Dijkstra 单源最短路
///
/// 构建有向带权图后调用 `petgraph::algo::dijkstra`，返回 start 到 goal
/// 的最短距离；不可达返回 None。复杂度 O(E log V)。
/// （GraphMap 的边引用是 `(起点, 终点, &权值)` 元组，闭包中解构取权值。）
pub fn shortest_path(start: &str, goal: &str, edges: &[(&str, &str, u32)]) -> Option<u32> {
    let mut g: DiGraphMap<&str, u32> = DiGraphMap::new();
    for &(a, b, w) in edges {
        let _ = g.add_edge(a, b, w);
    }
    let dist = petgraph::algo::dijkstra(&g, start, Some(goal), |(_, _, w)| *w);
    dist.get(goal).copied()
}

/// BFS 统计从 start 可达的节点数
///
/// `petgraph::visit::Bfs` 按层遍历，计数包含起点在内的所有可达节点。
/// 复杂度 O(V + E)。
pub fn bfs_reachable(start: &str, edges: &[(&str, &str)]) -> usize {
    let mut g: UnGraphMap<&str, ()> = UnGraphMap::new();
    for &(a, b) in edges {
        let _ = g.add_edge(a, b, ());
    }
    let mut count = 0;
    let mut bfs = petgraph::visit::Bfs::new(&g, start);
    while let Some(_node) = bfs.next(&g) {
        count += 1;
    }
    count
}

/// 无向图最小生成树总权值
///
/// `petgraph::algo::min_spanning_tree`（Kruskal 算法）返回
/// `Element` 迭代器：先逐个产出 `Node`，再产出 MST 的 `Edge`；
/// 这里只累加 `Edge` 变体的权值。复杂度 O(E log E)。
pub fn mst_weight(edges: &[(&str, &str, u32)]) -> u32 {
    let mut g: UnGraphMap<&str, u32> = UnGraphMap::new();
    for &(a, b, w) in edges {
        let _ = g.add_edge(a, b, w);
    }
    petgraph::algo::min_spanning_tree(&g)
        .map(|e| match e {
            petgraph::data::Element::Node { .. } => 0,
            petgraph::data::Element::Edge { weight, .. } => weight,
        })
        .sum()
}

/// 检测有向图是否有环
///
/// `petgraph::algo::is_cyclic_directed` 基于 DFS 颜色标记，
/// 有环返回 true。常用于任务调度前的合法性检查。
pub fn has_cycle(edges: &[(&str, &str)]) -> bool {
    let mut g: DiGraphMap<&str, ()> = DiGraphMap::new();
    for &(a, b) in edges {
        let _ = g.add_edge(a, b, ());
    }
    petgraph::algo::is_cyclic_directed(&g)
}

/// 有向无环图的拓扑排序
///
/// `petgraph::algo::toposort`（Kahn 算法）返回节点序列；若图含环则
/// 返回 Err，这里统一转为空 Vec。复杂度 O(V + E)。
pub fn topological_order(edges: &[(&str, &str)]) -> Vec<String> {
    let mut g: DiGraphMap<&str, ()> = DiGraphMap::new();
    for &(a, b) in edges {
        let _ = g.add_edge(a, b, ());
    }
    match petgraph::algo::toposort(&g, None) {
        Ok(order) => order.into_iter().map(|n| n.to_string()).collect(),
        Err(_) => Vec::new(),
    }
}

/// 无向图连通分量个数
///
/// `petgraph::algo::connected_components` 基于并查集，复杂度 O(V + E)。
pub fn connected_components(edges: &[(&str, &str)]) -> usize {
    let mut g: UnGraphMap<&str, ()> = UnGraphMap::new();
    for &(a, b) in edges {
        let _ = g.add_edge(a, b, ());
    }
    petgraph::algo::connected_components(&g)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_shortest_path() {
        let edges = [("A", "B", 1), ("B", "D", 2), ("A", "D", 10)];
        assert_eq!(shortest_path("A", "D", &edges), Some(3));
        assert_eq!(shortest_path("A", "Z", &edges), None);
    }

    #[test]
    fn test_bfs_reachable() {
        let edges = [("A", "B"), ("B", "C"), ("X", "Y")];
        assert_eq!(bfs_reachable("A", &edges), 3);
    }

    #[test]
    fn test_mst_weight() {
        let edges = [("A", "B", 1), ("B", "C", 2), ("A", "C", 3)];
        assert_eq!(mst_weight(&edges), 3);
    }

    #[test]
    fn test_has_cycle() {
        assert!(has_cycle(&[("A", "B"), ("B", "A")]));
        assert!(!has_cycle(&[("A", "B"), ("B", "C")]));
    }

    #[test]
    fn test_topological_order() {
        let order = topological_order(&[("A", "B"), ("B", "C")]);
        assert_eq!(
            order,
            vec!["A".to_string(), "B".to_string(), "C".to_string()]
        );
    }

    #[test]
    fn test_connected_components() {
        let edges = [("A", "B"), ("C", "D")];
        assert_eq!(connected_components(&edges), 2);
    }
}
