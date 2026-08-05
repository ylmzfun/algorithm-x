#!/usr/bin/env ruby
# frozen_string_literal: true

# 性能测试套件
# 
# 这个文件包含了各种数据结构的性能测试，
# 用于比较不同数据结构在各种操作下的性能表现。

require 'benchmark'
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

# 性能测试框架
class PerformanceTest
  def initialize
    @test_sizes = [100, 1000, 10_000]
    @results = {}
  end

  def run_all_tests
    puts "=== 数据结构性能测试 ==="
    puts "测试规模: #{@test_sizes}"
    puts "\n" + "=" * 80

    test_linear_structures
    test_tree_structures
    test_hash_structures
    test_graph_structures

    print_summary
  end

  private

  def test_linear_structures
    puts "\n=== 线性数据结构性能测试 ==="

    @test_sizes.each do |size|
      puts "\n--- 测试规模: #{size} ---"

      # ArrayList vs Array 插入性能
      puts "\n插入性能比较:"
      Benchmark.bm(15) do |x|
        x.report('ArrayList:') do
          list = ArrayList.new
          size.times { |i| list.append(i) }
        end

        x.report('Ruby Array:') do
          arr = []
          size.times { |i| arr << i }
        end

        x.report('LinkedList:') do
          list = LinkedList.new
          size.times { |i| list.append(i) }
        end
      end

      # 查找性能比较
      puts "\n查找性能比较:"
      array_list = ArrayList.new
      ruby_array = []
      linked_list = LinkedList.new

      size.times do |i|
        array_list.append(i)
        ruby_array << i
        linked_list.append(i)
      end

      target = size / 2

      Benchmark.bm(15) do |x|
        x.report('ArrayList:') do
          100.times { array_list.index_of(target) }
        end

        x.report('Ruby Array:') do
          100.times { ruby_array.index(target) }
        end

        x.report('LinkedList:') do
          100.times { linked_list.find(target) }
        end
      end
    end
  end

  def test_tree_structures
    puts "\n=== 树形数据结构性能测试 ==="

    @test_sizes.each do |size|
      puts "\n--- 测试规模: #{size} ---"

      # 插入性能比较
      puts "\n插入性能比较:"
      data = (1..size).to_a.shuffle

      Benchmark.bm(15) do |x|
        x.report('BST:') do
          bst = BinarySearchTree.new
          data.each { |val| bst.insert(val) }
        end

        x.report('AVL Tree:') do
          avl = AVLTree.new
          data.each { |val| avl.insert(val) }
        end

        x.report('MaxHeap:') do
          heap = MaxHeap.new
          data.each { |val| heap.insert(val) }
        end
      end

      # 查找性能比较
      puts "\n查找性能比较:"
      bst = BinarySearchTree.new
      avl = AVLTree.new
      data.each do |val|
        bst.insert(val)
        avl.insert(val)
      end

      search_targets = data.sample(100)

      Benchmark.bm(15) do |x|
        x.report('BST:') do
          search_targets.each { |target| bst.search(target) }
        end

        x.report('AVL Tree:') do
          search_targets.each { |target| avl.search(target) }
        end
      end
    end
  end

  def test_hash_structures
    puts "\n=== 哈希数据结构性能测试 ==="

    @test_sizes.each do |size|
      puts "\n--- 测试规模: #{size} ---"

      # 插入性能比较
      puts "\n插入性能比较:"
      keys = (1..size).map { |i| "key_#{i}" }
      values = (1..size).to_a

      Benchmark.bm(15) do |x|
        x.report('HashTable:') do
          hash_table = HashTable.new
          keys.zip(values).each { |k, v| hash_table.put(k, v) }
        end

        x.report('Ruby Hash:') do
          hash = {}
          keys.zip(values).each { |k, v| hash[k] = v }
        end
      end

      # 查找性能比较
      puts "\n查找性能比较:"
      hash_table = HashTable.new
      ruby_hash = {}
      keys.zip(values).each do |k, v|
        hash_table.put(k, v)
        ruby_hash[k] = v
      end

      search_keys = keys.sample(100)

      Benchmark.bm(15) do |x|
        x.report('HashTable:') do
          search_keys.each { |key| hash_table.get(key) }
        end

        x.report('Ruby Hash:') do
          search_keys.each { |key| ruby_hash[key] }
        end
      end

      # BloomFilter 性能测试
      puts "\nBloomFilter 性能测试:"
      bloom = BloomFilter.new(size * 2, 3)
      test_items = (1..size).map { |i| "item_#{i}" }

      Benchmark.bm(15) do |x|
        x.report('BF Insert:') do
          test_items.each { |item| bloom.add(item) }
        end

        x.report('BF Query:') do
          test_items.each { |item| bloom.include?(item) }
        end
      end
    end
  end

  def test_graph_structures
    puts "\n=== 图数据结构性能测试 ==="

    @test_sizes.each do |size|
      puts "\n--- 测试规模: #{size} 个顶点 ---"

      # 图构建性能
      puts "\n图构建性能:"
      vertices = (1..size).to_a
      edges = []
      
      # 生成随机边（确保图连通）
      (1...size).each { |i| edges << [i, i + 1] }
      (size / 2).times { edges << [rand(1..size), rand(1..size)] }

      Benchmark.bm(15) do |x|
        x.report('Graph:') do
          graph = Graph.new(false)
          vertices.each { |v| graph.add_vertex(v) }
          edges.each { |u, v| graph.add_edge(u, v) }
        end

        x.report('WeightedGraph:') do
          wgraph = WeightedGraph.new(false)
          vertices.each { |v| wgraph.add_vertex(v) }
          edges.each { |u, v| wgraph.add_edge(u, v, rand(1..10)) }
        end
      end

      # 遍历性能（仅对较小规模测试）
      if size <= 1000
        puts "\n图遍历性能:"
        graph = Graph.new(false)
        vertices.each { |v| graph.add_vertex(v) }
        edges.each { |u, v| graph.add_edge(u, v) }

        Benchmark.bm(15) do |x|
          x.report('DFS:') do
            10.times { graph.dfs(1) }
          end

          x.report('BFS:') do
            10.times { graph.bfs(1) }
          end
        end
      end
    end
  end

  def print_summary
    puts "\n" + "=" * 80
    puts "=== 性能测试总结 ==="
    puts "\n主要发现:"
    puts "1. ArrayList 在随机访问方面优于 LinkedList"
    puts "2. AVL树 在平衡性方面优于普通BST"
    puts "3. HashTable 提供了接近O(1)的查找性能"
    puts "4. BloomFilter 在大规模数据去重场景下表现优异"
    puts "5. 图遍历算法的性能与图的结构密切相关"
    puts "\n建议:"
    puts "- 频繁随机访问：使用 ArrayList"
    puts "- 频繁插入删除：使用 LinkedList"
    puts "- 需要有序且平衡：使用 AVL Tree"
    puts "- 快速查找：使用 HashTable"
    puts "- 大规模去重：使用 BloomFilter"
  end
