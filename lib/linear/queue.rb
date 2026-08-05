# 队列 (Queue) 实现
# 
# 思路：
# 队列是一种先进先出（FIFO - First In First Out）的线性数据结构。
# 在队尾进行插入操作（enqueue），在队头进行删除操作（dequeue）。
# 可以用数组、链表或循环数组作为底层实现。
# 
# 作用：
# 1. 任务调度：操作系统的进程调度
# 2. 缓冲区：数据流处理中的缓冲
# 3. 广度优先搜索：BFS算法的实现
# 4. 异步处理：消息队列、任务队列
# 5. 资源分配：打印队列、网络请求队列
# 
# 应用场景：
# 1. Web服务器：请求处理队列
# 2. 游戏开发：事件处理队列
# 3. 数据库：事务处理队列
# 4. 网络编程：数据包处理队列
# 5. 多线程编程：线程间通信
# 6. 实时系统：实时任务调度

# 基于数组的队列实现
class Queue
  attr_reader :size

  def initialize
    @items = []
    @front = 0
    @rear = 0
    @size = 0
  end

  # 入队操作
  # 时间复杂度：O(1)
  def enqueue(item)
    @items[@rear] = item
    @rear += 1
    @size += 1
    self
  end
  alias_method :<<, :enqueue
  alias_method :push, :enqueue

  # 出队操作
  # 时间复杂度：O(1)
  def dequeue
    raise RuntimeError, "Queue is empty" if empty?
    
    item = @items[@front]
    @items[@front] = nil  # 清除引用
    @front += 1
    @size -= 1
    
    # 重置索引以节省空间
    if empty?
      @front = @rear = 0
    end
    
    item
  end
  alias_method :shift, :dequeue

  # 查看队头元素（不删除）
  # 时间复杂度：O(1)
  def front
    raise RuntimeError, "Queue is empty" if empty?
    @items[@front]
  end
  alias_method :peek, :front

  # 查看队尾元素（不删除）
  # 时间复杂度：O(1)
  def rear
    raise RuntimeError, "Queue is empty" if empty?
    @items[@rear - 1]
  end
  alias_method :back, :rear

  # 检查队列是否为空
  def empty?
    @size == 0
  end

  # 清空队列
  def clear
    @items.clear
    @front = @rear = 0
    @size = 0
    self
  end

  # 转换为数组
  def to_a
    @items[@front, @size]
  end

  # 迭代器（从队头到队尾）
  def each
    return enum_for(:each) unless block_given?
    
    @front.upto(@rear - 1) do |i|
      yield @items[i]
    end
    self
  end

  # 字符串表示
  def to_s
    "Queue[#{to_a.join(', ')}] (front: #{empty? ? 'empty' : front}, rear: #{empty? ? 'empty' : rear})"
  end

  def inspect
    "#<Queue:#{object_id} size=#{@size} front=#{empty? ? 'nil' : front.inspect} rear=#{empty? ? 'nil' : rear.inspect}>"
  end
end

# 循环队列实现（固定大小，空间效率更高）
class CircularQueue
  attr_reader :size, :capacity

  def initialize(capacity = 10)
    @capacity = capacity
    @items = Array.new(@capacity)
    @front = 0
    @rear = 0
    @size = 0
  end

  # 入队操作
  # 时间复杂度：O(1)
  def enqueue(item)
    return false if full?

    @items[@rear] = item
    @rear = (@rear + 1) % @capacity
    @size += 1
    self
  end

  # 出队操作
  # 时间复杂度：O(1)
  def dequeue
    raise RuntimeError, "Queue is empty" if empty?
    
    item = @items[@front]
    @items[@front] = nil
    @front = (@front + 1) % @capacity
    @size -= 1
    item
  end

  # 查看队头元素
  def front
    raise RuntimeError, "Queue is empty" if empty?
    @items[@front]
  end

  # 查看队尾元素
  def rear
    raise RuntimeError, "Queue is empty" if empty?
    rear_index = (@rear - 1 + @capacity) % @capacity
    @items[rear_index]
  end

  # 检查是否为空
  def empty?
    @size == 0
  end

  # 检查是否已满
  def full?
    @size == @capacity
  end

  # 清空队列
  def clear
    @items.fill(nil)
    @front = @rear = 0
    @size = 0
    self
  end

  # 转换为数组
  def to_a
    result = []
    return result if empty?
    
    i = @front
    @size.times do
      result << @items[i]
      i = (i + 1) % @capacity
    end
    result
  end

  def to_s
    "CircularQueue[#{to_a.join(', ')}] (#{@size}/#{@capacity})"
  end
