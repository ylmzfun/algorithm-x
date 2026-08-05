# 动态数组 (ArrayList) 实现
# 
# 思路：
# 动态数组是一种可以自动调整大小的数组数据结构。当元素数量超过当前容量时，
# 会自动扩容（通常是当前容量的2倍），当元素数量远小于容量时，会自动缩容。
# 
# 作用：
# 1. 提供类似数组的随机访问能力（O(1)时间复杂度）
# 2. 支持动态增删元素，无需预先指定大小
# 3. 内存使用相对紧凑，局部性好
# 
# 应用场景：
# 1. Web开发：存储用户列表、商品列表等需要频繁访问的数据
# 2. 数据处理：批量处理数据时的临时存储
# 3. 缓存系统：LRU缓存的底层存储结构
# 4. 游戏开发：存储游戏对象、粒子系统等
# 5. 设计模式：观察者模式中存储观察者列表

class ArrayList
  # 默认初始容量
  DEFAULT_CAPACITY = 10
  # 扩容因子
  GROWTH_FACTOR = 2
  # 缩容阈值（当使用率低于25%时缩容）
  SHRINK_THRESHOLD = 0.25

  attr_reader :size, :capacity

  def initialize(initial_capacity = DEFAULT_CAPACITY)
    @capacity = [initial_capacity, DEFAULT_CAPACITY].max
    @data = Array.new(@capacity)
    @size = 0
  end

  # 在末尾添加元素
  # 时间复杂度：平均 O(1)，最坏 O(n)
  def push(element)
    ensure_capacity(@size + 1)
    @data[@size] = element
    @size += 1
    self
  end
  alias_method :<<, :push
  alias_method :append, :push
  alias_method :add, :push

  # 在指定位置插入元素
  # 时间复杂度：O(n)
  def insert(index, element)
    raise IndexError, "Index #{index} out of bounds" if index < 0 || index > @size
    
    ensure_capacity(@size + 1)
    
    # 将index位置及之后的元素向后移动
    (@size - 1).downto(index) do |i|
      @data[i + 1] = @data[i]
    end
    
    @data[index] = element
    @size += 1
    self
  end

  # 获取指定位置的元素
  # 时间复杂度：O(1)
  def get(index)
    raise IndexError, "Index #{index} out of bounds" if index < 0 || index >= @size
    @data[index]
  end
  alias_method :[], :get

  # 设置指定位置的元素
  # 时间复杂度：O(1)
  def set(index, element)
    raise IndexError, "Index #{index} out of bounds" if index < 0 || index >= @size
    old_value = @data[index]
    @data[index] = element
    old_value
  end
  alias_method :[]=, :set

  # 删除指定位置的元素
  # 时间复杂度：O(n)
  def delete_at(index)
    raise IndexError, "Index #{index} out of bounds" if index < 0 || index >= @size
    
    deleted_element = @data[index]
    
    # 将index之后的元素向前移动
    (index + 1).upto(@size - 1) do |i|
      @data[i - 1] = @data[i]
    end
    
    @size -= 1
    @data[@size] = nil  # 清除引用
    
    # 检查是否需要缩容
    shrink_if_needed
    
    deleted_element
  end
  alias_method :delete, :delete_at

  # 删除末尾元素
  # 时间复杂度：O(1)
  def pop
    raise RuntimeError, "ArrayList is empty" if empty?
    
    @size -= 1
    deleted_element = @data[@size]
    @data[@size] = nil  # 清除引用
    
    shrink_if_needed
    deleted_element
  end

  # 查找元素的索引
  # 时间复杂度：O(n)
  def index_of(element)
    0.upto(@size - 1) do |i|
      return i if @data[i] == element
    end
    -1  # 未找到
  end

  # 检查是否包含指定元素
  # 时间复杂度：O(n)
  def include?(element)
    index_of(element) != -1
  end
  alias_method :contains?, :include?

  # 清空数组
  def clear
    @size = 0
    @capacity = DEFAULT_CAPACITY
    @data = Array.new(@capacity)
    self
  end

  # 检查是否为空
  def empty?
    @size == 0
  end

  # 获取第一个元素
  def first
    raise RuntimeError, "ArrayList is empty" if empty?
    @data[0]
  end

  # 获取最后一个元素
  def last
    raise RuntimeError, "ArrayList is empty" if empty?
    @data[@size - 1]
  end

  # 转换为Ruby数组
  def to_a
    @data[0, @size]
  end

  # 迭代器
  def each
    return enum_for(:each) unless block_given?
    
    0.upto(@size - 1) do |i|
      yield @data[i]
    end
    self
  end

  # 字符串表示
  def to_s
    "ArrayList[#{to_a.join(', ')}]"
  end

  def inspect
    "#<ArrayList:#{object_id} size=#{@size} capacity=#{@capacity} data=#{to_a.inspect}>"
  end

  private

  # 确保容量足够
  def ensure_capacity(min_capacity)
    return if min_capacity <= @capacity
    
    new_capacity = [@capacity * GROWTH_FACTOR, min_capacity].max
    resize(new_capacity)
  end

  # 检查是否需要缩容
  def shrink_if_needed
    return if @capacity <= DEFAULT_CAPACITY
    return if @size.to_f / @capacity > SHRINK_THRESHOLD
    
    new_capacity = [@capacity / GROWTH_FACTOR, DEFAULT_CAPACITY].max
    resize(new_capacity) if new_capacity < @capacity
  end

  # 调整容量
  def resize(new_capacity)
    old_data = @data
    @capacity = new_capacity
    @data = Array.new(@capacity)
    
    # 复制现有数据
    0.upto(@size - 1) do |i|
      @data[i] = old_data[i]
    end
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== ArrayList 使用示例 ==="
  
  # 创建动态数组
  list = ArrayList.new
  puts "创建空数组: #{list}"
  
  # 添加元素
  list.push(1).push(2).push(3)
  puts "添加元素后: #{list}"
  
  # 插入元素
  list.insert(1, 'inserted')
  puts "在索引1插入元素: #{list}"
  
  # 访问元素
  puts "索引0的元素: #{list[0]}"
  puts "最后一个元素: #{list.last}"
  
  # 查找元素
  puts "元素2的索引: #{list.index_of(2)}"
  puts "是否包含元素3: #{list.include?(3)}"
  
  # 删除元素
  deleted = list.delete_at(1)
  puts "删除索引1的元素 '#{deleted}': #{list}"
  
  # 弹出元素
  popped = list.pop
  puts "弹出元素 '#{popped}': #{list}"
  
  # 迭代
  print "遍历元素: "
  list.each { |item| print "#{item} " }
  puts
  
  puts "\n=== 性能测试 ==="
  
  # 性能测试
  large_list = ArrayList.new
  start_time = Time.now
  
  # 添加10000个元素
  10000.times { |i| large_list.push(i) }
  
  end_time = Time.now
  puts "添加10000个元素耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  puts "最终大小: #{large_list.size}, 容量: #{large_list.capacity}"
end