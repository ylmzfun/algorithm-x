#!/usr/bin/env ruby
# 数据结构使用示例和应用场景演示
# 
# 本文件展示了各种数据结构在实际业务场景中的应用，
# 包括电商系统、社交网络、缓存系统、搜索引擎等。

require_relative '../lib/linear/array_list'
require_relative '../lib/linear/linked_list'
require_relative '../lib/linear/stack'
require_relative '../lib/linear/queue'
require_relative '../lib/tree/binary_tree'
require_relative '../lib/tree/bst'
require_relative '../lib/tree/heap'
require_relative '../lib/graph/graph'
require_relative '../lib/graph/weighted_graph'
require_relative '../lib/hash/hash_table'
require_relative '../lib/hash/bloom_filter'

# 电商系统示例
module ECommerceSystem
  # 购物车实现（使用ArrayList）
  class ShoppingCart
    def initialize
      @items = ArrayList.new
      @total_amount = 0
    end

    def add_item(product_id, name, price, quantity = 1)
      item = {
        product_id: product_id,
        name: name,
        price: price,
        quantity: quantity,
        subtotal: price * quantity
      }
      @items.add(item)
      @total_amount += item[:subtotal]
      puts "已添加 #{name} x#{quantity} 到购物车"
    end

    def remove_item(index)
      if index >= 0 && index < @items.size
        item = @items.delete(index)
        @total_amount -= item[:subtotal]
        puts "已移除 #{item[:name]} 从购物车"
        item
      end
    end

    def update_quantity(index, new_quantity)
      if index >= 0 && index < @items.size
        item = @items.get(index)
        old_subtotal = item[:subtotal]
        item[:quantity] = new_quantity
        item[:subtotal] = item[:price] * new_quantity
        @total_amount = @total_amount - old_subtotal + item[:subtotal]
        @items.set(index, item)
      end
    end

    def checkout
      puts "\n=== 购物车结算 ==="
      @items.each_with_index do |item, index|
        puts "#{index + 1}. #{item[:name]} x#{item[:quantity]} = ¥#{item[:subtotal]}"
      end
      puts "总计: ¥#{@total_amount}"
      @total_amount
    end

    def clear
      @items.clear
      @total_amount = 0
      puts "购物车已清空"
    end

    def size
      @items.size
    end
  end

  # 订单处理系统（使用Queue）
  class OrderProcessor
    def initialize
      @pending_orders = Queue.new
      @processing_orders = Queue.new
      @completed_orders = ArrayList.new
      @order_id_counter = 1
    end

    def place_order(customer_id, items, total_amount)
      order = {
        id: @order_id_counter,
        customer_id: customer_id,
        items: items,
        total_amount: total_amount,
        status: 'pending',
        created_at: Time.now
      }
      @order_id_counter += 1
      @pending_orders.enqueue(order)
      puts "订单 ##{order[:id]} 已提交，等待处理"
      order[:id]
    end

    def process_next_order
      return nil if @pending_orders.empty?
      
      order = @pending_orders.dequeue
      order[:status] = 'processing'
      order[:processing_started_at] = Time.now
      @processing_orders.enqueue(order)
      puts "开始处理订单 ##{order[:id]}"
      order
    end

    def complete_order
      return nil if @processing_orders.empty?
      
      order = @processing_orders.dequeue
      order[:status] = 'completed'
      order[:completed_at] = Time.now
      @completed_orders.add(order)
      puts "订单 ##{order[:id]} 处理完成"
      order
    end

    def get_order_status(order_id)
      # 在各个队列中查找订单
      [@pending_orders, @processing_orders].each do |queue|
        queue.each do |order|
          return order[:status] if order[:id] == order_id
        end
      end
      
      @completed_orders.each do |order|
        return order[:status] if order[:id] == order_id
      end
      
      'not_found'
    end

    def statistics
      {
        pending: @pending_orders.size,
        processing: @processing_orders.size,
        completed: @completed_orders.size,
        total: @order_id_counter - 1
      }
    end
  end

  # 商品分类系统（使用BST）
  class ProductCatalog
    def initialize
      @categories = BinarySearchTree.new
      @products_by_category = HashTable.new
    end

    def add_category(category_id, name, parent_id = nil)
      category = {
        id: category_id,
        name: name,
        parent_id: parent_id,
        product_count: 0
      }
      @categories.insert(category_id, category)
      @products_by_category.put(category_id, ArrayList.new)
      puts "分类 '#{name}' 已添加"
    end

    def add_product(product_id, name, price, category_id)
      if @categories.search(category_id)
        product = {
          id: product_id,
          name: name,
          price: price,
          category_id: category_id
        }
        
        products = @products_by_category.get(category_id)
        products.add(product)
        
        # 更新分类商品数量
        category = @categories.search(category_id)
        category[:product_count] += 1
        
        puts "商品 '#{name}' 已添加到分类 #{category_id}"
      else
        puts "分类 #{category_id} 不存在"
      end
    end

    def get_products_by_category(category_id)
      @products_by_category.get(category_id) || ArrayList.new
    end

    def search_products_by_price_range(category_id, min_price, max_price)
      products = get_products_by_category(category_id)
      result = ArrayList.new
      
      products.each do |product|
        if product[:price] >= min_price && product[:price] <= max_price
          result.add(product)
        end
      end
      
      result
    end

    def get_category_tree
      result = []
      @categories.inorder_traversal { |id, category| result << category }
      result.sort_by { |cat| cat[:id] }
    end
  end