end

# 基于链表的队列实现
class LinkedQueue
  attr_reader :size

  # 队列节点
  class QueueNode
    attr_accessor :data, :next

    def initialize(data, next_node = nil)
      @data = data
      @next = next_node
    end
  end

  def initialize
    @front = nil
    @rear = nil
    @size = 0
  end

  # 入队操作
  # 时间复杂度：O(1)
  def enqueue(item)
    new_node = QueueNode.new(item)
    
    if @rear.nil?
      @front = @rear = new_node
    else
      @rear.next = new_node
      @rear = new_node
    end
    
    @size += 1
    self
  end

  # 出队操作
  # 时间复杂度：O(1)
  def dequeue
    raise RuntimeError, "Queue is empty" if empty?
    
    item = @front.data
    @front = @front.next
    
    if @front.nil?
      @rear = nil
    end
    
    @size -= 1
    item
  end

  # 查看队头元素
  def front
    raise RuntimeError, "Queue is empty" if empty?
    @front.data
  end

  # 查看队尾元素
  def rear
    raise RuntimeError, "Queue is empty" if empty?
    @rear.data
  end

  # 检查是否为空
  def empty?
    @front.nil?
  end

  # 清空队列
  def clear
    @front = @rear = nil
    @size = 0
    self
  end

  # 转换为数组
  def to_a
    result = []
    current = @front
    while current
      result << current.data
      current = current.next
    end
    result
  end

  def to_s
    "LinkedQueue[#{to_a.join(', ')}]"
  end
end

# 双端队列（Deque - Double Ended Queue）
class Deque
  attr_reader :size

  def initialize
    @items = []
    @size = 0
  end

  # 在前端添加元素
  def add_front(item)
    @items.unshift(item)
    @size += 1
    self
  end
  alias_method :prepend, :add_front

  # 在后端添加元素
  def add_rear(item)
    @items.push(item)
    @size += 1
    self
  end
  alias_method :append, :add_rear

  # 从前端删除元素
  def remove_front
    raise RuntimeError, "Deque is empty" if empty?
    @size -= 1
    @items.shift
  end

  # 从后端删除元素
  def remove_rear
    raise RuntimeError, "Deque is empty" if empty?
    @size -= 1
    @items.pop
  end

  # 查看前端元素
  def front
    raise RuntimeError, "Deque is empty" if empty?
    @items.first
  end

  # 查看后端元素
  def rear
    raise RuntimeError, "Deque is empty" if empty?
    @items.last
  end

  # 检查是否为空
  def empty?
    @size == 0
  end

  # 清空双端队列
  def clear
    @items.clear
    @size = 0
    self
  end

  def to_a
    @items.dup
  end

  def to_s
    "Deque[#{@items.join(', ')}]"
  end
end

# 优先队列实现
class PriorityQueue
  attr_reader :size

  def initialize(&comparator)
    @items = []
    @size = 0
    @compare = comparator || proc { |a, b| a <=> b }
  end

  # 入队（按优先级插入）
  # 时间复杂度：O(n)
  def enqueue(item, priority = item)
    element = { item: item, priority: priority }
    
    # 找到正确的插入位置
    insert_index = @size
    0.upto(@size - 1) do |i|
      if @compare.call(priority, @items[i][:priority]) < 0
        insert_index = i
        break
      end
    end
    
    @items.insert(insert_index, element)
    @size += 1
    self
  end

  # 出队（移除最高优先级元素）
  # 时间复杂度：O(1)
  def dequeue
    raise RuntimeError, "Priority queue is empty" if empty?
    
    @size -= 1
    @items.shift[:item]
  end

  # 查看最高优先级元素
  def peek
    raise RuntimeError, "Priority queue is empty" if empty?
    @items.first[:item]
  end

  # 检查是否为空
  def empty?
    @size == 0
  end

  # 清空队列
  def clear
    @items.clear
    @size = 0
    self
  end

  def to_s
    items_str = @items.map { |elem| "#{elem[:item]}(#{elem[:priority]})" }.join(', ')
    "PriorityQueue[#{items_str}]"
  end
end

