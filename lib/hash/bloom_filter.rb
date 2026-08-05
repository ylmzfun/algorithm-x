# 布隆过滤器 (Bloom Filter) 实现
# 
# 思路：
# 布隆过滤器是一个空间高效的概率数据结构，用于测试元素是否在集合中。
# 使用位数组和多个哈希函数，可能有假阳性但不会有假阴性。
# 通过调整位数组大小和哈希函数数量来控制误判率。
# 
# 作用：
# 1. 快速过滤：大数据集的快速成员检测
# 2. 缓存优化：避免不必要的数据库查询
# 3. 网络应用：URL去重、垃圾邮件过滤
# 4. 分布式系统：数据分片、负载均衡
# 
# 应用场景：
# 1. 数据库：查询优化、索引过滤
# 2. 缓存系统：缓存穿透防护
# 3. 网络爬虫：URL去重、已访问检测
# 4. 分布式存储：数据定位、副本检测
# 5. 安全系统：恶意URL检测、黑名单过滤
# 6. 大数据处理：数据去重、预过滤

require 'digest'

# 布隆过滤器实现
class BloomFilter
  attr_reader :size, :hash_count, :bit_array, :inserted_count

  def initialize(expected_elements, false_positive_rate = 0.01)
    @expected_elements = expected_elements
    @false_positive_rate = false_positive_rate

    # 计算最优参数
    @size = optimal_size(expected_elements, false_positive_rate)
    @hash_count = optimal_hash_count(@size, expected_elements)

    # 初始化位数组
    @bit_array = Array.new(@size, false)
    @inserted_count = 0
  end

  # 预期的假阳性率
  def expected_false_positive_rate
    @false_positive_rate
  end

  # 添加元素
  def add(element)
    hash_values = get_hash_values(element)
    
    hash_values.each do |hash_value|
      index = hash_value % @size
      @bit_array[index] = true
    end
    
    @inserted_count += 1
    self
  end

  # 批量添加元素
  def add_all(elements)
    elements.each { |element| add(element) }
    self
  end

  # 检查元素是否可能存在
  def might_contain?(element)
    hash_values = get_hash_values(element)
    
    hash_values.all? do |hash_value|
      index = hash_value % @size
      @bit_array[index]
    end
  end

  # 检查元素肯定不存在
  def definitely_not_contain?(element)
    !might_contain?(element)
  end

  # 计算当前误判率
  def current_false_positive_rate
    return 0.0 if @inserted_count == 0
    
    # 计算当前位数组中1的比例
    ones_count = @bit_array.count(true)
    ones_ratio = ones_count.to_f / @size
    
    # 估算误判率
    (ones_ratio ** @hash_count).round(6)
  end

  # 获取位数组使用率
  def utilization
    ones_count = @bit_array.count(true)
    (ones_count.to_f / @size).round(4)
  end

  # 检查是否为空
  def empty?
    @inserted_count == 0
  end

  # 清空过滤器
  def clear
    @bit_array.fill(false)
    @inserted_count = 0
    self
  end

  # 合并两个布隆过滤器（OR操作）
  def union(other)
    raise ArgumentError, "Size mismatch" if @size != other.size
    raise ArgumentError, "Hash count mismatch" if @hash_count != other.hash_count
    
    result = BloomFilter.allocate
    result.instance_variable_set(:@size, @size)
    result.instance_variable_set(:@hash_count, @hash_count)
    result.instance_variable_set(:@expected_elements, @expected_elements)
    result.instance_variable_set(:@false_positive_rate, @false_positive_rate)
    result.instance_variable_set(:@inserted_count, @inserted_count + other.inserted_count)
    
    # 位数组OR操作
    union_bits = @bit_array.zip(other.bit_array).map { |a, b| a || b }
    result.instance_variable_set(:@bit_array, union_bits)
    
    result
  end

  # 交集操作（AND操作）
  def intersection(other)
    raise ArgumentError, "Size mismatch" if @size != other.size
    raise ArgumentError, "Hash count mismatch" if @hash_count != other.hash_count
    
    result = BloomFilter.allocate
    result.instance_variable_set(:@size, @size)
    result.instance_variable_set(:@hash_count, @hash_count)
    result.instance_variable_set(:@expected_elements, @expected_elements)
    result.instance_variable_set(:@false_positive_rate, @false_positive_rate)
    result.instance_variable_set(:@inserted_count, [@inserted_count, other.inserted_count].min)
    
    # 位数组AND操作
    intersection_bits = @bit_array.zip(other.bit_array).map { |a, b| a && b }
    result.instance_variable_set(:@bit_array, intersection_bits)
    
    result
  end

  # 获取过滤器统计信息
  def statistics
    {
      size: @size,
      hash_count: @hash_count,
      expected_elements: @expected_elements,
      inserted_count: @inserted_count,
      expected_fpr: @false_positive_rate,
      current_fpr: current_false_positive_rate,
      utilization: utilization,
      memory_usage_bits: @size,
      memory_usage_bytes: (@size / 8.0).ceil
    }
  end

  # 序列化为字符串
  def to_s
    "BloomFilter[size: #{@size}, hashes: #{@hash_count}, elements: #{@inserted_count}, fpr: #{current_false_positive_rate}]"
  end

  def inspect
    "#<BloomFilter:#{object_id} size=#{@size} inserted=#{@inserted_count}>"
  end

  # 导出位数组（用于持久化）
  def export_bits
    @bit_array.map { |bit| bit ? '1' : '0' }.join
  end

  # 从位数组导入（用于恢复）
  def import_bits(bit_string)
    raise ArgumentError, "Bit string length mismatch" if bit_string.length != @size
    
    @bit_array = bit_string.chars.map { |char| char == '1' }
    # 注意：导入时无法准确恢复inserted_count，需要外部提供
    self
  end

  private

  # 计算最优位数组大小
  def optimal_size(expected_elements, false_positive_rate)
    # m = -(n * ln(p)) / (ln(2)^2)
    size = -(expected_elements * Math.log(false_positive_rate)) / (Math.log(2) ** 2)
    size.ceil
  end

  # 计算最优哈希函数数量
  def optimal_hash_count(size, expected_elements)
    # k = (m / n) * ln(2)
    hash_count = (size.to_f / expected_elements) * Math.log(2)
    [hash_count.round, 1].max
  end

  # 生成多个哈希值
  def get_hash_values(element)
    # 使用双重哈希技术生成多个哈希值
    str = element.to_s
    hash1 = Digest::MD5.hexdigest(str).to_i(16)
    hash2 = Digest::SHA1.hexdigest(str).to_i(16)
    
    hash_values = []
    @hash_count.times do |i|
      hash_value = (hash1 + i * hash2).abs
      hash_values << hash_value
    end
    
    hash_values
  end
