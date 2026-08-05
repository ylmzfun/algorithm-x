# 哈希表 (Hash Table) 实现
# 
# 思路：
# 哈希表使用哈希函数将键映射到数组索引，实现O(1)平均时间复杂度的查找、插入、删除。
# 处理冲突的方法包括链地址法（拉链法）和开放地址法（线性探测、二次探测、双重哈希）。
# 需要动态调整大小以维持较低的负载因子，保证性能。
# 
# 作用：
# 1. 快速查找：键值对的快速存储和检索
# 2. 缓存实现：LRU缓存、内存缓存
# 3. 索引构建：数据库索引、搜索引擎
# 4. 去重操作：集合实现、重复检测
# 
# 应用场景：
# 1. 数据库：索引结构、查询优化
# 2. 缓存系统：Redis、Memcached
# 3. 编程语言：变量存储、符号表
# 4. 网络应用：会话管理、路由表
# 5. 算法优化：空间换时间、快速查找
# 6. 分布式系统：一致性哈希、负载均衡

# 哈希表节点类（用于链地址法）
class HashNode
  attr_accessor :key, :value, :next

  def initialize(key, value)
    @key = key
    @value = value
    @next = nil
  end

  def to_s
    "#{@key} => #{@value}"
  end
end

# 基础哈希表实现（链地址法）
class HashTable
  DEFAULT_CAPACITY = 16
  LOAD_FACTOR_THRESHOLD = 0.75
  SHRINK_THRESHOLD = 0.25
  MIN_CAPACITY = 8

  attr_reader :size, :capacity, :load_factor

  def initialize(capacity = DEFAULT_CAPACITY)
    @capacity = [capacity, MIN_CAPACITY].max
    @buckets = Array.new(@capacity)
    @size = 0
  end

  # 哈希函数（简单的除法哈希）
  def hash_function(key)
    key.hash.abs % @capacity
  end

  # 插入或更新键值对
  def put(key, value)
    index = hash_function(key)
    
    if @buckets[index].nil?
      @buckets[index] = HashNode.new(key, value)
      @size += 1
    else
      current = @buckets[index]
      
      # 查找是否已存在该键
      while current
        if current.key == key
          old_value = current.value
          current.value = value
          return old_value
        end
        
        if current.next.nil?
          current.next = HashNode.new(key, value)
          @size += 1
          break
        end
        
        current = current.next
      end
    end
    
    # 检查是否需要扩容
    resize_if_needed
    nil
  end

  # 获取值
  def get(key)
    index = hash_function(key)
    current = @buckets[index]
    
    while current
      return current.value if current.key == key
      current = current.next
    end
    
    nil
  end

  # 删除键值对
  def delete(key)
    index = hash_function(key)
    current = @buckets[index]
    
    return nil if current.nil?
    
    # 如果要删除的是第一个节点
    if current.key == key
      @buckets[index] = current.next
      @size -= 1
      resize_if_needed
      return current.value
    end
    
    # 查找要删除的节点
    while current.next
      if current.next.key == key
        deleted_value = current.next.value
        current.next = current.next.next
        @size -= 1
        resize_if_needed
        return deleted_value
      end
      current = current.next
    end
    
    nil
  end

  # 检查是否包含键
  def has_key?(key)
    !get(key).nil?
  end

  # 检查是否为空
  def empty?
    @size == 0
  end

  # 获取所有键
  def keys
    result = []
    @buckets.each do |head|
      current = head
      while current
        result << current.key
        current = current.next
      end
    end
    result
  end

  # 获取所有值
  def values
    result = []
    @buckets.each do |head|
      current = head
      while current
        result << current.value
        current = current.next
      end
    end
    result
  end

  # 获取所有键值对
  def entries
    result = []
    @buckets.each do |head|
      current = head
      while current
        result << [current.key, current.value]
        current = current.next
      end
    end
    result
  end

  # 清空哈希表
  def clear
    @buckets = Array.new(@capacity)
    @size = 0
    self
  end

  # 计算负载因子
  def load_factor
    @size.to_f / @capacity
  end

  # 获取冲突统计
  def collision_stats
    chain_lengths = @buckets.map do |head|
      length = 0
      current = head
      while current
        length += 1
        current = current.next
      end
      length
    end
    
    non_empty_buckets = chain_lengths.count { |length| length > 0 }
    max_chain_length = chain_lengths.max || 0
    avg_chain_length = non_empty_buckets > 0 ? @size.to_f / non_empty_buckets : 0
    
    {
      total_buckets: @capacity,
      used_buckets: non_empty_buckets,
      max_chain_length: max_chain_length,
      avg_chain_length: avg_chain_length.round(2),
      load_factor: load_factor.round(3)
    }
  end

  # 遍历所有键值对
  def each
    return enum_for(:each) unless block_given?
    
    @buckets.each do |head|
      current = head
      while current
        yield current.key, current.value
        current = current.next
      end
    end
    
    self
  end

  # 转换为数组
  def to_a
    entries
  end

  # 转换为哈希
  def to_h
    result = {}
    each { |key, value| result[key] = value }
    result
  end

  def to_s
    "HashTable[size: #{@size}, capacity: #{@capacity}, load_factor: #{load_factor.round(3)}]"
  end

  def inspect
    "#<HashTable:#{object_id} size=#{@size} capacity=#{@capacity}>"
  end

  # 打印哈希表结构
  def print_structure
    puts "HashTable Structure (#{@size} items, #{@capacity} buckets):"
    @buckets.each_with_index do |head, index|
      if head
        chain = []
        current = head
        while current
          chain << "#{current.key}=>#{current.value}"
          current = current.next
        end
        puts "  [#{index}]: #{chain.join(' -> ')}"
      end
    end
  end

  private

  # 检查是否需要调整大小
  def resize_if_needed
    if load_factor > LOAD_FACTOR_THRESHOLD
      resize(@capacity * 2)
    elsif load_factor < SHRINK_THRESHOLD && @capacity > MIN_CAPACITY
      resize([@capacity / 2, MIN_CAPACITY].max)
    end
  end

  # 调整哈希表大小
  def resize(new_capacity)
    old_buckets = @buckets
    @capacity = new_capacity
    @buckets = Array.new(@capacity)
    old_size = @size
    @size = 0
    
    # 重新插入所有元素（直接插入避免递归调用resize）
    old_buckets.each do |head|
      current = head
      while current
        index = hash_function(current.key)
        
        if @buckets[index].nil?
          @buckets[index] = HashNode.new(current.key, current.value)
          @size += 1
        else
          # 找到链表末尾插入新节点
          tail = @buckets[index]
          while tail.next
            tail = tail.next
          end
          tail.next = HashNode.new(current.key, current.value)
          @size += 1
        end
        
        current = current.next
      end
    end
  end
