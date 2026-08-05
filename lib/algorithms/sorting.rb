# encoding: utf-8
# 排序算法集合
#
# 思路：
# 排序是计算机科学中最基础的算法之一，不同的排序算法适用于不同的场景。
# 本模块包含了常见的比较排序和非比较排序算法，每种算法都有其独特的优势和局限。
#
# 作用：
# 1. 数据组织：将无序数据变为有序，便于后续处理
# 2. 搜索加速：有序数据可以支持二分查找等高效搜索
# 3. 数据分析：排序是许多统计和数据挖掘算法的基础
# 4. 用户界面：列表展示、排行榜等功能的核心
#
# 应用场景：
# 1. 数据库：索引构建、查询优化
# 2. 搜索引擎：结果排序、相关性排序
# 3. 电商系统：价格排序、销量排序
# 4. 金融系统：交易记录排序、风险排序

module SortingAlgorithms
  # ==================== 比较排序（O(n²)） ====================

  # 冒泡排序
  # 思路：重复遍历数组，比较相邻元素并交换，将最大元素"冒泡"到末尾
  # 时间复杂度：O(n²)，最好 O(n)，最坏 O(n²)
  # 空间复杂度：O(1)
  # 稳定性：稳定
  def self.bubble_sort(array)
    arr = array.dup
    n = arr.length
    (0...n - 1).each do |i|
      swapped = false
      (0...n - 1 - i).each do |j|
        if arr[j] > arr[j + 1]
          arr[j], arr[j + 1] = arr[j + 1], arr[j]
          swapped = true
        end
      end
      break unless swapped
    end
    arr
  end

  # 选择排序
  # 思路：每次从未排序部分找出最小元素，放到已排序部分的末尾
  # 时间复杂度：O(n²)，所有情况相同
  # 空间复杂度：O(1)
  # 稳定性：不稳定
  def self.selection_sort(array)
    arr = array.dup
    n = arr.length
    (0...n - 1).each do |i|
      min_idx = i
      (i + 1...n).each do |j|
        min_idx = j if arr[j] < arr[min_idx]
      end
      arr[i], arr[min_idx] = arr[min_idx], arr[i] if min_idx != i
    end
    arr
  end

  # 插入排序
  # 思路：将未排序元素逐个插入到已排序部分的正确位置
  # 时间复杂度：O(n²)，最好 O(n)，最坏 O(n²)
  # 空间复杂度：O(1)
  # 稳定性：稳定
  def self.insertion_sort(array)
    arr = array.dup
    n = arr.length
    (1...n).each do |i|
      key = arr[i]
      j = i - 1
      while j >= 0 && arr[j] > key
        arr[j + 1] = arr[j]
        j -= 1
      end
      arr[j + 1] = key
    end
    arr
  end

  # 希尔排序
  # 思路：插入排序的改进版，通过比较间隔一定距离的元素来工作
  # 时间复杂度：O(n log² n) ~ O(n^(3/2))
  # 空间复杂度：O(1)
  # 稳定性：不稳定
  def self.shell_sort(array)
    arr = array.dup
    n = arr.length
    gap = n / 2
    while gap > 0
      (gap...n).each do |i|
        temp = arr[i]
        j = i
        while j >= gap && arr[j - gap] > temp
          arr[j] = arr[j - gap]
          j -= gap
        end
        arr[j] = temp
      end
      gap /= 2
    end
    arr
  end

  # ==================== 比较排序（O(n log n)） ====================

  # 归并排序
  # 思路：分治策略，将数组递归分成两半，排序后合并
  # 时间复杂度：O(n log n)，所有情况相同
  # 空间复杂度：O(n)
  # 稳定性：稳定
  def self.merge_sort(array)
    return array.dup if array.length <= 1

    arr = array.dup
    merge_sort_helper(arr, 0, arr.length - 1)
    arr
  end

  # 快速排序
  # 思路：分治策略，选择一个基准元素（pivot），将小于基准的放左边，大于的放右边
  # 时间复杂度：平均 O(n log n)，最坏 O(n²)
  # 空间复杂度：O(log n)（递归栈）
  # 稳定性：不稳定
  def self.quick_sort(array)
    return array.dup if array.length <= 1

    arr = array.dup
    quick_sort_helper(arr, 0, arr.length - 1)
    arr
  end

  # 三路快速排序（优化重复元素场景）
  # 思路：将数组分为小于、等于、大于基准三部分，避免重复元素导致的性能退化
  def self.quick_sort_3way(array)
    return array.dup if array.length <= 1

    arr = array.dup
    quick_sort_3way_helper(arr, 0, arr.length - 1)
    arr
  end

  # 堆排序
  # 思路：利用最大堆的性质，每次取出堆顶元素放到数组末尾
  # 时间复杂度：O(n log n)，所有情况相同
  # 空间复杂度：O(1)
  # 稳定性：不稳定
  def self.heap_sort(array)
    arr = array.dup
    n = arr.length

    # 构建最大堆
    (n / 2 - 1).downto(0) do |i|
      heapify(arr, n, i)
    end

    # 逐个提取元素
    (n - 1).downto(1) do |i|
      arr[0], arr[i] = arr[i], arr[0]
      heapify(arr, i, 0)
    end
    arr
  end

  # ==================== 非比较排序（O(n + k)） ====================

  # 计数排序
  # 思路：统计每个元素出现的次数，适合整数且范围不大的场景
  # 时间复杂度：O(n + k)，k 为值的范围
  # 空间复杂度：O(k)
  # 稳定性：稳定（从后向前遍历版本）
  def self.counting_sort(array)
    return array.dup if array.empty?

    arr = array.dup
    min_val = arr.min
    max_val = arr.max
    range = max_val - min_val + 1

    # 统计计数
    count = Array.new(range, 0)
    arr.each { |num| count[num - min_val] += 1 }

    # 累加计数（用于确定位置）
    (1...range).each { |i| count[i] += count[i - 1] }

    # 从后向前遍历，保证稳定性
    output = Array.new(arr.length)
    (arr.length - 1).downto(0) do |i|
      idx = count[arr[i] - min_val] - 1
      output[idx] = arr[i]
      count[arr[i] - min_val] -= 1
    end
    output
  end

  # 桶排序
  # 思路：将元素分布到多个桶中，每个桶内排序后合并
  # 时间复杂度：平均 O(n + k)，最坏 O(n²)
  # 空间复杂度：O(n + k)
  # 稳定性：依赖内部排序算法
  def self.bucket_sort(array, bucket_size = 5)
    return array.dup if array.empty?

    arr = array.dup
    min_val = arr.min
    max_val = arr.max
    bucket_count = ((max_val - min_val) / bucket_size).floor + 1

    # 创建桶
    buckets = Array.new(bucket_count) { [] }
    arr.each do |num|
      idx = ((num - min_val) / bucket_size).floor
      buckets[idx] << num
    end

    # 对每个桶排序并合并
    result = []
    buckets.each do |bucket|
      result.concat(bucket.sort) unless bucket.empty?
    end
    result
  end

  # 基数排序（LSD）
  # 思路：从最低位开始，逐位排序，适合整数和字符串
  # 时间复杂度：O(d * (n + k))，d 为位数
  # 空间复杂度：O(n + k)
  # 稳定性：稳定
  def self.radix_sort(array)
    return array.dup if array.empty?

    arr = array.dup
    max_val = arr.max

    # 从个位开始，对每一位进行计数排序
    exp = 1
    while max_val / exp > 0
      arr = counting_sort_by_digit(arr, exp)
      exp *= 10
    end
    arr
  end

  # ==================== 特殊排序 ====================

  # 鸡尾酒排序（双向冒泡排序）
  # 思路：冒泡排序的变体，先从左到右冒泡，再从右到左冒泡
  # 时间复杂度：O(n²)，最好 O(n)
  # 空间复杂度：O(1)
  # 稳定性：稳定
  def self.cocktail_sort(array)
    arr = array.dup
    n = arr.length
    swapped = true
    start = 0
    finish = n - 1

    while swapped
      swapped = false

      # 从左到右
      (start...finish).each do |i|
        if arr[i] > arr[i + 1]
          arr[i], arr[i + 1] = arr[i + 1], arr[i]
          swapped = true
        end
      end
      break unless swapped
      swapped = false
      finish -= 1

      # 从右到左
      (finish - 1).downto(start) do |i|
        if arr[i] > arr[i + 1]
          arr[i], arr[i + 1] = arr[i + 1], arr[i]
          swapped = true
        end
      end
      start += 1
    end
    arr
  end

  # Timsort 风格的简单归并插入排序
  # 思路：结合插入排序和归并排序的混合排序（简化版）
  def self.tim_sort(array, run = 32)
    arr = array.dup
    n = arr.length

    # 对每个小块使用插入排序
    (0...n).step(run) do |start_idx|
      end_idx = [start_idx + run - 1, n - 1].min
      insertion_sort_range(arr, start_idx, end_idx)
    end

    # 归并所有小块
    size = run
    while size < n
      (0...n).step(size * 2) do |left|
        mid = [left + size - 1, n - 1].min
        right = [left + size * 2 - 1, n - 1].min
        merge_range(arr, left, mid, right) if mid < right
      end
      size *= 2
    end
    arr
  end

  # ==================== 工具方法 ====================

  # 检查数组是否已排序
  def self.sorted?(array)
    (0...array.length - 1).each do |i|
      return false if array[i] > array[i + 1]
    end
    true
  end

  # 原地反转数组
  def self.reverse!(array)
    left = 0
    right = array.length - 1
    while left < right
      array[left], array[right] = array[right], array[left]
      left += 1
      right -= 1
    end
    array
  end

  # 部分排序（找到第 k 小的元素）
  def self.partial_sort(array, k)
    return [] if k <= 0 || array.empty?
    return array.sort.first(k) if k >= array.length

    arr = array.dup
    quick_select_partial(arr, 0, arr.length - 1, k)
    arr[0...k].sort
  end

  # 查找第 k 大的元素（快速选择算法）
  def self.quick_select(array, k)
    return nil if k <= 0 || k > array.length
    arr = array.dup
    quick_select_helper(arr, 0, arr.length - 1, k - 1)
  end

  # 生成随机数组
  def self.random_array(size, min = 0, max = 1000)
    Array.new(size) { rand(min..max) }
  end

  # 生成近乎有序的数组（用于测试）
  def self.nearly_sorted_array(size, swaps = 5)
    arr = (1..size).to_a
    swaps.times do
      i = rand(size)
      j = rand(size)
      arr[i], arr[j] = arr[j], arr[i]
    end
    arr
  end

  # 性能对比测试
  def self.benchmark(array, algorithms = nil)
    algorithms ||= %w[bubble_sort selection_sort insertion_sort shell_sort
                      merge_sort quick_sort quick_sort_3way heap_sort
                      counting_sort bucket_sort radix_sort]

    results = {}
    puts "排序算法性能对比 (数组长度: #{array.length})"
    puts "-" * 55
    puts "算法名称".ljust(25) + "耗时(ms)".rjust(15) + "是否稳定".rjust(12)
    puts "-" * 55

    algorithms.each do |algo_name|
      begin
        start = Time.now
        result = send(algo_name, array)
        elapsed = (Time.now - start) * 1000
        stable = result == send(algo_name, array.sort)
        results[algo_name] = { time: elapsed, stable: stable }
        puts algo_name.ljust(25) + elapsed.round(3).to_s.rjust(15) + stable.to_s.rjust(12)
      rescue => e
        puts algo_name.ljust(25) + "ERROR".rjust(15)
      end
    end
    results
  end

  private

  # 归并排序辅助方法
  def self.merge_sort_helper(arr, left, right)
    return if left >= right

    mid = left + (right - left) / 2
    merge_sort_helper(arr, left, mid)
    merge_sort_helper(arr, mid + 1, right)
    merge_range(arr, left, mid, right)
  end

  def self.merge_range(arr, left, mid, right)
    left_arr = arr[left..mid]
    right_arr = arr[mid + 1..right]
    i = 0
    j = 0
    k = left

    while i < left_arr.length && j < right_arr.length
      if left_arr[i] <= right_arr[j]
        arr[k] = left_arr[i]
        i += 1
      else
        arr[k] = right_arr[j]
        j += 1
      end
      k += 1
    end

    while i < left_arr.length
      arr[k] = left_arr[i]
      i += 1
      k += 1
    end

    while j < right_arr.length
      arr[k] = right_arr[j]
      j += 1
      k += 1
    end
  end

  # 快速排序辅助方法
  def self.quick_sort_helper(arr, low, high)
    return if low >= high

    pi = partition(arr, low, high)
    quick_sort_helper(arr, low, pi - 1)
    quick_sort_helper(arr, pi + 1, high)
  end

  def self.partition(arr, low, high)
    # 三数取中法选择基准
    mid = low + (high - low) / 2
    if arr[low] > arr[mid]
      arr[low], arr[mid] = arr[mid], arr[low]
    end
    if arr[low] > arr[high]
      arr[low], arr[high] = arr[high], arr[low]
    end
    if arr[mid] > arr[high]
      arr[mid], arr[high] = arr[high], arr[mid]
    end
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]

    pivot = arr[high - 1]
    i = low
    (low...high - 1).each do |j|
      if arr[j] <= pivot
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
      end
    end
    arr[i], arr[high - 1] = arr[high - 1], arr[i]
    i
  end

  # 三路快排辅助方法
  def self.quick_sort_3way_helper(arr, low, high)
    return if low >= high

    lt, gt = partition_3way(arr, low, high)
    quick_sort_3way_helper(arr, low, lt - 1)
    quick_sort_3way_helper(arr, gt + 1, high)
  end

  def self.partition_3way(arr, low, high)
    pivot = arr[low]
    lt = low
    i = low + 1
    gt = high

    while i <= gt
      if arr[i] < pivot
        arr[lt], arr[i] = arr[i], arr[lt]
        lt += 1
        i += 1
      elsif arr[i] > pivot
        arr[i], arr[gt] = arr[gt], arr[i]
        gt -= 1
      else
        i += 1
      end
    end
    [lt, gt]
  end

  # 堆排序辅助方法
  def self.heapify(arr, n, i)
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    largest = left if left < n && arr[left] > arr[largest]
    largest = right if right < n && arr[right] > arr[largest]

    return if largest == i

    arr[i], arr[largest] = arr[largest], arr[i]
    heapify(arr, n, largest)
  end

  # 基数排序辅助方法：按指定位数排序
  def self.counting_sort_by_digit(arr, exp)
    n = arr.length
    output = Array.new(n)
    count = Array.new(10, 0)

    arr.each { |num| count[(num / exp) % 10] += 1 }
    (1...10).each { |i| count[i] += count[i - 1] }

    (n - 1).downto(0) do |i|
      digit = (arr[i] / exp) % 10
      output[count[digit] - 1] = arr[i]
      count[digit] -= 1
    end
    output
  end

  # Timsort辅助：对指定范围进行插入排序
  def self.insertion_sort_range(arr, left, right)
    (left + 1..right).each do |i|
      key = arr[i]
      j = i - 1
      while j >= left && arr[j] > key
        arr[j + 1] = arr[j]
        j -= 1
      end
      arr[j + 1] = key
    end
  end

  # 快速选择辅助方法
  def self.quick_select_helper(arr, low, high, k)
    return arr[low] if low == high

    pi = partition(arr, low, high)
    if pi == k
      arr[pi]
    elsif pi > k
      quick_select_helper(arr, low, pi - 1, k)
    else
      quick_select_helper(arr, pi + 1, high, k)
    end
  end

  def self.quick_select_partial(arr, low, high, k)
    return if low >= high

    pi = partition(arr, low, high)
    if pi > k
      quick_select_partial(arr, low, pi - 1, k)
    elsif pi < k
      quick_select_partial(arr, pi + 1, high, k)
    end
  end