end

# 计数布隆过滤器（支持删除操作）
class CountingBloomFilter
  attr_reader :size, :hash_count, :counters, :inserted_count

  def initialize(expected_elements, false_positive_rate = 0.01, counter_size = 4)
    @expected_elements = expected_elements
    @false_positive_rate = false_positive_rate
    @counter_size = counter_size
    @max_count = (2 ** counter_size) - 1
    
    # 计算最优参数
    @size = optimal_size(expected_elements, false_positive_rate)
    @hash_count = optimal_hash_count(@size, expected_elements)
    
    # 初始化计数器数组
    @counters = Array.new(@size, 0)
    @inserted_count = 0
  end

  # 添加元素
  def add(element)
    hash_values = get_hash_values(element)
    
    hash_values.each do |hash_value|
      index = hash_value % @size
      @counters[index] = [@counters[index] + 1, @max_count].min
    end
    
    @inserted_count += 1
    self
  end

  # 删除元素
  def remove(element)
    return false unless might_contain?(element)
    
    hash_values = get_hash_values(element)
    
    # 检查是否所有计数器都大于0
    can_remove = hash_values.all? do |hash_value|
      index = hash_value % @size
      @counters[index] > 0
    end
    
    if can_remove
      hash_values.each do |hash_value|
        index = hash_value % @size
        @counters[index] -= 1
      end
      @inserted_count -= 1
      true
    else
      false
    end
  end

  # 检查元素是否可能存在
  def might_contain?(element)
    hash_values = get_hash_values(element)
    
    hash_values.all? do |hash_value|
      index = hash_value % @size
      @counters[index] > 0
    end
  end

  # 清空过滤器
  def clear
    @counters.fill(0)
    @inserted_count = 0
    self
  end

  # 获取统计信息
  def statistics
    non_zero_counters = @counters.count { |c| c > 0 }
    max_counter = @counters.max
    avg_counter = non_zero_counters > 0 ? @counters.sum.to_f / non_zero_counters : 0
    
    {
      size: @size,
      hash_count: @hash_count,
      inserted_count: @inserted_count,
      non_zero_counters: non_zero_counters,
      max_counter: max_counter,
      avg_counter: avg_counter.round(2),
      utilization: (non_zero_counters.to_f / @size).round(4),
      memory_usage_bits: @size * @counter_size,
      memory_usage_bytes: (@size * @counter_size / 8.0).ceil
    }
  end

  def to_s
    "CountingBloomFilter[size: #{@size}, hashes: #{@hash_count}, elements: #{@inserted_count}]"
  end

  private

  def optimal_size(expected_elements, false_positive_rate)
    size = -(expected_elements * Math.log(false_positive_rate)) / (Math.log(2) ** 2)
    size.ceil
  end

  def optimal_hash_count(size, expected_elements)
    hash_count = (size.to_f / expected_elements) * Math.log(2)
    [hash_count.round, 1].max
  end

  def get_hash_values(element)
    str = element.to_s
    hash1 = Digest::MD5.hexdigest(str).to_i(16)
    hash2 = Digest::SHA1.hexdigest(str).to_i(16)
    
    hash_values = []
    @hash_count.times do |i|
      hash_value = (hash1 + i * hash2).abs
      hash_values << hash_value
    end
    
    hash_values
  end
