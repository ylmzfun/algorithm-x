# 图 (Graph) 实现
# 
# 思路：
# 图是由顶点(Vertex)和边(Edge)组成的数据结构，用于表示对象之间的关系。
# 可以用邻接表或邻接矩阵来实现。邻接表适合稀疏图，邻接矩阵适合稠密图。
# 图可以是有向的或无向的，带权重的或不带权重的。
# 
# 作用：
# 1. 网络建模：社交网络、计算机网络、交通网络
# 2. 路径查找：最短路径、连通性检测
# 3. 依赖关系：任务调度、编译依赖
# 4. 推荐系统：用户关系、物品关联
# 
# 应用场景：
# 1. 社交媒体：好友关系、信息传播
# 2. 地图导航：路径规划、交通优化
# 3. 网络分析：网页链接、引用关系
# 4. 游戏开发：地图连接、AI寻路
# 5. 数据库：关系建模、查询优化
# 6. 编译器：依赖分析、优化

# 图的顶点类
class Vertex
  attr_accessor :value, :visited, :distance, :parent
  attr_reader :id

  def initialize(id, value = nil)
    @id = id
    @value = value || id
    @visited = false
    @distance = Float::INFINITY
    @parent = nil
  end

  def reset
    @visited = false
    @distance = Float::INFINITY
    @parent = nil
  end

  def to_s
    @value.to_s
  end

  def inspect
    "#<Vertex:#{object_id} id=#{@id} value=#{@value.inspect}>"
  end

  def ==(other)
    other.is_a?(Vertex) && @id == other.id
  end

  def hash
    @id.hash
  end
end

# 图的边类
class Edge
  attr_accessor :from, :to, :weight

  def initialize(from, to, weight = 1)
    @from = from
    @to = to
    @weight = weight
  end

  def to_s
    "#{@from} -> #{@to} (#{@weight})"
  end

  def inspect
    "#<Edge:#{object_id} from=#{@from} to=#{@to} weight=#{@weight}>"
  end

  def ==(other)
    other.is_a?(Edge) && @from == other.from && @to == other.to
  end
end

