# encoding: utf-8
# 并查集 (Disjoint Set / Union-Find) 实现
#
# 思路：
# 并查集是一种用于处理不相交集合合并和查询的数据结构。
# 核心操作：Find（查找元素所属集合）和 Union（合并两个集合）。
# 通过路径压缩和按秩合并优化，使得操作近乎 O(α(n))（反阿克曼函数）。
#
# 作用：
# 1. 连通性检测：快速判断两个元素是否在同一集合
# 2. 集合合并：将两个不相交集合合并
# 3. 集合计数：统计集合数量和大小
#
# 应用场景：
# 1. 图算法：Kruskal 最小生成树、连通分量
# 2. 网络连接：社交网络中的好友关系
# 3. 图像处理：连通区域标记
# 4. 编译器：等价类合并
# 5. 游戏开发：区域划分、势力范围

class UnionFind
  attr_reader :size, :count

  def initialize(n)
    @parent = Array.new(n) { |i| i }
    @rank = Array.new(n, 0)
    @size = Array.new(n, 1)
    @count = n  # 集合数量
  end

  # 查找元素所属集合的根（带路径压缩）
  # 时间复杂度：近乎 O(1)
  def find(x)
    return x if @parent[x] == x

    # 路径压缩：将路径上所有节点直接指向根
    @parent[x] = find(@parent[x])
  end

  # 合并两个集合（按秩合并）
  # 时间复杂度：近乎 O(1)
  def union(x, y)
    root_x = find(x)
    root_y = find(y)

    return false if root_x == root_y

    # 按秩合并：将秩小的树合并到秩大的树
    if @rank[root_x] < @rank[root_y]
      @parent[root_x] = root_y
      @size[root_y] += @size[root_x]
    elsif @rank[root_x] > @rank[root_y]
      @parent[root_y] = root_x
      @size[root_x] += @size[root_y]
    else
      @parent[root_y] = root_x
      @rank[root_x] += 1
      @size[root_x] += @size[root_y]
    end

    @count -= 1
    true
  end

  # 检查两个元素是否在同一集合
  # 时间复杂度：近乎 O(1)
  def connected?(x, y)
    find(x) == find(y)
  end
  alias_method :same_set?, :connected?

  # 获取元素所在集合的大小
  # 时间复杂度：近乎 O(1)
  def set_size(x)
    @size[find(x)]
  end

  # 获取集合数量
  def set_count
    @count
  end

  # 获取所有集合
  def all_sets
    sets = {}
    @parent.length.times do |i|
      root = find(i)
      sets[root] ||= []
      sets[root] << i
    end
    sets.values
  end

  # 获取元素所在集合的所有成员
  def members(x)
    root = find(x)
    result = []
    @parent.length.times { |i| result << i if find(i) == root }
    result
  end

  # 重置
  def reset
    @parent.length.times do |i|
      @parent[i] = i
      @rank[i] = 0
      @size[i] = 1
    end
    @count = @parent.length
    self
  end

  def to_s
    "UnionFind[sets: #{@count}, elements: #{@parent.length}]"
  end

  def inspect
    sets_info = all_sets.map { |s| "[#{s.join(',')}]" }.join(' ')
    "#<UnionFind:#{object_id} sets=#{@count} #{sets_info}>"
  end
end

# 泛型并查集（支持任意类型元素）
class GenericUnionFind
  def initialize
    @parent = {}
    @rank = {}
    @size = {}
    @count = 0
  end

  # 添加元素
  def add(x)
    return if @parent.key?(x)
    @parent[x] = x
    @rank[x] = 0
    @size[x] = 1
    @count += 1
    self
  end

  # 查找
  def find(x)
    return nil unless @parent.key?(x)
    return x if @parent[x] == x
    @parent[x] = find(@parent[x])
  end

  # 合并
  def union(x, y)
    add(x) unless @parent.key?(x)
    add(y) unless @parent.key?(y)

    root_x = find(x)
    root_y = find(y)
    return false if root_x == root_y

    if @rank[root_x] < @rank[root_y]
      @parent[root_x] = root_y
      @size[root_y] += @size[root_x]
    elsif @rank[root_x] > @rank[root_y]
      @parent[root_y] = root_x
      @size[root_x] += @size[root_y]
    else
      @parent[root_y] = root_x
      @rank[root_x] += 1
      @size[root_x] += @size[root_y]
    end

    @count -= 1
    true
  end

  # 是否连通
  def connected?(x, y)
    return false unless @parent.key?(x) && @parent.key?(y)
    find(x) == find(y)
  end

  # 集合大小
  def set_size(x)
    return 0 unless @parent.key?(x)
    @size[find(x)]
  end

  def set_count
    @count
  end

  # 所有集合
  def all_sets
    sets = {}
    @parent.each_key do |x|
      root = find(x)
      sets[root] ||= []
      sets[root] << x
    end
    sets.values
  end

  def to_s
    "GenericUnionFind[sets: #{@count}, elements: #{@parent.size}]"
  end
