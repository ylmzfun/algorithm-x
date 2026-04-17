<?php

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Graph\Graph;
use DataStructures\Graph\WeightedGraph;

/**
 * 图数据结构使用示例
 */

echo "=== 图数据结构示例 ===\n\n";

// 1. 无向图示例
echo "1. 无向图示例:\n";
$undirectedGraph = new Graph(false); // 无向图

// 添加顶点
$cities = ['北京', '上海', '广州', '深圳', '杭州'];
foreach ($cities as $city) {
    $undirectedGraph->addVertex($city);
}

// 添加边（城市间的连接）
$undirectedGraph->addEdge('北京', '上海');
$undirectedGraph->addEdge('上海', '杭州');
$undirectedGraph->addEdge('上海', '广州');
$undirectedGraph->addEdge('广州', '深圳');
$undirectedGraph->addEdge('北京', '广州');

echo "顶点数: {$undirectedGraph->getVertexCount()}\n";
echo "边数: {$undirectedGraph->getEdgeCount()}\n";
echo "北京的邻居: " . implode(", ", $undirectedGraph->getNeighbors('北京')) . "\n";
echo "上海的度数: {$undirectedGraph->getDegree('上海')}\n\n";

// DFS 遍历
echo "从北京开始的DFS遍历: " . implode(" -> ", $undirectedGraph->dfs('北京')) . "\n";
// BFS 遍历
echo "从北京开始的BFS遍历: " . implode(" -> ", $undirectedGraph->bfs('北京')) . "\n";

// 路径查找
$path = $undirectedGraph->findPath('北京', '深圳');
if ($path) {
    echo "北京到深圳的路径: " . implode(" -> ", $path) . "\n";
} else {
    echo "北京到深圳没有路径\n";
}

// 检测环
echo "图中是否有环: " . ($undirectedGraph->hasCycle() ? "是" : "否") . "\n\n";

// 2. 有向图示例
echo "2. 有向图示例:\n";
$directedGraph = new Graph(true); // 有向图

// 构建课程依赖关系图
$courses = ['数学基础', '编程基础', '数据结构', '算法', '数据库', '软件工程'];
foreach ($courses as $course) {
    $directedGraph->addVertex($course);
}

// 添加依赖关系（前置课程 -> 后续课程）
$directedGraph->addEdge('数学基础', '算法');
$directedGraph->addEdge('编程基础', '数据结构');
$directedGraph->addEdge('数据结构', '算法');
$directedGraph->addEdge('编程基础', '数据库');
$directedGraph->addEdge('数据结构', '软件工程');
$directedGraph->addEdge('算法', '软件工程');

echo "课程数: {$directedGraph->getVertexCount()}\n";
echo "依赖关系数: {$directedGraph->getEdgeCount()}\n";
echo "数据结构的入度: {$directedGraph->getInDegree('数据结构')}\n";
echo "数据结构的出度: {$directedGraph->getDegree('数据结构')}\n\n";

// 拓扑排序（课程学习顺序）
$topologicalOrder = $directedGraph->topologicalSort();
if ($topologicalOrder) {
    echo "推荐的课程学习顺序: " . implode(" -> ", $topologicalOrder) . "\n";
} else {
    echo "课程依赖关系中存在循环，无法确定学习顺序\n";
}

// 检测有向图中的环
echo "课程依赖中是否有循环: " . ($directedGraph->hasCycle() ? "是" : "否") . "\n\n";

// 3. 加权图示例
echo "3. 加权图示例:\n";
$weightedGraph = new WeightedGraph(false); // 无向加权图

// 添加城市
$cities = ['A', 'B', 'C', 'D', 'E'];
foreach ($cities as $city) {
    $weightedGraph->addVertex($city);
}

// 添加带权重的边（距离）
$weightedGraph->addEdge('A', 'B', 4);
$weightedGraph->addEdge('A', 'C', 2);
$weightedGraph->addEdge('B', 'C', 1);
$weightedGraph->addEdge('B', 'D', 5);
$weightedGraph->addEdge('C', 'D', 8);
$weightedGraph->addEdge('C', 'E', 10);
$weightedGraph->addEdge('D', 'E', 2);

