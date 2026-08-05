# encoding: utf-8
# 字典树 (Trie / Prefix Tree) 实现
#
# 思路：
# Trie 是一种树形数据结构，用于高效地存储和检索字符串集合。
# 每个节点表示一个字符，从根到某个节点的路径构成一个前缀。
# 共享相同前缀的字符串共享相同路径，节省空间并加速前缀查询。
#
# 作用：
# 1. 前缀匹配：快速查找以某前缀开头的所有字符串
# 2. 自动补全：搜索引擎、输入法中的联想功能
# 3. 拼写检查：快速检查单词是否在词典中
# 4. 字典序遍历：按字母顺序输出所有字符串
#
# 应用场景：
# 1. 搜索引擎：搜索建议、热词联想
# 2. 输入法：候选词提示
# 3. 拼写检查器：词典查找
# 4. IP 路由：最长前缀匹配（路由表）
# 5. 基因序列：DNA 序列匹配

class TrieNode
  attr_accessor :children, :is_end, :value, :count

  def initialize
    @children = {}  # 子节点映射：字符 -> TrieNode
    @is_end = false # 是否为某个单词的结尾
    @value = nil    # 存储的值（可选）
    @count = 0      # 以该节点为前缀的单词数量
  end
end

class Trie
  attr_reader :size

  def initialize
    @root = TrieNode.new
    @size = 0
  end

  # 插入单词
  # 时间复杂度：O(m)，m 为单词长度
  def insert(word, value = nil)
    node = @root
    word.each_char do |char|
      node.children[char] ||= TrieNode.new
      node = node.children[char]
      node.count += 1
    end
    @size += 1 unless node.is_end
    node.is_end = true
    node.value = value || word
    self
  end
  alias_method :<<, :insert
  alias_method :add, :insert

  # 批量插入
  def insert_all(words)
    words.each { |word| insert(word) }
    self
  end

  # 搜索完整单词
  # 时间复杂度：O(m)
  def search(word)
    node = find_node(word)
    node && node.is_end ? node.value : nil
  end

  # 检查是否包含完整单词
  def include?(word)
    node = find_node(word)
    !node.nil? && node.is_end
  end

  # 检查是否有以指定前缀开头的单词
  def starts_with?(prefix)
    !find_node(prefix).nil?
  end

  # 获取以指定前缀开头的所有单词
  def words_with_prefix(prefix)
    result = []
    node = find_node(prefix)
    return result if node.nil?

    collect_words(node, prefix, result)
    result
  end

  # 获取以指定前缀开头的单词数量
  def count_prefix(prefix)
    node = find_node(prefix)
    node ? node.count : 0
  end

  # 删除单词
  # 时间复杂度：O(m)
  def delete(word)
    return false unless include?(word)
    delete_helper(@root, word, 0)
    @size -= 1
    true
  end

  # 获取所有单词
  def all_words
    words_with_prefix("")
  end

  # 模糊搜索（支持 . 作为通配符，匹配任意单个字符）
  def fuzzy_search(pattern)
    result = []
    fuzzy_search_helper(@root, pattern, 0, "", result)
    result
  end

  # 获取最长公共前缀
  def longest_common_prefix
    return "" if @root.children.empty?

    prefix = ""
    node = @root

    loop do
      return prefix if node.children.size != 1 || node.is_end
      char = node.children.keys.first
      prefix += char
      node = node.children[char]
    end
  end

  # 检查是否为空
  def empty?
    @size == 0
  end

  # 清空
  def clear
    @root = TrieNode.new
    @size = 0
    self
  end

  # 获取单词数量
  def word_count
    @size
  end

  # 统计不同前缀数量
  def prefix_count
    count_nodes(@root) - 1  # 减去根节点
  end

  # 压缩 Trie（合并单子节点链，减少空间）
  def compress
    new_root = compress_node(@root)
    new_trie = Trie.new
    new_trie.instance_variable_set(:@root, new_root)
    new_trie.instance_variable_set(:@size, @size)
    new_trie
  end

  def to_s
    "Trie[words: #{@size}]"
  end

  def inspect
    "#<Trie:#{object_id} words=#{@size}>"
  end

  private

  # 查找节点
  def find_node(prefix)
    node = @root
    prefix.each_char do |char|
      return nil unless node.children.key?(char)
      node = node.children[char]
    end
    node
  end

  # 收集以某节点为根的所有单词
  def collect_words(node, prefix, result)
    result << prefix if node.is_end

    node.children.each do |char, child|
      collect_words(child, prefix + char, result)
    end
  end

  # 删除辅助方法
  def delete_helper(node, word, index)
    if index == word.length
      node.is_end = false
      return node.children.empty?
    end

    char = word[index]
    child = node.children[char]
    return false if child.nil?

    should_delete = delete_helper(child, word, index + 1)

    if should_delete
      child.count -= 1
      if child.children.empty? && !child.is_end
        node.children.delete(char)
        return node.children.empty? && !node.is_end
      end
    end

    false
  end

  # 模糊搜索辅助方法
  def fuzzy_search_helper(node, pattern, index, current, result)
    if index == pattern.length
      result << current if node.is_end
      return
    end

    char = pattern[index]
    if char == '.'
      node.children.each do |child_char, child|
        fuzzy_search_helper(child, pattern, index + 1, current + child_char, result)
      end
    elsif node.children.key?(char)
      fuzzy_search_helper(node.children[char], pattern, index + 1, current + char, result)
    end
  end

  # 统计节点数
  def count_nodes(node)
    return 0 if node.nil?
    count = 1
    node.children.each_value { |child| count += count_nodes(child) }
    count
  end

  # 压缩节点
  def compress_node(node)
    return nil if node.nil?

    new_node = TrieNode.new
    new_node.is_end = node.is_end
    new_node.value = node.value
    new_node.count = node.count

    node.children.each do |char, child|
      compressed = compress_node(child)
      # 如果子节点只有一个子节点且不是单词结尾，可以合并
      if compressed && !compressed.is_end && compressed.children.size == 1
        grandchild_char = compressed.children.keys.first
        grandchild = compressed.children.values.first
        new_node.children[char + grandchild_char] = grandchild
      else
        new_node.children[char] = compressed
      end
    end
    new_node
  end
