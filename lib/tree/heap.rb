# 堆 (Heap) 实现
# 
# 思路：
# 堆是一种特殊的完全二叉树，满足堆性质：
# - 最大堆：父节点的值大于或等于其子节点的值
# - 最小堆：父节点的值小于或等于其子节点的值
# 通常用数组来实现，利用完全二叉树的性质进行索引计算
# 
# 作用：
# 1. 优先队列：高效的插入和删除最值操作
# 2. 堆排序：原地排序算法
# 3. 图算法：Dijkstra算法、Prim算法
# 4. 任务调度：操作系统的进程调度
# 
# 应用场景：
# 1. 操作系统：进程调度、内存管理
# 2. 数据库：查询优化、索引维护
# 3. 网络算法：最短路径、最小生成树
# 4. 实时系统：事件调度、定时器
# 5. 数据分析：Top-K问题、中位数维护
# 6. 游戏开发：AI决策、路径规划

# 最大堆实现
class MaxHeap
  attr_reader :size

  def initialize(array = [])
    @heap = []
    @size = 0
    
    # 如果提供了数组，使用heapify构建堆
    unless array.empty?
      @heap = array.dup
      @size = array.length
      heapify
    end
  end

  # 插入元素
  # 时间复杂度：O(log n)
  def insert(value)
    @heap[@size] = value
    @size += 1
    heapify_up(@size - 1)
    self
  end
  alias_method :push, :insert
  alias_method :<<, :insert

  # 删除并返回最大元素
  # 时间复杂度：O(log n)
  def extract_max
    raise RuntimeError, "Heap is empty" if empty?
    
    max_value = @heap[0]
    @size -= 1
    
    if @size > 0
      @heap[0] = @heap[@size]
      @heap[@size] = nil
      heapify_down(0)
    else
      @heap[0] = nil
    end
    
    max_value
  end
  alias_method :pop, :extract_max

  # 查看最大元素（不删除）
  # 时间复杂度：O(1)
  def peek
    raise RuntimeError, "Heap is empty" if empty?
    @heap[0]
  end
  alias_method :max, :peek
  alias_method :top, :peek

  # 检查堆是否为空
  def empty?
    @size == 0
  end

  # 清空堆
  def clear
    @heap.clear
    @size = 0
    self
  end

  # 增加指定位置元素的值
  # 时间复杂度：O(log n)
  def increase_key(index, new_value)
    raise IndexError, "Index out of bounds" if index < 0 || index >= @size
    raise ArgumentError, "New value must be greater than current value" if new_value < @heap[index]
    
    @heap[index] = new_value
    heapify_up(index)
    self
  end

  # 删除指定位置的元素
  # 时间复杂度：O(log n)
  def delete_at(index)
    raise IndexError, "Index out of bounds" if index < 0 || index >= @size
    
    deleted_value = @heap[index]
    @size -= 1
    
    if index == @size
      @heap[index] = nil
    else
      @heap[index] = @heap[@size]
      @heap[@size] = nil
      
      # 可能需要向上或向下调整
      parent_index = parent(index)
      if parent_index >= 0 && @heap[index] > @heap[parent_index]
        heapify_up(index)
      else
        heapify_down(index)
      end
    end
    
    deleted_value
  end

  # 替换堆顶元素
  # 时间复杂度：O(log n)
  def replace(new_value)
    raise RuntimeError, "Heap is empty" if empty?
    
    old_value = @heap[0]
    @heap[0] = new_value
    heapify_down(0)
    old_value
  end

  # 合并两个堆
  def merge(other_heap)
    new_heap = MaxHeap.new
    combined_array = to_a + other_heap.to_a
    new_heap.instance_variable_set(:@heap, combined_array)
    new_heap.instance_variable_set(:@size, combined_array.length)
    new_heap.heapify
    new_heap
  end

  # 转换为数组
  def to_a
    @heap[0, @size]
  end

  # 转换为有序数组（堆排序）
  # 时间复杂度：O(n log n)
  def to_sorted_array
    sorted = []
    temp_heap = MaxHeap.new(to_a)
    
    while !temp_heap.empty?
      sorted.unshift(temp_heap.extract_max)
    end
    
    sorted
  end

  # 验证堆性质
  def valid_heap?(index = 0)
    return true if index >= @size
    
    left_child = left_child_index(index)
    right_child = right_child_index(index)
    
    # 检查左子节点
    if left_child < @size && @heap[index] < @heap[left_child]
      return false
    end
    
    # 检查右子节点
    if right_child < @size && @heap[index] < @heap[right_child]
      return false
    end
    
    # 递归检查子树
    valid_heap?(left_child) && valid_heap?(right_child)
  end

  # 获取堆的高度
  def height
    return -1 if empty?
    Math.log2(@size).floor
  end

  # 迭代器（层序遍历）
  def each
    return enum_for(:each) unless block_given?
    
    0.upto(@size - 1) do |i|
      yield @heap[i]
    end
    self
  end

  # 字符串表示
  def to_s
    "MaxHeap[#{to_a.join(', ')}] (max: #{empty? ? 'empty' : peek})"
  end

  def inspect
    "#<MaxHeap:#{object_id} size=#{@size} max=#{empty? ? 'nil' : peek.inspect}>"
  end

  protected

  # 从数组构建堆（自底向上）
  # 时间复杂度：O(n)
  def heapify
    # 从最后一个非叶子节点开始向上调整
    ((@size / 2) - 1).downto(0) do |i|
      heapify_down(i)
    end
  end

  private

  # 向上调整（用于插入）
  def heapify_up(index)
    parent_index = parent(index)
    
    while index > 0 && @heap[index] > @heap[parent_index]
      swap(index, parent_index)
      index = parent_index
      parent_index = parent(index)
    end
  end

  # 向下调整（用于删除）
  def heapify_down(index)
    while true
      largest = index
      left = left_child_index(index)
      right = right_child_index(index)
      
      # 找到最大的节点
      if left < @size && @heap[left] > @heap[largest]
        largest = left
      end
      
      if right < @size && @heap[right] > @heap[largest]
        largest = right
      end
      
      # 如果当前节点已经是最大的，停止调整
      break if largest == index
      
      swap(index, largest)
      index = largest
    end
  end

  # 交换两个元素
  def swap(i, j)
    @heap[i], @heap[j] = @heap[j], @heap[i]
  end

  # 获取父节点索引
  def parent(index)
    (index - 1) / 2
  end

  # 获取左子节点索引
  def left_child_index(index)
    2 * index + 1
  end

  # 获取右子节点索引
  def right_child_index(index)
    2 * index + 2
  end
