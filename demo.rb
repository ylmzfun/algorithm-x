#!/usr/bin/env ruby
# Ruby 数据结构演示程序
# 
# 这个演示程序展示了各种数据结构的基本用法和实际应用场景

require_relative 'lib/linear/array_list'
require_relative 'lib/linear/linked_list'
require_relative 'lib/linear/stack'
require_relative 'lib/linear/queue'
require_relative 'lib/tree/binary_tree'
require_relative 'lib/tree/bst'
require_relative 'lib/tree/heap'
require_relative 'lib/graph/graph'
require_relative 'lib/graph/weighted_graph'
require_relative 'lib/hash/hash_table'
require_relative 'lib/hash/bloom_filter'

def demo_linear_structures
  puts "=== 线性数据结构演示 ==="
  
  # ArrayList 演示
  puts "\n1. ArrayList - 动态数组"
  list = ArrayList.new
  puts "创建空数组: #{list.to_a}"
  
  [10, 20, 30, 40, 50].each { |x| list.append(x) }
  puts "添加元素后: #{list.to_a}"
  
  list.insert(2, 25)
  puts "在索引2插入25: #{list.to_a}"
  
  list.delete_at(1)
  puts "删除索引1的元素: #{list.to_a}"
  
  puts "查找30的索引: #{list.index_of(30)}"
  puts "数组大小: #{list.size}, 容量: #{list.capacity}"
  
  # LinkedList 演示
  puts "\n2. LinkedList - 链表"
  linked_list = LinkedList.new
  puts "创建空链表: #{linked_list.to_a}"
  
  %w[Apple Banana Cherry Date].each { |fruit| linked_list.append(fruit) }
  puts "添加水果: #{linked_list.to_a}"
  
  linked_list.prepend("Avocado")
  puts "在头部添加Avocado: #{linked_list.to_a}"
  
  linked_list.delete("Banana")
  puts "删除Banana: #{linked_list.to_a}"
  
  linked_list.reverse!
  puts "反转链表: #{linked_list.to_a}"
  
  # Stack 演示
  puts "\n3. Stack - 栈 (LIFO)"
  stack = Stack.new
  puts "创建空栈: #{stack.to_a}"
  
  [1, 2, 3, 4, 5].each { |x| stack.push(x) }
  puts "压入元素: #{stack.to_a}"
  
  puts "栈顶元素: #{stack.peek}"
  puts "弹出元素: #{stack.pop}"
  puts "弹出后栈: #{stack.to_a}"
  
  # 栈的实际应用：括号匹配
  expressions = ["((()))", "((())", "()()()"]
  expressions.each do |expr|
    result = StackApplications.balanced_parentheses?(expr)
    puts "#{expr} 括号匹配: #{result ? '✓' : '✗'}"
  end
  
  # Queue 演示
  puts "\n4. Queue - 队列 (FIFO)"
  queue = Queue.new
  puts "创建空队列: #{queue.to_a}"
  
  %w[任务1 任务2 任务3 任务4].each { |task| queue.enqueue(task) }
  puts "加入任务: #{queue.to_a}"
  
  puts "队首任务: #{queue.peek}"
  puts "处理任务: #{queue.dequeue}"
  puts "处理后队列: #{queue.to_a}"
  
  # 优先队列演示
  puts "\n5. PriorityQueue - 优先队列"
  pq = PriorityQueue.new
  
  [["紧急任务", 1], ["普通任务", 3], ["重要任务", 2]].each do |task, priority|
    pq.enqueue(task, priority)
  end
  
  puts "按优先级处理任务:"
  until pq.empty?
    result = pq.dequeue
    if result.is_a?(Array)
      task, priority = result
      puts "  处理: #{task} (优先级: #{priority})"
    else
      puts "  处理: #{result}"
    end
  end
end