end

# 社交网络系统示例
module SocialNetwork
  # 用户关系图（使用Graph）
  class UserNetwork
    def initialize
      @network = Graph.new(false)  # 无向图表示双向关系
      @user_profiles = HashTable.new
    end

    def add_user(user_id, name, email)
      @network.add_vertex(user_id)
      profile = {
        id: user_id,
        name: name,
        email: email,
        friends_count: 0,
        joined_at: Time.now
      }
      @user_profiles.put(user_id, profile)
      puts "用户 #{name} 已加入网络"
    end

    def add_friendship(user1_id, user2_id)
      if @network.add_edge(user1_id, user2_id)
        # 更新好友数量
        @user_profiles.get(user1_id)[:friends_count] += 1
        @user_profiles.get(user2_id)[:friends_count] += 1
        
        user1_name = @user_profiles.get(user1_id)[:name]
        user2_name = @user_profiles.get(user2_id)[:name]
        puts "#{user1_name} 和 #{user2_name} 成为好友"
        true
      else
        false
      end
    end

    def get_friends(user_id)
      neighbors = @network.neighbors(user_id)
      friends = []
      neighbors.each do |neighbor|
        profile = @user_profiles.get(neighbor.id)
        friends << profile if profile
      end
      friends
    end

    def find_mutual_friends(user1_id, user2_id)
      friends1 = Set.new(@network.neighbors(user1_id).map(&:id))
      friends2 = Set.new(@network.neighbors(user2_id).map(&:id))
      mutual_ids = friends1.intersection(friends2)
      
      mutual_friends = []
      mutual_ids.each do |id|
        profile = @user_profiles.get(id)
        mutual_friends << profile if profile
      end
      mutual_friends
    end

    def find_shortest_connection(user1_id, user2_id)
      path = @network.find_path(user1_id, user2_id)
      if path.empty?
        puts "#{user1_id} 和 #{user2_id} 之间没有连接"
        []
      else
        user_names = path.map { |id| @user_profiles.get(id)[:name] }
        puts "连接路径: #{user_names.join(' -> ')}"
        path
      end
    end

    def suggest_friends(user_id, max_suggestions = 5)
      user_friends = Set.new(@network.neighbors(user_id).map(&:id))
      suggestions = HashTable.new
      
      # 基于共同好友推荐
      user_friends.each do |friend_id|
        friend_friends = @network.neighbors(friend_id)
        friend_friends.each do |potential_friend|
          next if potential_friend.id == user_id
          next if user_friends.include?(potential_friend.id)
          
          count = suggestions.get(potential_friend.id) || 0
          suggestions.put(potential_friend.id, count + 1)
        end
      end
      
      # 按共同好友数量排序
      sorted_suggestions = suggestions.entries.sort_by { |id, count| -count }
      result = []
      
      sorted_suggestions.first(max_suggestions).each do |id, mutual_count|
        profile = @user_profiles.get(id)
        result << {
          user: profile,
          mutual_friends_count: mutual_count
        }
      end
      
      result
    end

    def network_statistics
      {
        total_users: @network.vertex_count,
        total_friendships: @network.edge_count,
        average_friends: @network.vertex_count > 0 ? (@network.edge_count * 2.0 / @network.vertex_count).round(2) : 0,
        is_connected: @network.connected?
      }
    end
  end

  # 动态消息流（使用Heap实现优先级队列）
  class NewsFeed
    def initialize
      @posts = MaxHeap.new  # 按时间戳和优先级排序
      @user_feeds = HashTable.new
      @post_id_counter = 1
    end

    def create_post(user_id, content, priority = 1)
      post = {
        id: @post_id_counter,
        user_id: user_id,
        content: content,
        priority: priority,
        timestamp: Time.now.to_f,
        likes: 0,
        comments: []
      }
      @post_id_counter += 1
      
      # 使用组合分数：优先级 * 1000 + 时间戳的小数部分
      score = priority * 1000 + (post[:timestamp] % 1000)
      @posts.insert(score, post)
      
      puts "用户 #{user_id} 发布了新动态"
      post[:id]
    end

    def get_top_posts(count = 10)
      top_posts = []
      temp_heap = MaxHeap.new
      
      # 取出前N个帖子
      count.times do
        break if @posts.empty?
        score, post = @posts.extract_max
        top_posts << post
        temp_heap.insert(score, post)
      end
      
      # 将帖子放回堆中
      while !temp_heap.empty?
        score, post = temp_heap.extract_max
        @posts.insert(score, post)
      end
      
      top_posts
    end

    def like_post(post_id)
      # 简化实现：在实际应用中需要更复杂的索引
      puts "帖子 #{post_id} 获得一个赞"
    end

    def add_comment(post_id, user_id, comment)
      puts "用户 #{user_id} 评论了帖子 #{post_id}: #{comment}"
    end
  end
