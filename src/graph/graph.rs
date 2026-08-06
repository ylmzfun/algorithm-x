/// 图的表示
///
/// - 邻接矩阵：适合稠密图，O(V²) 空间
/// - 邻接表：适合稀疏图，O(V+E) 空间
use std::collections::HashMap;
use std::hash::Hash;

/// 邻接表实现的通用图
///
/// 使用 HashMap 存储邻接关系，节点类型为泛型 K。
#[derive(Debug, Clone)]
pub struct Graph<K: Eq + Hash + Clone> {
    adj: HashMap<K, Vec<(K, i32)>>, // node → [(neighbor, weight)]
}

impl<K: Eq + Hash + Clone> Graph<K> {
    pub fn new() -> Self {
        Self {
            adj: HashMap::new(),
        }
    }

    pub fn add_node(&mut self, node: K) {
        self.adj.entry(node).or_default();
    }

    /// 添加无向边
    pub fn add_undirected_edge(&mut self, from: K, to: K, weight: i32) {
        self.adj
            .entry(from.clone())
            .or_default()
            .push((to.clone(), weight));
        self.adj.entry(to).or_default().push((from, weight));
    }

    /// 添加有向边
    pub fn add_directed_edge(&mut self, from: K, to: K, weight: i32) {
        self.adj.entry(from).or_default().push((to.clone(), weight));
        self.adj.entry(to).or_default();
    }

    pub fn nodes(&self) -> Vec<&K> {
        self.adj.keys().collect()
    }

    pub fn neighbors(&self, node: &K) -> Option<&[(K, i32)]> {
        self.adj.get(node).map(|v| v.as_slice())
    }

    pub fn node_count(&self) -> usize {
        self.adj.len()
    }

    pub fn edge_count(&self) -> usize {
        self.adj.values().map(|v| v.len()).sum()
    }
}

/// 邻接矩阵图
///
/// 使用 Vec<Vec<Option<i32>>> 存储，适合稠密图。
#[derive(Debug, Clone)]
pub struct DenseGraph {
    /// matrix[i][j] = Some(weight) 表示有边，None 表示无边
    matrix: Vec<Vec<Option<i32>>>,
    node_count: usize,
}

impl DenseGraph {
    pub fn new(node_count: usize) -> Self {
        Self {
            matrix: vec![vec![None; node_count]; node_count],
            node_count,
        }
    }

    pub fn add_edge(&mut self, from: usize, to: usize, weight: i32) {
        if from < self.node_count && to < self.node_count {
            self.matrix[from][to] = Some(weight);
        }
    }

    pub fn add_undirected_edge(&mut self, from: usize, to: usize, weight: i32) {
        self.add_edge(from, to, weight);
        self.add_edge(to, from, weight);
    }

    pub fn has_edge(&self, from: usize, to: usize) -> bool {
        from < self.node_count && to < self.node_count && self.matrix[from][to].is_some()
    }

    pub fn weight(&self, from: usize, to: usize) -> Option<i32> {
        if from < self.node_count && to < self.node_count {
            self.matrix[from][to]
        } else {
            None
        }
    }
}

// ===== 图的常见转换 =====

/// 将邻接表转为邻接矩阵
impl<K: Eq + Hash + Clone + Copy> From<&Graph<K>> for DenseGraph {
    fn from(_graph: &Graph<K>) -> Self {
        // 简化：仅适用于 K = usize 的情况在实际场景中
        unimplemented!("use to_dense_graph for numeric graphs")
    }
}

/// 创建有向邻接表图：edges = [(from, to, weight)]
pub fn build_directed_graph<K: Eq + Hash + Clone>(edges: &[(K, K, i32)]) -> Graph<K> {
    let mut graph = Graph::new();
    for (from, to, weight) in edges {
        graph.add_node(from.clone());
        graph.add_node(to.clone());
        graph.add_directed_edge(from.clone(), to.clone(), *weight);
    }
    graph
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_adj_list_graph() {
        let mut g = Graph::new();
        g.add_undirected_edge(1, 2, 10);
        g.add_undirected_edge(2, 3, 20);
        g.add_undirected_edge(1, 3, 15);

        assert_eq!(g.node_count(), 3);
        let n1 = g.neighbors(&1).unwrap();
        assert_eq!(n1.len(), 2);
        assert!(n1.contains(&(2, 10)));
        assert!(n1.contains(&(3, 15)));
    }

    #[test]
    fn test_dense_graph() {
        let mut g = DenseGraph::new(3);
        g.add_undirected_edge(0, 1, 5);
        g.add_edge(1, 2, 10);

        assert!(g.has_edge(0, 1));
        assert!(g.has_edge(1, 0));
        assert!(!g.has_edge(0, 2));
        assert_eq!(g.weight(1, 2), Some(10));
    }
}
