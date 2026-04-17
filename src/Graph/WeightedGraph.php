<?php

namespace DataStructures\Graph;

require_once 'Graph.php';

/**
 * WeightedGraph - 加权图数据结构实现
 * 
 * 思路：
 * 1. 继承自基础图类，增加边权重支持
 * 2. 使用邻接表存储，每条边包含目标顶点和权重
 * 3. 实现最短路径算法（Dijkstra、Floyd-Warshall）
 * 4. 支持最小生成树算法（Prim、Kruskal）
 * 
 * 作用：
 * - 表示带权重的关系网络
 * - 最短路径计算
 * - 最小生成树构建
 * - 网络流量分析
 * 
 * 业务场景：
 * 1. 地图导航：道路网络，考虑距离、时间、费用
 * 2. 网络路由：数据包传输的最优路径
 * 3. 供应链优化：运输成本最小化
 * 4. 社交网络：关系强度分析
 * 5. 金融网络：交易成本优化
 * 6. 游戏开发：地形权重，AI寻路
 * 7. 物流配送：配送路线优化
 * 8. 电力网络：输电线路规划
 * 9. 通信网络：信号传输优化
 * 10. 项目管理：任务依赖和时间成本
 */

/**
 * 加权边类
 */
class WeightedEdge
{
    public $from;
    public $to;
    public float $weight;
    
    public function __construct($from, $to, float $weight)
    {
        $this->from = $from;
        $this->to = $to;
        $this->weight = $weight;
    }
    
    public function toString(): string
    {
        return "({$this->from} -> {$this->to}, weight: {$this->weight})";
    }
}

class WeightedGraph extends Graph
{
    protected array $weights; // 存储边的权重
    
    public function __construct(bool $isDirected = false)
    {
        parent::__construct($isDirected);
        $this->weights = [];
    }
    
    /**
     * 添加带权重的边
     * 时间复杂度：O(1)
     */
    public function addEdge($from, $to, float $weight = 1.0): void
    {
        $this->addVertex($from);
        $this->addVertex($to);
        
        // 检查边是否已存在
        if (!$this->hasEdge($from, $to)) {
            $this->adjacencyList[$from][] = $to;
            $this->edgeCount++;
        }
        
        // 设置权重
        $this->weights[$from][$to] = $weight;
        
        // 如果是无向图，添加反向边
        if (!$this->isDirected) {
            if (!in_array($from, $this->adjacencyList[$to])) {
                $this->adjacencyList[$to][] = $from;
            }
            $this->weights[$to][$from] = $weight;
        }
    }
    
    /**
     * 删除边
     * 时间复杂度：O(V)
     */
    public function removeEdge($from, $to): bool
    {
        $result = parent::removeEdge($from, $to);
        
        if ($result) {
            unset($this->weights[$from][$to]);
            if (!$this->isDirected) {
                unset($this->weights[$to][$from]);
            }
        }
        
        return $result;
    }
    
    /**
     * 获取边的权重
     * 时间复杂度：O(1)
     */
    public function getWeight($from, $to): ?float
    {
        return $this->weights[$from][$to] ?? null;
    }
    
    /**
     * 设置边的权重
     * 时间复杂度：O(1)
     */
    public function setWeight($from, $to, float $weight): bool
    {
        if (!$this->hasEdge($from, $to)) {
            return false;
        }
        
        $this->weights[$from][$to] = $weight;
        if (!$this->isDirected) {
            $this->weights[$to][$from] = $weight;
        }
        
        return true;
    }
    
    /**
     * 获取所有加权边
     * 时间复杂度：O(V + E)
     */
    public function getWeightedEdges(): array
    {
        $edges = [];
        
        foreach ($this->adjacencyList as $from => $neighbors) {
            foreach ($neighbors as $to) {
                if ($this->isDirected || $from <= $to) {
                    $weight = $this->getWeight($from, $to);
                    $edges[] = new WeightedEdge($from, $to, $weight);
                }
            }
        }
        
        return $edges;
    }
    