# 队列的实际应用示例
module QueueApplications
  # 任务调度器
  class TaskScheduler
    def initialize
      @task_queue = Queue.new
      @running = false
    end

    def add_task(task)
      @task_queue.enqueue(task)
    end

    def start
      @running = true
      while @running && !@task_queue.empty?
        task = @task_queue.dequeue
        puts "执行任务: #{task}"
        # 模拟任务执行
        sleep(0.1)
      end
    end

    def stop
      @running = false
    end

    def pending_tasks
      @task_queue.size
    end

    def has_tasks?
      !@task_queue.empty?
    end

    def next_task
      @task_queue.dequeue
    end
  end

  # 简单的缓冲区实现
  class Buffer
    def initialize(capacity = 10)
      @buffer = CircularQueue.new(capacity)
      @capacity = capacity
    end

    def write(data)
      if @buffer.full?
        puts "缓冲区已满，丢弃最旧数据"
        @buffer.dequeue
      end
      @buffer.enqueue(data)
    end

    def read
      return nil if @buffer.empty?
      @buffer.dequeue
    end

    def available_data
      @buffer.size
    end

    def to_s
      "Buffer: #{@buffer.to_a}"
    end
  end

  # 广度优先搜索示例
  def self.bfs_tree_traversal(root)
    return [] if root.nil?
    
    result = []
    queue = Queue.new
    queue.enqueue(root)
    
    while !queue.empty?
      node = queue.dequeue
      result << node.value
      
      # 假设节点有left和right子节点
      queue.enqueue(node.left) if node.left
      queue.enqueue(node.right) if node.right
    end
    
    result
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== Queue 使用示例 ==="
  
  # 基本队列操作
  queue = Queue.new
  puts "创建空队列: #{queue}"
  
  # 入队操作
  queue.enqueue(1).enqueue(2).enqueue(3)
  puts "入队后: #{queue}"
  
  # 查看队头和队尾
  puts "队头元素: #{queue.front}"
  puts "队尾元素: #{queue.rear}"
  
  # 出队操作
  dequeued = queue.dequeue
  puts "出队元素 #{dequeued}: #{queue}"
  
  # 遍历队列
  print "从队头到队尾遍历: "
  queue.each { |item| print "#{item} " }
  puts
  
  puts "\n=== CircularQueue 使用示例 ==="
  
  circular_queue = CircularQueue.new(5)
  puts "创建容量为5的循环队列: #{circular_queue}"
  
  # 填满队列
  5.times { |i| circular_queue.enqueue(i + 1) }
  puts "填满后: #{circular_queue}"
  
  # 出队再入队
  circular_queue.dequeue
  circular_queue.dequeue
  circular_queue.enqueue(6)
  circular_queue.enqueue(7)
  puts "出队2个，入队2个: #{circular_queue}"
  
  puts "\n=== LinkedQueue 使用示例 ==="
  
  linked_queue = LinkedQueue.new
  linked_queue.enqueue('a').enqueue('b').enqueue('c')
  puts "链表队列: #{linked_queue}"
  
  puts "\n=== Deque 使用示例 ==="
  
  deque = Deque.new
  deque.add_front(2).add_rear(3).add_front(1).add_rear(4)
  puts "双端队列: #{deque}"
  
  puts "从前端删除: #{deque.remove_front}"
  puts "从后端删除: #{deque.remove_rear}"
  puts "删除后: #{deque}"
  
  puts "\n=== PriorityQueue 使用示例 ==="
  
  # 数字优先队列（小的优先级高）
  pq = PriorityQueue.new
  pq.enqueue('任务C', 3).enqueue('任务A', 1).enqueue('任务B', 2)
  puts "优先队列: #{pq}"
  
  puts "按优先级出队:"
  while !pq.empty?
    puts "  #{pq.dequeue}"
  end
  
  puts "\n=== 队列应用示例 ==="
  
  # 任务调度器
  scheduler = QueueApplications::TaskScheduler.new
  scheduler.add_task("发送邮件")
  scheduler.add_task("生成报告")
  scheduler.add_task("备份数据")
  
  puts "待处理任务数: #{scheduler.pending_tasks}"
  puts "开始执行任务:"
  scheduler.start
  
  # 缓冲区示例
  puts "\n缓冲区示例:"
  buffer = QueueApplications::Buffer.new(3)
  
  5.times do |i|
    buffer.write("数据#{i + 1}")
    puts buffer
  end
  
  puts "读取数据:"
  while buffer.available_data > 0
    puts "读取: #{buffer.read}"
  end
  
  puts "\n=== 性能测试 ==="
  
  # 性能测试
  large_queue = Queue.new
  start_time = Time.now
  
  # 入队100000个元素
  100000.times { |i| large_queue.enqueue(i) }
  
  # 出队100000个元素
  100000.times { large_queue.dequeue }
  
  end_time = Time.now
  puts "100000次入队+出队操作耗时: #{((end_time - start_time) * 1000).round(2)}ms"
end