<?php

namespace DataStructures\Algorithms;

use DataStructures\Graph\Graph;
use DataStructures\Graph\WeightedGraph;
use DataStructures\Linear\Queue;
use DataStructures\Linear\Stack;
use DataStructures\Linear\PriorityQueue;

/**
 * 图算法集合
 * 包含常见的图算法实现
 */
class GraphAlgorithms
{
    /**
     * 深度优先搜索 (DFS)
     * 时间复杂度: O(V + E)
     * 空间复杂度: O(V)
     */
    public static function dfs(Graph $graph, $startVertex): array
    {
        $visited = [];
        $result = [];
        
        self::dfsRecursive($graph, $startVertex, $visited, $result);
        
        return $result;
    }
    
    private static function dfsRecursive(Graph $graph, $vertex, array &$visited, array &$result): void
    {
        $visited[$vertex] = true;
        $result[] = $vertex;
        
        foreach ($graph->getNeighbors($vertex) as $neighbor) {
            if (!isset($visited[$neighbor])) {
                self::dfsRecursive($graph, $neighbor, $visited, $result);
            }
        }
    }
    
    /**
     * 广度优先搜索 (BFS)
     * 时间复杂度: O(V + E)
     * 空间复杂度: O(V)
     */
    public static function bfs(Graph $graph, $startVertex): array
    {
        $visited = [];
        $result = [];
        $queue = new Queue();
        
        $queue->enqueue($startVertex);
        $visited[$startVertex] = true;
        
        while (!$queue->isEmpty()) {
            $vertex = $queue->dequeue();
            $result[] = $vertex;
            
            foreach ($graph->getNeighbors($vertex) as $neighbor) {
                if (!isset($visited[$neighbor])) {
                    $visited[$neighbor] = true;
                    $queue->enqueue($neighbor);
                }
            }
        }
        
        return $result;
    }
    
    /**
     * 拓扑排序 (使用DFS)
     * 时间复杂度: O(V + E)
     * 空间复杂度: O(V)
     */
    public static function topologicalSort(Graph $graph): array
    {
        $visited = [];
        $stack = new Stack();
        
        foreach ($graph->getVertices() as $vertex) {
            if (!isset($visited[$vertex])) {
                self::topologicalSortUtil($graph, $vertex, $visited, $stack);
            }
        }
        
        $result = [];
        while (!$stack->isEmpty()) {
            $result[] = $stack->pop();
        }
        
        return $result;
    }
    
    private static function topologicalSortUtil(Graph $graph, $vertex, array &$visited, Stack $stack): void
    {
        $visited[$vertex] = true;
        
        foreach ($graph->getNeighbors($vertex) as $neighbor) {
            if (!isset($visited[$neighbor])) {
                self::topologicalSortUtil($graph, $neighbor, $visited, $stack);
            }
        }
        
        $stack->push($vertex);
    }
    