end

# 缓存系统示例
module CacheSystem
  # 多级缓存系统
  class MultiLevelCache
    def initialize
      @l1_cache = HashTableApplications::LRUCache.new(100)    # L1缓存：100个条目
      @l2_cache = HashTableApplications::LRUCache.new(1000)   # L2缓存：1000个条目
      @bloom_filter = BloomFilter.new(10000, 0.01)            # 布隆过滤器
      @cache_stats = {
        l1_hits: 0, l1_misses: 0,
        l2_hits: 0, l2_misses: 0,
        db_queries: 0
      }
    end

    def get(key)
      # L1缓存查找
      value = @l1_cache.get(key)
      if value
        @cache_stats[:l1_hits] += 1
        return value
      end
      @cache_stats[:l1_misses] += 1
      
      # L2缓存查找
      value = @l2_cache.get(key)
      if value
        @cache_stats[:l2_hits] += 1
        @l1_cache.put(key, value)  # 提升到L1
        return value
      end
      @cache_stats[:l2_misses] += 1
      
      # 布隆过滤器检查
      unless @bloom_filter.might_contain?(key)
        return nil  # 肯定不存在
      end
      
      # 模拟数据库查询
      @cache_stats[:db_queries] += 1
      value = simulate_db_query(key)
      
      if value
        @l1_cache.put(key, value)
        @l2_cache.put(key, value)
        @bloom_filter.add(key)
      end
      
      value
    end

    def put(key, value)
      @l1_cache.put(key, value)
      @l2_cache.put(key, value)
      @bloom_filter.add(key)
    end

    def statistics
      total_requests = @cache_stats[:l1_hits] + @cache_stats[:l1_misses]
      l1_hit_rate = total_requests > 0 ? (@cache_stats[:l1_hits].to_f / total_requests * 100).round(2) : 0
      
      l2_requests = @cache_stats[:l2_hits] + @cache_stats[:l2_misses]
      l2_hit_rate = l2_requests > 0 ? (@cache_stats[:l2_hits].to_f / l2_requests * 100).round(2) : 0
      
      {
        l1_hit_rate: "#{l1_hit_rate}%",
        l2_hit_rate: "#{l2_hit_rate}%",
        db_queries: @cache_stats[:db_queries],
        total_requests: total_requests
      }
    end

    private

    def simulate_db_query(key)
      # 模拟数据库查询延迟
      sleep(0.001)
      
      # 模拟50%的命中率
      rand < 0.5 ? "value_for_#{key}" : nil
    end
  end