end

# 开放地址法哈希表实现
class OpenAddressingHashTable
  DEFAULT_CAPACITY = 16
  LOAD_FACTOR_THRESHOLD = 0.7
  DELETED = :deleted  # 删除标记

  attr_reader :size, :capacity

  def initialize(capacity = DEFAULT_CAPACITY)
    @capacity = capacity
    @keys = Array.new(@capacity)
    @values = Array.new(@capacity)
    @size = 0
  end

  # 哈希函数
  def hash_function(key, attempt = 0)
    # 线性探测
    (key.hash.abs + attempt) % @capacity
  end

  # 插入或更新
  def put(key, value)
    resize_if_needed
    
    attempt = 0
    
    while attempt < @capacity
      index = hash_function(key, attempt)
      
      if @keys[index].nil? || @keys[index] == DELETED
        @keys[index] = key
        @values[index] = value
        @size += 1
        return nil
      elsif @keys[index] == key
        old_value = @values[index]
        @values[index] = value
        return old_value
      end
      
      attempt += 1
    end
    
    raise "HashTable is full"
  end

  # 获取值
  def get(key)
    attempt = 0
    
    while attempt < @capacity
      index = hash_function(key, attempt)
      
      return nil if @keys[index].nil?
      return @values[index] if @keys[index] == key
      
      attempt += 1
    end
    
    nil
  end

  # 删除
  def delete(key)
    attempt = 0
    
    while attempt < @capacity
      index = hash_function(key, attempt)
      
      return nil if @keys[index].nil?
      
      if @keys[index] == key
        deleted_value = @values[index]
        @keys[index] = DELETED
        @values[index] = nil
        @size -= 1
        return deleted_value
      end
      
      attempt += 1
    end
    
    nil
  end

  # 检查是否包含键
  def has_key?(key)
    !get(key).nil?
  end

  # 检查是否为空
  def empty?
    @size == 0
  end

  # 获取所有键
  def keys
    result = []
    @keys.each_with_index do |key, index|
      result << key if key && key != DELETED
    end
    result
  end

  # 获取所有值
  def values
    result = []
    @keys.each_with_index do |key, index|
      result << @values[index] if key && key != DELETED
    end
    result
  end

  # 负载因子
  def load_factor
    @size.to_f / @capacity
  end

  # 清空
  def clear
    @keys = Array.new(@capacity)
    @values = Array.new(@capacity)
    @size = 0
    self
  end

  def to_s
    "OpenAddressingHashTable[size: #{@size}, capacity: #{@capacity}, load_factor: #{load_factor.round(3)}]"
  end

  private

  def resize_if_needed
    if load_factor > LOAD_FACTOR_THRESHOLD
      resize(@capacity * 2)
    end
  end

  def resize(new_capacity)
    old_keys = @keys
    old_values = @values
    
    @capacity = new_capacity
    @keys = Array.new(@capacity)
    @values = Array.new(@capacity)
    old_size = @size
    @size = 0
    
    old_keys.each_with_index do |key, index|
      if key && key != DELETED
        put(key, old_values[index])
      end
    end
  end
