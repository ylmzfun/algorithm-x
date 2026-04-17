<?php

namespace DataStructures\Graph;

/**
 * Graph - 图数据结构实现
 * 
 * 思路：
 * 1. 使用邻接表表示图
 * 2. 支持有向图和无向图
 * 3. 提供基本的图操作：添加顶点、添加边、遍历等
 * 4. 实现DFS和BFS遍历算法
 * 
 * 作用：
 * - 表示复杂的关系网络
 * - 路径查找和最短路径算法
 * - 网络分析和社交网络分析
 * - 依赖关系管理
 * 
 * 业务场景：
 * 1. 社交网络：用户关系图，好友推荐
 * 2. 地图导航：道路网络，最短路径规划
 * 3. 网络拓扑：计算机网络结构分析
 * 4. 依赖管理：软件包依赖关系
 * 5. 推荐系统：商品关联推荐
 * 6. 工作流管理：任务依赖关系
 * 7. 知识图谱：实体关系网络
 * 8. 游戏开发：地图连通性，AI寻路
 * 9. 供应链管理：供应商关系网络
 * 10. 生物信息学：蛋白质相互作用网络
 */
class Graph
{
    protected array $adjacencyList;
    protected bool $isDirected;
    protected int $vertexCount;
    protected int $edgeCount;
    
    public function __construct(bool $isDirected = false)
    {
        $this->adjacencyList = [];
        $this->isDirected = $isDirected;
        $this->vertexCount = 0;
        $this->edgeCount = 0;
    }
    
    /**
     * 添加顶点
     * 时间复杂度：O(1)
     */
    public function addVertex($vertex): void
    {
        if (!isset($this->adjacencyList[$vertex])) {
            $this->adjacencyList[$vertex] = [];
            $this->vertexCount++;
        }
    }
    
    /**
     * 删除顶点
     * 时间复杂度：O(V + E)
     */
    public function removeVertex($vertex): bool
    {
        if (!isset($this->adjacencyList[$vertex])) {
            return false;
        }
        
        // 删除所有指向该顶点的边
        foreach ($this->adjacencyList as $v => $neighbors) {
            $this->removeEdge($v, $vertex);
        }
        
        // 删除该顶点的所有边
        $this->edgeCount -= count($this->adjacencyList[$vertex]);
        unset($this->adjacencyList[$vertex]);
        $this->vertexCount--;
        
        return true;
    }
    
    /**
     * 添加边
     * 时间复杂度：O(1)
     */
    public function addEdge($from, $to): void
    {
        $this->addVertex($from);
        $this->addVertex($to);
        
        if (!in_array($to, $this->adjacencyList[$from])) {
            $this->adjacencyList[$from][] = $to;
            $this->edgeCount++;
        }
        
        // 如果是无向图，添加反向边
        if (!$this->isDirected && !in_array($from, $this->adjacencyList[$to])) {
            $this->adjacencyList[$to][] = $from;
        }
    }
    
    /**
     * 删除边
     * 时间复杂度：O(V)
     */
    public function removeEdge($from, $to): bool
    {
        if (!isset($this->adjacencyList[$from])) {
            return false;
        }
        
        $index = array_search($to, $this->adjacencyList[$from]);
        if ($index !== false) {
            array_splice($this->adjacencyList[$from], $index, 1);
            $this->edgeCount--;
            
            // 如果是无向图，删除反向边
            if (!$this->isDirected && isset($this->adjacencyList[$to])) {
                $reverseIndex = array_search($from, $this->adjacencyList[$to]);
                if ($reverseIndex !== false) {
                    array_splice($this->adjacencyList[$to], $reverseIndex, 1);
                }
            }
            
            return true;
        }
        
        return false;
    }
    
    /**
     * 检查边是否存在
     * 时间复杂度：O(V)
     */
    public function hasEdge($from, $to): bool
    {
        return isset($this->adjacencyList[$from]) && 
               in_array($to, $this->adjacencyList[$from]);
    }
    
    /**
     * 检查顶点是否存在
     * 时间复杂度：O(1)
     */
    public function hasVertex($vertex): bool
    {
        return isset($this->adjacencyList[$vertex]);
    }
    
    /**
     * 获取顶点的邻居
     * 时间复杂度：O(1)
     */
    public function getNeighbors($vertex): array
    {
        return $this->adjacencyList[$vertex] ?? [];
    }
    