def demo_tree_structures
  puts "\n=== 树形数据结构演示 ==="
  
  # BinaryTree 演示
  puts "\n1. BinaryTree - 二叉树"
  tree = BinaryTree.new
  root = BinaryTree.build_from_array([1, 2, 3, 4, 5, 6, 7], 0)
  tree.root = root
  
  puts "从数组构建二叉树: [1, 2, 3, 4, 5, 6, 7]"
  puts "树的高度: #{tree.height}"
  puts "节点数量: #{tree.count_nodes}"
  puts "是否平衡: #{tree.balanced?}"
  
  puts "中序遍历: #{tree.inorder_traversal}"
  puts "前序遍历: #{tree.preorder_traversal}"
  puts "后序遍历: #{tree.postorder_traversal}"
  puts "层序遍历: #{tree.level_order_traversal}"
  
  # BST 演示
  puts "\n2. BinarySearchTree - 二叉搜索树"
  bst = BinarySearchTree.new
  
  values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
  puts "插入值: #{values}"
  values.each { |val| bst.insert(val) }
  
  puts "BST中序遍历(有序): #{bst.inorder_traversal}"
  puts "最小值: #{bst.min}, 最大值: #{bst.max}"
  puts "查找40: #{bst.search(40) ? '找到' : '未找到'}"
  puts "40的前驱: #{bst.predecessor(40)}, 后继: #{bst.successor(40)}"
  puts "第3小的元素: #{bst.kth_smallest(3)}"
  puts "范围[25,55]内的值: #{bst.range_search(25, 55)}"
  
  # Heap 演示
  puts "\n3. Heap - 堆"
  
  # 最大堆
  max_heap = MaxHeap.new
  numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
  puts "插入数字: #{numbers}"
  numbers.each { |num| max_heap.insert(num) }
  
  puts "最大堆顶部: #{max_heap.peek}"
  puts "提取最大值: #{max_heap.extract_max}"
  puts "堆排序结果: #{HeapApplications.heap_sort(numbers.dup)}"
  
  # 最小堆
  min_heap = MinHeap.new
  numbers.each { |num| min_heap.insert(num) }
  puts "最小堆顶部: #{min_heap.peek}"
  
  # TopK应用
  top_k = HeapApplications::TopK.new(3)
  [10, 5, 8, 12, 3, 7, 15, 1, 9].each { |x| top_k.add(x) }
  puts "Top 3 最大值: #{top_k.top_k}"
end

def demo_graph_structures
  puts "\n=== 图数据结构演示 ==="
  
  # Graph 演示
  puts "\n1. Graph - 无向图"
  graph = Graph.new(false)
  
  # 构建一个简单的社交网络
  people = %w[Alice Bob Charlie David Eve]
  people.each { |person| graph.add_vertex(person) }
  
  # 添加友谊关系
  friendships = [
    ['Alice', 'Bob'], ['Alice', 'Charlie'], ['Bob', 'David'],
    ['Charlie', 'David'], ['Charlie', 'Eve'], ['David', 'Eve']
  ]
  
  friendships.each { |person1, person2| graph.add_edge(person1, person2) }
  
  puts "社交网络成员: #{people}"
  puts "友谊关系: #{friendships}"
  puts "图的顶点数: #{graph.vertex_count}, 边数: #{graph.edge_count}"
  
  puts "从Alice开始的DFS遍历: #{graph.dfs('Alice')}"
  puts "从Alice开始的BFS遍历: #{graph.bfs('Alice')}"
  
  path = graph.find_path('Alice', 'Eve')
  puts "Alice到Eve的路径: #{path}"
  
  puts "图是否连通: #{graph.connected?}"
  
  # WeightedGraph 演示
  puts "\n2. WeightedGraph - 加权图"
  weighted_graph = WeightedGraph.new(false)
  
  # 构建城市交通网络
  cities = %w[北京 上海 广州 深圳 杭州]
  cities.each { |city| weighted_graph.add_vertex(city) }
  
  # 添加城市间距离（公里）
  routes = [
    ['北京', '上海', 1200], ['北京', '广州', 2100], ['上海', '杭州', 180],
    ['上海', '广州', 1400], ['广州', '深圳', 120], ['杭州', '广州', 1000]
  ]
  
  routes.each { |city1, city2, distance| weighted_graph.add_edge(city1, city2, distance) }
  
  puts "城市交通网络: #{cities}"
  puts "路线和距离: #{routes.map { |c1, c2, d| "#{c1}-#{c2}: #{d}km" }}"
  
  # 最短路径
  shortest = weighted_graph.shortest_path('北京', '深圳')
  puts "北京到深圳最短路径: #{shortest[:path].join(' -> ')}"
  puts "最短距离: #{shortest[:distance]}km"
  
  # 最小生成树
  mst = weighted_graph.kruskal_mst
  total_cost = mst[:total_weight]
  puts "最小生成树总成本: #{total_cost}km"
