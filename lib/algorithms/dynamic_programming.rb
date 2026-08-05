# encoding: utf-8
# 动态规划算法集合
#
# 思路：
# 动态规划（DP）是一种通过将复杂问题分解为更小的子问题来求解的方法。
# 核心思想：记忆化存储子问题的解，避免重复计算。
# 适用条件：最优子结构 + 重叠子问题。
#
# 作用：
# 1. 最优化问题：寻找最大/最小值
# 2. 计数问题：计算方案数量
# 3. 决策问题：是否存在可行解
#
# 应用场景：
# 1. 算法竞赛：经典 DP 题型
# 2. 资源分配：背包问题、投资组合
# 3. 生物信息：序列比对
# 4. 自然语言处理：编辑距离、分词

module DynamicProgramming
  # ==================== 背包问题 ====================

  # 0/1 背包问题
  # 思路：每件物品只能选或不选（0/1），在容量限制下最大化总价值
  # dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i-1]] + val[i-1])
  # 时间复杂度：O(n * capacity)
  def self.knapsack_01(weights, values, capacity)
    n = weights.length
    dp = Array.new(capacity + 1, 0)

    n.times do |i|
      capacity.downto(weights[i]) do |w|
        dp[w] = [dp[w], dp[w - weights[i]] + values[i]].max
      end
    end
    dp[capacity]
  end

  # 0/1 背包（带方案回溯）
  def self.knapsack_01_with_items(weights, values, capacity)
    n = weights.length
    dp = Array.new(n + 1) { Array.new(capacity + 1, 0) }

    (1..n).each do |i|
      (0..capacity).each do |w|
        if weights[i - 1] <= w
          dp[i][w] = [dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1]].max
        else
          dp[i][w] = dp[i - 1][w]
        end
      end
    end

    # 回溯找出选择的物品
    items = []
    w = capacity
    n.downto(1) do |i|
      if dp[i][w] != dp[i - 1][w]
        items << i - 1
        w -= weights[i - 1]
      end
    end

    { max_value: dp[n][capacity], items: items.reverse }
  end

  # 完全背包问题（每件物品可选无限次）
  # 时间复杂度：O(n * capacity)
  def self.unbounded_knapsack(weights, values, capacity)
    n = weights.length
    dp = Array.new(capacity + 1, 0)

    (1..capacity).each do |w|
      n.times do |i|
        if weights[i] <= w
          dp[w] = [dp[w], dp[w - weights[i]] + values[i]].max
        end
      end
    end
    dp[capacity]
  end

  # ==================== 序列问题 ====================

  # 最长公共子序列（LCS）
  # 思路：dp[i][j] 表示 str1[0..i-1] 和 str2[0..j-1] 的 LCS 长度
  # 时间复杂度：O(n*m)
  def self.longest_common_subsequence(str1, str2)
    n = str1.length
    m = str2.length
    dp = Array.new(n + 1) { Array.new(m + 1, 0) }

    (1..n).each do |i|
      (1..m).each do |j|
        if str1[i - 1] == str2[j - 1]
          dp[i][j] = dp[i - 1][j - 1] + 1
        else
          dp[i][j] = [dp[i - 1][j], dp[i][j - 1]].max
        end
      end
    end

    # 回溯构造 LCS
    lcs = ""
    i = n
    j = m
    while i > 0 && j > 0
      if str1[i - 1] == str2[j - 1]
        lcs = str1[i - 1] + lcs
        i -= 1
        j -= 1
      elsif dp[i - 1][j] > dp[i][j - 1]
        i -= 1
      else
        j -= 1
      end
    end

    { length: dp[n][m], sequence: lcs }
  end

  # 最长递增子序列（LIS）
  # 时间复杂度：O(n²) 简单版 | O(n log n) 优化版
  def self.longest_increasing_subsequence(array)
    return [] if array.empty?

    n = array.length
    dp = Array.new(n, 1)
    prev = Array.new(n, -1)

    (1...n).each do |i|
      (0...i).each do |j|
        if array[i] > array[j] && dp[j] + 1 > dp[i]
          dp[i] = dp[j] + 1
          prev[i] = j
        end
      end
    end

    # 找到最长的结尾
    max_len = dp.max
    end_idx = dp.index(max_len)

    # 回溯构造 LIS
    lis = []
    while end_idx >= 0
      lis.unshift(array[end_idx])
      end_idx = prev[end_idx]
    end

    lis
  end

  # 最长递增子序列（O(n log n) 优化版）
  def self.lis_optimized(array)
    return [] if array.empty?

    tails = []  # tails[i] = 长度为 i+1 的 LIS 的最小结尾值
    prev = Array.new(array.length, -1)
    indices = []

    array.each_with_index do |num, i|
      # 二分查找插入位置
      pos = tails.bsearch_index { |x| x >= num } || tails.length

      if pos == tails.length
        tails << num
      else
        tails[pos] = num
      end
      indices[pos] = i
      prev[i] = pos > 0 ? indices[pos - 1] : -1
    end

    # 回溯
    lis = []
    idx = indices[tails.length - 1]
    while idx >= 0
      lis.unshift(array[idx])
      idx = prev[idx]
    end
    lis
  end

  # 最大子数组和（Kadane 算法）
  # 思路：dp[i] = max(num[i], dp[i-1] + num[i])
  # 时间复杂度：O(n)
  def self.maximum_subarray(array)
    return 0 if array.empty?

    max_ending_here = max_so_far = array[0]
    start = finish = temp_start = 0

    (1...array.length).each do |i|
      if array[i] > max_ending_here + array[i]
        max_ending_here = array[i]
        temp_start = i
      else
        max_ending_here += array[i]
      end

      if max_ending_here > max_so_far
        max_so_far = max_ending_here
        start = temp_start
        finish = i
      end
    end

    { max_sum: max_so_far, subarray: array[start..finish], start: start, end: finish }
  end

  # ==================== 硬币 / 找零问题 ====================

  # 硬币找零（最少硬币数）
  # 思路：dp[i] = min(dp[i - coin] + 1) for each coin
  # 时间复杂度：O(amount * coins.length)
  def self.coin_change(coins, amount)
    dp = Array.new(amount + 1, Float::INFINITY)
    dp[0] = 0

    (1..amount).each do |i|
      coins.each do |coin|
        if coin <= i
          dp[i] = [dp[i], dp[i - coin] + 1].min
        end
      end
    end
    dp[amount] == Float::INFINITY ? -1 : dp[amount]
  end

  # 硬币找零（组合数）
  # 思路：dp[i] 表示组成金额 i 的组合数
  # 时间复杂度：O(amount * coins.length)
  def self.coin_change_combinations(coins, amount)
    dp = Array.new(amount + 1, 0)
    dp[0] = 1

    coins.each do |coin|
      (coin..amount).each do |i|
        dp[i] += dp[i - coin]
      end
    end
    dp[amount]
  end

  # ==================== 路径问题 ====================

  # 网格路径数（从左上角到右下角）
  # 思路：dp[i][j] = dp[i-1][j] + dp[i][j-1]
  # 时间复杂度：O(m*n)
  def self.unique_paths(m, n)
    dp = Array.new(n, 1)

    (1...m).each do |i|
      (1...n).each do |j|
        dp[j] += dp[j - 1]
      end
    end
    dp[n - 1]
  end

  # 带障碍物的网格路径数
  def self.unique_paths_with_obstacles(grid)
    m = grid.length
    n = grid[0].length
    dp = Array.new(n, 0)
    dp[0] = grid[0][0] == 0 ? 1 : 0

    (0...m).each do |i|
      (0...n).each do |j|
        if grid[i][j] == 1
          dp[j] = 0
        elsif j > 0
          dp[j] += dp[j - 1]
        end
      end
    end
    dp[n - 1]
  end

  # 最小路径和
  # 时间复杂度：O(m*n)
  def self.minimum_path_sum(grid)
    m = grid.length
    n = grid[0].length
    dp = Array.new(n, 0)

    m.times do |i|
      n.times do |j|
        if i == 0 && j == 0
          dp[j] = grid[i][j]
        elsif i == 0
          dp[j] = dp[j - 1] + grid[i][j]
        elsif j == 0
          dp[j] = dp[j] + grid[i][j]
        else
          dp[j] = [dp[j], dp[j - 1]].min + grid[i][j]
        end
      end
    end
    dp[n - 1]
  end

  # ==================== 经典 DP ====================

  # 斐波那契数列
  # 时间复杂度：O(n)
  def self.fibonacci(n)
    return n if n <= 1
    a, b = 0, 1
    (2..n).each { a, b = b, a + b }
    b
  end

  # 爬楼梯（每次爬1或2阶，多少种方式到顶）
  # 思路：dp[i] = dp[i-1] + dp[i-2]，本质是斐波那契
  # 时间复杂度：O(n)
  def self.climb_stairs(n)
    return 1 if n <= 1
    a, b = 1, 1
    (2..n).each { a, b = b, a + b }
    b
  end

  # 打家劫舍（不能偷相邻的）
  # 思路：dp[i] = max(dp[i-1], dp[i-2] + nums[i])
  # 时间复杂度：O(n)
  def self.house_robber(nums)
    return 0 if nums.empty?
    return nums[0] if nums.length == 1

    prev2 = nums[0]
    prev1 = [nums[0], nums[1]].max

    (2...nums.length).each do |i|
      current = [prev1, prev2 + nums[i]].max
      prev2 = prev1
      prev1 = current
    end
    prev1
  end

  # 三角形最小路径和
  # 时间复杂度：O(n²)
  def self.triangle_minimum_path(triangle)
    return 0 if triangle.empty?

    dp = triangle.last.dup

    (triangle.length - 2).downto(0) do |i|
      (0..i).each do |j|
        dp[j] = [dp[j], dp[j + 1]].min + triangle[i][j]
      end
    end
    dp[0]
  end

  # 分割等和子集（能否将数组分成和相等的两个子集）
  # 转化为 0/1 背包：能否选出若干元素使和为 sum/2
  # 时间复杂度：O(n * sum)
  def self.can_partition(nums)
    total = nums.sum
    return false if total.odd?
    target = total / 2

    dp = Array.new(target + 1, false)
    dp[0] = true

    nums.each do |num|
      target.downto(num) do |i|
        dp[i] ||= dp[i - num]
      end
    end
    dp[target]
  end

  # ==================== 区间 DP ====================

  # 矩阵链乘法（最少标量乘法次数）
  # 时间复杂度：O(n³)
  def self.matrix_chain_order(dimensions)
    n = dimensions.length - 1
    dp = Array.new(n) { Array.new(n, 0) }

    (2..n).each do |len|
      (0..n - len).each do |i|
        j = i + len - 1
        dp[i][j] = Float::INFINITY
        (i...j).each do |k|
          cost = dp[i][k] + dp[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
          dp[i][j] = [dp[i][j], cost].min
        end
      end
    end
    dp[0][n - 1]
  end

  # 戳气球（Burst Balloons）
  # 时间复杂度：O(n³)
  def self.burst_balloons(nums)
    n = nums.length
    balloons = [1] + nums + [1]
    dp = Array.new(n + 2) { Array.new(n + 2, 0) }

    (2..n + 1).each do |len|
      (0..n + 1 - len).each do |i|
        j = i + len
        (i + 1...j).each do |k|
          coins = balloons[i] * balloons[k] * balloons[j] + dp[i][k] + dp[k][j]
          dp[i][j] = [dp[i][j], coins].max
        end
      end
    end
    dp[0][n + 1]
  end

  # 性能对比测试
  def self.benchmark
    puts "动态规划算法性能演示"
    puts "-" * 50

    # 背包问题
    n = 100
    weights = Array.new(n) { rand(1..100) }
    values = Array.new(n) { rand(1..500) }
    capacity = 5000

    start = Time.now
    result = knapsack_01(weights, values, capacity)
    elapsed = (Time.now - start) * 1000
    puts "0/1背包 (#{n}件物品, 容量#{capacity}): #{elapsed.round(3)}ms, 最大价值:#{result}"

    # LCS
    str1 = "AGGTAB" * 50
    str2 = "GXTXAYB" * 50
    start = Time.now
    result = longest_common_subsequence(str1, str2)
    elapsed = (Time.now - start) * 1000
    puts "LCS (长度#{str1.length}x#{str2.length}): #{elapsed.round(3)}ms, LCS长度:#{result[:length]}"

    # LIS O(n²) vs O(n log n)
    arr = Array.new(1000) { rand(1..10000) }
    start = Time.now
    result1 = longest_increasing_subsequence(arr)
    elapsed1 = (Time.now - start) * 1000

    start = Time.now
    result2 = lis_optimized(arr)
    elapsed2 = (Time.now - start) * 1000

    puts "LIS (#{arr.length}元素):"
    puts "  O(n²): #{elapsed1.round(3)}ms, 长度:#{result1.length}"
    puts "  O(n log n): #{elapsed2.round(3)}ms, 长度:#{result2.length}"
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== 动态规划算法演示 ==="

  # 背包问题
  puts "\n=== 0/1 背包 ==="
  weights = [2, 3, 4, 5]
  values = [3, 4, 5, 6]
  capacity = 8
  puts "物品重量: #{weights}"
  puts "物品价值: #{values}"
  puts "背包容量: #{capacity}"
  result = DynamicProgramming.knapsack_01_with_items(weights, values, capacity)
  puts "最大价值: #{result[:max_value]}"
  puts "选择的物品索引: #{result[:items]}"

  puts "\n完全背包: #{DynamicProgramming.unbounded_knapsack(weights, values, capacity)}"

  # 序列问题
  puts "\n=== 最长公共子序列 ==="
  str1, str2 = "ABCDGH", "AEDFHR"
  lcs = DynamicProgramming.longest_common_subsequence(str1, str2)
  puts "输入: '#{str1}', '#{str2}'"
  puts "LCS: '#{lcs[:sequence]}', 长度: #{lcs[:length]}"

  puts "\n=== 最长递增子序列 ==="
  arr = [10, 9, 2, 5, 3, 7, 101, 18]
  lis1 = DynamicProgramming.longest_increasing_subsequence(arr)
  lis2 = DynamicProgramming.lis_optimized(arr)
  puts "输入: #{arr}"
  puts "LIS(O(n²)): #{lis1}"
  puts "LIS(O(n log n)): #{lis2}"

  puts "\n=== 最大子数组和 ==="
  arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
  result = DynamicProgramming.maximum_subarray(arr)
  puts "输入: #{arr}"
  puts "最大和: #{result[:max_sum]}"
  puts "子数组: #{result[:subarray]}"

  # 硬币问题
  puts "\n=== 硬币找零 ==="
  coins = [1, 2, 5]
  amount = 11
  puts "硬币: #{coins}, 金额: #{amount}"
  puts "最少硬币数: #{DynamicProgramming.coin_change(coins, amount)}"
  puts "组合数: #{DynamicProgramming.coin_change_combinations(coins, amount)}"

  # 路径问题
  puts "\n=== 网格路径 ==="
  puts "3x7 网格路径数: #{DynamicProgramming.unique_paths(3, 7)}"

  grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
  puts "最小路径和 (#{grid}): #{DynamicProgramming.minimum_path_sum(grid)}"

  # 经典 DP
  puts "\n=== 经典问题 ==="
  puts "斐波那契(20): #{DynamicProgramming.fibonacci(20)}"
  puts "爬楼梯(10阶): #{DynamicProgramming.climb_stairs(10)}"
  nums = [2, 7, 9, 3, 1]
  puts "打家劫舍 (#{nums}): #{DynamicProgramming.house_robber(nums)}"

  triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
  puts "三角形最小路径和: #{DynamicProgramming.triangle_minimum_path(triangle)}"

  puts "\n分割等和子集 [1,5,11,5]: #{DynamicProgramming.can_partition([1, 5, 11, 5])}"
  puts "分割等和子集 [1,2,3,5]: #{DynamicProgramming.can_partition([1, 2, 3, 5])}"

  # 性能对比
  puts
  DynamicProgramming.benchmark
end
