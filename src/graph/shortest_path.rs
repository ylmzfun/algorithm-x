/// 最短路径算法
///
/// - Dijkstra：单源，非负权重，O((V+E) log V)
/// - Bellman-Ford：单源，可处理负权重，O(VE)
/// - Floyd-Warshall：多源，O(V³)

use std::cmp::Reverse;
use std::collections::BinaryHeap;

/// Dijkstra 最短路径
///
/// 使用优先队列（最小堆）每次选择距离最小的节点。
/// 返回从 start 到每个节点的最短距离。
pub fn dijkstra(graph: &[Vec<(usize, i32)>], start: usize) -> Vec<i32> {
    let n = graph.len();
    let mut dist = vec![i32::MAX; n];
    dist[start] = 0;

    let mut heap = BinaryHeap::new();
    heap.push(Reverse((0, start)));

    while let Some(Reverse((d, u))) = heap.pop() {
        if d > dist[u] {
            continue; // 过时的记录，跳过
        }
        for &(v, w) in &graph[u] {
            let new_dist = d + w;
            if new_dist < dist[v] {
                dist[v] = new_dist;
                heap.push(Reverse((new_dist, v)));
            }
        }
    }
    dist
}

/// Bellman-Ford 最短路径（可检测负权环）
///
/// 对每条边松弛 V-1 次。
/// 返回 (distances, has_negative_cycle)。
pub fn bellman_ford(n: usize, edges: &[(usize, usize, i32)], start: usize) -> (Vec<i32>, bool) {
    let mut dist = vec![i32::MAX; n];
    dist[start] = 0;

    // 松弛 V-1 轮
    for _ in 0..n - 1 {
        let mut updated = false;
        for &(u, v, w) in edges {
            if dist[u] != i32::MAX {
                let new_dist = dist[u] + w;
                if new_dist < dist[v] {
                    dist[v] = new_dist;
                    updated = true;
                }
            }
        }
        if !updated {
            break; // 提前终止：本轮无更新
        }
    }

    // 检测负权环
    let mut has_negative_cycle = false;
    for &(u, v, w) in edges {
        if dist[u] != i32::MAX && dist[u] + w < dist[v] {
            has_negative_cycle = true;
            break;
        }
    }

    (dist, has_negative_cycle)
}

/// Floyd-Warshall 多源最短路径
///
/// 三重循环动态规划，O(V³)。
/// 返回 dist[i][j] 表示从 i 到 j 的最短距离。
pub fn floyd_warshall(n: usize, edges: &[(usize, usize, i32)]) -> Vec<Vec<i32>> {
    let mut dist = vec![vec![i32::MAX; n]; n];

    // 初始化：自己到自己的距离为 0
    for i in 0..n {
        dist[i][i] = 0;
    }
    // 直接边
    for &(u, v, w) in edges {
        dist[u][v] = dist[u][v].min(w);
    }

    // 三重循环
    for k in 0..n {
        for i in 0..n {
            for j in 0..n {
                if dist[i][k] != i32::MAX && dist[k][j] != i32::MAX {
                    let through_k = dist[i][k] + dist[k][j];
                    if through_k < dist[i][j] {
                        dist[i][j] = through_k;
                    }
                }
            }
        }
    }
    dist
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dijkstra() {
        // 图:
        // 0 --4-- 1 --1-- 2
        // |      |      /
        // 2      5     /
        // |      |   /
        // 3 --1-- 4
        let graph = vec![
            vec![(1, 4), (3, 2)],            // node 0
            vec![(0, 4), (2, 1), (4, 5)],     // node 1
            vec![(1, 1), (4, 2)],            // node 2
            vec![(0, 2), (4, 1)],            // node 3
            vec![(1, 5), (2, 2), (3, 1)],    // node 4
        ];
        let dist = dijkstra(&graph, 0);
        assert_eq!(dist, vec![0, 4, 5, 2, 3]);
    }

    #[test]
    fn test_bellman_ford() {
        let edges = vec![
            (0, 1, 4),
            (0, 2, 2),
            (1, 3, -3),
            (2, 1, 1),
            (2, 3, 5),
        ];
        let (dist, neg) = bellman_ford(4, &edges, 0);
        assert!(!neg);
        assert_eq!(dist, vec![0, 3, 2, 0]);
    }

    #[test]
    fn test_bellman_ford_negative_cycle() {
        let edges = vec![(0, 1, 1), (1, 2, -1), (2, 0, -1)];
        let (_, neg) = bellman_ford(3, &edges, 0);
        assert!(neg);
    }

    #[test]
    fn test_floyd_warshall() {
        let edges = vec![(0, 1, 3), (0, 2, 8), (1, 2, 2)];
        let dist = floyd_warshall(3, &edges);
        assert_eq!(dist[0][2], 5); // 0→1→2 = 3+2
        assert_eq!(dist[0][0], 0);
    }
}
