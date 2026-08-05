#!/usr/bin/env ruby
# 数据结构测试运行器
# 
# 这个文件包含了所有数据结构的基础测试用例，
# 用于验证实现的正确性和性能。

require_relative '../lib/linear/array_list'
require_relative '../lib/linear/linked_list'
require_relative '../lib/linear/stack'
require_relative '../lib/linear/queue'
require_relative '../lib/tree/binary_tree'
require_relative '../lib/tree/bst'
require_relative '../lib/tree/avl_tree'
require_relative '../lib/tree/heap'
require_relative '../lib/graph/graph'
require_relative '../lib/graph/weighted_graph'
require_relative '../lib/hash/hash_table'
require_relative '../lib/hash/bloom_filter'

# 简单的测试框架
class TestFramework
  def initialize
    @tests_run = 0
    @tests_passed = 0
    @tests_failed = 0
    @current_test_suite = nil
  end

  def test_suite(name)
    @current_test_suite = name
    puts "\n=== #{name} 测试 ==="
    yield
    puts "#{name} 测试完成: #{@tests_passed}/#{@tests_run} 通过"
  end

  def test(description)
    @tests_run += 1
    print "  测试: #{description} ... "
    
    begin
      yield
      @tests_passed += 1
      puts "✓ 通过"
    rescue => e
      @tests_failed += 1
      puts "✗ 失败: #{e.message}"
      puts "    #{e.backtrace.first}"
    end
  end

  def assert(condition, message = "断言失败")
    raise message unless condition
  end

  def assert_equal(expected, actual, message = nil)
    message ||= "期望 #{expected}, 实际 #{actual}"
    assert(expected == actual, message)
  end

  def assert_not_nil(value, message = "值不应为nil")
    assert(!value.nil?, message)
  end

  def assert_nil(value, message = "值应为nil")
    assert(value.nil?, message)
  end

  def assert_true(value, message = "值应为true")
    assert(value == true, message)
  end

  def assert_false(value, message = "值应为false")
    assert(value == false, message)
  end

  def summary
    puts "\n=== 测试总结 ==="
    puts "总测试数: #{@tests_run}"
    puts "通过: #{@tests_passed}"
    puts "失败: #{@tests_failed}"
    puts "成功率: #{(@tests_passed.to_f / @tests_run * 100).round(2)}%"
  end
end