end

# 使用示例和性能测试
if __FILE__ == $0
  puts "=== 排序算法演示 ==="

  # 测试数据
  small_array = [64, 34, 25, 12, 22, 11, 90]
  puts "原始数组: #{small_array}"
  puts

  # 各种排序算法
  algorithms = {
    "冒泡排序" => :bubble_sort,
    "选择排序" => :selection_sort,
    "插入排序" => :insertion_sort,
    "希尔排序" => :shell_sort,
    "归并排序" => :merge_sort,
    "快速排序" => :quick_sort,
    "三路快排" => :quick_sort_3way,
    "堆排序" => :heap_sort,
    "计数排序" => :counting_sort,
    "桶排序" => :bucket_sort,
    "基数排序" => :radix_sort,
    "鸡尾酒排序" => :cocktail_sort,
    "Tim排序" => :tim_sort
  }

  algorithms.each do |name, method|
    result = SortingAlgorithms.send(method, small_array)
    puts "#{name.ljust(10)}: #{result}"
  end

  puts "\n=== 特殊功能 ==="
  puts "是否已排序: #{SortingAlgorithms.sorted?(small_array.sort)}"
  puts "第3小的元素: #{SortingAlgorithms.quick_select(small_array, 3)}"
  puts "前3小的元素: #{SortingAlgorithms.partial_sort(small_array, 3)}"

  puts "\n=== 近乎有序的数组排序 ==="
  nearly = SortingAlgorithms.nearly_sorted_array(10, 3)
  puts "近乎有序: #{nearly}"
  puts "插入排序后: #{SortingAlgorithms.insertion_sort(nearly)}"

  puts "\n=== 大规模性能对比 ==="
  test_array = SortingAlgorithms.random_array(5000)
  SortingAlgorithms.benchmark(test_array)
end