end

# 哈希表应用示例
module HashTableApplications
  # LRU缓存实现
  class LRUCache
    def initialize(capacity)
      @capacity = capacity
      @cache = HashTable.new
      @head = Node.new(nil, nil)
      @tail = Node.new(nil, nil)
      @head.next = @tail
      @tail.prev = @head
    end

    def get(key)
      if @cache.has_key?(key)
        node = @cache.get(key)
        move_to_head(node)
        node.value
      else
        nil
      end
    end

    def put(key, value)
      if @cache.has_key?(key)
        node = @cache.get(key)
        node.value = value
        move_to_head(node)
      else
        if @cache.size >= @capacity
          # 删除尾部节点
          tail_node = @tail.prev
          remove_node(tail_node)
          @cache.delete(tail_node.key)
        end
        
        new_node = Node.new(key, value)
        @cache.put(key, new_node)
        add_to_head(new_node)
      end
    end

    def size
      @cache.size
    end

    def keys
      result = []
      current = @head.next
      while current != @tail
        result << current.key
        current = current.next
      end
      result
    end

    private

    class Node
      attr_accessor :key, :value, :prev, :next
      
      def initialize(key, value)
        @key = key
        @value = value
        @prev = nil
        @next = nil
      end
    end

    def add_to_head(node)
      node.prev = @head
      node.next = @head.next
      @head.next.prev = node
      @head.next = node
    end

    def remove_node(node)
      node.prev.next = node.next
      node.next.prev = node.prev
    end

    def move_to_head(node)
      remove_node(node)
      add_to_head(node)
    end
  end

  # 计数器
  class Counter
    def initialize
      @counts = HashTable.new
    end

    def increment(key, amount = 1)
      current = @counts.get(key) || 0
      @counts.put(key, current + amount)
    end

    def decrement(key, amount = 1)
      increment(key, -amount)
    end

    def get(key)
      @counts.get(key) || 0
    end

    def most_common(n = nil)
      entries = @counts.entries.sort_by { |key, count| -count }
      n ? entries.first(n) : entries
    end

    def total
      @counts.values.sum
    end

    def keys
      @counts.keys
    end

    def clear
      @counts.clear
    end
  end

  # 字符串索引
  class StringIndex
    def initialize
      @index = HashTable.new
    end

    def add_document(doc_id, content)
      words = content.downcase.split(/\W+/).reject(&:empty?)
      
      words.each do |word|
        if @index.has_key?(word)
          doc_set = @index.get(word)
        else
          doc_set = Set.new
          @index.put(word, doc_set)
        end
        doc_set.add(doc_id)
      end
    end

    def search(query)
      words = query.downcase.split(/\W+/).reject(&:empty?)
      return Set.new if words.empty?
      
      result = @index.get(words.first) || Set.new
      
      words[1..-1].each do |word|
        word_docs = @index.get(word) || Set.new
        result = result.intersection(word_docs)
      end
      
      result.to_a
    end

    def word_count
      @index.size
    end

    def document_frequency(word)
      doc_set = @index.get(word.downcase)
      doc_set ? doc_set.size : 0
    end
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== HashTable 使用示例 ==="
  
  # 基础哈希表测试
  ht = HashTable.new(8)
  
  puts "插入键值对:"
  data = {
    "apple" => 5,
    "banana" => 3,
    "orange" => 8,
    "grape" => 12,
    "kiwi" => 6,
    "mango" => 9,
    "peach" => 4,
    "pear" => 7
  }
  
  data.each { |key, value| ht.put(key, value) }
  
  puts ht
  ht.print_structure
  
  puts "\n查找操作:"
  puts "apple: #{ht.get('apple')}"
  puts "banana: #{ht.get('banana')}"
  puts "watermelon: #{ht.get('watermelon')}"
  
  puts "\n包含检查:"
  puts "包含apple: #{ht.has_key?('apple')}"
  puts "包含watermelon: #{ht.has_key?('watermelon')}"
  
  puts "\n删除操作:"
  deleted = ht.delete('banana')
  puts "删除banana: #{deleted}"
  puts "删除后大小: #{ht.size}"
  
  puts "\n遍历操作:"
  puts "所有键: #{ht.keys}"
  puts "所有值: #{ht.values}"
  puts "所有条目: #{ht.entries}"
  
  puts "\n冲突统计:"
  stats = ht.collision_stats
  puts "总桶数: #{stats[:total_buckets]}"
  puts "使用桶数: #{stats[:used_buckets]}"
  puts "最大链长: #{stats[:max_chain_length]}"
  puts "平均链长: #{stats[:avg_chain_length]}"
  puts "负载因子: #{stats[:load_factor]}"
  
  puts "\n=== 开放地址法哈希表 ==="
  
  oht = OpenAddressingHashTable.new(8)
  
  # 插入相同数据
  data.each { |key, value| oht.put(key, value) }
  
  puts oht
  puts "查找apple: #{oht.get('apple')}"
  puts "删除banana: #{oht.delete('banana')}"
  puts "所有键: #{oht.keys}"
  
  puts "\n=== 应用示例 ==="
  
  # LRU缓存
  puts "\nLRU缓存:"
  cache = HashTableApplications::LRUCache.new(3)
  
  cache.put("a", 1)
  cache.put("b", 2)
  cache.put("c", 3)
  puts "缓存大小: #{cache.size}"
  
  puts "获取a: #{cache.get('a')}"
  cache.put("d", 4)  # 应该淘汰b
  puts "获取b: #{cache.get('b')}"  # 应该返回nil
  
  # 计数器
  puts "\n计数器:"
  counter = HashTableApplications::Counter.new
  
  text = "the quick brown fox jumps over the lazy dog the fox is quick"
  text.split.each { |word| counter.increment(word) }
  
  puts "单词计数:"
  counter.most_common(5).each { |word, count| puts "  #{word}: #{count}" }
  puts "总词数: #{counter.total}"
  
  # 字符串索引
  puts "\n字符串索引:"
  index = HashTableApplications::StringIndex.new
  
  documents = {
    1 => "Ruby is a dynamic programming language",
    2 => "Python is also a dynamic language",
    3 => "Java is a static programming language",
    4 => "Ruby and Python are both dynamic"
  }
  
  documents.each { |id, content| index.add_document(id, content) }
  
  puts "搜索'dynamic': #{index.search('dynamic')}"
  puts "搜索'programming language': #{index.search('programming language')}"
  puts "搜索'Ruby dynamic': #{index.search('Ruby dynamic')}"
  puts "词汇表大小: #{index.word_count}"
  
  puts "\n=== 性能测试 ==="
  
  # 大规模数据测试
  large_ht = HashTable.new
  
  start_time = Time.now
  
  # 插入10000个键值对
  10000.times do |i|
    key = "key_#{i}"
    value = i * 2
    large_ht.put(key, value)
  end
  
  end_time = Time.now
  
  puts "插入10000个元素耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  puts "最终哈希表: #{large_ht}"
  
  # 查找性能测试
  start_time = Time.now
  
  1000.times do |i|
    key = "key_#{rand(10000)}"
    large_ht.get(key)
  end
  
  end_time = Time.now
  
  puts "1000次随机查找耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  
  # 冲突分析
  stats = large_ht.collision_stats
  puts "\n大规模数据冲突统计:"
  puts "负载因子: #{stats[:load_factor]}"
  puts "最大链长: #{stats[:max_chain_length]}"
  puts "平均链长: #{stats[:avg_chain_length]}"
end