end

# 最小堆实现
class MinHeap < MaxHeap
  # 插入元素
  def insert(value)
    @heap[@size] = value
    @size += 1
    heapify_up(@size - 1)
    self
  end

  # 删除并返回最小元素
  def extract_min
    raise RuntimeError, "Heap is empty" if empty?
    
    min_value = @heap[0]
    @size -= 1
    
    if @size > 0
      @heap[0] = @heap[@size]
      @heap[@size] = nil
      heapify_down(0)
    else
      @heap[0] = nil
    end
    
    min_value
  end
  alias_method :pop, :extract_min

  # 查看最小元素
  def peek
    raise RuntimeError, "Heap is empty" if empty?
    @heap[0]
  end
  alias_method :min, :peek
  alias_method :top, :peek

  # 减少指定位置元素的值
  def decrease_key(index, new_value)
    raise IndexError, "Index out of bounds" if index < 0 || index >= @size
    raise ArgumentError, "New value must be less than current value" if new_value > @heap[index]
    
    @heap[index] = new_value
    heapify_up(index)
    self
  end

  # 转换为有序数组（堆排序）
  def to_sorted_array
    sorted = []
    temp_heap = MinHeap.new(to_a)
    
    while !temp_heap.empty?
      sorted << temp_heap.extract_min
    end
    
    sorted
  end

  # 验证最小堆性质
  def valid_heap?(index = 0)
    return true if index >= @size
    
    left_child = left_child_index(index)
    right_child = right_child_index(index)
    
    # 检查左子节点
    if left_child < @size && @heap[index] > @heap[left_child]
      return false
    end
    
    # 检查右子节点
    if right_child < @size && @heap[index] > @heap[right_child]
      return false
    end
    
    # 递归检查子树
    valid_heap?(left_child) && valid_heap?(right_child)
  end

  def to_s
    "MinHeap[#{to_a.join(', ')}] (min: #{empty? ? 'empty' : peek})"
  end

  private

  # 向上调整（最小堆版本）
  def heapify_up(index)
    parent_index = parent(index)
    
    while index > 0 && @heap[index] < @heap[parent_index]
      swap(index, parent_index)
      index = parent_index
      parent_index = parent(index)
    end
  end

  # 向下调整（最小堆版本）
  def heapify_down(index)
    while true
      smallest = index
      left = left_child_index(index)
      right = right_child_index(index)
      
      # 找到最小的节点
      if left < @size && @heap[left] < @heap[smallest]
        smallest = left
      end
      
      if right < @size && @heap[right] < @heap[smallest]
        smallest = right
      end
      
      # 如果当前节点已经是最小的，停止调整
      break if smallest == index
      
      swap(index, smallest)
      index = smallest
    end
  end