    /**
     * Dijkstra最短路径算法
     * 时间复杂度：O((V + E) log V)
     */
    public function dijkstra($start): array
    {
        if (!$this->hasVertex($start)) {
            return [];
        }
        
        $distances = [];
        $previous = [];
        $visited = [];
        $vertices = $this->getVertices();
        
        // 初始化距离
        foreach ($vertices as $vertex) {
            $distances[$vertex] = $vertex === $start ? 0 : PHP_FLOAT_MAX;
            $previous[$vertex] = null;
        }
        
        // 使用优先队列（最小堆）
        $queue = new \SplPriorityQueue();
        $queue->setExtractFlags(\SplPriorityQueue::EXTR_DATA);
        $queue->insert($start, 0);
        
        while (!$queue->isEmpty()) {
            $current = $queue->extract();
            
            if (isset($visited[$current])) {
                continue;
            }
            
            $visited[$current] = true;
            
            foreach ($this->getNeighbors($current) as $neighbor) {
                if (isset($visited[$neighbor])) {
                    continue;
                }
                
                $weight = $this->getWeight($current, $neighbor);
                $newDistance = $distances[$current] + $weight;
                
                if ($newDistance < $distances[$neighbor]) {
                    $distances[$neighbor] = $newDistance;
                    $previous[$neighbor] = $current;
                    $queue->insert($neighbor, -$newDistance); // 负值因为SplPriorityQueue是最大堆
                }
            }
        }
        
        return [
            'distances' => $distances,
            'previous' => $previous
        ];
    }
    
    /**
     * 获取两点间的最短路径
     * 时间复杂度：O((V + E) log V)
     */
    public function getShortestPath($start, $end): ?array
    {
        $result = $this->dijkstra($start);
        
        if ($result['distances'][$end] === PHP_FLOAT_MAX) {
            return null; // 无法到达
        }
        
        $path = [];
        $current = $end;
        
        while ($current !== null) {
            array_unshift($path, $current);
            $current = $result['previous'][$current];
        }
        
        return [
            'path' => $path,
            'distance' => $result['distances'][$end]
        ];
    }
    
    /**
     * Floyd-Warshall全源最短路径算法
     * 时间复杂度：O(V³)
     */
    public function floydWarshall(): array
    {
        $vertices = $this->getVertices();
        $n = count($vertices);
        $vertexIndex = array_flip($vertices);
        
        // 初始化距离矩阵
        $dist = [];
        for ($i = 0; $i < $n; $i++) {
            for ($j = 0; $j < $n; $j++) {
                if ($i === $j) {
                    $dist[$i][$j] = 0;
                } else {
                    $from = $vertices[$i];
                    $to = $vertices[$j];
                    $weight = $this->getWeight($from, $to);
                    $dist[$i][$j] = $weight !== null ? $weight : PHP_FLOAT_MAX;
                }
            }
        }
        
        // Floyd-Warshall算法
        for ($k = 0; $k < $n; $k++) {
            for ($i = 0; $i < $n; $i++) {
                for ($j = 0; $j < $n; $j++) {
                    if ($dist[$i][$k] !== PHP_FLOAT_MAX && 
                        $dist[$k][$j] !== PHP_FLOAT_MAX && 
                        $dist[$i][$k] + $dist[$k][$j] < $dist[$i][$j]) {
                        $dist[$i][$j] = $dist[$i][$k] + $dist[$k][$j];
                    }
                }
            }
        }
        
        // 转换回顶点标识
        $result = [];
        for ($i = 0; $i < $n; $i++) {
            for ($j = 0; $j < $n; $j++) {
                $from = $vertices[$i];
                $to = $vertices[$j];
                $result[$from][$to] = $dist[$i][$j];
            }
        }
        
        return $result;
    }
    
    /**
     * Prim最小生成树算法
     * 时间复杂度：O((V + E) log V)
     */
    public function primMST(): array
    {
        if ($this->isDirected) {
            throw new \InvalidArgumentException("MST is only defined for undirected graphs");
        }
        
        $vertices = $this->getVertices();
        if (empty($vertices)) {
            return [];
        }
        
        $mst = [];
        $visited = [];
        $start = $vertices[0];
        $visited[$start] = true;
        
        $edges = new \SplPriorityQueue();
        $edges->setExtractFlags(\SplPriorityQueue::EXTR_DATA);
        
        // 添加起始顶点的所有边
        foreach ($this->getNeighbors($start) as $neighbor) {
            $weight = $this->getWeight($start, $neighbor);
            $edges->insert(new WeightedEdge($start, $neighbor, $weight), -$weight);
        }
        
        while (!$edges->isEmpty() && count($visited) < count($vertices)) {
            $edge = $edges->extract();
            
            if (isset($visited[$edge->to])) {
                continue;
            }
            
            $mst[] = $edge;
            $visited[$edge->to] = true;
            
            // 添加新顶点的所有边
            foreach ($this->getNeighbors($edge->to) as $neighbor) {
                if (!isset($visited[$neighbor])) {
                    $weight = $this->getWeight($edge->to, $neighbor);
                    $edges->insert(new WeightedEdge($edge->to, $neighbor, $weight), -$weight);
                }
            }
        }
        
        return $mst;
    }
    
