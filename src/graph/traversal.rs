/// 图的遍历：BFS 与 DFS
///
/// 包括经典应用：
/// - BFS：最短路径（无权图）、层序遍历
/// - DFS：连通分量、环检测、拓扑排序辅助
use std::collections::{HashMap, HashSet, VecDeque};
use std::hash::Hash;

// ==================== BFS ====================

/// BFS 遍历（返回访问顺序）
pub fn bfs_order<K: Eq + Hash + Clone>(graph: &HashMap<K, Vec<K>>, start: &K) -> Vec<K> {
    let mut order = Vec::new();
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();

    visited.insert(start.clone());
    queue.push_back(start.clone());

    while let Some(node) = queue.pop_front() {
        order.push(node.clone());
        if let Some(neighbors) = graph.get(&node) {
            for neighbor in neighbors {
                if visited.insert(neighbor.clone()) {
                    queue.push_back(neighbor.clone());
                }
            }
        }
    }
    order
}

/// BFS 单源最短路径（无权图）
///
/// 返回从 start 到每个可达节点的距离。
pub fn bfs_shortest_path<K: Eq + Hash + Clone>(
    graph: &HashMap<K, Vec<K>>,
    start: &K,
) -> HashMap<K, usize> {
    let mut dist = HashMap::new();
    let mut queue = VecDeque::new();

    dist.insert(start.clone(), 0);
    queue.push_back(start.clone());

    while let Some(node) = queue.pop_front() {
        let curr_dist = dist[&node];
        if let Some(neighbors) = graph.get(&node) {
            for neighbor in neighbors {
                if !dist.contains_key(neighbor) {
                    dist.insert(neighbor.clone(), curr_dist + 1);
                    queue.push_back(neighbor.clone());
                }
            }
        }
    }
    dist
}

// ==================== DFS ====================

/// DFS 遍历（返回访问顺序）
pub fn dfs_order<K: Eq + Hash + Clone>(graph: &HashMap<K, Vec<K>>, start: &K) -> Vec<K> {
    let mut order = Vec::new();
    let mut visited = HashSet::new();
    dfs_recursive(graph, start, &mut visited, &mut order);
    order
}

fn dfs_recursive<K: Eq + Hash + Clone>(
    graph: &HashMap<K, Vec<K>>,
    node: &K,
    visited: &mut HashSet<K>,
    order: &mut Vec<K>,
) {
    visited.insert(node.clone());
    order.push(node.clone());

    if let Some(neighbors) = graph.get(node) {
        for n in neighbors {
            if !visited.contains(n) {
                dfs_recursive(graph, n, visited, order);
            }
        }
    }
}

/// DFS 迭代版本（显式栈）
pub fn dfs_iterative<K: Eq + Hash + Clone>(graph: &HashMap<K, Vec<K>>, start: &K) -> Vec<K> {
    let mut order = Vec::new();
    let mut visited = HashSet::new();
    let mut stack = vec![start.clone()];

    while let Some(node) = stack.pop() {
        if !visited.insert(node.clone()) {
            continue;
        }
        order.push(node.clone());
        if let Some(neighbors) = graph.get(&node) {
            // 逆序推入栈以保持遍历顺序一致（与递归版本相同）
            for n in neighbors.iter().rev() {
                if !visited.contains(n) {
                    stack.push(n.clone());
                }
            }
        }
    }
    order
}

/// DFS 检测有向图中是否存在环（三色法）
///
/// 0 = 未访问 (White), 1 = 访问中 (Gray), 2 = 已完成 (Black)
pub fn has_cycle_directed<K: Eq + Hash + Clone>(graph: &HashMap<K, Vec<K>>) -> bool {
    let mut color: HashMap<&K, u8> = HashMap::new();
    for node in graph.keys() {
        color.insert(node, 0);
    }
    for node in graph.keys() {
        if color[node] == 0 {
            if dfs_cycle_detect(graph, node, &mut color) {
                return true;
            }
        }
    }
    false
}

fn dfs_cycle_detect<'a, K: Eq + Hash + Clone>(
    graph: &'a HashMap<K, Vec<K>>,
    node: &'a K,
    color: &mut HashMap<&'a K, u8>,
) -> bool {
    color.insert(node, 1); // Gray — 正在访问

    if let Some(neighbors) = graph.get(node) {
        for n in neighbors {
            let c = color.get(n).copied().unwrap_or(2);
            if c == 1 {
                return true; // 发现后向边
            }
            if c == 0 && dfs_cycle_detect(graph, n, color) {
                return true;
            }
        }
    }

    color.insert(node, 2); // Black — 已完成
    false
}