# 测试用例
def run_all_tests
  framework = TestFramework.new

  # ArrayList 测试
  framework.test_suite("ArrayList") do
    framework.test("创建和基本操作") do
      list = ArrayList.new
      framework.assert_true(list.empty?)
      framework.assert_equal(0, list.size)
      
      list.add(1)
      list.add(2)
      list.add(3)
      
      framework.assert_false(list.empty?)
      framework.assert_equal(3, list.size)
      framework.assert_equal(1, list.get(0))
      framework.assert_equal(3, list.get(2))
    end

    framework.test("插入和删除") do
      list = ArrayList.new
      list.add(1)
      list.add(3)
      list.insert(1, 2)
      
      framework.assert_equal(3, list.size)
      framework.assert_equal(2, list.get(1))
      
      deleted = list.delete(1)
      framework.assert_equal(2, deleted)
      framework.assert_equal(2, list.size)
    end

    framework.test("自动扩容") do
      list = ArrayList.new(2)
      5.times { |i| list.add(i) }
      
      framework.assert_equal(5, list.size)
      framework.assert(list.capacity >= 5)
    end

    framework.test("查找操作") do
      list = ArrayList.new
      list.add("apple")
      list.add("banana")
      list.add("cherry")
      
      framework.assert_equal(1, list.index_of("banana"))
      framework.assert_equal(-1, list.index_of("grape"))
      framework.assert_true(list.contains?("apple"))
      framework.assert_false(list.contains?("grape"))
    end
  end

  # LinkedList 测试
  framework.test_suite("LinkedList") do
    framework.test("基本操作") do
      list = LinkedList.new
      framework.assert_true(list.empty?)
      
      list.append(1)
      list.append(2)
      list.prepend(0)
      
      framework.assert_equal(3, list.size)
      framework.assert_equal(0, list.get(0))
      framework.assert_equal(2, list.get(2))
    end

    framework.test("删除操作") do
      list = LinkedList.new
      list.append(1)
      list.append(2)
      list.append(3)
      
      framework.assert_not_nil(list.remove(2))
      framework.assert_equal(2, list.size)
      framework.assert_false(list.contains?(2))
    end

    framework.test("反转操作") do
      list = LinkedList.new
      [1, 2, 3, 4].each { |x| list.append(x) }
      
      list.reverse!
      framework.assert_equal(4, list.get(0))
      framework.assert_equal(1, list.get(3))
    end
  end

  # Stack 测试
  framework.test_suite("Stack") do
    framework.test("LIFO操作") do
      stack = Stack.new
      framework.assert_true(stack.empty?)
      
      stack.push(1)
      stack.push(2)
      stack.push(3)
      
      framework.assert_equal(3, stack.size)
      framework.assert_equal(3, stack.peek)
      framework.assert_equal(3, stack.pop)
      framework.assert_equal(2, stack.pop)
      framework.assert_equal(1, stack.size)
    end

    framework.test("栈应用 - 括号匹配") do
      result1 = StackApplications.balanced_parentheses?("((())())")
      result2 = StackApplications.balanced_parentheses?("((())()")
      
      framework.assert_true(result1)
      framework.assert_false(result2)
    end
  end

  # Queue 测试
  framework.test_suite("Queue") do
    framework.test("FIFO操作") do
      queue = Queue.new
      framework.assert_true(queue.empty?)
      
      queue.enqueue(1)
      queue.enqueue(2)
      queue.enqueue(3)
      
      framework.assert_equal(3, queue.size)
      framework.assert_equal(1, queue.peek)
      framework.assert_equal(1, queue.dequeue)
      framework.assert_equal(2, queue.dequeue)
      framework.assert_equal(1, queue.size)
    end

    framework.test("循环队列") do
      queue = CircularQueue.new(3)
      
      queue.enqueue(1)
      queue.enqueue(2)
      queue.enqueue(3)
      
      framework.assert_true(queue.full?)
      framework.assert_false(queue.enqueue(4))

      framework.assert_equal(1, queue.dequeue)
      framework.assert_not_nil(queue.enqueue(4))
    end
  end

  # BinaryTree 测试
  framework.test_suite("BinaryTree") do
    framework.test("树构建和遍历") do
      tree = BinaryTree.from_array([1, 2, 3, 4, 5, 6, 7])

      inorder = tree.inorder_traversal
      preorder = tree.preorder_traversal

      framework.assert_equal([4, 2, 5, 1, 6, 3, 7], inorder)
      framework.assert_equal([1, 2, 4, 5, 3, 6, 7], preorder)
    end

    framework.test("树的属性") do
      tree = BinaryTree.from_array([1, 2, 3, 4, 5])

      framework.assert_equal(2, tree.height)
      framework.assert_equal(5, tree.count_nodes)
      framework.assert_true(tree.is_balanced?)
    end
  end

  # BST 测试
  framework.test_suite("BinarySearchTree") do
    framework.test("插入和查找") do
      bst = BinarySearchTree.new
      
      [5, 3, 7, 2, 4, 6, 8].each { |x| bst.insert(x) }
      
      framework.assert_not_nil(bst.search(5))
      framework.assert_not_nil(bst.search(3))
      framework.assert_nil(bst.search(10))
      
      inorder = bst.inorder_traversal
      framework.assert_equal([2, 3, 4, 5, 6, 7, 8], inorder)
    end

    framework.test("删除操作") do
      bst = BinarySearchTree.new
      [5, 3, 7, 2, 4, 6, 8].each { |x| bst.insert(x) }
      
      bst.delete(3)
      framework.assert_nil(bst.search(3))
      
      inorder = bst.inorder_traversal
      framework.assert_equal([2, 4, 5, 6, 7, 8], inorder)
    end

    framework.test("最值查找") do
      bst = BinarySearchTree.new
      [5, 3, 7, 2, 4, 6, 8].each { |x| bst.insert(x) }
      
      framework.assert_equal(2, bst.min)
      framework.assert_equal(8, bst.max)
    end
  end

  # AVL Tree 测试
  framework.test_suite("AVL Tree") do
    framework.test("基本操作") do
      avl = AVLTree.new
      framework.assert_true(avl.empty?)
      
      values = [10, 20, 30, 40, 50, 25]
      values.each { |val| avl.insert(val) }
      
      framework.assert_false(avl.empty?)
      framework.assert_equal(6, avl.size)
      framework.assert_true(avl.include?(25))
      framework.assert_false(avl.include?(100))
    end

    framework.test("自平衡特性") do
      avl = AVLTree.new
      # 插入会导致不平衡的序列
      [1, 2, 3, 4, 5, 6, 7].each { |val| avl.insert(val) }
      
      framework.assert_true(avl.balanced?)
      framework.assert(avl.height <= 4)  # AVL树高度应该较小
    end

    framework.test("中序遍历有序性") do
      avl = AVLTree.new
      values = [50, 30, 70, 20, 40, 60, 80]
      values.each { |val| avl.insert(val) }
      
      inorder = avl.inorder_traversal
      framework.assert_equal([20, 30, 40, 50, 60, 70, 80], inorder)
    end

    framework.test("删除后保持平衡") do
      avl = AVLTree.new
      [10, 5, 15, 2, 7, 12, 20].each { |val| avl.insert(val) }
      
      avl.delete(2)
      framework.assert_true(avl.balanced?)
      framework.assert_equal(6, avl.size)
    end

    framework.test("最值查找") do
      avl = AVLTree.new
      [50, 30, 70, 20, 40, 60, 80].each { |val| avl.insert(val) }
      
      framework.assert_equal(20, avl.min)
      framework.assert_equal(80, avl.max)
    end
  end

  # Heap 测试
  framework.test_suite("Heap") do
    framework.test("最大堆操作") do
      heap = MaxHeap.new
      
      [3, 1, 4, 1, 5, 9, 2, 6].each { |x| heap.insert(x) }
      
      framework.assert_equal(9, heap.peek)
      framework.assert_equal(9, heap.extract_max)
      framework.assert_equal(6, heap.extract_max)
      framework.assert_equal(5, heap.extract_max)
    end

    framework.test("最小堆操作") do
      heap = MinHeap.new
      
      [3, 1, 4, 1, 5, 9, 2, 6].each { |x| heap.insert(x) }
      
      framework.assert_equal(1, heap.peek)
      framework.assert_equal(1, heap.extract_min)
      framework.assert_equal(1, heap.extract_min)
      framework.assert_equal(2, heap.extract_min)
    end

    framework.test("堆排序") do
      array = [3, 1, 4, 1, 5, 9, 2, 6]
      sorted = HeapApplications.heap_sort(array)
      
      framework.assert_equal([1, 1, 2, 3, 4, 5, 6, 9], sorted)
    end
  end

  # Graph 测试
  framework.test_suite("Graph") do
    framework.test("图构建和基本操作") do
      graph = Graph.new(false)
      
      %w[A B C D].each { |v| graph.add_vertex(v) }
      
      graph.add_edge('A', 'B')
      graph.add_edge('B', 'C')
      graph.add_edge('C', 'D')
      
      framework.assert_equal(4, graph.vertex_count)
      framework.assert_equal(3, graph.edge_count)
      framework.assert_true(graph.has_edge?('A', 'B'))
      framework.assert_false(graph.has_edge?('A', 'D'))
    end

    framework.test("图遍历") do
      graph = Graph.new(false)
      
      %w[A B C D].each { |v| graph.add_vertex(v) }
      graph.add_edge('A', 'B')
      graph.add_edge('A', 'C')
      graph.add_edge('B', 'D')
      
      dfs_result = graph.dfs('A')
      bfs_result = graph.bfs('A')
      
      framework.assert_equal(4, dfs_result.size)
      framework.assert_equal(4, bfs_result.size)
      framework.assert_equal('A', bfs_result.first)
    end

    framework.test("路径查找") do
      graph = Graph.new(false)
      
      %w[A B C D].each { |v| graph.add_vertex(v) }
      graph.add_edge('A', 'B')
      graph.add_edge('B', 'C')
      graph.add_edge('C', 'D')
      
      path = graph.find_path('A', 'D')
      framework.assert_equal(['A', 'B', 'C', 'D'], path)
    end
  end

  # WeightedGraph 测试
  framework.test_suite("WeightedGraph") do
    framework.test("加权图基本操作") do
      graph = WeightedGraph.new(false)
      
      %w[A B C D].each { |v| graph.add_vertex(v) }
      
      graph.add_edge('A', 'B', 5)
      graph.add_edge('B', 'C', 3)
      graph.add_edge('A', 'C', 8)
      
      framework.assert_equal(5, graph.get_weight('A', 'B'))
      framework.assert_equal(3, graph.get_weight('B', 'C'))
    end

    framework.test("最短路径算法") do
      graph = WeightedGraph.new(false)
      
      %w[A B C D].each { |v| graph.add_vertex(v) }
      graph.add_edge('A', 'B', 1)
      graph.add_edge('B', 'C', 2)
      graph.add_edge('A', 'C', 5)
      graph.add_edge('C', 'D', 1)
      
      result = graph.shortest_path('A', 'D')
      framework.assert_equal(['A', 'B', 'C', 'D'], result[:path])
      framework.assert_equal(4, result[:distance])
    end
  end

  # HashTable 测试
  framework.test_suite("HashTable") do
    framework.test("基本操作") do
      ht = HashTable.new
      
      ht.put("key1", "value1")
      ht.put("key2", "value2")
      ht.put("key3", "value3")
      
      framework.assert_equal("value1", ht.get("key1"))
      framework.assert_equal("value2", ht.get("key2"))
      framework.assert_nil(ht.get("nonexistent"))
      
      framework.assert_equal(3, ht.size)
      framework.assert_true(ht.has_key?("key1"))
      framework.assert_false(ht.has_key?("key4"))
    end

    framework.test("删除操作") do
      ht = HashTable.new
      
      ht.put("key1", "value1")
      ht.put("key2", "value2")
      
      deleted = ht.delete("key1")
      framework.assert_equal("value1", deleted)
      framework.assert_nil(ht.get("key1"))
      framework.assert_equal(1, ht.size)
    end

    framework.test("自动扩容") do
      ht = HashTable.new(4)
      
      # 添加足够多的元素触发扩容
      10.times { |i| ht.put("key#{i}", "value#{i}") }
      
      framework.assert_equal(10, ht.size)
      framework.assert(ht.capacity > 4)
      
      # 验证所有元素仍然可以访问
      10.times { |i| framework.assert_equal("value#{i}", ht.get("key#{i}")) }
    end
  end

  # BloomFilter 测试
  framework.test_suite("BloomFilter") do
    framework.test("基本操作") do
      bf = BloomFilter.new(1000, 0.01)
      
      framework.assert_true(bf.empty?)
      
      bf.add("apple")
      bf.add("banana")
      bf.add("cherry")
      
      framework.assert_false(bf.empty?)
      framework.assert_true(bf.might_contain?("apple"))
      framework.assert_true(bf.might_contain?("banana"))
      framework.assert_false(bf.definitely_not_contain?("apple"))
    end

    framework.test("假阳性测试") do
      bf = BloomFilter.new(100, 0.1)
      
      # 添加一些元素
      %w[a b c d e].each { |x| bf.add(x) }
      
      # 测试已添加的元素（应该都返回true）
      %w[a b c d e].each do |x|
        framework.assert_true(bf.might_contain?(x))
      end
      
      # 测试未添加的元素（可能有假阳性）
      not_added = %w[f g h i j k l m n o p q r s t u v w x y z]
      false_positives = not_added.count { |x| bf.might_contain?(x) }
      
      # 假阳性率应该大致符合预期（允许一定误差）
      actual_fpr = false_positives.to_f / not_added.size
      framework.assert(actual_fpr <= 0.2, "假阳性率过高: #{actual_fpr}")
    end

    framework.test("集合操作") do
      bf1 = BloomFilter.new(100, 0.01)
      bf2 = BloomFilter.new(100, 0.01)
      
      %w[a b c].each { |x| bf1.add(x) }
      %w[c d e].each { |x| bf2.add(x) }
      
      union_bf = bf1.union(bf2)
      
      framework.assert_true(union_bf.might_contain?("a"))
      framework.assert_true(union_bf.might_contain?("d"))
      framework.assert_true(union_bf.might_contain?("c"))
    end
  end

  framework.summary