# 无向图实现（邻接表）
class Graph
  attr_reader :vertices, :edges, :directed

  def initialize(directed = false)
    @vertices = {}
    @adjacency_list = {}
    @edges = []
    @directed = directed
  end

  # 添加顶点
  def add_vertex(id, value = nil)
    return false if @vertices.key?(id)
    
    vertex = Vertex.new(id, value)
    @vertices[id] = vertex
    @adjacency_list[id] = []
    true
  end

  # 删除顶点
  def remove_vertex(id)
    return false unless @vertices.key?(id)
    
    # 删除所有相关的边
    @adjacency_list[id].each do |neighbor|
      remove_edge(id, neighbor.id)
    end
    
    # 删除指向该顶点的边
    @vertices.each_key do |vertex_id|
      remove_edge(vertex_id, id)
    end
    
    @vertices.delete(id)
    @adjacency_list.delete(id)
    true
  end

  # 添加边
  def add_edge(from_id, to_id, weight = 1)
    return false unless @vertices.key?(from_id) && @vertices.key?(to_id)
    
    from_vertex = @vertices[from_id]
    to_vertex = @vertices[to_id]
    
    # 检查边是否已存在
    return false if has_edge?(from_id, to_id)
    
    edge = Edge.new(from_vertex, to_vertex, weight)
    @edges << edge
    
    @adjacency_list[from_id] << to_vertex
    
    # 如果是无向图，添加反向边
    unless @directed
      @adjacency_list[to_id] << from_vertex
    end
    
    true
  end

  # 删除边
  def remove_edge(from_id, to_id)
    return false unless @vertices.key?(from_id) && @vertices.key?(to_id)
    
    from_vertex = @vertices[from_id]
    to_vertex = @vertices[to_id]
    
    # 从邻接表中删除
    @adjacency_list[from_id].delete(to_vertex)
    
    unless @directed
      @adjacency_list[to_id].delete(from_vertex)
    end
    
    # 从边列表中删除
    @edges.reject! { |edge| edge.from == from_vertex && edge.to == to_vertex }
    
    true
  end

  # 检查是否有边
  def has_edge?(from_id, to_id)
    return false unless @vertices.key?(from_id) && @vertices.key?(to_id)
    
    to_vertex = @vertices[to_id]
    @adjacency_list[from_id].include?(to_vertex)
  end

  # 获取顶点的邻居
  def neighbors(vertex_id)
    return [] unless @vertices.key?(vertex_id)
    @adjacency_list[vertex_id].dup
  end

  # 获取顶点的度数
  def degree(vertex_id)
    return 0 unless @vertices.key?(vertex_id)
    @adjacency_list[vertex_id].size
  end

  # 获取顶点的入度（有向图）
  def in_degree(vertex_id)
    return 0 unless @vertices.key?(vertex_id)
    return degree(vertex_id) unless @directed
    
    count = 0
    @adjacency_list.each_value do |neighbors|
      count += 1 if neighbors.include?(@vertices[vertex_id])
    end
    count
  end

  # 获取顶点的出度（有向图）
  def out_degree(vertex_id)
    degree(vertex_id)
  end

  # 获取边的权重
  def edge_weight(from_id, to_id)
    return nil unless has_edge?(from_id, to_id)
    
    from_vertex = @vertices[from_id]
    to_vertex = @vertices[to_id]
    
    edge = @edges.find { |e| e.from == from_vertex && e.to == to_vertex }
    edge ? edge.weight : nil
  end

  # 深度优先搜索 (DFS)
  def dfs(start_id, &block)
    return [] unless @vertices.key?(start_id)
    
    reset_vertices
    result = []
    dfs_helper(start_id, result, &block)
    result
  end

  # 广度优先搜索 (BFS)
  def bfs(start_id, &block)
    return [] unless @vertices.key?(start_id)
    
    reset_vertices
    result = []
    queue = [start_id]
    @vertices[start_id].visited = true
    
    while !queue.empty?
      current_id = queue.shift
      current_vertex = @vertices[current_id]
      
      if block_given?
        yield current_vertex
      else
        result << current_vertex.value
      end
      
      @adjacency_list[current_id].each do |neighbor|
        unless neighbor.visited
          neighbor.visited = true
          queue << neighbor.id
        end
      end
    end
    
    block_given? ? self : result
  end

  # 检查图的连通性
  def connected?
    return true if @vertices.empty?
    
    # 从任意顶点开始DFS，看是否能访问所有顶点
    start_id = @vertices.keys.first
    visited_count = dfs(start_id).size
    
    visited_count == @vertices.size
  end

  # 查找两点间的路径
  def find_path(start_id, end_id)
    return [] unless @vertices.key?(start_id) && @vertices.key?(end_id)
    return [start_id] if start_id == end_id
    
    reset_vertices
    queue = [start_id]
    @vertices[start_id].visited = true
    @vertices[start_id].parent = nil
    
    while !queue.empty?
      current_id = queue.shift
      
      @adjacency_list[current_id].each do |neighbor|
        unless neighbor.visited
          neighbor.visited = true
          neighbor.parent = @vertices[current_id]
          queue << neighbor.id
          
          if neighbor.id == end_id
            return reconstruct_path(end_id)
          end
        end
      end
    end
    
    []  # 没有找到路径
  end

  # 检查是否有环（无向图）
  def has_cycle?
    return false if @vertices.empty?
    
    reset_vertices
    
    @vertices.each_key do |vertex_id|
      next if @vertices[vertex_id].visited
      return true if has_cycle_helper(vertex_id, nil)
    end
    
    false
  end

  # 拓扑排序（有向无环图）
  def topological_sort
    return [] unless @directed
    
    # 计算所有顶点的入度
    in_degrees = {}
    @vertices.each_key { |id| in_degrees[id] = in_degree(id) }
    
    # 找到所有入度为0的顶点
    queue = []
    in_degrees.each { |id, degree| queue << id if degree == 0 }
    
    result = []
    
    while !queue.empty?
      current_id = queue.shift
      result << current_id
      
      # 减少邻居的入度
      @adjacency_list[current_id].each do |neighbor|
        in_degrees[neighbor.id] -= 1
        queue << neighbor.id if in_degrees[neighbor.id] == 0
      end
    end
    
    # 如果结果长度不等于顶点数，说明有环
    result.size == @vertices.size ? result : []
  end

  # 获取所有连通分量
  def connected_components
    reset_vertices
    components = []
    
    @vertices.each_key do |vertex_id|
      next if @vertices[vertex_id].visited
      
      component = dfs(vertex_id)
      components << component unless component.empty?
    end
    
    components
  end

  # 图的基本信息
  def vertex_count
    @vertices.size
  end

  def edge_count
    @edges.size
  end

  def empty?
    @vertices.empty?
  end

  def clear
    @vertices.clear
    @adjacency_list.clear
    @edges.clear
    self
  end

  # 转换为邻接矩阵
  def to_adjacency_matrix
    size = @vertices.size
    return [] if size == 0
    
    vertex_ids = @vertices.keys.sort
    matrix = Array.new(size) { Array.new(size, 0) }
    
    vertex_ids.each_with_index do |from_id, i|
      vertex_ids.each_with_index do |to_id, j|
        if has_edge?(from_id, to_id)
          matrix[i][j] = edge_weight(from_id, to_id)
        end
      end
    end
    
    matrix
  end

  # 从邻接矩阵创建图
  def self.from_adjacency_matrix(matrix, directed = false)
    graph = Graph.new(directed)
    size = matrix.size
    
    # 添加顶点
    size.times { |i| graph.add_vertex(i) }
    
    # 添加边
    size.times do |i|
      size.times do |j|
        if matrix[i][j] != 0
          graph.add_edge(i, j, matrix[i][j])
        end
      end
    end
    
    graph
  end

  # 字符串表示
  def to_s
    type = @directed ? "Directed" : "Undirected"
    "#{type}Graph[vertices: #{vertex_count}, edges: #{edge_count}]"
  end

  def inspect
    "#<Graph:#{object_id} directed=#{@directed} vertices=#{vertex_count} edges=#{edge_count}>"
  end

  # 打印图的结构
  def print_graph
    puts "Graph Structure:"
    @adjacency_list.each do |vertex_id, neighbors|
      neighbor_list = neighbors.map(&:id).join(", ")
      puts "  #{vertex_id} -> [#{neighbor_list}]"
    end
  end

  private

  # DFS辅助方法
  def dfs_helper(vertex_id, result, &block)
    vertex = @vertices[vertex_id]
    vertex.visited = true
    
    if block_given?
      yield vertex
    else
      result << vertex.value
    end
    
    @adjacency_list[vertex_id].each do |neighbor|
      unless neighbor.visited
        dfs_helper(neighbor.id, result, &block)
      end
    end
  end

  # 重置所有顶点的访问状态
  def reset_vertices
    @vertices.each_value(&:reset)
  end

  # 重构路径
  def reconstruct_path(end_id)
    path = []
    current = @vertices[end_id]
    
    while current
      path.unshift(current.id)
      current = current.parent
    end
    
    path
  end

  # 检查环的辅助方法（无向图）
  def has_cycle_helper(vertex_id, parent_id)
    @vertices[vertex_id].visited = true
    
    @adjacency_list[vertex_id].each do |neighbor|
      if neighbor.visited
        # 如果邻居已访问且不是父节点，则有环
        return true if neighbor.id != parent_id
      else
        # 递归检查邻居
        return true if has_cycle_helper(neighbor.id, vertex_id)
      end
    end
    
    false
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== Graph 使用示例 ==="
  
  # 创建无向图
  graph = Graph.new(false)
  
  # 添加顶点
  %w[A B C D E F].each { |vertex| graph.add_vertex(vertex) }
  
  # 添加边
  edges = [
    ['A', 'B'], ['A', 'C'], ['B', 'D'], 
    ['C', 'D'], ['D', 'E'], ['E', 'F']
  ]
  
  edges.each { |from, to| graph.add_edge(from, to) }
  
  puts "无向图信息:"
  puts graph
  graph.print_graph
  
  puts "\n图的属性:"
  puts "顶点数: #{graph.vertex_count}"
  puts "边数: #{graph.edge_count}"
  puts "是否连通: #{graph.connected?}"
  puts "是否有环: #{graph.has_cycle?}"
  
  puts "\n遍历算法:"
  puts "DFS从A开始: #{graph.dfs('A')}"
  puts "BFS从A开始: #{graph.bfs('A')}"
  
  puts "\n路径查找:"
  path = graph.find_path('A', 'F')
  puts "A到F的路径: #{path.join(' -> ')}"
  
  puts "\n顶点度数:"
  %w[A B C D E F].each do |vertex|
    puts "#{vertex}的度数: #{graph.degree(vertex)}"
  end
  
  puts "\n连通分量:"
  components = graph.connected_components
  components.each_with_index do |component, index|
    puts "分量#{index + 1}: #{component}"
  end
  
  puts "\n=== 有向图示例 ==="
  
  # 创建有向图
  directed_graph = Graph.new(true)
  
  # 添加顶点
  (0..5).each { |i| directed_graph.add_vertex(i) }
  
  # 添加边（创建一个DAG用于拓扑排序）
  directed_edges = [
    [5, 2], [5, 0], [4, 0], [4, 1], 
    [2, 3], [3, 1]
  ]
  
  directed_edges.each { |from, to| directed_graph.add_edge(from, to) }
  
  puts "有向图信息:"
  puts directed_graph
  directed_graph.print_graph
  
  puts "\n拓扑排序:"
  topo_order = directed_graph.topological_sort
  puts "拓扑序列: #{topo_order}"
  
  puts "\n顶点的入度和出度:"
  (0..5).each do |vertex|
    puts "顶点#{vertex}: 入度=#{directed_graph.in_degree(vertex)}, 出度=#{directed_graph.out_degree(vertex)}"
  end
  
  puts "\n=== 邻接矩阵示例 ==="
  
  # 创建小图并转换为邻接矩阵
  small_graph = Graph.new(false)
  [0, 1, 2].each { |i| small_graph.add_vertex(i) }
  small_graph.add_edge(0, 1, 2)
  small_graph.add_edge(1, 2, 3)
  small_graph.add_edge(0, 2, 1)
  
  matrix = small_graph.to_adjacency_matrix
  puts "邻接矩阵:"
  matrix.each { |row| puts "  #{row}" }
  
  # 从邻接矩阵创建图
  matrix_graph = Graph.from_adjacency_matrix(matrix, false)
  puts "\n从邻接矩阵重建的图:"
  matrix_graph.print_graph
  
  puts "\n=== 性能测试 ==="
  
  # 创建大图进行性能测试
  large_graph = Graph.new(false)
  
  start_time = Time.now
  
  # 添加1000个顶点
  1000.times { |i| large_graph.add_vertex(i) }
  
  # 添加随机边
  2000.times do
    from = rand(1000)
    to = rand(1000)
    large_graph.add_edge(from, to) if from != to
  end
  
  end_time = Time.now
  
  puts "构建1000顶点图耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  puts "最终图信息: #{large_graph}"
  
  # DFS性能测试
  start_time = Time.now
  large_graph.dfs(0)
  end_time = Time.now
  
  puts "DFS遍历耗时: #{((end_time - start_time) * 1000).round(2)}ms"
end