end

# 堆的实际应用示例
module HeapApplications
  # 优先队列实现
  class PriorityQueue
    def initialize(type = :max)
      @heap = type == :max ? MaxHeap.new : MinHeap.new
      @type = type
    end

    def enqueue(item, priority = item)
      # 对于最大堆，优先级高的值大；对于最小堆，优先级高的值小
      element = @type == :max ? priority : -priority
      @heap.insert([element, item])
      self
    end

    def dequeue
      return nil if empty?
      
      priority, item = @heap.pop
      item
    end

    def peek
      return nil if empty?
      
      priority, item = @heap.peek
      item
    end

    def empty?
      @heap.empty?
    end

    def size
      @heap.size
    end

    def to_s
      "PriorityQueue(#{@type})[size: #{size}]"
    end
  end

  # Top-K 问题解决器
  class TopK
    def initialize(k)
      @k = k
      @min_heap = MinHeap.new
    end

    def add(value)
      if @min_heap.size < @k
        @min_heap.insert(value)
      elsif value > @min_heap.peek
        @min_heap.replace(value)
      end
      self
    end

    def top_k
      @min_heap.to_a.sort.reverse
    end

    def kth_largest
      @min_heap.empty? ? nil : @min_heap.peek
    end
  end

  # 中位数维护器
  class MedianFinder
    def initialize
      @max_heap = MaxHeap.new  # 存储较小的一半
      @min_heap = MinHeap.new  # 存储较大的一半
    end

    def add_number(num)
      # 如果最大堆为空或者数字小于等于最大堆的最大值，加入最大堆
      if @max_heap.empty? || num <= @max_heap.peek
        @max_heap.insert(num)
      else
        @min_heap.insert(num)
      end

      # 平衡两个堆的大小
      balance_heaps
      self
    end

    def find_median
      return nil if @max_heap.empty? && @min_heap.empty?

      if @max_heap.size > @min_heap.size
        @max_heap.peek.to_f
      elsif @min_heap.size > @max_heap.size
        @min_heap.peek.to_f
      else
        (@max_heap.peek + @min_heap.peek) / 2.0
      end
    end

    def size
      @max_heap.size + @min_heap.size
    end

    private

    def balance_heaps
      # 确保两个堆的大小差不超过1
      if @max_heap.size > @min_heap.size + 1
        @min_heap.insert(@max_heap.extract_max)
      elsif @min_heap.size > @max_heap.size + 1
        @max_heap.insert(@min_heap.extract_min)
      end
    end
  end

  # 堆排序实现
  def self.heap_sort(array)
    return array if array.length <= 1
    
    # 构建最大堆
    heap = MaxHeap.new(array)
    
    # 依次取出最大元素
    sorted = []
    while !heap.empty?
      sorted.unshift(heap.extract_max)
    end
    
    sorted
  end

  # 原地堆排序
  def self.heap_sort_in_place(array)
    return array if array.length <= 1
    
    n = array.length
    
    # 构建最大堆
    ((n / 2) - 1).downto(0) do |i|
      heapify_down(array, n, i)
    end
    
    # 依次将最大元素移到数组末尾
    (n - 1).downto(1) do |i|
      array[0], array[i] = array[i], array[0]
      heapify_down(array, i, 0)
    end
    
    array
  end

  private

  def self.heapify_down(array, heap_size, index)
    while true
      largest = index
      left = 2 * index + 1
      right = 2 * index + 2
      
      if left < heap_size && array[left] > array[largest]
        largest = left
      end
      
      if right < heap_size && array[right] > array[largest]
        largest = right
      end
      
      break if largest == index
      
      array[index], array[largest] = array[largest], array[index]
      index = largest
    end
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== MaxHeap 使用示例 ==="
  
  # 创建最大堆
  max_heap = MaxHeap.new
  values = [4, 10, 3, 5, 1, 15, 20, 17]
  
  puts "插入值: #{values}"
  values.each { |val| max_heap.insert(val) }
  
  puts "最大堆: #{max_heap}"
  puts "堆顶元素: #{max_heap.peek}"
  puts "堆大小: #{max_heap.size}"
  puts "堆高度: #{max_heap.height}"
  puts "是否为有效堆: #{max_heap.valid_heap?}"
  
  puts "\n依次取出最大元素:"
  while !max_heap.empty?
    puts "取出: #{max_heap.extract_max}, 剩余: #{max_heap.to_a}"
  end
  
  puts "\n=== MinHeap 使用示例 ==="
  
  # 创建最小堆
  min_heap = MinHeap.new(values)
  puts "从数组构建最小堆: #{min_heap}"
  puts "堆顶元素: #{min_heap.peek}"
  puts "是否为有效堆: #{min_heap.valid_heap?}"
  
  puts "\n有序输出:"
  sorted = min_heap.to_sorted_array
  puts "排序结果: #{sorted}"
  
  puts "\n=== PriorityQueue 使用示例 ==="
  
  # 优先队列
  pq = HeapApplications::PriorityQueue.new(:max)
  
  pq.enqueue("任务A", 3)
  pq.enqueue("任务B", 1)
  pq.enqueue("任务C", 5)
  pq.enqueue("任务D", 2)
  
  puts "优先队列: #{pq}"
  puts "按优先级处理任务:"
  while !pq.empty?
    puts "  处理: #{pq.dequeue}"
  end
  
  puts "\n=== TopK 问题示例 ==="
  
  # Top-K 最大值
  top_k = HeapApplications::TopK.new(3)
  data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
  
  puts "数据流: #{data}"
  data.each { |val| top_k.add(val) }
  
  puts "Top-3 最大值: #{top_k.top_k}"
  puts "第3大的数: #{top_k.kth_largest}"
  
  puts "\n=== 中位数维护示例 ==="
  
  # 中位数查找器
  median_finder = HeapApplications::MedianFinder.new
  stream = [5, 15, 1, 3, 8, 7, 9, 2, 6]
  
  puts "数据流中位数变化:"
  stream.each do |num|
    median_finder.add_number(num)
    puts "添加 #{num}, 当前中位数: #{median_finder.find_median}"
  end
  
  puts "\n=== 堆排序示例 ==="
  
  unsorted = [64, 34, 25, 12, 22, 11, 90]
  puts "原数组: #{unsorted}"
  
  sorted1 = HeapApplications.heap_sort(unsorted.dup)
  puts "堆排序结果: #{sorted1}"
  
  sorted2 = HeapApplications.heap_sort_in_place(unsorted.dup)
  puts "原地堆排序结果: #{sorted2}"
  
  puts "\n=== 性能测试 ==="
  
  # 性能测试
  large_heap = MaxHeap.new
  test_data = (1..10000).to_a.shuffle
  
  start_time = Time.now
  test_data.each { |val| large_heap.insert(val) }
  end_time = Time.now
  
  puts "插入10000个元素耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  puts "堆大小: #{large_heap.size}"
  puts "堆高度: #{large_heap.height}"
  
  # 提取性能测试
  start_time = Time.now
  1000.times { large_heap.extract_max }
  end_time = Time.now
  
  puts "提取1000个最大元素耗时: #{((end_time - start_time) * 1000).round(2)}ms"
end