    /**
     * 获取顶点的度数
     * 时间复杂度：O(1)
     */
    public function getDegree($vertex): int
    {
        if (!isset($this->adjacencyList[$vertex])) {
            return 0;
        }
        
        $outDegree = count($this->adjacencyList[$vertex]);
        
        if ($this->isDirected) {
            return $outDegree;
        }
        
        return $outDegree;
    }
    
    /**
     * 获取顶点的入度（仅对有向图有意义）
     * 时间复杂度：O(V + E)
     */
    public function getInDegree($vertex): int
    {
        if (!$this->isDirected) {
            return $this->getDegree($vertex);
        }
        
        $inDegree = 0;
        foreach ($this->adjacencyList as $neighbors) {
            if (in_array($vertex, $neighbors)) {
                $inDegree++;
            }
        }
        
        return $inDegree;
    }
    
    /**
     * 获取所有顶点
     * 时间复杂度：O(V)
     */
    public function getVertices(): array
    {
        return array_keys($this->adjacencyList);
    }
    
    /**
     * 获取所有边
     * 时间复杂度：O(V + E)
     */
    public function getEdges(): array
    {
        $edges = [];
        
        foreach ($this->adjacencyList as $from => $neighbors) {
            foreach ($neighbors as $to) {
                if ($this->isDirected || $from <= $to) {
                    $edges[] = [$from, $to];
                }
            }
        }
        
        return $edges;
    }
    
    /**
     * 获取顶点数量
     */
    public function getVertexCount(): int
    {
        return $this->vertexCount;
    }
    
    /**
     * 获取边数量
     */
    public function getEdgeCount(): int
    {
        return $this->edgeCount;
    }
    
    /**
     * 检查图是否为空
     */
    public function isEmpty(): bool
    {
        return $this->vertexCount === 0;
    }
    
    /**
     * 深度优先搜索（DFS）
     * 时间复杂度：O(V + E)
     */
    public function dfs($startVertex, callable $callback = null): array
    {
        if (!$this->hasVertex($startVertex)) {
            return [];
        }
        
        $visited = [];
        $result = [];
        $this->dfsHelper($startVertex, $visited, $result, $callback);
        
        return $result;
    }
    
    private function dfsHelper($vertex, array &$visited, array &$result, callable $callback = null): void
    {
        $visited[$vertex] = true;
        $result[] = $vertex;
        
        if ($callback !== null) {
            call_user_func($callback, $vertex);
        }
        
        foreach ($this->getNeighbors($vertex) as $neighbor) {
            if (!isset($visited[$neighbor])) {
                $this->dfsHelper($neighbor, $visited, $result, $callback);
            }
        }
    }
    
    /**
     * 广度优先搜索（BFS）
     * 时间复杂度：O(V + E)
     */
    public function bfs($startVertex, callable $callback = null): array
    {
        if (!$this->hasVertex($startVertex)) {
            return [];
        }
        
        $visited = [$startVertex => true];
        $queue = [$startVertex];
        $result = [];
        
        while (!empty($queue)) {
            $vertex = array_shift($queue);
            $result[] = $vertex;
            
            if ($callback !== null) {
                call_user_func($callback, $vertex);
            }
            
            foreach ($this->getNeighbors($vertex) as $neighbor) {
                if (!isset($visited[$neighbor])) {
                    $visited[$neighbor] = true;
                    $queue[] = $neighbor;
                }
            }
        }
        
        return $result;
    }
    
    /**
     * 查找两个顶点之间的路径
     * 时间复杂度：O(V + E)
     */
    public function findPath($start, $end): ?array
    {
        if (!$this->hasVertex($start) || !$this->hasVertex($end)) {
            return null;
        }
        
        if ($start === $end) {
            return [$start];
        }
        
        $visited = [$start => true];
        $queue = [[$start]];
        
        while (!empty($queue)) {
            $path = array_shift($queue);
            $vertex = end($path);
            
            foreach ($this->getNeighbors($vertex) as $neighbor) {
                if ($neighbor === $end) {
                    return array_merge($path, [$neighbor]);
                }
                
                if (!isset($visited[$neighbor])) {
                    $visited[$neighbor] = true;
                    $queue[] = array_merge($path, [$neighbor]);
                }
            }
        }
        
        return null;
    }
    
    /**
     * 检查图是否连通
     * 时间复杂度：O(V + E)
     */
    public function isConnected(): bool
    {
        if ($this->isEmpty()) {
            return true;
        }
        
        $vertices = $this->getVertices();
        $visited = $this->dfs($vertices[0]);
        
        return count($visited) === $this->vertexCount;
    }
    
