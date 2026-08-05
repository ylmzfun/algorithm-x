# 加权图 (Weighted Graph) 实现
# 
# 思路：
# 加权图是在普通图的基础上为每条边添加权重值，用于表示边的成本、距离、时间等。
# 支持最短路径算法（Dijkstra、Floyd-Warshall）、最小生成树算法（Kruskal、Prim）等。
# 权重可以是正数、负数或零，不同算法对权重有不同要求。
# 
# 作用：
# 1. 路径优化：最短路径、最小成本路径
# 2. 网络设计：最小生成树、网络连接成本
# 3. 调度优化：任务调度、资源分配
# 4. 图分析：中心性分析、关键路径
# 
# 应用场景：
# 1. 地图导航：路径规划、交通成本
# 2. 网络路由：数据包路由、带宽优化
# 3. 供应链：物流成本、运输优化
# 4. 金融分析：风险评估、投资组合
# 5. 社交网络：影响力传播、关系强度
# 6. 游戏AI：移动成本、策略规划

require_relative 'graph'
require 'set'

# 加权图类，继承自基础图类
class WeightedGraph < Graph
  def initialize(directed = false)
    super(directed)
    @edge_weights = {}  # 存储边的权重
  end

  # 添加带权重的边
  def add_edge(from_id, to_id, weight = 1)
    return false unless super(from_id, to_id, weight)
    
    # 存储权重信息
    @edge_weights[[from_id, to_id]] = weight
    @edge_weights[[to_id, from_id]] = weight unless @directed
    
    true
  end

  # 删除边时同时删除权重信息
  def remove_edge(from_id, to_id)
    return false unless super(from_id, to_id)
    
    @edge_weights.delete([from_id, to_id])
    @edge_weights.delete([to_id, from_id]) unless @directed
    
    true
  end

  # 获取边的权重
  def get_weight(from_id, to_id)
    @edge_weights[[from_id, to_id]]
  end

  # 更新边的权重
  def update_weight(from_id, to_id, new_weight)
    return false unless has_edge?(from_id, to_id)
    
    @edge_weights[[from_id, to_id]] = new_weight
    @edge_weights[[to_id, from_id]] = new_weight unless @directed
    
    # 更新边对象的权重
    from_vertex = @vertices[from_id]
    to_vertex = @vertices[to_id]
    edge = @edges.find { |e| e.from == from_vertex && e.to == to_vertex }
    edge.weight = new_weight if edge
    
    true
  end

  # Dijkstra最短路径算法
  def dijkstra(start_id)
    return {} unless @vertices.key?(start_id)
    
    distances = {}
    previous = {}
    unvisited = Set.new(@vertices.keys)
    
    # 初始化距离
    @vertices.each_key do |vertex_id|
      distances[vertex_id] = vertex_id == start_id ? 0 : Float::INFINITY
      previous[vertex_id] = nil
    end
    
    while !unvisited.empty?
      # 找到未访问顶点中距离最小的
      current = unvisited.min_by { |vertex_id| distances[vertex_id] }
      break if distances[current] == Float::INFINITY
      
      unvisited.delete(current)
      
      # 更新邻居的距离
      neighbors(current).each do |neighbor|
        next unless unvisited.include?(neighbor.id)
        
        alt_distance = distances[current] + get_weight(current, neighbor.id)
        
        if alt_distance < distances[neighbor.id]
          distances[neighbor.id] = alt_distance
          previous[neighbor.id] = current
        end
      end
    end
    
    { distances: distances, previous: previous }
  end

  # 获取两点间的最短路径
  def shortest_path(start_id, end_id)
    result = dijkstra(start_id)
    return { path: [], distance: Float::INFINITY } unless result[:distances][end_id] < Float::INFINITY
    
    path = []
    current = end_id
    
    while current
      path.unshift(current)
      current = result[:previous][current]
    end
    
    { path: path, distance: result[:distances][end_id] }
  end

  # 获取从起点到所有点的最短路径
  def shortest_paths(start_id)
    result = dijkstra(start_id)
    paths = {}
    
    @vertices.each_key do |vertex_id|
      next if vertex_id == start_id
      
      if result[:distances][vertex_id] < Float::INFINITY
        path = []
        current = vertex_id
        
        while current
          path.unshift(current)
          current = result[:previous][current]
        end
        
        paths[vertex_id] = {
          path: path,
          distance: result[:distances][vertex_id]
        }
      end
    end
    
    paths
  end

  # Floyd-Warshall算法（所有点对最短路径）
  def floyd_warshall
    vertex_ids = @vertices.keys.sort
    n = vertex_ids.size
    
    # 初始化距离矩阵
    dist = Array.new(n) { Array.new(n, Float::INFINITY) }
    
    # 设置直接连接的边
    vertex_ids.each_with_index do |i_id, i|
      vertex_ids.each_with_index do |j_id, j|
        if i == j
          dist[i][j] = 0
        elsif has_edge?(i_id, j_id)
          dist[i][j] = get_weight(i_id, j_id)
        end
      end
    end
    
    # Floyd-Warshall核心算法
    n.times do |k|
      n.times do |i|
        n.times do |j|
          if dist[i][k] + dist[k][j] < dist[i][j]
            dist[i][j] = dist[i][k] + dist[k][j]
          end
        end
      end
    end
    
    # 转换为哈希格式
    result = {}
    vertex_ids.each_with_index do |i_id, i|
      result[i_id] = {}
      vertex_ids.each_with_index do |j_id, j|
        result[i_id][j_id] = dist[i][j]
      end
    end
    
    result
  end

  # Bellman-Ford算法（支持负权重）
  def bellman_ford(start_id)
    return { distances: {}, previous: {}, has_negative_cycle: true } unless @vertices.key?(start_id)
    
    distances = {}
    previous = {}
    
    # 初始化
    @vertices.each_key do |vertex_id|
      distances[vertex_id] = vertex_id == start_id ? 0 : Float::INFINITY
      previous[vertex_id] = nil
    end
    
    # 松弛边 |V| - 1 次
    (@vertices.size - 1).times do
      @edges.each do |edge|
        from_id = edge.from.id
        to_id = edge.to.id
        weight = edge.weight
        
        if distances[from_id] != Float::INFINITY && distances[from_id] + weight < distances[to_id]
          distances[to_id] = distances[from_id] + weight
          previous[to_id] = from_id
        end
      end
    end
    
    # 检查负权重环
    has_negative_cycle = false
    @edges.each do |edge|
      from_id = edge.from.id
      to_id = edge.to.id
      weight = edge.weight
      
      if distances[from_id] != Float::INFINITY && distances[from_id] + weight < distances[to_id]
        has_negative_cycle = true
        break
      end
    end
    
    {
      distances: distances,
      previous: previous,
      has_negative_cycle: has_negative_cycle
    }
  end

  # Kruskal最小生成树算法
  def kruskal_mst
    return [] if @directed  # 只适用于无向图
    
    # 并查集实现
    parent = {}
    rank = {}
    
    # 初始化并查集
    @vertices.each_key do |vertex_id|
      parent[vertex_id] = vertex_id
      rank[vertex_id] = 0
    end
    
    # 查找根节点
    find = lambda do |x|
      if parent[x] != x
        parent[x] = find.call(parent[x])  # 路径压缩
      end
      parent[x]
    end
    
    # 合并两个集合
    union = lambda do |x, y|
      root_x = find.call(x)
      root_y = find.call(y)
      
      return false if root_x == root_y
      
      # 按秩合并
      if rank[root_x] < rank[root_y]
        parent[root_x] = root_y
      elsif rank[root_x] > rank[root_y]
        parent[root_y] = root_x
      else
        parent[root_y] = root_x
        rank[root_x] += 1
      end
      
      true
    end
    
    # 按权重排序边
    sorted_edges = @edges.sort_by(&:weight)
    mst_edges = []
    total_weight = 0
    
    sorted_edges.each do |edge|
      from_id = edge.from.id
      to_id = edge.to.id
      
      if union.call(from_id, to_id)
        mst_edges << edge
        total_weight += edge.weight
        break if mst_edges.size == @vertices.size - 1
      end
    end
    
    { edges: mst_edges, total_weight: total_weight }
  end

  # Prim最小生成树算法
  def prim_mst(start_id = nil)
    return { edges: [], total_weight: 0 } if @directed || @vertices.empty?
    
    start_id ||= @vertices.keys.first
    return { edges: [], total_weight: 0 } unless @vertices.key?(start_id)
    
    mst_edges = []
    total_weight = 0
    visited = Set.new([start_id])
    
    while visited.size < @vertices.size
      min_edge = nil
      min_weight = Float::INFINITY
      
      # 找到连接已访问和未访问顶点的最小权重边
      visited.each do |vertex_id|
        neighbors(vertex_id).each do |neighbor|
          next if visited.include?(neighbor.id)
          
          weight = get_weight(vertex_id, neighbor.id)
          if weight < min_weight
            min_weight = weight
            min_edge = [vertex_id, neighbor.id, weight]
          end
        end
      end
      
      break unless min_edge
      
      from_id, to_id, weight = min_edge
      visited.add(to_id)
      
      # 创建边对象
      edge = Edge.new(@vertices[from_id], @vertices[to_id], weight)
      mst_edges << edge
      total_weight += weight
    end
    
    { edges: mst_edges, total_weight: total_weight }
  end

  # 检查是否有负权重边
  def has_negative_weights?
    @edges.any? { |edge| edge.weight < 0 }
  end

  # 获取图中的最小和最大权重
  def weight_range
    return [nil, nil] if @edges.empty?
    
    weights = @edges.map(&:weight)
    [weights.min, weights.max]
  end

  # 计算图的总权重
  def total_weight
    total = @edges.sum(&:weight)
    @directed ? total : total / 2
  end

  # 获取权重分布统计
  def weight_statistics
    return {} if @edges.empty?
    
    weights = @edges.map(&:weight)
    weights = weights.uniq.sort unless @directed  # 无向图去重
    
    {
      count: weights.size,
      min: weights.min,
      max: weights.max,
      sum: weights.sum,
      average: weights.sum.to_f / weights.size,
      median: weights.size.odd? ? weights[weights.size / 2] : (weights[weights.size / 2 - 1] + weights[weights.size / 2]) / 2.0
    }
  end

  # 清空图时也清空权重信息
  def clear
    super
    @edge_weights.clear
    self
  end

  # 打印带权重的图结构
  def print_weighted_graph
    puts "Weighted Graph Structure:"
    @adjacency_list.each do |vertex_id, neighbors|
      neighbor_info = neighbors.map do |neighbor|
        weight = get_weight(vertex_id, neighbor.id)
        "#{neighbor.id}(#{weight})"
      end.join(", ")
      puts "  #{vertex_id} -> [#{neighbor_info}]"
    end
  end

  def to_s
    type = @directed ? "Directed" : "Undirected"
    "#{type}WeightedGraph[vertices: #{vertex_count}, edges: #{edge_count}, total_weight: #{total_weight}]"
  end
