#!/usr/bin/env ruby
# encoding: utf-8
# 算法测试运行器
#
# 测试覆盖排序、搜索、字符串匹配、动态规划算法
# 以及新增数据结构：Trie、UnionFind

require_relative '../lib/algorithms/sorting'
require_relative '../lib/algorithms/searching'
require_relative '../lib/algorithms/string'
require_relative '../lib/algorithms/dynamic_programming'
require_relative '../lib/data_structures/trie'
require_relative '../lib/data_structures/union_find'

class TestFramework
  def initialize
    @tests_run = 0
    @tests_passed = 0
    @tests_failed = 0
  end

  def test_suite(name)
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
    end
  end

  def assert(condition, message = "断言失败")
    raise message unless condition
  end

  def assert_equal(expected, actual, message = nil)
    message ||= "期望 #{expected.inspect}, 实际 #{actual.inspect}"
    raise message unless expected == actual
  end

  def assert_not_nil(value, message = "值不应为nil")
    raise message if value.nil?
  end

  def assert_nil(value, message = "值应为nil")
    raise message unless value.nil?
  end

  def assert_true(value, message = "值应为true")
    raise message unless value
  end

  def assert_false(value, message = "值应为false")
    raise message if value
  end

  def summary
    puts "\n=== 测试总结 ==="
    puts "总测试数: #{@tests_run}"
    puts "通过: #{@tests_passed}"
    puts "失败: #{@tests_failed}"
    puts "成功率: #{(@tests_passed.to_f / @tests_run * 100).round(2)}%"
  end
end

