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

    // ==================== 最大流 ====================

    /**
     * Edmonds-Karp 最大流算法（Ford-Fulkerson 的 BFS 实现）
     * 时间复杂度: O(V * E²)
     * 空间复杂度: O(V + E)
     *
     * @param array $graph 邻接表表示的容量图: ['u' => ['v' => capacity, ...], ...]
     * @param mixed $source 源点
     * @param mixed $sink 汇点
     * @return array ['maxFlow' => int, 'flow' => array]
     */
    public static function maxFlowEdmondsKarp(array $graph, $source, $sink): array
    {
        // 构建残余图
        $residual = [];
        $vertices = [];

        foreach ($graph as $u => $edges) {
            $vertices[$u] = true;
            foreach ($edges as $v => $cap) {
                $vertices[$v] = true;
                $residual[$u][$v] = $cap;
                if (!isset($residual[$v][$u])) {
                    $residual[$v][$u] = 0;
                }
            }
        }

        $maxFlow = 0;
        $flow = [];

        while (true) {
            // BFS 找增广路径
            $parent = [];
            $queue = new Queue();
            $queue->enqueue($source);
            $visited = [$source => true];

            while (!$queue->isEmpty()) {
                $u = $queue->dequeue();

                if ($u === $sink) {
                    break;
                }

                if (isset($residual[$u])) {
                    foreach ($residual[$u] as $v => $cap) {
                        if (!isset($visited[$v]) && $cap > 0) {
                            $visited[$v] = true;
                            $parent[$v] = $u;
                            $queue->enqueue($v);
                        }
                    }
                }
            }

            // 没有增广路径
            if (!isset($parent[$sink])) {
                break;
            }

            // 找瓶颈容量
            $bottleneck = PHP_INT_MAX;
            $v = $sink;
            while ($v !== $source) {
                $u = $parent[$v];
                $bottleneck = min($bottleneck, $residual[$u][$v]);
                $v = $u;
            }

            // 更新残余图
            $v = $sink;
            while ($v !== $source) {
                $u = $parent[$v];
                $residual[$u][$v] -= $bottleneck;
                $residual[$v][$u] += $bottleneck;

                if (!isset($flow[$u][$v])) {
                    $flow[$u][$v] = 0;
                }
                $flow[$u][$v] += $bottleneck;

                $v = $u;
            }

            $maxFlow += $bottleneck;
        }

        return ['maxFlow' => $maxFlow, 'flow' => $flow];
    }

    /**
     * Dinic 最大流算法
     * 时间复杂度: O(V² * E)，实践中更快
     *
     * @param array $graph
     * @param mixed $source
     * @param mixed $sink
     * @return array
     */
    public static function maxFlowDinic(array $graph, $source, $sink): array
    {
        $vertices = [];
        $edges = [];
        $edgeCount = 0;

        foreach ($graph as $u => $adj) {
            $vertices[$u] = true;
            foreach ($adj as $v => $cap) {
                $vertices[$v] = true;
            }
        }
        $vertices = array_keys($vertices);
        $n = count($vertices);
        $vertexIndex = array_flip($vertices);

        $adj = array_fill(0, $n, []);

        $addEdge = function($u, $v, $cap) use (&$edges, &$adj, &$edgeCount) {
            $edges[] = ['to' => $v, 'cap' => $cap, 'rev' => $edgeCount + 1];
            $adj[$u][] = $edgeCount++;
            $edges[] = ['to' => $u, 'cap' => 0, 'rev' => $edgeCount - 1];
            $adj[$v][] = $edgeCount++;
        };

        foreach ($graph as $u => $adjList) {
            $ui = $vertexIndex[$u];
            foreach ($adjList as $v => $cap) {
                $vi = $vertexIndex[$v];
                $addEdge($ui, $vi, $cap);
            }
        }

        $s = $vertexIndex[$source];
        $t = $vertexIndex[$sink];

        $level = [];
        $iter = [];

        $bfs = function() use (&$level, &$adj, &$edges, $s, $n) {
            $level = array_fill(0, $n, -1);
            $queue = new Queue();
            $level[$s] = 0;
            $queue->enqueue($s);

            while (!$queue->isEmpty()) {
                $u = $queue->dequeue();
                foreach ($adj[$u] as $ei) {
                    $e = $edges[$ei];
                    if ($e['cap'] > 0 && $level[$e['to']] < 0) {
                        $level[$e['to']] = $level[$u] + 1;
                        $queue->enqueue($e['to']);
                    }
                }
            }

            return $level[$t] >= 0;
        };

        $dfs = function($u, $f) use (&$dfs, &$level, &$iter, &$adj, &$edges, $t): int {
            if ($u === $t) {
                return $f;
            }

            for (; $iter[$u] < count($adj[$u]); $iter[$u]++) {
                $ei = $adj[$u][$iter[$u]];
                $e = &$edges[$ei];

                if ($e['cap'] > 0 && $level[$u] < $level[$e['to']]) {
                    $d = $dfs($e['to'], min($f, $e['cap']));
                    if ($d > 0) {
                        $e['cap'] -= $d;
                        $edges[$e['rev']]['cap'] += $d;
                        return $d;
                    }
                }
            }

            return 0;
        };

        $maxFlow = 0;
        while ($bfs()) {
            $iter = array_fill(0, $n, 0);
            while (($f = $dfs($s, PHP_INT_MAX)) > 0) {
                $maxFlow += $f;
            }
        }

        // 从残余图重构流量
        $flow = [];
        foreach ($graph as $u => $adjList) {
            $ui = $vertexIndex[$u];
            foreach ($adjList as $v => $cap) {
                $vi = $vertexIndex[$v];
                foreach ($adj[$ui] as $ei) {
                    $e = $edges[$ei];
                    if ($e['to'] === $vi) {
                        $sent = $graph[$u][$v] - $e['cap'];
                        if ($sent > 0) {
                            $flow[$u][$v] = $sent;
                        }
                        break;
                    }
                }
            }
        }

        return ['maxFlow' => $maxFlow, 'flow' => $flow];
    }

    // ==================== 二分图匹配 ====================

    /**
     * 匈牙利算法 - 二分图最大匹配
     * 时间复杂度: O(V * E)
     *
     * @param array $leftNodes 左侧节点列表
     * @param array $rightNodes 右侧节点列表
     * @param array $edges 边列表: ['left_node' => ['right_node1', 'right_node2', ...]]
     * @return array ['matching' => [left => right, ...], 'count' => int]
     */
    public static function hungarianBipartiteMatching(array $leftNodes, array $rightNodes, array $edges): array
    {
        $matchR = [];  // right -> left
        $matchL = [];  // left -> right

        $tryKuhn = function($u) use (&$tryKuhn, &$matchR, &$matchL, $edges, $rightNodes) {
            $visited = [];
            $stack = [[$u, 0]]; // [current_node, neighbor_index]

            while (!empty($stack)) {
                [$cur, $idx] = $stack[count($stack) - 1];

                $neighbors = $edges[$cur] ?? [];
                if ($idx >= count($neighbors)) {
                    array_pop($stack);
                    continue;
                }

                $v = $neighbors[$idx];
                $stack[count($stack) - 1][1] = $idx + 1;

                if (!in_array($v, $rightNodes)) {
                    continue;
                }

                if (!isset($matchR[$v])) {
                    // 找到增广路径，回溯更新匹配
                    $matchR[$v] = $cur;
                    $matchL[$cur] = $v;

                    // 回溯更新路径上的匹配
                    for ($i = count($stack) - 2; $i >= 0; $i -= 2) {
                        $leftNode = $stack[$i][0];
                        $rightNode = $stack[$i + 1][0] ?? null;
                        if ($rightNode !== null) {
                            $matchR[$rightNode] = $leftNode;
                            $matchL[$leftNode] = $rightNode;
                        }
                    }
                    return true;
                }

                $nextU = $matchR[$v];
                if ($nextU !== $cur && !in_array([$nextU, 0], $stack)) {
                    $stack[] = [$v, $idx]; // 占位：记录当前右边的节点，后面不会再用了
                    // 实际用递归思路：从matchR[v]重新开始
                    $stack[] = [$nextU, 0];
                }
            }
            return false;
        };

        // 对每个左侧节点尝试匹配（使用 DFS 风格更简洁）
        $dfs = function($u, &$visited) use (&$dfs, &$matchR, $edges): bool {
            $neighbors = $edges[$u] ?? [];
            foreach ($neighbors as $v) {
                if (isset($visited[$v])) {
                    continue;
                }
                $visited[$v] = true;

                if (!isset($matchR[$v]) || $dfs($matchR[$v], $visited)) {
                    $matchR[$v] = $u;
                    return true;
                }
            }
            return false;
        };

        $matchR = [];
        foreach ($leftNodes as $u) {
            $visited = [];
            $dfs($u, $visited);
        }

        // 转换为 left -> right 的匹配
        $matching = [];
        foreach ($matchR as $v => $u) {
            $matching[$u] = $v;
        }

        return ['matching' => $matching, 'count' => count($matching)];
    }

    // ==================== Kosaraju SCC ====================

    /**
     * Kosaraju 强连通分量算法
     * 时间复杂度: O(V + E)
     * 空间复杂度: O(V)
     *
     * @param Graph $graph
     * @return array 强连通分量列表
     */
    public static function kosarajuSCC(Graph $graph): array
    {
        $vertices = $graph->getVertices();
        $visited = [];
        $finishOrder = [];

        // 第一遍 DFS：记录完成顺序
        $dfs1 = function($v) use (&$dfs1, $graph, &$visited, &$finishOrder) {
            $visited[$v] = true;
            foreach ($graph->getNeighbors($v) as $neighbor) {
                if (!isset($visited[$neighbor])) {
                    $dfs1($neighbor);
                }
            }
            $finishOrder[] = $v;
        };

        foreach ($vertices as $v) {
            if (!isset($visited[$v])) {
                $dfs1($v);
            }
        }

        // 构建反向图
        $reverseGraph = [];
        foreach ($vertices as $v) {
            $reverseGraph[$v] = [];
        }
        foreach ($vertices as $u) {
            foreach ($graph->getNeighbors($u) as $v) {
                $reverseGraph[$v][] = $u;
            }
        }

        // 第二遍 DFS：按完成顺序逆序处理
        $visited = [];
        $sccs = [];

        $dfs2 = function($v) use (&$dfs2, &$reverseGraph, &$visited, &$currentSCC) {
            $visited[$v] = true;
            $currentSCC[] = $v;
            foreach ($reverseGraph[$v] as $neighbor) {
                if (!isset($visited[$neighbor])) {
                    $dfs2($neighbor);
                }
            }
        };

        for ($i = count($finishOrder) - 1; $i >= 0; $i--) {
            $v = $finishOrder[$i];
            if (!isset($visited[$v])) {
                $currentSCC = [];
                $dfs2($v);
                $sccs[] = $currentSCC;
            }
        }

        return $sccs;
    }

    // ==================== 桥和割点 ====================

    /**
     * 查找无向图中的桥（割边）
     * 时间复杂度: O(V + E)
     *
     * @param Graph $graph 无向图
     * @return array 桥的列表，每条桥为 ['u' => $u, 'v' => $v]
     */
    public static function findBridges(Graph $graph): array
    {
        $vertices = $graph->getVertices();
        $visited = [];
        $disc = [];
        $low = [];
        $time = 0;
        $bridges = [];

        $dfs = function($u, $parent) use (&$dfs, $graph, &$visited, &$disc, &$low, &$time, &$bridges) {
            $visited[$u] = true;
            $disc[$u] = $low[$u] = ++$time;

            foreach ($graph->getNeighbors($u) as $v) {
                if (!isset($visited[$v])) {
                    $dfs($v, $u);
                    $low[$u] = min($low[$u], $low[$v]);

                    if ($low[$v] > $disc[$u]) {
                        $bridges[] = ['u' => $u, 'v' => $v];
                    }
                } elseif ($v !== $parent) {
                    $low[$u] = min($low[$u], $disc[$v]);
                }
            }
        };

        foreach ($vertices as $v) {
            if (!isset($visited[$v])) {
                $dfs($v, null);
            }
        }

        return $bridges;
    }

    /**
     * 查找无向图中的割点（关节点）
     * 时间复杂度: O(V + E)
     *
     * @param Graph $graph 无向图
     * @return array 割点列表
     */
    public static function findArticulationPoints(Graph $graph): array
    {
        $vertices = $graph->getVertices();
        $visited = [];
        $disc = [];
        $low = [];
        $isArticulation = [];
        $time = 0;

        $dfs = function($u, $parent) use (&$dfs, $graph, &$visited, &$disc, &$low, &$time, &$isArticulation) {
            $visited[$u] = true;
            $disc[$u] = $low[$u] = ++$time;
            $children = 0;

            foreach ($graph->getNeighbors($u) as $v) {
                if (!isset($visited[$v])) {
                    $children++;
                    $dfs($v, $u);
                    $low[$u] = min($low[$u], $low[$v]);

                    // 非根节点的割点条件
                    if ($parent !== null && $low[$v] >= $disc[$u]) {
                        $isArticulation[$u] = true;
                    }
                } elseif ($v !== $parent) {
                    $low[$u] = min($low[$u], $disc[$v]);
                }
            }

            // 根节点的割点条件
            if ($parent === null && $children > 1) {
                $isArticulation[$u] = true;
            }
        };

        foreach ($vertices as $v) {
            if (!isset($visited[$v])) {
                $dfs($v, null);
            }
        }

        return array_keys($isArticulation);
    }

    // ==================== LCA ====================

    /**
     * 最近公共祖先 (LCA) - 倍增法
     *
     * 直接对树结构计算 LCA，树以邻接表表示。
     * 时间复杂度: 预处理 O(n log n)，查询 O(log n)
     *
     * @param array $tree 邻接表: ['node' => ['child1', 'child2', ...]]
     * @param mixed $root 根节点
     * @param mixed $u
     * @param mixed $v
     * @return mixed|null
     */
    public static function lca(array $tree, $root, $u, $v)
    {
        $nodes = [];
        $collectNodes = function($node) use (&$collectNodes, $tree, &$nodes) {
            $nodes[$node] = true;
            if (isset($tree[$node])) {
                foreach ($tree[$node] as $child) {
                    $collectNodes($child);
                }
            }
        };
        $collectNodes($root);

        $nodeList = array_keys($nodes);
        $nodeIndex = array_flip($nodeList);
        $n = count($nodeList);

        $maxLog = (int)ceil(log($n, 2)) + 1;
        $up = array_fill(0, $n, array_fill(0, $maxLog, -1));
        $depth = array_fill(0, $n, 0);

        // DFS 预处理
        $dfs = function($node, $parentNode, $d) use (&$dfs, $tree, &$up, &$depth, $nodeIndex, $maxLog): void {
            $idx = $nodeIndex[$node];
            $depth[$idx] = $d;

            if ($parentNode !== null) {
                $up[$idx][0] = $nodeIndex[$parentNode];
                for ($j = 1; $j < $maxLog; $j++) {
                    if ($up[$idx][$j - 1] !== -1) {
                        $up[$idx][$j] = $up[$up[$idx][$j - 1]][$j - 1];
                    }
                }
            }

            if (isset($tree[$node])) {
                foreach ($tree[$node] as $child) {
                    $dfs($child, $node, $d + 1);
                }
            }
        };

        $dfs($root, null, 0);

        // 查询
        $ui = $nodeIndex[$u];
        $vi = $nodeIndex[$v];

        // 让深度相同
        if ($depth[$ui] < $depth[$vi]) {
            [$ui, $vi] = [$vi, $ui];
        }

        $diff = $depth[$ui] - $depth[$vi];
        for ($j = 0; $j < $maxLog; $j++) {
            if ($diff & (1 << $j)) {
                $ui = $up[$ui][$j];
            }
        }

        if ($ui === $vi) {
            return $nodeList[$ui];
        }

        // 同时上跳
        for ($j = $maxLog - 1; $j >= 0; $j--) {
            if ($up[$ui][$j] !== $up[$vi][$j]) {
                $ui = $up[$ui][$j];
                $vi = $up[$vi][$j];
            }
        }

        return $nodeList[$up[$ui][0]];
    }

    // ==================== 最小费用最大流 ====================

    /**
     * 最小费用最大流 - 连续最短路算法 (SPFA)
     *
     * 在保证最大流的前提下，使总费用最小。
     * 每条边有容量 capacity 和单位费用 cost。
     *
     * 时间复杂度: O(flow × V × E)，使用SPFA
     *
     * @param array $graph 邻接表: ['u' => [['to' => 'v', 'cap' => c, 'cost' => w], ...], ...]
     * @param mixed $source 源点
     * @param mixed $sink 汇点
     * @return array ['maxFlow' => int, 'minCost' => int, 'flow' => array]
     */
    public static function minCostMaxFlow(array $graph, $source, $sink): array
    {
        // 构建边列表
        $edges = [];
        $adj = [];
        $edgeCount = 0;

        $addEdge = function($from, $to, $cap, $cost) use (&$edges, &$adj, &$edgeCount) {
            $edges[] = ['to' => $to, 'cap' => $cap, 'cost' => $cost, 'rev' => $edgeCount + 1];
            $adj[$from][] = $edgeCount++;
            $edges[] = ['to' => $from, 'cap' => 0, 'cost' => -$cost, 'rev' => $edgeCount - 1];
            $adj[$to][] = $edgeCount++;
        };

        foreach ($graph as $u => $neighbors) {
            if (!isset($adj[$u])) {
                $adj[$u] = [];
            }
            foreach ($neighbors as $edge) {
                $v = $edge['to'];
                $cap = $edge['cap'];
                $cost = $edge['cost'];
                if (!isset($adj[$v])) {
                    $adj[$v] = [];
                }
                $addEdge($u, $v, $cap, $cost);
            }
        }

        if (!isset($adj[$source]) || !isset($adj[$sink])) {
            return ['maxFlow' => 0, 'minCost' => 0, 'flow' => []];
        }

        $maxFlow = 0;
        $minCost = 0;
        $dist = [];
        $prevEdge = [];
        $prevNode = [];
        $inQueue = [];

        while (true) {
            // SPFA 找费用最短路
            $dist = [];
            $prevEdge = [];
            $prevNode = [];
            $inQueue = [];

            foreach ($adj as $node => $_) {
                $dist[$node] = PHP_INT_MAX;
                $inQueue[$node] = false;
            }

            $queue = new Queue();
            $dist[$source] = 0;
            $inQueue[$source] = true;
            $queue->enqueue($source);

            while (!$queue->isEmpty()) {
                $u = $queue->dequeue();
                $inQueue[$u] = false;

                foreach ($adj[$u] as $ei) {
                    $e = $edges[$ei];
                    if ($e['cap'] > 0 && $dist[$u] + $e['cost'] < $dist[$e['to']]) {
                        $dist[$e['to']] = $dist[$u] + $e['cost'];
                        $prevNode[$e['to']] = $u;
                        $prevEdge[$e['to']] = $ei;

                        if (!$inQueue[$e['to']]) {
                            $inQueue[$e['to']] = true;
                            $queue->enqueue($e['to']);
                        }
                    }
                }
            }

            // 无法到达汇点
            if (!isset($dist[$sink]) || $dist[$sink] === PHP_INT_MAX) {
                break;
            }

            // 找瓶颈容量
            $bottleneck = PHP_INT_MAX;
            $v = $sink;
            while ($v !== $source) {
                $ei = $prevEdge[$v];
                $bottleneck = min($bottleneck, $edges[$ei]['cap']);
                $v = $prevNode[$v];
            }

            // 增广
            $v = $sink;
            while ($v !== $source) {
                $ei = $prevEdge[$v];
                $edges[$ei]['cap'] -= $bottleneck;
                $edges[$edges[$ei]['rev']]['cap'] += $bottleneck;
                $v = $prevNode[$v];
            }

            $maxFlow += $bottleneck;
            $minCost += $bottleneck * $dist[$sink];
        }

        // 重构流量
        $flow = [];
        foreach ($graph as $u => $neighbors) {
            foreach ($neighbors as $i => $edge) {
                $v = $edge['to'];
                // 找到对应的正向边
                foreach ($adj[$u] as $ei) {
                    $e = $edges[$ei];
                    if ($e['to'] === $v) {
                        $sent = $graph[$u][$i]['cap'] - $e['cap'];
                        if ($sent > 0) {
                            $flow[$u][$v] = ['flow' => $sent, 'cost' => $edge['cost'] * $sent];
                        }
                        break;
                    }
                }
            }
        }

        return ['maxFlow' => $maxFlow, 'minCost' => $minCost, 'flow' => $flow];
    }
}