end

# 性能测试
def run_performance_tests
  puts "\n=== 性能测试 ==="
  
  # 测试不同数据结构的插入性能
  puts "\n插入性能测试 (10000个元素):"
  
  test_size = 10000
  
  # ArrayList
  start_time = Time.now
  array_list = ArrayList.new
  test_size.times { |i| array_list.append(i) }
  array_time = Time.now - start_time
  
  # LinkedList
  start_time = Time.now
  linked_list = LinkedList.new
  test_size.times { |i| linked_list.append(i) }
  linked_time = Time.now - start_time
  
  # HashTable
  start_time = Time.now
  hash_table = HashTable.new
  test_size.times { |i| hash_table.put(i, "value_#{i}") }
  hash_time = Time.now - start_time
  
  puts "ArrayList: #{(array_time * 1000).round(2)}ms"
  puts "LinkedList: #{(linked_time * 1000).round(2)}ms"
  puts "HashTable: #{(hash_time * 1000).round(2)}ms"
  
  # 测试查找性能
  puts "\n查找性能测试 (1000次随机查找):"
  
  search_count = 1000
  
  # ArrayList查找
  start_time = Time.now
  search_count.times { array_list[rand(test_size)] }
  array_search_time = Time.now - start_time
  
  # HashTable查找
  start_time = Time.now
  search_count.times { hash_table.get(rand(test_size)) }
  hash_search_time = Time.now - start_time
  
  puts "ArrayList: #{(array_search_time * 1000).round(2)}ms"
  puts "HashTable: #{(hash_search_time * 1000).round(2)}ms"
  
  # BST性能测试
  puts "\n BST性能测试:"
  bst = BinarySearchTree.new
  
  start_time = Time.now
  1000.times { |i| bst.insert(rand(10000)) }
  bst_insert_time = Time.now - start_time
  
  start_time = Time.now
  1000.times { bst.search(rand(10000)) }
  bst_search_time = Time.now - start_time
  
  puts "BST插入1000个元素: #{(bst_insert_time * 1000).round(2)}ms"
  puts "BST查找1000次: #{(bst_search_time * 1000).round(2)}ms"
  
  # 图算法性能测试
  puts "\n图算法性能测试:"
  graph = WeightedGraph.new(false)
  
  # 创建一个100个节点的图
  100.times { |i| graph.add_vertex(i) }
  
  start_time = Time.now
  # 添加随机边
  200.times do
    from = rand(100)
    to = rand(100)
    weight = rand(1..10)
    graph.add_edge(from, to, weight) if from != to
  end
  graph_build_time = Time.now - start_time
  
  start_time = Time.now
  graph.dijkstra(0)
  dijkstra_time = Time.now - start_time
  
  puts "构建100节点图: #{(graph_build_time * 1000).round(2)}ms"
  puts "Dijkstra算法: #{(dijkstra_time * 1000).round(2)}ms"