echo "加权图顶点数: {$weightedGraph->getVertexCount()}\n";
echo "加权图边数: {$weightedGraph->getEdgeCount()}\n";
echo "A到B的距离: {$weightedGraph->getWeight('A', 'B')}\n";
echo "C到E的距离: {$weightedGraph->getWeight('C', 'E')}\n\n";

// Dijkstra 最短路径
echo "Dijkstra算法 - 从A到所有点的最短距离:\n";
$distances = $weightedGraph->dijkstra('A');
foreach ($distances as $vertex => $distance) {
    if ($distance === PHP_INT_MAX) {
        echo "A到{$vertex}: 不可达\n";
    } else {
        echo "A到{$vertex}: {$distance}\n";
    }
}
echo "\n";

// 最小生成树 (Prim算法)
echo "Prim算法 - 最小生成树:\n";
$mst = $weightedGraph->primMST();
if ($mst) {
    $totalWeight = 0;
    foreach ($mst as $edge) {
        echo "{$edge['from']} - {$edge['to']}: {$edge['weight']}\n";
        $totalWeight += $edge['weight'];
    }
    echo "最小生成树总权重: {$totalWeight}\n";
} else {
    echo "无法构建最小生成树\n";
}
echo "\n";

// 4. 实际应用场景示例
echo "4. 实际应用场景示例:\n";

// 社交网络分析
echo "社交网络分析:\n";
$socialNetwork = new Graph(false);

$users = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'];
foreach ($users as $user) {
    $socialNetwork->addVertex($user);
}

// 添加好友关系
$friendships = [
    ['Alice', 'Bob'],
    ['Alice', 'Charlie'],
    ['Bob', 'David'],
    ['Charlie', 'David'],
    ['Charlie', 'Eve'],
    ['David', 'Frank'],
    ['Eve', 'Frank']
];

foreach ($friendships as $friendship) {
    $socialNetwork->addEdge($friendship[0], $friendship[1]);
}

echo "用户数: {$socialNetwork->getVertexCount()}\n";
echo "好友关系数: {$socialNetwork->getEdgeCount()}\n";
echo "Alice的好友: " . implode(", ", $socialNetwork->getNeighbors('Alice')) . "\n";
echo "Charlie的好友数: {$socialNetwork->getDegree('Charlie')}\n";

// 查找两个用户之间的关系路径
$connectionPath = $socialNetwork->findPath('Alice', 'Frank');
if ($connectionPath) {
    echo "Alice和Frank的连接路径: " . implode(" -> ", $connectionPath) . "\n";
    echo "关系度数: " . (count($connectionPath) - 1) . "\n";
} else {
    echo "Alice和Frank没有连接\n";
}
echo "\n";

// 物流配送网络
echo "物流配送网络:\n";
$logisticsNetwork = new WeightedGraph(true); // 有向加权图

$locations = ['仓库', '配送中心A', '配送中心B', '客户1', '客户2', '客户3'];
foreach ($locations as $location) {
    $logisticsNetwork->addVertex($location);
}

// 添加配送路线和成本
$routes = [
    ['仓库', '配送中心A', 10],
    ['仓库', '配送中心B', 15],
    ['配送中心A', '客户1', 5],
    ['配送中心A', '客户2', 8],
    ['配送中心B', '客户2', 6],
    ['配送中心B', '客户3', 4],
    ['配送中心A', '配送中心B', 3]
];

foreach ($routes as $route) {
    $logisticsNetwork->addEdge($route[0], $route[1], $route[2]);
}

echo "配送网络节点数: {$logisticsNetwork->getVertexCount()}\n";
echo "配送路线数: {$logisticsNetwork->getEdgeCount()}\n";

// 计算从仓库到所有地点的最短配送成本
echo "从仓库到各地点的最短配送成本:\n";
$deliveryCosts = $logisticsNetwork->dijkstra('仓库');
foreach ($deliveryCosts as $location => $cost) {
    if ($location !== '仓库') {
        if ($cost === PHP_INT_MAX) {
            echo "仓库到{$location}: 不可达\n";
        } else {
            echo "仓库到{$location}: {$cost}\n";
        }
    }
}
echo "\n";

echo "=== 示例结束 ===\n";