end

# 搜索引擎示例
module SearchEngine
  # 倒排索引（使用HashTable和ArrayList）
  class InvertedIndex
    def initialize
      @index = HashTable.new
      @documents = HashTable.new
      @doc_id_counter = 1
    end

    def add_document(title, content)
      doc_id = @doc_id_counter
      @doc_id_counter += 1
      
      document = {
        id: doc_id,
        title: title,
        content: content,
        word_count: 0
      }
      
      @documents.put(doc_id, document)
      
      # 分词并建立索引
      words = tokenize("#{title} #{content}")
      document[:word_count] = words.size
      
      words.each do |word|
        if @index.has_key?(word)
          doc_list = @index.get(word)
        else
          doc_list = ArrayList.new
          @index.put(word, doc_list)
        end
        
        # 避免重复添加同一文档
        unless doc_list.any? { |doc_info| doc_info[:doc_id] == doc_id }
          doc_list.add({
            doc_id: doc_id,
            frequency: words.count(word)
          })
        end
      end
      
      puts "文档 '#{title}' 已索引 (ID: #{doc_id})"
      doc_id
    end

    def search(query)
      words = tokenize(query)
      return [] if words.empty?
      
      # 获取包含查询词的文档
      candidate_docs = Set.new
      word_doc_lists = []
      
      words.each do |word|
        doc_list = @index.get(word)
        if doc_list
          word_doc_lists << doc_list
          doc_list.each { |doc_info| candidate_docs.add(doc_info[:doc_id]) }
        end
      end
      
      return [] if candidate_docs.empty?
      
      # 计算文档相关性分数
      scored_docs = []
      candidate_docs.each do |doc_id|
        score = calculate_relevance_score(doc_id, words, word_doc_lists)
        document = @documents.get(doc_id)
        
        scored_docs << {
          document: document,
          score: score
        }
      end
      
      # 按分数排序
      scored_docs.sort_by { |item| -item[:score] }
    end

    def get_word_statistics(word)
      doc_list = @index.get(word)
      return nil unless doc_list
      
      {
        word: word,
        document_frequency: doc_list.size,
        total_frequency: doc_list.sum { |doc_info| doc_info[:frequency] }
      }
    end

    def index_statistics
      {
        total_documents: @documents.size,
        total_words: @index.size,
        average_doc_length: calculate_average_doc_length
      }
    end

    private

    def tokenize(text)
      text.downcase.scan(/\w+/).reject { |word| word.length < 2 }
    end

    def calculate_relevance_score(doc_id, query_words, word_doc_lists)
      score = 0
      
      query_words.each_with_index do |word, index|
        doc_list = word_doc_lists[index]
        next unless doc_list
        
        doc_info = doc_list.find { |info| info[:doc_id] == doc_id }
        if doc_info
          # 简单的TF-IDF近似
          tf = doc_info[:frequency]
          idf = Math.log(@documents.size.to_f / doc_list.size)
          score += tf * idf
        end
      end
      
      score
    end

    def calculate_average_doc_length
      return 0 if @documents.size == 0
      
      total_words = 0
      @documents.each { |doc_id, doc| total_words += doc[:word_count] }
      (total_words.to_f / @documents.size).round(2)
    end
  end