    /**
     * 检测有向图中的环
     * 时间复杂度: O(V + E)
     * 空间复杂度: O(V)
     */
    public static function hasCycle(Graph $graph): bool
    {
        $visited = [];
        $recStack = [];
        
        foreach ($graph->getVertices() as $vertex) {
            if (!isset($visited[$vertex])) {
                if (self::hasCycleUtil($graph, $vertex, $visited, $recStack)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    private static function hasCycleUtil(Graph $graph, $vertex, array &$visited, array &$recStack): bool
    {
        $visited[$vertex] = true;
        $recStack[$vertex] = true;
        
        foreach ($graph->getNeighbors($vertex) as $neighbor) {
            if (!isset($visited[$neighbor])) {
                if (self::hasCycleUtil($graph, $neighbor, $visited, $recStack)) {
                    return true;
                }
            } elseif (isset($recStack[$neighbor])) {
                return true;
            }
        }
        
        unset($recStack[$vertex]);
        return false;
    }
    
    /**
     * Dijkstra最短路径算法
     * 时间复杂度: O((V + E) log V)
     * 空间复杂度: O(V)
     */
    public static function dijkstra(WeightedGraph $graph, $startVertex): array
    {
        $distances = [];
        $previous = [];
        $pq = new PriorityQueue();
        
        // 初始化距离
        foreach ($graph->getVertices() as $vertex) {
            $distances[$vertex] = $vertex === $startVertex ? 0 : PHP_INT_MAX;
            $previous[$vertex] = null;
            $pq->enqueue(['vertex' => $vertex, 'distance' => $distances[$vertex]], $distances[$vertex]);
        }
        
        while (!$pq->isEmpty()) {
            $current = $pq->dequeue();
            $currentVertex = $current['vertex'];
            
            foreach ($graph->getNeighbors($currentVertex) as $neighbor) {
                $weight = $graph->getWeight($currentVertex, $neighbor);
                $newDistance = $distances[$currentVertex] + $weight;
                
                if ($newDistance < $distances[$neighbor]) {
                    $distances[$neighbor] = $newDistance;
                    $previous[$neighbor] = $currentVertex;
                    $pq->enqueue(['vertex' => $neighbor, 'distance' => $newDistance], $newDistance);
                }
            }
        }
        
        return ['distances' => $distances, 'previous' => $previous];
    }
    
    /**
     * Floyd-Warshall全源最短路径算法
     * 时间复杂度: O(V³)
     * 空间复杂度: O(V²)
     */
    public static function floydWarshall(WeightedGraph $graph): array
    {
        $vertices = $graph->getVertices();
        $n = count($vertices);
        $vertexMap = array_flip($vertices);
        
        // 初始化距离矩阵
        $dist = [];
        for ($i = 0; $i < $n; $i++) {
            for ($j = 0; $j < $n; $j++) {
                if ($i === $j) {
                    $dist[$i][$j] = 0;
                } else {
                    $vertex1 = $vertices[$i];
                    $vertex2 = $vertices[$j];
                    $weight = $graph->getWeight($vertex1, $vertex2);
                    $dist[$i][$j] = $weight !== null ? $weight : PHP_INT_MAX;
                }
            }
        }
        
        // Floyd-Warshall算法
        for ($k = 0; $k < $n; $k++) {
            for ($i = 0; $i < $n; $i++) {
                for ($j = 0; $j < $n; $j++) {
                    if ($dist[$i][$k] !== PHP_INT_MAX && $dist[$k][$j] !== PHP_INT_MAX) {
                        $dist[$i][$j] = min($dist[$i][$j], $dist[$i][$k] + $dist[$k][$j]);
                    }
                }
            }
        }
        
        // 转换回顶点名称
        $result = [];
        for ($i = 0; $i < $n; $i++) {
            for ($j = 0; $j < $n; $j++) {
                $result[$vertices[$i]][$vertices[$j]] = $dist[$i][$j];
            }
        }
        
        return $result;
    }
    
    /**
     * Bellman-Ford算法（处理负权边）
     * 时间复杂度: O(VE)
     * 空间复杂度: O(V)
     */
    public static function bellmanFord(WeightedGraph $graph, $startVertex): array
    {
        $vertices = $graph->getVertices();
        $distances = [];
        $previous = [];
        
        // 初始化
        foreach ($vertices as $vertex) {
            $distances[$vertex] = $vertex === $startVertex ? 0 : PHP_INT_MAX;
            $previous[$vertex] = null;
        }
        
        // 松弛边 V-1 次
        for ($i = 0; $i < count($vertices) - 1; $i++) {
            foreach ($vertices as $u) {
                if ($distances[$u] !== PHP_INT_MAX) {
                    foreach ($graph->getNeighbors($u) as $v) {
                        $weight = $graph->getWeight($u, $v);
                        if ($distances[$u] + $weight < $distances[$v]) {
                            $distances[$v] = $distances[$u] + $weight;
                            $previous[$v] = $u;
                        }
                    }
                }
            }
        }
        
        // 检查负权环
        $hasNegativeCycle = false;
        foreach ($vertices as $u) {
            if ($distances[$u] !== PHP_INT_MAX) {
                foreach ($graph->getNeighbors($u) as $v) {
                    $weight = $graph->getWeight($u, $v);
                    if ($distances[$u] + $weight < $distances[$v]) {
                        $hasNegativeCycle = true;
                        break 2;
                    }
                }
            }
        }
        
        return [
            'distances' => $distances,
            'previous' => $previous,
            'hasNegativeCycle' => $hasNegativeCycle
        ];
    }
    
    /**
     * Kruskal最小生成树算法
     * 时间复杂度: O(E log E)
     * 空间复杂度: O(V)
     */
    public static function kruskal(WeightedGraph $graph): array
    {
        $edges = [];
        $vertices = $graph->getVertices();
        
        // 获取所有边
        foreach ($vertices as $u) {
            foreach ($graph->getNeighbors($u) as $v) {
                $weight = $graph->getWeight($u, $v);
                $edges[] = ['u' => $u, 'v' => $v, 'weight' => $weight];
            }
        }
        
        // 按权重排序
        usort($edges, function($a, $b) {
            return $a['weight'] <=> $b['weight'];
        });
        
        // 并查集
        $parent = [];
        $rank = [];
        foreach ($vertices as $vertex) {
            $parent[$vertex] = $vertex;
            $rank[$vertex] = 0;
        }
        
        $mst = [];
        $totalWeight = 0;
        
        foreach ($edges as $edge) {
            $rootU = self::find($parent, $edge['u']);
            $rootV = self::find($parent, $edge['v']);
            
            if ($rootU !== $rootV) {
                $mst[] = $edge;
                $totalWeight += $edge['weight'];
                self::union($parent, $rank, $rootU, $rootV);
            }
        }
        
        return ['mst' => $mst, 'totalWeight' => $totalWeight];
    }
    
    private static function find(array &$parent, $vertex)
    {
        if ($parent[$vertex] !== $vertex) {
            $parent[$vertex] = self::find($parent, $parent[$vertex]);
        }
        return $parent[$vertex];
    }
    
    private static function union(array &$parent, array &$rank, $rootU, $rootV): void
    {
        if ($rank[$rootU] < $rank[$rootV]) {
            $parent[$rootU] = $rootV;
        } elseif ($rank[$rootU] > $rank[$rootV]) {
            $parent[$rootV] = $rootU;
        } else {
            $parent[$rootV] = $rootU;
            $rank[$rootU]++;
        }
    }
    
    /**
     * 强连通分量 (Tarjan算法)
     * 时间复杂度: O(V + E)
     * 空间复杂度: O(V)
     */
    public static function stronglyConnectedComponents(Graph $graph): array
    {
        $index = 0;
        $stack = new Stack();
        $indices = [];
        $lowLinks = [];
        $onStack = [];
        $sccs = [];
        
        foreach ($graph->getVertices() as $vertex) {
            if (!isset($indices[$vertex])) {
                self::tarjanSCC($graph, $vertex, $index, $stack, $indices, $lowLinks, $onStack, $sccs);
            }
        }
        
        return $sccs;
    }
    
    private static function tarjanSCC(Graph $graph, $vertex, int &$index, Stack $stack, 
                                     array &$indices, array &$lowLinks, array &$onStack, array &$sccs): void
    {
        $indices[$vertex] = $index;
        $lowLinks[$vertex] = $index;
        $index++;
        $stack->push($vertex);
        $onStack[$vertex] = true;
        
        foreach ($graph->getNeighbors($vertex) as $neighbor) {
            if (!isset($indices[$neighbor])) {
                self::tarjanSCC($graph, $neighbor, $index, $stack, $indices, $lowLinks, $onStack, $sccs);
                $lowLinks[$vertex] = min($lowLinks[$vertex], $lowLinks[$neighbor]);
            } elseif (isset($onStack[$neighbor]) && $onStack[$neighbor]) {
                $lowLinks[$vertex] = min($lowLinks[$vertex], $indices[$neighbor]);
            }
        }
        
        if ($lowLinks[$vertex] === $indices[$vertex]) {
            $scc = [];
            do {
                $w = $stack->pop();
                $onStack[$w] = false;
                $scc[] = $w;
            } while ($w !== $vertex);
            $sccs[] = $scc;
        }
    }
    
    /**
     * 获取图的连通分量数量
     */
    public static function countConnectedComponents(Graph $graph): int
    {
        $visited = [];
        $count = 0;
        
        foreach ($graph->getVertices() as $vertex) {
            if (!isset($visited[$vertex])) {
                self::dfsRecursive($graph, $vertex, $visited, $dummy = []);
                $count++;
            }
        }
        
        return $count;
    }
    
    /**
     * 检查图是否为二分图
     */
    public static function isBipartite(Graph $graph): bool
    {
        $colors = [];
        
        foreach ($graph->getVertices() as $vertex) {
            if (!isset($colors[$vertex])) {
                if (!self::isBipartiteUtil($graph, $vertex, $colors, 0)) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    private static function isBipartiteUtil(Graph $graph, $vertex, array &$colors, int $color): bool
    {
        $colors[$vertex] = $color;
        
        foreach ($graph->getNeighbors($vertex) as $neighbor) {
            if (!isset($colors[$neighbor])) {
                if (!self::isBipartiteUtil($graph, $neighbor, $colors, 1 - $color)) {
                    return false;
                }
            } elseif ($colors[$neighbor] === $color) {
                return false;
            }
        }
        
        return true;
    }
}