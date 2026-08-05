# encoding: utf-8
# 搜索算法集合
#
# 思路：
# 搜索算法用于在数据集（通常是数组）中查找特定元素。
# 根据数据是否有序，可以选择线性搜索或二分搜索等不同策略。
#
# 作用：
# 1. 元素查找：定位特定数据的位置
# 2. 边界查找：找到满足条件的第一个/最后一个位置
# 3. 范围搜索：确定元素所在区间
#
# 应用场景：
# 1. 数据库查询：索引查找、范围扫描
# 2. 词典查找：单词搜索、自动补全
# 3. 调试工具：断点定位、符号查找

module SearchingAlgorithms
  # 线性搜索
  # 思路：从头到尾逐个遍历，找到目标元素
  # 时间复杂度：O(n)
  # 空间复杂度：O(1)
  def self.linear_search(array, target)
    array.each_with_index do |element, index|
      return index if element == target
    end
    -1
  end

  # 二分搜索（迭代版本）
  # 思路：在有序数组中，每次与中间元素比较，将搜索范围减半
  # 时间复杂度：O(log n)
  # 空间复杂度：O(1)
  def self.binary_search(array, target)
    left = 0
    right = array.length - 1

    while left <= right
      mid = left + (right - left) / 2
      if array[mid] == target
        return mid
      elsif array[mid] < target
        left = mid + 1
      else
        right = mid - 1
      end
    end
    -1
  end

  # 二分搜索（递归版本）
  # 思路：同迭代版本，使用递归实现
  def self.binary_search_recursive(array, target, left = 0, right = array.length - 1)
    return -1 if left > right

    mid = left + (right - left) / 2
    if array[mid] == target
      mid
    elsif array[mid] < target
      binary_search_recursive(array, target, mid + 1, right)
    else
      binary_search_recursive(array, target, left, mid - 1)
    end
  end

  # 找到第一个等于目标值的位置（lower_bound）
  # 思路：二分查找，即使找到目标也继续向左搜索
  # 时间复杂度：O(log n)
  def self.lower_bound(array, target)
    left = 0
    right = array.length

    while left < right
      mid = left + (right - left) / 2
      if array[mid] < target
        left = mid + 1
      else
        right = mid
      end
    end
    left
  end

  # 找到第一个大于目标值的位置（upper_bound）
  # 思路：二分查找，找到大于目标的第一个位置
  # 时间复杂度：O(log n)
  def self.upper_bound(array, target)
    left = 0
    right = array.length

    while left < right
      mid = left + (right - left) / 2
      if array[mid] <= target
        left = mid + 1
      else
        right = mid
      end
    end
    left
  end

  # 查找目标值的范围 [first, last]
  def self.search_range(array, target)
    first = lower_bound(array, target)
    return [-1, -1] if first == array.length || array[first] != target
    last = upper_bound(array, target) - 1
    [first, last]
  end

  # 跳跃搜索
  # 思路：以固定步长跳跃前进，在可能包含目标的块内进行线性搜索
  # 时间复杂度：O(√n)
  def self.jump_search(array, target)
    n = array.length
    step = Math.sqrt(n).to_i
    prev = 0

    # 找到目标所在的块
    while prev < n && array[[step, n].min - 1] < target
      prev = step
      step += Math.sqrt(n).to_i
      return -1 if prev >= n
    end

    # 在线性块中搜索
    while prev < [step, n].min
      return prev if array[prev] == target
      prev += 1
    end
    -1
  end

  # 指数搜索（适合无界数组或链表）
  # 思路：从索引1开始，每次扩大一倍，直到找到包含目标的区间，然后二分搜索
  # 时间复杂度：O(log n)
  def self.exponential_search(array, target)
    return -1 if array.empty?
    return 0 if array[0] == target

    i = 1
    i *= 2 while i < array.length && array[i] <= target

    left = i / 2
    right = [i, array.length - 1].min
    binary_search_range(array, target, left, right)
  end

  # 插值搜索（适合均匀分布的有序数组）
  # 思路：根据目标值估算其大致位置，而非直接取中点
  # 时间复杂度：平均 O(log log n)，最坏 O(n)
  def self.interpolation_search(array, target)
    left = 0
    right = array.length - 1

    while left <= right && target >= array[left] && target <= array[right]
      return left if left == right

      # 插值公式
      pos = left + ((target - array[left]) * (right - left) / (array[right] - array[left]))

      return pos if array[pos] == target

      if array[pos] < target
        left = pos + 1
      else
        right = pos - 1
      end
    end
    -1
  end

  # 斐波那契搜索
  # 思路：利用斐波那契数列的性质进行二分搜索
  # 时间复杂度：O(log n)
  def self.fibonacci_search(array, target)
    n = array.length
    fib2 = 0  # F(k-2)
    fib1 = 1  # F(k-1)
    fib = fib2 + fib1  # F(k)

    while fib < n
      fib2 = fib1
      fib1 = fib
      fib = fib2 + fib1
    end

    offset = -1

    while fib > 1
      i = [offset + fib2, n - 1].min

      if array[i] < target
        fib = fib1
        fib1 = fib2
        fib2 = fib - fib1
        offset = i
      elsif array[i] > target
        fib = fib2
        fib1 -= fib2
        fib2 = fib - fib1
      else
        return i
      end
    end

    return offset + 1 if fib1 == 1 && offset + 1 < n && array[offset + 1] == target
    -1
  end

  # 在旋转有序数组中搜索（无重复元素）
  # 思路：先确定有序的一半，再判断目标在哪一半
  # 时间复杂度：O(log n)
  def self.search_in_rotated_array(array, target)
    left = 0
    right = array.length - 1

    while left <= right
      mid = left + (right - left) / 2
      return mid if array[mid] == target

      # 判断哪一半是有序的
      if array[left] <= array[mid]  # 左半有序
        if array[left] <= target && target < array[mid]
          right = mid - 1
        else
          left = mid + 1
        end
      else  # 右半有序
        if array[mid] < target && target <= array[right]
          left = mid + 1
        else
          right = mid - 1
        end
      end
    end
    -1
  end

  # 在旋转有序数组中搜索（有重复元素）
  # 时间复杂度：O(log n)，最坏 O(n)
  def self.search_in_rotated_array_with_duplicates(array, target)
    left = 0
    right = array.length - 1

    while left <= right
      mid = left + (right - left) / 2
      return true if array[mid] == target

      # 处理重复元素的情况
      if array[left] == array[mid] && array[mid] == array[right]
        left += 1
        right -= 1
      elsif array[left] <= array[mid]
        if array[left] <= target && target < array[mid]
          right = mid - 1
        else
          left = mid + 1
        end
      else
        if array[mid] < target && target <= array[right]
          left = mid + 1
        else
          right = mid - 1
        end
      end
    end
    false
  end

  # 寻找旋转有序数组的最小值
  def self.find_min_in_rotated_array(array)
    left = 0
    right = array.length - 1

    while left < right
      mid = left + (right - left) / 2
      if array[mid] > array[right]
        left = mid + 1
      else
        right = mid
      end
    end
    array[left]
  end

  # 寻找峰值元素（大于相邻元素的元素）
  def self.find_peak_element(array)
    left = 0
    right = array.length - 1

    while left < right
      mid = left + (right - left) / 2
      if array[mid] < array[mid + 1]
        left = mid + 1
      else
        right = mid
      end
    end
    left
  end

  # 在二维有序矩阵中搜索（每行每列都递增）
  # 思路：从右上角开始，像走阶梯一样，大的向下，小的向左
  # 时间复杂度：O(m + n)
  def self.search_in_2d_matrix(matrix, target)
    return false if matrix.empty? || matrix[0].empty?

    rows = matrix.length
    cols = matrix[0].length
    row = 0
    col = cols - 1

    while row < rows && col >= 0
      if matrix[row][col] == target
        return [row, col]
      elsif matrix[row][col] < target
        row += 1
      else
        col -= 1
      end
    end
    nil
  end

  # 性能对比测试
  def self.benchmark(array, target)
    puts "搜索算法性能对比 (数组长度: #{array.length})"
    puts "-" * 55

    algorithms = {
      "线性搜索" => :linear_search,
      "二分搜索(迭代)" => :binary_search,
      "二分搜索(递归)" => :binary_search_recursive,
      "跳跃搜索" => :jump_search,
      "指数搜索" => :exponential_search,
      "插值搜索" => :interpolation_search,
      "斐波那契搜索" => :fibonacci_search
    }

    sorted = array.sort
    algorithms.each do |name, method|
      start = Time.now
      1000.times { send(method, sorted, target) }
      elapsed = (Time.now - start) * 1000
      puts "#{name.ljust(15)}: #{elapsed.round(4)}ms"
    end
    puts "-" * 55
  end

  private

  # 指定范围的二分搜索
  def self.binary_search_range(array, target, left, right)
    while left <= right
      mid = left + (right - left) / 2
      return mid if array[mid] == target
      if array[mid] < target
        left = mid + 1
      else
        right = mid - 1
      end
    end
    -1
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== 搜索算法演示 ==="

  sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
  puts "有序数组: #{sorted_array}"
  puts

  # 基本搜索
  target = 11
  puts "搜索目标: #{target}"
  puts "线性搜索: 索引 #{SearchingAlgorithms.linear_search(sorted_array, target)}"
  puts "二分搜索: 索引 #{SearchingAlgorithms.binary_search(sorted_array, target)}"
  puts "跳跃搜索: 索引 #{SearchingAlgorithms.jump_search(sorted_array, target)}"
  puts "插值搜索: 索引 #{SearchingAlgorithms.interpolation_search(sorted_array, target)}"
  puts "斐波那契搜索: 索引 #{SearchingAlgorithms.fibonacci_search(sorted_array, target)}"

  # 边界搜索
  puts "\n=== 边界搜索 ==="
  dup_array = [1, 2, 2, 2, 3, 3, 5, 5, 5, 7]
  puts "含重复元素的数组: #{dup_array}"
  puts "lower_bound(3): #{SearchingAlgorithms.lower_bound(dup_array, 3)}"
  puts "upper_bound(3): #{SearchingAlgorithms.upper_bound(dup_array, 3)}"
  puts "search_range(5): #{SearchingAlgorithms.search_range(dup_array, 5)}"

  # 旋转数组搜索
  puts "\n=== 旋转数组搜索 ==="
  rotated = [4, 5, 6, 7, 0, 1, 2]
  puts "旋转数组: #{rotated}"
  puts "搜索0: 索引 #{SearchingAlgorithms.search_in_rotated_array(rotated, 0)}"
  puts "最小值: #{SearchingAlgorithms.find_min_in_rotated_array(rotated)}"

  # 二维矩阵搜索
  puts "\n=== 二维矩阵搜索 ==="
  matrix = [
    [1, 4, 7, 11],
    [2, 5, 8, 12],
    [3, 6, 9, 16],
    [10, 13, 14, 17]
  ]
  puts "搜索5: #{SearchingAlgorithms.search_in_2d_matrix(matrix, 5)}"
  puts "搜索15: #{SearchingAlgorithms.search_in_2d_matrix(matrix, 15).inspect}"

  # 性能对比
  puts "\n=== 性能对比 ==="
  test_array = (1..100000).to_a
  SearchingAlgorithms.benchmark(test_array, 77777)
end