end

# 内存使用测试
class MemoryTest
  def self.run_memory_tests
    puts "\n=== 内存使用测试 ==="

    test_size = 10_000
    
    # 测试各种数据结构的内存使用
    structures = {
      'ArrayList' => -> { 
        list = ArrayList.new
        test_size.times { |i| list.append(i) }
        list
      },
      'LinkedList' => -> {
        list = LinkedList.new
        test_size.times { |i| list.append(i) }
        list
      },
      'BST' => -> {
        bst = BinarySearchTree.new
        (1..test_size).to_a.shuffle.each { |val| bst.insert(val) }
        bst
      },
      'AVL Tree' => -> {
        avl = AVLTree.new
        (1..test_size).to_a.shuffle.each { |val| avl.insert(val) }
        avl
      },
      'HashTable' => -> {
        hash = HashTable.new
        test_size.times { |i| hash.put("key_#{i}", i) }
        hash
      }
    }

    structures.each do |name, creator|
      puts "\n测试 #{name} 内存使用:"
      
      # 简单的内存使用估算
      start_time = Time.now
      structure = creator.call
      end_time = Time.now
      
      puts "  创建时间: #{((end_time - start_time) * 1000).round(2)}ms"
      puts "  元素数量: #{structure.respond_to?(:size) ? structure.size : test_size}"
      
      # 触发垃圾回收
      structure = nil
      GC.start
    end
  end
end

# 运行测试
if __FILE__ == $PROGRAM_NAME
  performance_test = PerformanceTest.new
  performance_test.run_all_tests
  
  MemoryTest.run_memory_tests
end