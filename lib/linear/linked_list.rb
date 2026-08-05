# 链表 (LinkedList) 实现
# 
# 思路：
# 链表是一种线性数据结构，由节点组成，每个节点包含数据和指向下一个节点的指针。
# 与数组不同，链表的元素在内存中不是连续存储的，通过指针连接。
# 
# 作用：
# 1. 动态内存分配，大小可以在运行时改变
# 2. 插入和删除操作效率高（O(1)，如果已知位置）
# 3. 不需要预先分配固定大小的内存
# 
# 应用场景：
# 1. 实现其他数据结构：栈、队列、图的邻接表
# 2. 音乐播放器：歌曲列表的前进后退
# 3. 浏览器历史记录：前进后退功能
# 4. 撤销/重做功能：编辑器的操作历史
# 5. LRU缓存：最近最少使用缓存算法
# 6. 区块链：每个区块指向前一个区块

# 链表节点类
class ListNode
  attr_accessor :data, :next

  def initialize(data, next_node = nil)
    @data = data
    @next = next_node
  end

  def to_s
    @data.to_s
  end
end

# 单向链表实现
class LinkedList
  attr_reader :size

  def initialize
    @head = nil
    @tail = nil
    @size = 0
  end

  # 在链表头部添加元素
  # 时间复杂度：O(1)
  def prepend(data)
    new_node = ListNode.new(data, @head)
    @head = new_node
    @tail = new_node if @tail.nil?
    @size += 1
    self
  end
  alias_method :unshift, :prepend

  # 在链表尾部添加元素
  # 时间复杂度：O(1)
  def append(data)
    new_node = ListNode.new(data)
    
    if @tail.nil?
      @head = @tail = new_node
    else
      @tail.next = new_node
      @tail = new_node
    end
    
    @size += 1
    self
  end
  alias_method :push, :append
  alias_method :<<, :append

  # 在指定位置插入元素
  # 时间复杂度：O(n)
  def insert(index, data)
    raise IndexError, "Index #{index} out of bounds" if index < 0 || index > @size
    
    return prepend(data) if index == 0
    return append(data) if index == @size
    
    new_node = ListNode.new(data)
    prev_node = get_node_at(index - 1)
    new_node.next = prev_node.next
    prev_node.next = new_node
    
    @size += 1
    self
  end

  # 获取指定位置的元素
  # 时间复杂度：O(n)
  def get(index)
    node = get_node_at(index)
    node&.data
  end
  alias_method :[], :get

  # 设置指定位置的元素
  # 时间复杂度：O(n)
  def set(index, data)
    node = get_node_at(index)
    raise IndexError, "Index #{index} out of bounds" if node.nil?
    
    old_data = node.data
    node.data = data
    old_data
  end
  alias_method :[]=, :set

  # 删除头部元素
  # 时间复杂度：O(1)
  def shift
    return nil if @head.nil?
    
    deleted_data = @head.data
    @head = @head.next
    
    if @head.nil?
      @tail = nil
    end
    
    @size -= 1
    deleted_data
  end

  # 删除尾部元素
  # 时间复杂度：O(n)
  def pop
    return nil if @head.nil?
    return shift if @size == 1
    
    # 找到倒数第二个节点
    current = @head
    while current.next != @tail
      current = current.next
    end
    
    deleted_data = @tail.data
    @tail = current
    @tail.next = nil
    @size -= 1
    
    deleted_data
  end

  # 删除指定位置的元素
  # 时间复杂度：O(n)
  def delete_at(index)
    raise IndexError, "Index #{index} out of bounds" if index < 0 || index >= @size
    
    return shift if index == 0
    
    prev_node = get_node_at(index - 1)
    deleted_node = prev_node.next
    prev_node.next = deleted_node.next
    
    # 如果删除的是尾节点，更新tail指针
    @tail = prev_node if deleted_node == @tail
    
    @size -= 1
    deleted_node.data
  end

  # 删除第一个匹配的元素
  # 时间复杂度：O(n)
  def delete(data)
    return nil if @head.nil?

    # 如果要删除的是头节点
    if @head.data == data
      return shift
    end

    current = @head
    while current.next && current.next.data != data
      current = current.next
    end

    # 找到了要删除的节点
    if current.next
      deleted_node = current.next
      current.next = deleted_node.next

      # 如果删除的是尾节点，更新tail指针
      @tail = current if deleted_node == @tail

      @size -= 1
      return deleted_node.data
    end

    nil  # 未找到
  end
  alias_method :remove, :delete

  # 查找元素的索引
  # 时间复杂度：O(n)
  def index_of(data)
    current = @head
    index = 0
    
    while current
      return index if current.data == data
      current = current.next
      index += 1
    end
    
    -1  # 未找到
  end

  # 检查是否包含指定元素
  # 时间复杂度：O(n)
  def include?(data)
    index_of(data) != -1
  end
  alias_method :contains?, :include?

  # 获取第一个元素
  def first
    @head&.data
  end

  # 获取最后一个元素
  def last
    @tail&.data
  end

  # 检查是否为空
  def empty?
    @size == 0
  end

  # 清空链表
  def clear
    @head = @tail = nil
    @size = 0
    self
  end

  # 反转链表
  # 时间复杂度：O(n)
  def reverse!
    return self if @size <= 1
    
    @tail = @head
    prev = nil
    current = @head
    
    while current
      next_node = current.next
      current.next = prev
      prev = current
      current = next_node
    end
    
    @head = prev
    self
  end

  # 返回反转后的新链表
  def reverse
    new_list = LinkedList.new
    each { |data| new_list.prepend(data) }
    new_list
  end

  # 转换为数组
  def to_a
    result = []
    each { |data| result << data }
    result
  end

  # 迭代器
  def each
    return enum_for(:each) unless block_given?
    
    current = @head
    while current
      yield current.data
      current = current.next
    end
    self
  end

  # 字符串表示
  def to_s
    "LinkedList[#{to_a.join(' -> ')}]"
  end

  def inspect
    "#<LinkedList:#{object_id} size=#{@size} data=[#{to_a.join(', ')}]>"
  end

  private

  # 获取指定位置的节点
  def get_node_at(index)
    return nil if index < 0 || index >= @size
    
    current = @head
    index.times { current = current.next }
    current
  end