end

# 布隆过滤器应用示例
module BloomFilterApplications
  # URL去重器
  class URLDeduplicator
    def initialize(expected_urls = 1000000, false_positive_rate = 0.01)
      @bloom_filter = BloomFilter.new(expected_urls, false_positive_rate)
      @processed_count = 0
      @duplicate_count = 0
    end

    def process_url(url)
      normalized_url = normalize_url(url)
      
      if @bloom_filter.might_contain?(normalized_url)
        @duplicate_count += 1
        false  # 可能是重复URL
      else
        @bloom_filter.add(normalized_url)
        @processed_count += 1
        true   # 新URL
      end
    end

    def statistics
      {
        processed_urls: @processed_count,
        potential_duplicates: @duplicate_count,
        filter_stats: @bloom_filter.statistics
      }
    end

    private

    def normalize_url(url)
      # 简单的URL标准化
      url.downcase.gsub(/\/$/, '').gsub(/^https?:\/\//, '')
    end
  end

  # 缓存穿透防护
  class CachePenetrationGuard
    def initialize(expected_keys = 100000)
      @bloom_filter = BloomFilter.new(expected_keys, 0.01)
      @cache_hits = 0
      @cache_misses = 0
      @prevented_queries = 0
    end

    def add_cache_key(key)
      @bloom_filter.add(key)
    end

    def check_cache_key(key)
      if @bloom_filter.might_contain?(key)
        @cache_hits += 1
        true  # 可能在缓存中
      else
        @prevented_queries += 1
        false # 肯定不在缓存中
      end
    end

    def record_cache_miss(key)
      @cache_misses += 1
      # 将不存在的key也加入过滤器，防止重复查询
      @bloom_filter.add("MISS:#{key}")
    end

    def statistics
      {
        cache_hits: @cache_hits,
        cache_misses: @cache_misses,
        prevented_queries: @prevented_queries,
        filter_stats: @bloom_filter.statistics
      }
    end
  end

  # 恶意IP检测器
  class MaliciousIPDetector
    def initialize(blacklist_size = 10000)
      @bloom_filter = BloomFilter.new(blacklist_size, 0.001)  # 更低的误判率
      @blocked_count = 0
      @checked_count = 0
    end

    def add_malicious_ip(ip)
      @bloom_filter.add(ip)
    end

    def add_malicious_ips(ips)
      ips.each { |ip| add_malicious_ip(ip) }
    end

    def is_malicious?(ip)
      @checked_count += 1
      
      if @bloom_filter.might_contain?(ip)
        @blocked_count += 1
        true  # 可能是恶意IP
      else
        false # 肯定不是恶意IP
      end
    end

    def statistics
      {
        checked_ips: @checked_count,
        blocked_ips: @blocked_count,
        block_rate: @checked_count > 0 ? (@blocked_count.to_f / @checked_count).round(4) : 0,
        filter_stats: @bloom_filter.statistics
      }
    end
  end

  # 数据去重系统
  class DataDeduplicator
    def initialize(expected_items = 1000000)
      @bloom_filter = CountingBloomFilter.new(expected_items, 0.01)
      @processed_items = 0
      @unique_items = 0
      @duplicate_items = 0
    end

    def process_item(item)
      @processed_items += 1
      
      if @bloom_filter.might_contain?(item)
        @duplicate_items += 1
        false  # 可能是重复项
      else
        @bloom_filter.add(item)
        @unique_items += 1
        true   # 新项目
      end
    end

    def remove_item(item)
      if @bloom_filter.remove(item)
        @unique_items -= 1
        true
      else
        false
      end
    end

    def statistics
      {
        processed_items: @processed_items,
        unique_items: @unique_items,
        duplicate_items: @duplicate_items,
        deduplication_rate: @processed_items > 0 ? (@duplicate_items.to_f / @processed_items).round(4) : 0,
        filter_stats: @bloom_filter.statistics
      }
    end
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== BloomFilter 使用示例 ==="
  
  # 基础布隆过滤器测试
  bf = BloomFilter.new(1000, 0.01)
  
  puts "布隆过滤器信息:"
  puts bf
  puts "统计信息: #{bf.statistics}"
  
  puts "\n添加元素:"
  fruits = %w[apple banana orange grape kiwi mango peach pear]
  fruits.each { |fruit| bf.add(fruit) }
  
  puts "添加后统计: #{bf.statistics}"
  
  puts "\n成员检测:"
  test_items = %w[apple banana watermelon strawberry orange]
  test_items.each do |item|
    result = bf.might_contain?(item)
    puts "#{item}: #{result ? '可能存在' : '肯定不存在'}"
  end
  
  puts "\n当前误判率: #{bf.current_false_positive_rate}"
  puts "位数组使用率: #{bf.utilization}"
  
  puts "\n=== 计数布隆过滤器 ==="
  
  cbf = CountingBloomFilter.new(1000, 0.01)
  
  # 添加和删除测试
  puts "添加元素:"
  fruits.each { |fruit| cbf.add(fruit) }
  puts cbf.statistics
  
  puts "\n删除测试:"
  puts "删除apple: #{cbf.remove('apple')}"
  puts "删除watermelon: #{cbf.remove('watermelon')}"
  puts "apple还存在吗: #{cbf.might_contain?('apple')}"
  
  puts "删除后统计: #{cbf.statistics}"
  
  puts "\n=== 布隆过滤器操作 ==="
  
  # 创建两个过滤器进行集合操作
  bf1 = BloomFilter.new(1000, 0.01)
  bf2 = BloomFilter.new(1000, 0.01)
  
  # 添加不同的元素
  %w[a b c d e].each { |item| bf1.add(item) }
  %w[d e f g h].each { |item| bf2.add(item) }
  
  # 并集操作
  union_bf = bf1.union(bf2)
  puts "并集测试:"
  %w[a c f h z].each do |item|
    puts "#{item}: #{union_bf.might_contain?(item) ? '可能存在' : '肯定不存在'}"
  end
  
  # 交集操作
  intersection_bf = bf1.intersection(bf2)
  puts "\n交集测试:"
  %w[a d f h].each do |item|
    puts "#{item}: #{intersection_bf.might_contain?(item) ? '可能存在' : '肯定不存在'}"
  end
  
  puts "\n=== 应用示例 ==="
  
  # URL去重器
  puts "\nURL去重器:"
  deduplicator = BloomFilterApplications::URLDeduplicator.new(10000, 0.01)
  
  urls = [
    "https://www.example.com/",
    "http://www.example.com",
    "https://www.google.com/search?q=ruby",
    "https://www.example.com/",  # 重复
    "https://github.com/ruby/ruby",
    "https://www.google.com/search?q=ruby"  # 重复
  ]
  
  urls.each do |url|
    is_new = deduplicator.process_url(url)
    puts "#{url}: #{is_new ? '新URL' : '可能重复'}"
  end
  
  puts "去重统计: #{deduplicator.statistics}"
  
  # 缓存穿透防护
  puts "\n缓存穿透防护:"
  guard = BloomFilterApplications::CachePenetrationGuard.new(1000)
  
  # 模拟缓存中的key
  cached_keys = %w[user:1 user:2 user:3 product:100 product:101]
  cached_keys.each { |key| guard.add_cache_key(key) }
  
  # 模拟查询
  queries = %w[user:1 user:999 product:100 product:999 order:1]
  queries.each do |key|
    should_check_cache = guard.check_cache_key(key)
    puts "查询#{key}: #{should_check_cache ? '检查缓存' : '跳过查询'}"
    
    # 模拟缓存未命中
    guard.record_cache_miss(key) unless should_check_cache
  end
  
  puts "防护统计: #{guard.statistics}"
  
  # 恶意IP检测
  puts "\n恶意IP检测:"
  detector = BloomFilterApplications::MaliciousIPDetector.new(1000)
  
  # 添加恶意IP
  malicious_ips = %w[192.168.1.100 10.0.0.50 172.16.0.200]
  detector.add_malicious_ips(malicious_ips)
  
  # 检测IP
  test_ips = %w[192.168.1.100 192.168.1.1 10.0.0.50 8.8.8.8 172.16.0.200]
  test_ips.each do |ip|
    is_malicious = detector.is_malicious?(ip)
    puts "IP #{ip}: #{is_malicious ? '可能恶意' : '安全'}"
  end
  
  puts "检测统计: #{detector.statistics}"
  
  puts "\n=== 性能测试 ==="
  
  # 大规模数据测试
  large_bf = BloomFilter.new(100000, 0.01)
  
  start_time = Time.now
  
  # 添加50000个元素
  50000.times do |i|
    large_bf.add("item_#{i}")
  end
  
  end_time = Time.now
  
  puts "添加50000个元素耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  puts "最终过滤器: #{large_bf}"
  
  # 查询性能测试
  start_time = Time.now
  
  hit_count = 0
  10000.times do |i|
    item = "item_#{rand(100000)}"
    hit_count += 1 if large_bf.might_contain?(item)
  end
  
  end_time = Time.now
  
  puts "10000次查询耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  puts "命中次数: #{hit_count}"
  
  # 误判率测试
  false_positives = 0
  test_count = 10000
  
  test_count.times do |i|
    # 测试不存在的元素
    item = "not_exist_#{i}"
    false_positives += 1 if large_bf.might_contain?(item)
  end
  
  actual_fpr = false_positives.to_f / test_count
  puts "\n误判率测试:"
  puts "预期误判率: #{large_bf.statistics[:expected_fpr]}"
  puts "实际误判率: #{actual_fpr.round(6)}"
  puts "测试样本: #{test_count}"
  puts "误判次数: #{false_positives}"
end