end

# Trie 应用示例
module TrieApplications
  # 自动补全系统
  class Autocomplete
    def initialize(words = [])
      @trie = Trie.new
      words.each { |word| @trie.insert(word) }
    end

    def add_word(word)
      @trie.insert(word)
    end

    def suggest(prefix, limit = 10)
      @trie.words_with_prefix(prefix).first(limit)
    end

    def word_count
      @trie.size
    end
  end

  # 拼写检查器
  class SpellChecker
    def initialize(dictionary)
      @trie = Trie.new
      dictionary.each { |word| @trie.insert(word.downcase) }
    end

    def correct?(word)
      @trie.include?(word.downcase)
    end

    def suggest(word)
      word = word.downcase
      return [word] if @trie.include?(word)

      suggestions = []
      # 尝试相同前缀
      (1...word.length).reverse_each do |i|
        prefix = word[0...i]
        matches = @trie.words_with_prefix(prefix)
        suggestions.concat(matches) unless matches.empty?
        break if suggestions.size >= 5
      end
      suggestions.first(5)
    end
  end

  # IP 路由表（最长前缀匹配）
  class IPRouter
    def initialize
      @trie = Trie.new
    end

    def add_route(prefix, gateway)
      @trie.insert(prefix, gateway)
    end

    def lookup(ip)
      binary = ip_to_binary(ip)
      longest_match = nil
      longest_len = -1

      (1..binary.length).each do |len|
        prefix = binary[0...len]
        if @trie.starts_with?(prefix)
          node = @trie.send(:find_node, prefix)
          if node&.is_end
            longest_match = node.value
            longest_len = len
          end
        end
      end
      longest_match
    end

    private

    def ip_to_binary(ip)
      ip.split('.').map { |octet| octet.to_i.to_s(2).rjust(8, '0') }.join
    end
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== Trie 字典树演示 ==="

  trie = Trie.new
  words = %w[hello world hell help heap hero her here helm]
  trie.insert_all(words)

  puts "插入单词: #{words}"
  puts "单词数量: #{trie.size}"

  puts "\n搜索测试:"
  puts "包含 'hello': #{trie.include?('hello')}"
  puts "包含 'world': #{trie.include?('world')}"
  puts "包含 'heaven': #{trie.include?('heaven')}"

  puts "\n前缀搜索:"
  puts "以 'he' 开头: #{trie.words_with_prefix('he')}"
  puts "以 'hel' 开头: #{trie.words_with_prefix('hel')}"
  puts "以 'wo' 开头: #{trie.words_with_prefix('wo')}"
  puts "前缀 'he' 的单词数: #{trie.count_prefix('he')}"

  puts "\n模糊搜索:"
  puts "模式 'he..': #{trie.fuzzy_search('he..')}"
  puts "模式 'h...': #{trie.fuzzy_search('h...')}"

  puts "\n最长公共前缀: #{trie.longest_common_prefix}"

  puts "\n删除 'hello'..."
  trie.delete('hello')
  puts "包含 'hello': #{trie.include?('hello')}"
  puts "以 'hel' 开头: #{trie.words_with_prefix('hel')}"
  puts "单词数量: #{trie.size}"

  puts "\n=== 自动补全示例 ==="
  autocomplete = TrieApplications::Autocomplete.new(%w[
    apple application append apply
    banana band banner
    cat catalog catch
  ])

  puts "输入 'app' 的建议: #{autocomplete.suggest('app')}"
  puts "输入 'ba' 的建议: #{autocomplete.suggest('ba')}"
  puts "输入 'cat' 的建议: #{autocomplete.suggest('cat')}"

  puts "\n=== 拼写检查示例 ==="
  checker = TrieApplications::SpellChecker.new(%w[hello world help hero her])
  puts "正确拼写 'hello': #{checker.correct?('hello')}"
  puts "正确拼写 'he1lo': #{checker.correct?('he1lo')}"
  puts "对 'he1lo' 的建议: #{checker.suggest('he1lo')}"
end