def run_all_tests
  f = TestFramework.new

  # ==================== 排序算法测试 ====================
  f.test_suite("排序算法") do
    array = [64, 34, 25, 12, 22, 11, 90]
    expected = [11, 12, 22, 25, 34, 64, 90]

    f.test("冒泡排序") do
      result = SortingAlgorithms.bubble_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("选择排序") do
      result = SortingAlgorithms.selection_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("插入排序") do
      result = SortingAlgorithms.insertion_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("希尔排序") do
      result = SortingAlgorithms.shell_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("归并排序") do
      result = SortingAlgorithms.merge_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("快速排序") do
      result = SortingAlgorithms.quick_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("三路快速排序") do
      result = SortingAlgorithms.quick_sort_3way(array)
      f.assert_equal(expected, result)
    end

    f.test("堆排序") do
      result = SortingAlgorithms.heap_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("计数排序") do
      result = SortingAlgorithms.counting_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("桶排序") do
      result = SortingAlgorithms.bucket_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("基数排序") do
      result = SortingAlgorithms.radix_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("鸡尾酒排序") do
      result = SortingAlgorithms.cocktail_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("Tim排序") do
      result = SortingAlgorithms.tim_sort(array)
      f.assert_equal(expected, result)
    end

    f.test("已排序检查") do
      f.assert_true(SortingAlgorithms.sorted?(expected))
      f.assert_false(SortingAlgorithms.sorted?(array))
    end

    f.test("快速选择（第k小元素）") do
      f.assert_equal(11, SortingAlgorithms.quick_select(array, 1))
      f.assert_equal(25, SortingAlgorithms.quick_select(array, 4))
      f.assert_equal(90, SortingAlgorithms.quick_select(array, 7))
    end
  end

  # ==================== 搜索算法测试 ====================
  f.test_suite("搜索算法") do
    sorted = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 11

    f.test("线性搜索") do
      f.assert_equal(5, SearchingAlgorithms.linear_search(sorted, target))
      f.assert_equal(-1, SearchingAlgorithms.linear_search(sorted, 100))
    end

    f.test("二分搜索（迭代）") do
      f.assert_equal(5, SearchingAlgorithms.binary_search(sorted, target))
      f.assert_equal(-1, SearchingAlgorithms.binary_search(sorted, 100))
    end

    f.test("二分搜索（递归）") do
      f.assert_equal(5, SearchingAlgorithms.binary_search_recursive(sorted, target))
      f.assert_equal(-1, SearchingAlgorithms.binary_search_recursive(sorted, 100))
    end

    f.test("下界/上界搜索") do
      dup = [1, 2, 2, 2, 3, 3, 5]
      f.assert_equal(1, SearchingAlgorithms.lower_bound(dup, 2))
      f.assert_equal(4, SearchingAlgorithms.upper_bound(dup, 2))
      f.assert_equal([1, 3], SearchingAlgorithms.search_range(dup, 2))
    end

    f.test("跳跃搜索") do
      f.assert_equal(5, SearchingAlgorithms.jump_search(sorted, target))
    end

    f.test("指数搜索") do
      f.assert_equal(5, SearchingAlgorithms.exponential_search(sorted, target))
    end

    f.test("插值搜索") do
      f.assert_equal(5, SearchingAlgorithms.interpolation_search(sorted, target))
    end

    f.test("斐波那契搜索") do
      f.assert_equal(5, SearchingAlgorithms.fibonacci_search(sorted, target))
    end

    f.test("旋转数组搜索") do
      rotated = [4, 5, 6, 7, 0, 1, 2]
      f.assert_equal(4, SearchingAlgorithms.search_in_rotated_array(rotated, 0))
      f.assert_equal(-1, SearchingAlgorithms.search_in_rotated_array(rotated, 3))
      f.assert_equal(0, SearchingAlgorithms.find_min_in_rotated_array(rotated))
    end

    f.test("峰值查找") do
      peaks = [1, 2, 3, 1]
      f.assert_equal(2, SearchingAlgorithms.find_peak_element(peaks))
    end

    f.test("二维矩阵搜索") do
      matrix = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
      f.assert_equal([1, 1], SearchingAlgorithms.search_in_2d_matrix(matrix, 5))
      f.assert_nil(SearchingAlgorithms.search_in_2d_matrix(matrix, 10))
    end
  end

  # ==================== 字符串算法测试 ====================
  f.test_suite("字符串算法") do
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    expected_pos = [10]

    f.test("暴力匹配") do
      f.assert_equal(expected_pos, StringAlgorithms.brute_force(text, pattern))
    end

    f.test("KMP算法") do
      f.assert_equal(expected_pos, StringAlgorithms.kmp_search(text, pattern))
    end

    f.test("Rabin-Karp算法") do
      f.assert_equal(expected_pos, StringAlgorithms.rabin_karp(text, pattern))
    end

    f.test("Boyer-Moore算法") do
      f.assert_equal(expected_pos, StringAlgorithms.boyer_moore(text, pattern))
    end

    f.test("Z-Algorithm匹配") do
      f.assert_equal(expected_pos, StringAlgorithms.z_search(text, pattern))
    end

    f.test("Z数组计算") do
      z = StringAlgorithms.z_algorithm("aabcaabxaaaz")
      f.assert_not_nil(z)
    end

    f.test("最长公共子串") do
      result = StringAlgorithms.longest_common_substring("abcdef", "zbcde")
      f.assert_equal("bcde", result)
    end

    f.test("编辑距离") do
      f.assert_equal(3, StringAlgorithms.edit_distance("kitten", "sitting"))
      f.assert_equal(0, StringAlgorithms.edit_distance("same", "same"))
    end

    f.test("最长回文子串") do
      f.assert_equal("bab", StringAlgorithms.longest_palindrome("babad"))
      f.assert_equal("bb", StringAlgorithms.longest_palindrome("cbbd"))
    end

    f.test("回文判断") do
      f.assert_true(StringAlgorithms.palindrome?("racecar"))
      f.assert_false(StringAlgorithms.palindrome?("hello"))
    end
  end

  # ==================== 动态规划测试 ====================
  f.test_suite("动态规划") do
    f.test("0/1背包") do
      result = DynamicProgramming.knapsack_01([2, 3, 4, 5], [3, 4, 5, 6], 8)
      f.assert_equal(10, result)
    end

    f.test("0/1背包带方案回溯") do
      result = DynamicProgramming.knapsack_01_with_items([2, 3, 4, 5], [3, 4, 5, 6], 8)
      f.assert_equal(10, result[:max_value])
    end

    f.test("完全背包") do
      result = DynamicProgramming.unbounded_knapsack([2, 3, 4], [3, 4, 5], 8)
      f.assert_equal(12, result)
    end

    f.test("最长公共子序列") do
      result = DynamicProgramming.longest_common_subsequence("ABCDGH", "AEDFHR")
      f.assert_equal(3, result[:length])
      f.assert_equal("ADH", result[:sequence])
    end

    f.test("最长递增子序列 O(n²)") do
      result = DynamicProgramming.longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
      f.assert_equal([2, 5, 7, 101], result)
    end

    f.test("最长递增子序列 O(n log n)") do
      result = DynamicProgramming.lis_optimized([10, 9, 2, 5, 3, 7, 101, 18])
      f.assert_equal(4, result.length)
    end

    f.test("最大子数组和") do
      result = DynamicProgramming.maximum_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
      f.assert_equal(6, result[:max_sum])
    end

    f.test("硬币找零（最少硬币）") do
      f.assert_equal(3, DynamicProgramming.coin_change([1, 2, 5], 11))
      f.assert_equal(-1, DynamicProgramming.coin_change([2], 3))
    end

    f.test("硬币找零（组合数）") do
      f.assert_equal(4, DynamicProgramming.coin_change_combinations([1, 2, 5], 5))
    end

    f.test("网格路径") do
      f.assert_equal(28, DynamicProgramming.unique_paths(3, 7))
    end

    f.test("斐波那契") do
      f.assert_equal(55, DynamicProgramming.fibonacci(10))
      f.assert_equal(0, DynamicProgramming.fibonacci(0))
    end

    f.test("爬楼梯") do
      f.assert_equal(5, DynamicProgramming.climb_stairs(4))
    end

    f.test("打家劫舍") do
      f.assert_equal(12, DynamicProgramming.house_robber([2, 7, 9, 3, 1]))
    end

    f.test("分割等和子集") do
      f.assert_true(DynamicProgramming.can_partition([1, 5, 11, 5]))
      f.assert_false(DynamicProgramming.can_partition([1, 2, 3, 5]))
    end
  end

  # ==================== Trie 测试 ====================
  f.test_suite("Trie 字典树") do
    f.test("插入和搜索") do
      trie = Trie.new
      trie.insert("hello")
      trie.insert("world")

      f.assert_true(trie.include?("hello"))
      f.assert_true(trie.include?("world"))
      f.assert_false(trie.include?("hell"))
      f.assert_equal(2, trie.size)
    end

    f.test("前缀搜索") do
      trie = Trie.new
      %w[hello help hero her].each { |w| trie.insert(w) }

      f.assert_equal(%w[hello help hero her].sort, trie.words_with_prefix("he").sort)
      f.assert_equal(%w[help], trie.words_with_prefix("help"))
      f.assert_equal(4, trie.count_prefix("he"))
    end

    f.test("删除单词") do
      trie = Trie.new
      trie.insert_all(%w[hello help hero])

      f.assert_true(trie.delete("hello"))
      f.assert_false(trie.include?("hello"))
      f.assert_true(trie.include?("help"))
      f.assert_equal(2, trie.size)
    end

    f.test("模糊搜索") do
      trie = Trie.new
      trie.insert_all(%w[hello help hero her])

      results = trie.fuzzy_search("he..")
      f.assert_equal(%w[help hero].sort, results.sort)
    end

    f.test("最长公共前缀") do
      trie = Trie.new
      trie.insert_all(%w[flower flow flight])
      f.assert_equal("fl", trie.longest_common_prefix)
    end
  end

  # ==================== UnionFind 测试 ====================
  f.test_suite("UnionFind 并查集") do
    f.test("基本合并和查找") do
      uf = UnionFind.new(10)

      uf.union(0, 1)
      uf.union(1, 2)
      uf.union(3, 4)

      f.assert_true(uf.connected?(0, 2))
      f.assert_true(uf.connected?(3, 4))
      f.assert_false(uf.connected?(0, 3))
    end

    f.test("集合数量和大小") do
      uf = UnionFind.new(10)

      uf.union(0, 1)
      uf.union(1, 2)
      uf.union(3, 4)
      uf.union(5, 6)
      uf.union(6, 7)
      uf.union(7, 8)

      f.assert_equal(4, uf.set_count)
      f.assert_equal(3, uf.set_size(0))
      f.assert_equal(4, uf.set_size(5))
      f.assert_equal(1, uf.set_size(9))
    end

    f.test("重复合并") do
      uf = UnionFind.new(5)
      uf.union(0, 1)
      result = uf.union(0, 1)  # 已经连通，不应变化
      f.assert_false(result)
      f.assert_equal(4, uf.set_count)
    end

    f.test("GenericUnionFind（任意类型）") do
      guf = GenericUnionFind.new
      guf.union("Alice", "Bob")
      guf.union("Bob", "Charlie")

      f.assert_true(guf.connected?("Alice", "Charlie"))
      f.assert_false(guf.connected?("Alice", "David"))
      f.assert_equal(1, guf.set_count)
    end
  end

  f.summary
end

if __FILE__ == $0
  puts "Ruby 算法测试套件"
  puts "=" * 50
  run_all_tests
end
