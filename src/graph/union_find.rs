/// 并查集 (Union-Find / Disjoint Set)
///
/// 核心操作：
/// - `find(x)`：找到元素 x 所属集合的代表元
/// - `union(x, y)`：合并 x 和 y 所在集合
///
/// 优化：
/// - 路径压缩 (Path Compression)：find 时将路径上所有节点直接指向根
/// - 按秩合并 (Union by Rank)：将较矮的树合并到较高的树下

#[derive(Debug)]
pub struct UnionFind {
    /// parent[i] = 节点 i 的父节点
    parent: Vec<usize>,
    /// rank[i] = 以 i 为根的树高度上界
    rank: Vec<usize>,
}

impl UnionFind {
    /// 创建包含 n 个独立元素的并查集（编号 0..n-1）
    pub fn new(n: usize) -> Self {
        Self {
            parent: (0..n).collect(),
            rank: vec![0; n],
        }
    }

    /// 查找 x 所属集合的根（带路径压缩）
    ///
    /// 时间均摊接近 O(α(n))，其中 α 为反阿克曼函数，实际可视为常数。
    pub fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            self.parent[x] = self.find(self.parent[x]); // 路径压缩
        }
        self.parent[x]
    }

    /// 合并 x 和 y 所在集合（按秩合并）
    ///
    /// 返回 true 如果两个集合原本不同（成功合并），false 如果已在同一集合中。
    pub fn union(&mut self, x: usize, y: usize) -> bool {
        let root_x = self.find(x);
        let root_y = self.find(y);

        if root_x == root_y {
            return false;
        }

        match self.rank[root_x].cmp(&self.rank[root_y]) {
            std::cmp::Ordering::Less => {
                self.parent[root_x] = root_y;
            }
            std::cmp::Ordering::Greater => {
                self.parent[root_y] = root_x;
            }
            std::cmp::Ordering::Equal => {
                self.parent[root_y] = root_x;
                self.rank[root_x] += 1;
            }
        }
        true
    }

    /// 检查 x 和 y 是否在同一集合中
    pub fn connected(&mut self, x: usize, y: usize) -> bool {
        self.find(x) == self.find(y)
    }

    /// 返回当前连通分量个数
    pub fn count(&self) -> usize {
        self.parent
            .iter()
            .enumerate()
            .filter(|&(i, p)| i == *p)
            .count()
    }
}

// ========== 并查集经典应用 ==========

/// 无向图中连通分量的数量
///
/// 给定节点数 n 和边集 edges，返回连通分量的数量。
pub fn count_components(n: usize, edges: &[(usize, usize)]) -> usize {
    let mut uf = UnionFind::new(n);
    for &(u, v) in edges {
        uf.union(u, v);
    }
    uf.count()
}

/// 检测无向图中是否存在环
pub fn has_cycle(n: usize, edges: &[(usize, usize)]) -> bool {
    let mut uf = UnionFind::new(n);
    for &(u, v) in edges {
        if !uf.union(u, v) {
            return true; // 两个节点已在同一集合，说明有环
        }
    }
    false
}

/// 最小生成树 Kruskal 算法的辅助函数
///
/// 边按权重排序后，若两端不在同一集合则加入 MST。
pub fn kruskal_mst(n: usize, edges: &[(usize, usize, i32)]) -> Vec<(usize, usize, i32)> {
    let mut sorted_edges: Vec<&(usize, usize, i32)> = edges.iter().collect();
    sorted_edges.sort_by_key(|e| e.2);

    let mut uf = UnionFind::new(n);
    let mut mst = Vec::new();

    for &&(u, v, weight) in &sorted_edges {
        if uf.union(u, v) {
            mst.push((u, v, weight));
            if mst.len() == n - 1 {
                break;
            }
        }
    }
    mst
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_union_find_basic() {
        let mut uf = UnionFind::new(5);
        assert!(!uf.connected(0, 1));

        uf.union(0, 1);
        assert!(uf.connected(0, 1));

        uf.union(1, 2);
        assert!(uf.connected(0, 2));

        assert!(!uf.connected(0, 3));
        assert_eq!(uf.count(), 3); // {0,1,2} 和 {3} 和 {4} = 3 个集合
    }

    #[test]
    fn test_count_components() {
        let edges = [(0, 1), (1, 2), (3, 4)];
        assert_eq!(count_components(5, &edges), 2);
    }

    #[test]
    fn test_has_cycle() {
        let edges_no_cycle = [(0, 1), (1, 2), (3, 4)];
        assert!(!has_cycle(5, &edges_no_cycle));

        let edges_with_cycle = [(0, 1), (1, 2), (2, 0)];
        assert!(has_cycle(3, &edges_with_cycle));
    }

    #[test]
    fn test_kruskal_mst() {
        let edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4)];
        let mst = kruskal_mst(4, &edges);
        let total_weight: i32 = mst.iter().map(|(_, _, w)| w).sum();
        assert_eq!(total_weight, 6); // edges: (1,2,1), (1,3,2), (0,2,3)
        assert_eq!(mst.len(), 3);
    }
}