end

# 内存使用测试
def run_memory_tests
  puts "\n=== 内存使用测试 ==="
  
  # 获取当前内存使用（简化版本）
  def get_memory_usage
    `ps -o rss= -p #{Process.pid}`.to_i
  end
  
  initial_memory = get_memory_usage
  puts "初始内存使用: #{initial_memory} KB"
  
  # 测试大型数据结构的内存使用
  puts "\n创建大型数据结构:"
  
  # 大型ArrayList
  large_array = ArrayList.new
  100000.times { |i| large_array.append(i) }
  array_memory = get_memory_usage
  puts "ArrayList (100k元素): #{array_memory - initial_memory} KB"
  
  # 大型HashTable
  large_hash = HashTable.new
  50000.times { |i| large_hash.put(i, "value_#{i}") }
  hash_memory = get_memory_usage
  puts "HashTable (50k元素): #{hash_memory - array_memory} KB"
  
  # 大型BloomFilter
  large_bloom = BloomFilter.new(100000, 0.01)
  10000.times { |i| large_bloom.add("item_#{i}") }
  bloom_memory = get_memory_usage
  puts "BloomFilter (10k元素): #{bloom_memory - hash_memory} KB"
  
  puts "总内存增长: #{bloom_memory - initial_memory} KB"
end

# 主程序
if __FILE__ == $0
  puts "Ruby 数据结构测试套件"
  puts "=" * 50
  
  # 运行功能测试
  run_all_tests
  
  # 运行性能测试
  run_performance_tests
  
  # 运行内存测试
  run_memory_tests
  
  puts "\n测试完成！"
end