    /**
     * 检测环（仅对有向图）
     * 时间复杂度：O(V + E)
     */
    public function hasCycle(): bool
    {
        if (!$this->isDirected) {
            return $this->hasUndirectedCycle();
        }
        
        $visited = [];
        $recursionStack = [];
        
        foreach ($this->getVertices() as $vertex) {
            if (!isset($visited[$vertex])) {
                if ($this->hasCycleHelper($vertex, $visited, $recursionStack)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    private function hasCycleHelper($vertex, array &$visited, array &$recursionStack): bool
    {
        $visited[$vertex] = true;
        $recursionStack[$vertex] = true;
        
        foreach ($this->getNeighbors($vertex) as $neighbor) {
            if (!isset($visited[$neighbor])) {
                if ($this->hasCycleHelper($neighbor, $visited, $recursionStack)) {
                    return true;
                }
            } elseif (isset($recursionStack[$neighbor])) {
                return true;
            }
        }
        
        unset($recursionStack[$vertex]);
        return false;
    }
    
    /**
     * 检测无向图中的环
     */
    private function hasUndirectedCycle(): bool
    {
        $visited = [];
        
        foreach ($this->getVertices() as $vertex) {
            if (!isset($visited[$vertex])) {
                if ($this->hasUndirectedCycleHelper($vertex, -1, $visited)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    private function hasUndirectedCycleHelper($vertex, $parent, array &$visited): bool
    {
        $visited[$vertex] = true;
        
        foreach ($this->getNeighbors($vertex) as $neighbor) {
            if (!isset($visited[$neighbor])) {
                if ($this->hasUndirectedCycleHelper($neighbor, $vertex, $visited)) {
                    return true;
                }
            } elseif ($neighbor !== $parent) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * 拓扑排序（仅对有向无环图）
     * 时间复杂度：O(V + E)
     */
    public function topologicalSort(): ?array
    {
        if (!$this->isDirected || $this->hasCycle()) {
            return null;
        }
        
        $inDegree = [];
        $vertices = $this->getVertices();
        
        // 计算所有顶点的入度
        foreach ($vertices as $vertex) {
            $inDegree[$vertex] = $this->getInDegree($vertex);
        }
        
        $queue = [];
        foreach ($inDegree as $vertex => $degree) {
            if ($degree === 0) {
                $queue[] = $vertex;
            }
        }
        
        $result = [];
        
        while (!empty($queue)) {
            $vertex = array_shift($queue);
            $result[] = $vertex;
            
            foreach ($this->getNeighbors($vertex) as $neighbor) {
                $inDegree[$neighbor]--;
                if ($inDegree[$neighbor] === 0) {
                    $queue[] = $neighbor;
                }
            }
        }
        
        return count($result) === $this->vertexCount ? $result : null;
    }
    
    /**
     * 清空图
     */
    public function clear(): void
    {
        $this->adjacencyList = [];
        $this->vertexCount = 0;
        $this->edgeCount = 0;
    }
    
    /**
     * 获取图的字符串表示
     */
    public function toString(): string
    {
        $result = "Graph (" . ($this->isDirected ? "Directed" : "Undirected") . "):\n";
        $result .= "Vertices: " . $this->vertexCount . ", Edges: " . $this->edgeCount . "\n";
        
        foreach ($this->adjacencyList as $vertex => $neighbors) {
            $result .= "$vertex -> [" . implode(", ", $neighbors) . "]\n";
        }
        
        return $result;
    }
    
    /**
     * 从邻接矩阵创建图
     */
    public static function fromAdjacencyMatrix(array $matrix, bool $isDirected = false): Graph
    {
        $graph = new self($isDirected);
        $size = count($matrix);
        
        // 添加顶点
        for ($i = 0; $i < $size; $i++) {
            $graph->addVertex($i);
        }
        
        // 添加边
        for ($i = 0; $i < $size; $i++) {
            for ($j = 0; $j < $size; $j++) {
                if ($matrix[$i][$j] !== 0) {
                    $graph->addEdge($i, $j);
                }
            }
        }
        
        return $graph;
    }
    
    /**
     * 转换为邻接矩阵
     */
    public function toAdjacencyMatrix(): array
    {
        $vertices = $this->getVertices();
        $size = count($vertices);
        $vertexIndex = array_flip($vertices);
        
        $matrix = array_fill(0, $size, array_fill(0, $size, 0));
        
        foreach ($this->adjacencyList as $from => $neighbors) {
            $fromIndex = $vertexIndex[$from];
            foreach ($neighbors as $to) {
                $toIndex = $vertexIndex[$to];
                $matrix[$fromIndex][$toIndex] = 1;
            }
        }
        
        return $matrix;
    }
}