end

# 加权图应用示例
module WeightedGraphApplications
  # 路径规划系统
  class RouteOptimizer
    def initialize
      @graph = WeightedGraph.new(false)
    end

    def add_location(name)
      @graph.add_vertex(name)
    end

    def add_route(from, to, distance)
      @graph.add_edge(from, to, distance)
    end

    def find_shortest_route(from, to)
      @graph.shortest_path(from, to)
    end

    def find_all_routes(from)
      @graph.shortest_paths(from)
    end

    def optimize_network
      @graph.prim_mst
    end

    def print_network
      @graph.print_weighted_graph
    end
  end

  # 网络成本分析
  class NetworkCostAnalyzer
    def initialize(directed = true)
      @graph = WeightedGraph.new(directed)
    end

    def add_node(id, name = nil)
      @graph.add_vertex(id, name)
    end

    def add_connection(from, to, cost)
      @graph.add_edge(from, to, cost)
    end

    def analyze_costs
      {
        total_cost: @graph.total_weight,
        weight_stats: @graph.weight_statistics,
        has_negative_costs: @graph.has_negative_weights?
      }
    end

    def find_minimum_spanning_network
      @graph.kruskal_mst
    end

    def calculate_all_pairs_shortest_paths
      @graph.floyd_warshall
    end
  end

  # 任务调度系统
  class TaskScheduler
    def initialize
      @graph = WeightedGraph.new(true)  # 有向图表示依赖关系
    end

    def add_task(id, duration)
      @graph.add_vertex(id, duration)
    end

    def add_dependency(from_task, to_task, delay = 0)
      @graph.add_edge(from_task, to_task, delay)
    end

    def find_critical_path(start_task, end_task)
      # 使用最长路径算法找关键路径
      # 这里简化为最短路径的负权重版本
      result = @graph.shortest_path(start_task, end_task)
      {
        path: result[:path],
        duration: result[:distance]
      }
    end

    def schedule_tasks
      @graph.topological_sort
    end
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== WeightedGraph 使用示例 ==="
  
  # 创建加权无向图
  wgraph = WeightedGraph.new(false)
  
  # 添加城市顶点
  cities = %w[北京 上海 广州 深圳 杭州 南京]
  cities.each { |city| wgraph.add_vertex(city) }
  
  # 添加带权重的边（距离）
  routes = [
    ['北京', '上海', 1200], ['北京', '南京', 1000],
    ['上海', '杭州', 180], ['上海', '广州', 1400],
    ['杭州', '南京', 300], ['广州', '深圳', 140],
    ['南京', '杭州', 300]
  ]
  
  routes.each { |from, to, distance| wgraph.add_edge(from, to, distance) }
  
  puts "加权图信息:"
  puts wgraph
  wgraph.print_weighted_graph
  
  puts "\n权重统计:"
  stats = wgraph.weight_statistics
  puts "边数: #{stats[:count]}"
  puts "最短距离: #{stats[:min]}km"
  puts "最长距离: #{stats[:max]}km"
  puts "平均距离: #{stats[:average].round(2)}km"
  puts "总权重: #{wgraph.total_weight}km"
  
  puts "\n=== 最短路径算法 ==="
  
  # Dijkstra算法
  puts "\n从北京到各城市的最短路径:"
  paths = wgraph.shortest_paths('北京')
  paths.each do |city, info|
    puts "到#{city}: #{info[:path].join(' -> ')} (#{info[:distance]}km)"
  end
  
  # 特定路径
  result = wgraph.shortest_path('北京', '深圳')
  puts "\n北京到深圳最短路径:"
  puts "路径: #{result[:path].join(' -> ')}"
  puts "距离: #{result[:distance]}km"
  
  puts "\n=== 最小生成树算法 ==="
  
  # Kruskal算法
  kruskal_result = wgraph.kruskal_mst
  puts "\nKruskal最小生成树:"
  puts "总权重: #{kruskal_result[:total_weight]}km"
  puts "边:"
  kruskal_result[:edges].each do |edge|
    puts "  #{edge.from.id} - #{edge.to.id}: #{edge.weight}km"
  end
  
  # Prim算法
  prim_result = wgraph.prim_mst('北京')
  puts "\nPrim最小生成树（从北京开始）:"
  puts "总权重: #{prim_result[:total_weight]}km"
  puts "边:"
  prim_result[:edges].each do |edge|
    puts "  #{edge.from.id} - #{edge.to.id}: #{edge.weight}km"
  end
  
  puts "\n=== Floyd-Warshall算法 ==="
  
  # 所有点对最短路径
  all_paths = wgraph.floyd_warshall
  puts "\n所有城市间最短距离矩阵:"
  cities.each do |from_city|
    distances = cities.map { |to_city| all_paths[from_city][to_city] }
    puts "#{from_city}: #{distances.map { |d| d == Float::INFINITY ? '∞' : d.to_s }.join('\t')}"
  end
  
  puts "\n=== 应用示例 ==="
  
  # 路径规划系统
  puts "\n路径规划系统:"
  optimizer = WeightedGraphApplications::RouteOptimizer.new
  
  # 添加地点和路线
  %w[家 公司 超市 学校 医院].each { |place| optimizer.add_location(place) }
  
  connections = [
    ['家', '公司', 15], ['家', '超市', 8], ['家', '学校', 12],
    ['公司', '超市', 10], ['公司', '医院', 20],
    ['超市', '学校', 5], ['学校', '医院', 18]
  ]
  
  connections.each { |from, to, time| optimizer.add_route(from, to, time) }
  
  route = optimizer.find_shortest_route('家', '医院')
  puts "从家到医院最短路径: #{route[:path].join(' -> ')} (#{route[:distance]}分钟)"
  
  # 网络优化
  mst = optimizer.optimize_network
  puts "\n网络优化结果（最小生成树）:"
  puts "总成本: #{mst[:total_weight]}分钟"
  
  puts "\n=== 性能测试 ==="
  
  # 创建大型加权图
  large_wgraph = WeightedGraph.new(false)
  
  start_time = Time.now
  
  # 添加500个顶点
  500.times { |i| large_wgraph.add_vertex(i) }
  
  # 添加随机权重边
  1000.times do
    from = rand(500)
    to = rand(500)
    weight = rand(1..100)
    large_wgraph.add_edge(from, to, weight) if from != to
  end
  
  end_time = Time.now
  
  puts "构建500顶点加权图耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  puts "图信息: #{large_wgraph}"
  
  # Dijkstra性能测试
  start_time = Time.now
  large_wgraph.dijkstra(0)
  end_time = Time.now
  
  puts "Dijkstra算法耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  
  # MST性能测试
  start_time = Time.now
  large_wgraph.kruskal_mst
  end_time = Time.now
  
  puts "Kruskal算法耗时: #{((end_time - start_time) * 1000).round(2)}ms"
end