end

# 双向链表节点
class DoublyListNode
  attr_accessor :data, :next, :prev

  def initialize(data, next_node = nil, prev_node = nil)
    @data = data
    @next = next_node
    @prev = prev_node
  end

  def to_s
    @data.to_s
  end
end

# 双向链表实现
class DoublyLinkedList
  attr_reader :size

  def initialize
    @head = nil
    @tail = nil
    @size = 0
  end

  # 在头部添加元素
  # 时间复杂度：O(1)
  def prepend(data)
    new_node = DoublyListNode.new(data, @head)
    
    if @head
      @head.prev = new_node
    else
      @tail = new_node
    end
    
    @head = new_node
    @size += 1
    self
  end

  # 在尾部添加元素
  # 时间复杂度：O(1)
  def append(data)
    new_node = DoublyListNode.new(data, nil, @tail)
    
    if @tail
      @tail.next = new_node
    else
      @head = new_node
    end
    
    @tail = new_node
    @size += 1
    self
  end
  alias_method :push, :append

  # 删除头部元素
  # 时间复杂度：O(1)
  def shift
    return nil if @head.nil?
    
    deleted_data = @head.data
    @head = @head.next
    
    if @head
      @head.prev = nil
    else
      @tail = nil
    end
    
    @size -= 1
    deleted_data
  end

  # 删除尾部元素
  # 时间复杂度：O(1)
  def pop
    return nil if @tail.nil?
    
    deleted_data = @tail.data
    @tail = @tail.prev
    
    if @tail
      @tail.next = nil
    else
      @head = nil
    end
    
    @size -= 1
    deleted_data
  end

  # 其他方法与单向链表类似，但可以双向遍历
  def each_forward
    return enum_for(:each_forward) unless block_given?
    
    current = @head
    while current
      yield current.data
      current = current.next
    end
    self
  end
  alias_method :each, :each_forward

  def each_backward
    return enum_for(:each_backward) unless block_given?
    
    current = @tail
    while current
      yield current.data
      current = current.prev
    end
    self
  end

  def first
    @head&.data
  end

  def last
    @tail&.data
  end

  def empty?
    @size == 0
  end

  def to_a
    result = []
    each { |data| result << data }
    result
  end

  def to_s
    "DoublyLinkedList[#{to_a.join(' <-> ')}]"
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== LinkedList 使用示例 ==="
  
  # 单向链表测试
  list = LinkedList.new
  puts "创建空链表: #{list}"
  
  # 添加元素
  list.append(1).append(2).append(3)
  puts "尾部添加元素: #{list}"
  
  list.prepend(0)
  puts "头部添加元素: #{list}"
  
  # 插入元素
  list.insert(2, 'inserted')
  puts "在索引2插入元素: #{list}"
  
  # 访问元素
  puts "索引0的元素: #{list[0]}"
  puts "第一个元素: #{list.first}"
  puts "最后一个元素: #{list.last}"
  
  # 删除元素
  deleted = list.delete('inserted')
  puts "删除元素 '#{deleted}': #{list}"
  
  popped = list.pop
  puts "弹出尾部元素 '#{popped}': #{list}"
  
  shifted = list.shift
  puts "移除头部元素 '#{shifted}': #{list}"
  
  # 反转链表
  list.reverse!
  puts "反转后: #{list}"
  
  puts "\n=== DoublyLinkedList 使用示例 ==="
  
  # 双向链表测试
  dlist = DoublyLinkedList.new
  dlist.append(1).append(2).append(3)
  puts "双向链表: #{dlist}"
  
  print "正向遍历: "
  dlist.each_forward { |item| print "#{item} " }
  puts
  
  print "反向遍历: "
  dlist.each_backward { |item| print "#{item} " }
  puts
end