/// 计算无向图中连通分量的数量
pub fn connected_components<K: Eq + Hash + Clone>(graph: &HashMap<K, Vec<K>>) -> usize {
    let mut visited = HashSet::new();
    let mut count = 0;

    for node in graph.keys() {
        if !visited.contains(node) {
            count += 1;
            let mut stack = vec![node.clone()];
            while let Some(n) = stack.pop() {
                if visited.insert(n.clone()) {
                    if let Some(neighbors) = graph.get(&n) {
                        stack.extend(neighbors.iter().cloned());
                    }
                }
            }
        }
    }
    count
}

/// 拓扑排序 — Kahn 算法（BFS）
///
/// 返回拓扑序列，若图有环则返回 None。
pub fn topological_sort_bfs<K: Eq + Hash + Clone>(graph: &HashMap<K, Vec<K>>) -> Option<Vec<K>> {
    // 计算入度
    let mut indegree: HashMap<&K, usize> = HashMap::new();
    for node in graph.keys() {
        indegree.entry(node).or_insert(0);
    }
    for neighbors in graph.values() {
        for n in neighbors {
            *indegree.get_mut(n).unwrap() += 1;
        }
    }

    // 将入度为 0 的节点入队
    let mut queue: VecDeque<&K> = VecDeque::new();
    for (&node, &deg) in &indegree {
        if deg == 0 {
            queue.push_back(node);
        }
    }

    let mut result = Vec::new();
    while let Some(node) = queue.pop_front() {
        result.push(node.clone());
        if let Some(neighbors) = graph.get(node) {
            for n in neighbors {
                let deg = indegree.get_mut(n).unwrap();
                *deg -= 1;
                if *deg == 0 {
                    queue.push_back(n);
                }
            }
        }
    }

    if result.len() == graph.len() {
        Some(result)
    } else {
        None // 存在环
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn build_undirected_sample() -> HashMap<i32, Vec<i32>> {
        let mut g = HashMap::new();
        g.insert(0, vec![1, 2]);
        g.insert(1, vec![0, 3, 4]);
        g.insert(2, vec![0, 4]);
        g.insert(3, vec![1]);
        g.insert(4, vec![1, 2]);
        g
    }

    fn build_dag() -> HashMap<i32, Vec<i32>> {
        let mut g = HashMap::new();
        g.insert(0, vec![1, 2]);
        g.insert(1, vec![3]);
        g.insert(2, vec![3]);
        g.insert(3, vec![4]);
        g.insert(4, vec![]);
        g
    }

    #[test]
    fn test_bfs_order() {
        let g = build_undirected_sample();
        let order = bfs_order(&g, &0);
        assert_eq!(order[0], 0);
        assert!(order.contains(&1));
        assert!(order.contains(&2));
    }

    #[test]
    fn test_bfs_shortest_path() {
        let g = build_undirected_sample();
        let dist = bfs_shortest_path(&g, &0);
        assert_eq!(dist[&0], 0);
        assert_eq!(dist[&1], 1);
        assert_eq!(dist[&3], 2);
        assert_eq!(dist[&4], 2);
    }

    #[test]
    fn test_dfs_order() {
        let g = build_dag();
        let order = dfs_order(&g, &0);
        assert_eq!(order[0], 0);
        assert!(order.contains(&4));
    }

    #[test]
    fn test_has_cycle_directed() {
        let dag = build_dag();
        assert!(!has_cycle_directed(&dag));

        let mut cyclic = HashMap::new();
        cyclic.insert(0, vec![1]);
        cyclic.insert(1, vec![2]);
        cyclic.insert(2, vec![0]);
        assert!(has_cycle_directed(&cyclic));
    }

    #[test]
    fn test_topological_sort() {
        let dag = build_dag();
        let sorted = topological_sort_bfs(&dag).unwrap();
        // 验证拓扑序：每条边 from → to 满足 from 在 to 之前
        let pos: HashMap<i32, usize> = sorted.iter().enumerate().map(|(i, v)| (*v, i)).collect();
        for (from, neighbors) in &dag {
            for to in neighbors {
                assert!(pos[from] < pos[to]);
            }
        }
    }

    #[test]
    fn test_connected_components() {
        let g = build_undirected_sample();
        assert_eq!(connected_components(&g), 1);

        let mut g2 = HashMap::new();
        g2.insert(0, vec![1]);
        g2.insert(1, vec![0]);
        g2.insert(2, vec![3]);
        g2.insert(3, vec![2]);
        assert_eq!(connected_components(&g2), 2);
    }
}