    /**
     * Kruskal最小生成树算法
     * 时间复杂度：O(E log E)
     */
    public function kruskalMST(): array
    {
        if ($this->isDirected) {
            throw new \InvalidArgumentException("MST is only defined for undirected graphs");
        }
        
        $edges = $this->getWeightedEdges();
        $vertices = $this->getVertices();
        
        // 按权重排序边
        usort($edges, function($a, $b) {
            return $a->weight <=> $b->weight;
        });
        
        // 初始化并查集
        $parent = [];
        $rank = [];
        foreach ($vertices as $vertex) {
            $parent[$vertex] = $vertex;
            $rank[$vertex] = 0;
        }
        
        $find = function($x) use (&$parent, &$find) {
            if ($parent[$x] !== $x) {
                $parent[$x] = $find($parent[$x]);
            }
            return $parent[$x];
        };
        
        $union = function($x, $y) use (&$parent, &$rank, $find) {
            $rootX = $find($x);
            $rootY = $find($y);
            
            if ($rootX !== $rootY) {
                if ($rank[$rootX] < $rank[$rootY]) {
                    $parent[$rootX] = $rootY;
                } elseif ($rank[$rootX] > $rank[$rootY]) {
                    $parent[$rootY] = $rootX;
                } else {
                    $parent[$rootY] = $rootX;
                    $rank[$rootX]++;
                }
                return true;
            }
            return false;
        };
        
        $mst = [];
        foreach ($edges as $edge) {
            if ($union($edge->from, $edge->to)) {
                $mst[] = $edge;
                if (count($mst) === count($vertices) - 1) {
                    break;
                }
            }
        }
        
        return $mst;
    }
    
    /**
     * 计算最小生成树的总权重
     */
    public function getMSTWeight(): float
    {
        $mst = $this->primMST();
        $totalWeight = 0;
        
        foreach ($mst as $edge) {
            $totalWeight += $edge->weight;
        }
        
        return $totalWeight;
    }
    
    /**
     * 检测负权重环（Bellman-Ford算法）
     * 时间复杂度：O(VE)
     */
    public function hasNegativeCycle($start): bool
    {
        if (!$this->hasVertex($start)) {
            return false;
        }
        
        $vertices = $this->getVertices();
        $distances = [];
        
        // 初始化距离
        foreach ($vertices as $vertex) {
            $distances[$vertex] = $vertex === $start ? 0 : PHP_FLOAT_MAX;
        }
        
        // 松弛操作 V-1 次
        for ($i = 0; $i < count($vertices) - 1; $i++) {
            foreach ($this->getWeightedEdges() as $edge) {
                if ($distances[$edge->from] !== PHP_FLOAT_MAX) {
                    $newDistance = $distances[$edge->from] + $edge->weight;
                    if ($newDistance < $distances[$edge->to]) {
                        $distances[$edge->to] = $newDistance;
                    }
                }
            }
        }
        
        // 检查是否还能松弛
        foreach ($this->getWeightedEdges() as $edge) {
            if ($distances[$edge->from] !== PHP_FLOAT_MAX) {
                $newDistance = $distances[$edge->from] + $edge->weight;
                if ($newDistance < $distances[$edge->to]) {
                    return true; // 存在负权重环
                }
            }
        }
        
        return false;
    }
    
    /**
     * 获取图的统计信息
     */
    public function getStatistics(): array
    {
        $edges = $this->getWeightedEdges();
        $weights = array_map(function($edge) { return $edge->weight; }, $edges);
        
        return [
            'vertices' => $this->getVertexCount(),
            'edges' => $this->getEdgeCount(),
            'is_directed' => $this->isDirected,
            'is_connected' => $this->isConnected(),
            'has_cycle' => $this->hasCycle(),
            'min_weight' => !empty($weights) ? min($weights) : null,
            'max_weight' => !empty($weights) ? max($weights) : null,
            'avg_weight' => !empty($weights) ? array_sum($weights) / count($weights) : null,
        ];
    }
    
    /**
     * 清空图
     */
    public function clear(): void
    {
        parent::clear();
        $this->weights = [];
    }
    
    /**
     * 获取图的字符串表示
     */
    public function toString(): string
    {
        $result = "Weighted Graph (" . ($this->isDirected ? "Directed" : "Undirected") . "):\n";
        $result .= "Vertices: " . $this->vertexCount . ", Edges: " . $this->edgeCount . "\n";
        
        foreach ($this->adjacencyList as $vertex => $neighbors) {
            $result .= "$vertex -> [";
            $neighborStrings = [];
            foreach ($neighbors as $neighbor) {
                $weight = $this->getWeight($vertex, $neighbor);
                $neighborStrings[] = "$neighbor($weight)";
            }
            $result .= implode(", ", $neighborStrings) . "]\n";
        }
        
        return $result;
    }
}