end

# 运行示例
if __FILE__ == $0
  puts "=== 数据结构应用示例演示 ==="
  
  puts "\n=== 电商系统示例 ==="
  
  # 购物车演示
  puts "\n1. 购物车系统:"
  cart = ECommerceSystem::ShoppingCart.new
  cart.add_item(1, "iPhone 15", 6999, 1)
  cart.add_item(2, "AirPods Pro", 1999, 2)
  cart.add_item(3, "MacBook Pro", 15999, 1)
  cart.checkout
  
  # 订单处理演示
  puts "\n2. 订单处理系统:"
  processor = ECommerceSystem::OrderProcessor.new
  
  order1_id = processor.place_order("user123", ["iPhone", "AirPods"], 8998)
  order2_id = processor.place_order("user456", ["MacBook"], 15999)
  order3_id = processor.place_order("user789", ["iPad"], 3999)
  
  puts "处理队列状态: #{processor.statistics}"
  
  processor.process_next_order
  processor.complete_order
  processor.process_next_order
  
  puts "处理后状态: #{processor.statistics}"
  puts "订单 #{order1_id} 状态: #{processor.get_order_status(order1_id)}"
  
  # 商品分类演示
  puts "\n3. 商品分类系统:"
  catalog = ECommerceSystem::ProductCatalog.new
  
  catalog.add_category(1, "电子产品")
  catalog.add_category(2, "手机", 1)
  catalog.add_category(3, "电脑", 1)
  
  catalog.add_product(101, "iPhone 15", 6999, 2)
  catalog.add_product(102, "Samsung Galaxy", 5999, 2)
  catalog.add_product(103, "MacBook Pro", 15999, 3)
  catalog.add_product(104, "ThinkPad", 8999, 3)
  
  phones = catalog.search_products_by_price_range(2, 5000, 7000)
  puts "价格在5000-7000的手机: #{phones.size}个"
  
  puts "\n=== 社交网络示例 ==="
  
  # 用户网络演示
  puts "\n1. 用户关系网络:"
  network = SocialNetwork::UserNetwork.new
  
  # 添加用户
  network.add_user("alice", "Alice", "alice@example.com")
  network.add_user("bob", "Bob", "bob@example.com")
  network.add_user("charlie", "Charlie", "charlie@example.com")
  network.add_user("diana", "Diana", "diana@example.com")
  network.add_user("eve", "Eve", "eve@example.com")
  
  # 建立好友关系
  network.add_friendship("alice", "bob")
  network.add_friendship("bob", "charlie")
  network.add_friendship("charlie", "diana")
  network.add_friendship("alice", "eve")
  network.add_friendship("eve", "diana")
  
  # 查找连接
  network.find_shortest_connection("alice", "diana")
  
  # 好友推荐
  suggestions = network.suggest_friends("alice", 3)
  puts "\n为Alice推荐的好友:"
  suggestions.each do |suggestion|
    puts "  #{suggestion[:user][:name]} (#{suggestion[:mutual_friends_count]}个共同好友)"
  end
  
  puts "\n网络统计: #{network.network_statistics}"
  
  # 动态消息流演示
  puts "\n2. 动态消息流:"
  feed = SocialNetwork::NewsFeed.new
  
  feed.create_post("alice", "今天天气真好！", 1)
  feed.create_post("bob", "刚看了一部很棒的电影", 2)
  feed.create_post("charlie", "重要公告：新产品发布", 5)
  feed.create_post("diana", "分享一张美食照片", 1)
  
  puts "\n热门动态:"
  top_posts = feed.get_top_posts(3)
  top_posts.each_with_index do |post, index|
    puts "#{index + 1}. 用户#{post[:user_id]}: #{post[:content]}"
  end
  
  puts "\n=== 缓存系统示例 ==="
  
  cache = CacheSystem::MultiLevelCache.new
  
  # 模拟缓存访问
  puts "\n缓存访问测试:"
  test_keys = %w[user:1 user:2 user:3 user:1 user:4 user:2 user:5]
  
  test_keys.each do |key|
    value = cache.get(key)
    puts "#{key}: #{value || 'miss'}"
  end
  
  puts "\n缓存统计: #{cache.statistics}"
  
  puts "\n=== 搜索引擎示例 ==="
  
  search_engine = SearchEngine::InvertedIndex.new
  
  # 添加文档
  search_engine.add_document("Ruby编程指南", "Ruby是一种动态编程语言，具有简洁的语法和强大的功能")
  search_engine.add_document("Python入门教程", "Python是一种易学的编程语言，广泛用于数据科学和Web开发")
  search_engine.add_document("数据结构与算法", "学习数据结构和算法对编程能力的提升非常重要")
  search_engine.add_document("Web开发实战", "使用Ruby on Rails进行Web应用开发的实践指南")
  
  # 搜索测试
  puts "\n搜索结果:"
  queries = ["编程语言", "Ruby", "数据结构", "Web开发"]
  
  queries.each do |query|
    puts "\n搜索 '#{query}':"
    results = search_engine.search(query)
    
    if results.empty?
      puts "  没有找到相关文档"
    else
      results.first(3).each_with_index do |result, index|
        doc = result[:document]
        score = result[:score].round(2)
        puts "  #{index + 1}. #{doc[:title]} (相关度: #{score})"
      end
    end
  end
  
  puts "\n索引统计: #{search_engine.index_statistics}"
  
  # 词汇统计
  word_stats = search_engine.get_word_statistics("编程")
  puts "词汇'编程'统计: #{word_stats}" if word_stats
  
  puts "\n=== 性能对比测试 ==="
  
  # 不同数据结构的性能对比
  puts "\n数据结构性能对比 (10000次操作):"
  
  # ArrayList vs LinkedList 插入性能
  array_list = ArrayList.new
  linked_list = LinkedList.new
  
  start_time = Time.now
  10000.times { |i| array_list.add(i) }
  array_time = Time.now - start_time
  
  start_time = Time.now
  10000.times { |i| linked_list.append(i) }
  linked_time = Time.now - start_time
  
  puts "ArrayList插入: #{(array_time * 1000).round(2)}ms"
  puts "LinkedList插入: #{(linked_time * 1000).round(2)}ms"
  
  # HashTable vs BST 查找性能
  hash_table = HashTable.new
  bst = BinarySearchTree.new
  
  # 预填充数据
  1000.times do |i|
    hash_table.put(i, "value_#{i}")
    bst.insert(i, "value_#{i}")
  end
  
  # 查找测试
  start_time = Time.now
  1000.times { |i| hash_table.get(rand(1000)) }
  hash_time = Time.now - start_time
  
  start_time = Time.now
  1000.times { |i| bst.search(rand(1000)) }
  bst_time = Time.now - start_time
  
  puts "HashTable查找: #{(hash_time * 1000).round(2)}ms"
  puts "BST查找: #{(bst_time * 1000).round(2)}ms"
  
  puts "\n=== 演示完成 ==="
  puts "\n本演示展示了各种数据结构在实际业务场景中的应用："
  puts "- ArrayList: 购物车、商品列表"
  puts "- Queue: 订单处理、任务调度"
  puts "- BST: 商品分类、有序数据"
  puts "- Graph: 社交网络、关系分析"
  puts "- HashTable: 缓存系统、快速查找"
  puts "- Heap: 优先级队列、热门内容"
  puts "- BloomFilter: 缓存优化、去重检测"
  puts "\n每种数据结构都有其特定的优势和适用场景，"
  puts "选择合适的数据结构对系统性能和可维护性至关重要。"
end