end

def demo_hash_structures
  puts "\n=== 哈希数据结构演示 ==="
  
  # HashTable 演示
  puts "\n1. HashTable - 哈希表"
  ht = HashTable.new
  
  # 学生成绩管理
  students = {
    '张三' => 85, '李四' => 92, '王五' => 78,
    '赵六' => 88, '钱七' => 95, '孙八' => 82
  }
  
  students.each { |name, score| ht.put(name, score) }
  
  puts "学生成绩录入完成，共#{ht.size}名学生"
  puts "张三的成绩: #{ht.get('张三')}"
  puts "所有学生: #{ht.keys}"
  puts "所有成绩: #{ht.values}"
  
  # 统计成绩分布
  grade_distribution = Hash.new(0)
  ht.values.each do |score|
    case score
    when 90..100 then grade_distribution['优秀'] += 1
    when 80..89 then grade_distribution['良好'] += 1
    when 70..79 then grade_distribution['中等'] += 1
    else grade_distribution['需要努力'] += 1
    end
  end
  
  puts "成绩分布: #{grade_distribution}"
  puts "负载因子: #{ht.load_factor.round(2)}"
  
  # LRU缓存应用
  puts "\n2. LRU缓存应用"
  cache = HashTableApplications::LRUCache.new(3)
  
  puts "缓存容量: 3"
  cache.put('page1', '首页内容')
  cache.put('page2', '产品页面')
  cache.put('page3', '关于我们')
  puts "缓存状态: #{cache.keys}"
  
  cache.get('page1')  # 访问page1，使其成为最近使用
  cache.put('page4', '联系我们')  # 这会淘汰page2
  puts "添加page4后: #{cache.keys}"
  
  # BloomFilter 演示
  puts "\n3. BloomFilter - 布隆过滤器"
  bf = BloomFilter.new(1000, 0.01)
  
  # 网站访问去重
  urls = [
    'https://example.com/page1',
    'https://example.com/page2',
    'https://example.com/page3',
    'https://example.com/page1',  # 重复
    'https://example.com/page4'
  ]
  
  unique_visits = 0
  urls.each do |url|
    if bf.definitely_not_contain?(url)
      bf.add(url)
      unique_visits += 1
      puts "新访问: #{url}"
    else
      puts "可能重复访问: #{url}"
    end
  end
  
  puts "唯一访问数: #{unique_visits}"
  puts "布隆过滤器大小: #{bf.size} bits"
  puts "预期假阳性率: #{bf.expected_false_positive_rate.round(4)}"
end