end

# 带撤销功能的并查集（支持回退操作）
class PersistentUnionFind
  HistoryEntry = Struct.new(:x, :old_parent, :old_rank, :old_size, :old_count)

  def initialize(n)
    @parent = Array.new(n) { |i| i }
    @rank = Array.new(n, 0)
    @size = Array.new(n, 1)
    @count = n
    @history = []
  end

  def find(x)
    return x if @parent[x] == x
    find(@parent[x])  # 不进行路径压缩（保持可撤销性）
  end

  def union(x, y)
    root_x = find(x)
    root_y = find(y)
    return false if root_x == root_y

    if @rank[root_x] < @rank[root_y]
      root_x, root_y = root_y, root_x
    end

    # 记录操作历史
    @history << HistoryEntry.new(
      root_y,
      @parent[root_y],
      @rank[root_x],
      @size[root_x],
      @count
    )

    @parent[root_y] = root_x
    @rank[root_x] += 1 if @rank[root_x] == @rank[root_y]
    @size[root_x] += @size[root_y]
    @count -= 1
    true
  end

  # 撤销上一次 union 操作
  def undo
    return false if @history.empty?

    entry = @history.pop
    @parent[entry.x] = entry.old_parent
    @rank[find(entry.x)] = entry.old_rank
    @size[find(entry.x)] = entry.old_size
    @count = entry.old_count
    true
  end

  def connected?(x, y)
    find(x) == find(y)
  end

  def set_count
    @count
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== UnionFind 并查集演示 ==="

  uf = UnionFind.new(10)
  puts "创建10个元素的并查集: #{uf}"

  puts "\n合并操作:"
  uf.union(0, 1)
  uf.union(1, 2)
  uf.union(3, 4)
  uf.union(5, 6)
  uf.union(6, 7)
  uf.union(7, 8)

  puts "0和2连通: #{uf.connected?(0, 2)}"
  puts "0和3连通: #{uf.connected?(0, 3)}"
  puts "5和8连通: #{uf.connected?(5, 8)}"
  puts "集合数量: #{uf.set_count}"
  puts "包含0的集合大小: #{uf.set_size(0)}"

  puts "\n所有集合: #{uf.all_sets.map { |s| "[#{s.join(',')}]" }.join(' ')}"

  # 连通分量检测
  puts "\n=== 连通分量检测示例 ==="
  edges = [[0, 1], [0, 2], [1, 3], [4, 5], [4, 6], [7, 8]]

  graph_uf = UnionFind.new(10)
  edges.each { |a, b| graph_uf.union(a, b) }

  components = graph_uf.all_sets
  puts "图的连通分量: #{components.map { |s| "[#{s.join(',')}]" }.join(' ')}"
  puts "分量数量: #{graph_uf.set_count}"

  puts "\n=== GenericUnionFind 示例 ==="
  guf = GenericUnionFind.new
  guf.union("Alice", "Bob")
  guf.union("Bob", "Charlie")
  guf.union("David", "Eve")

  puts "Alice和Charlie连通: #{guf.connected?("Alice", "Charlie")}"
  puts "Alice和David连通: #{guf.connected?("Alice", "David")}"
  puts "集合: #{guf.all_sets}"

  puts "\n=== PersistentUnionFind 撤销示例 ==="
  puf = PersistentUnionFind.new(5)
  puf.union(0, 1)
  puf.union(2, 3)
  puts "合并前集合数: #{puf.set_count}"
  puf.union(1, 2)
  puts "合并后集合数: #{puf.set_count}"
  puf.undo
  puts "撤销后集合数: #{puf.set_count}"
  puts "0和2连通: #{puf.connected?(0, 2)}"
end