def demo_practical_applications
  puts "\n=== 实际应用场景演示 ==="
  
  # 1. 表达式求值（使用栈）
  puts "\n1. 表达式求值"
  expression = "3 + 4 * 2 - 1"
  postfix = StackApplications.infix_to_postfix(expression)
  result = StackApplications.evaluate_postfix(postfix)
  puts "中缀表达式: #{expression}"
  puts "后缀表达式: #{postfix}"
  puts "计算结果: #{result}"
  
  # 2. 任务调度（使用队列）
  puts "\n2. 任务调度系统"
  scheduler = QueueApplications::TaskScheduler.new
  
  tasks = [
    { id: 1, name: '发送邮件', priority: 2 },
    { id: 2, name: '备份数据', priority: 1 },
    { id: 3, name: '生成报告', priority: 3 },
    { id: 4, name: '清理日志', priority: 1 }
  ]
  
  tasks.each { |task| scheduler.add_task(task) }
  
  puts "任务调度顺序:"
  while scheduler.has_tasks?
    task = scheduler.next_task
    puts "  执行: #{task[:name]} (优先级: #{task[:priority]})"
  end
  
  # 3. 路径查找（使用图）
  puts "\n3. 最短路径查找"
  map = WeightedGraph.new(false)
  
  locations = %w[家 超市 学校 公园 医院]
  locations.each { |loc| map.add_vertex(loc) }
  
  roads = [
    ['家', '超市', 5], ['家', '学校', 8], ['超市', '公园', 3],
    ['学校', '公园', 2], ['学校', '医院', 4], ['公园', '医院', 6]
  ]
  
  roads.each { |from, to, distance| map.add_edge(from, to, distance) }
  
  route = map.shortest_path('家', '医院')
  puts "从家到医院的最短路径: #{route[:path].join(' -> ')}"
  puts "总距离: #{route[:distance]}分钟"
  
  # 4. 数据去重（使用布隆过滤器）
  puts "\n4. 大数据去重"
  deduplicator = BloomFilter.new(10000, 0.001)
  
  # 模拟处理大量数据
  data_stream = (1..1000).map { |i| "user_#{rand(500)}" }
  unique_count = 0
  
  data_stream.each do |item|
    if deduplicator.definitely_not_contain?(item)
      deduplicator.add(item)
      unique_count += 1
    end
  end
  
  puts "处理数据条数: #{data_stream.size}"
  puts "去重后唯一数据: #{unique_count}"
  puts "去重率: #{((data_stream.size - unique_count).to_f / data_stream.size * 100).round(2)}%"
end

def performance_comparison
  puts "\n=== 性能对比演示 ==="
  
  test_size = 10000
  
  puts "\n插入#{test_size}个元素的性能对比:"
  
  # ArrayList vs LinkedList
  start_time = Time.now
  array_list = ArrayList.new
  test_size.times { |i| array_list.append(i) }
  array_time = Time.now - start_time
  
  start_time = Time.now
  linked_list = LinkedList.new
  test_size.times { |i| linked_list.append(i) }
  linked_time = Time.now - start_time
  
  puts "ArrayList: #{(array_time * 1000).round(2)}ms"
  puts "LinkedList: #{(linked_time * 1000).round(2)}ms"
  puts "ArrayList比LinkedList快 #{(linked_time / array_time).round(1)}倍"
  
  # 查找性能对比
  puts "\n随机查找1000次的性能对比:"
  
  start_time = Time.now
  1000.times { array_list[rand(test_size)] }
  array_search_time = Time.now - start_time
  
  start_time = Time.now
  1000.times { linked_list.get(rand(test_size)) }
  linked_search_time = Time.now - start_time
  
  puts "ArrayList: #{(array_search_time * 1000).round(2)}ms"
  puts "LinkedList: #{(linked_search_time * 1000).round(2)}ms"
  puts "ArrayList比LinkedList快 #{(linked_search_time / array_search_time).round(1)}倍"
  
  # 内存使用对比
  puts "\n内存使用对比:"
  puts "ArrayList (#{test_size}元素): 约#{(test_size * 8 + array_list.capacity * 8) / 1024}KB"
  puts "LinkedList (#{test_size}元素): 约#{(test_size * 24) / 1024}KB"  # 每个节点约24字节
end

# 主程序
if __FILE__ == $0
  puts "🚀 Ruby 数据结构完整演示程序"
  puts "=" * 60
  
  demo_linear_structures
  demo_tree_structures
  demo_graph_structures
  demo_hash_structures
  demo_practical_applications
  performance_comparison
  
  puts "\n" + "=" * 60
  puts "✅ 演示完成！"
  puts "\n📚 本演示展示了以下数据结构的实现和应用:"
  puts "   • 线性结构: ArrayList, LinkedList, Stack, Queue"
  puts "   • 树形结构: BinaryTree, BST, Heap"
  puts "   • 图结构: Graph, WeightedGraph"
  puts "   • 哈希结构: HashTable, BloomFilter"
  puts "\n🎯 每种数据结构都有其特定的应用场景和性能特点"
  puts "   选择合适的数据结构是高效编程的关键！"
end