# 二叉搜索树 (Binary Search Tree, BST) 实现
# 
# 思路：
# 二叉搜索树是一种特殊的二叉树，满足以下性质：
# 1. 对于任意节点，其左子树中所有节点的值都小于该节点的值
# 2. 对于任意节点，其右子树中所有节点的值都大于该节点的值
# 3. 左右子树也都是二叉搜索树
# 
# 作用：
# 1. 快速搜索：平均时间复杂度O(log n)
# 2. 有序遍历：中序遍历得到有序序列
# 3. 动态维护有序集合
# 4. 范围查询：查找某个范围内的所有元素
# 
# 应用场景：
# 1. 数据库索引：B树的基础
# 2. 文件系统：目录结构的组织
# 3. 编译器：符号表的实现
# 4. 游戏开发：排行榜系统
# 5. 搜索引擎：倒排索引
# 6. 操作系统：进程调度、内存管理

require_relative 'binary_tree'

# 二叉搜索树类
class BinarySearchTree < BinaryTree
  def initialize
    super()
  end

  # 插入节点
  # 时间复杂度：平均 O(log n)，最坏 O(n)
  def insert(value)
    @root = insert_node(@root, value)
    @size += 1
    self
  end
  alias_method :<<, :insert
  alias_method :add, :insert

  # 删除节点
  # 时间复杂度：平均 O(log n)，最坏 O(n)
  def delete(value)
    initial_size = @size
    @root = delete_node(@root, value)
    @size -= 1 if @size > initial_size - 1
    self
  end
  alias_method :remove, :delete

  # 搜索节点
  # 时间复杂度：平均 O(log n)，最坏 O(n)
  def search(value, node = @root)
    return nil if node.nil?
    return node if node.value == value
    
    if value < node.value
      search(value, node.left)
    else
      search(value, node.right)
    end
  end
  alias_method :find, :search

  # 检查是否包含某个值
  # 时间复杂度：平均 O(log n)，最坏 O(n)
  def include?(value)
    !search(value).nil?
  end
  alias_method :contains?, :include?

  # 查找最小值
  # 时间复杂度：平均 O(log n)，最坏 O(n)
  def min(node = @root)
    return nil if node.nil?
    
    while node.left
      node = node.left
    end
    node.value
  end
  alias_method :minimum, :min

  # 查找最大值
  # 时间复杂度：平均 O(log n)，最坏 O(n)
  def max(node = @root)
    return nil if node.nil?
    
    while node.right
      node = node.right
    end
    node.value
  end
  alias_method :maximum, :max

  # 查找前驱节点（小于给定值的最大值）
  # 时间复杂度：平均 O(log n)，最坏 O(n)
  def predecessor(value)
    node = search(value)
    return nil if node.nil?
    
    # 如果有左子树，前驱是左子树的最大值
    if node.left
      return max(node.left)
    end
    
    # 否则，前驱是某个祖先节点
    predecessor = nil
    current = @root
    
    while current
      if value > current.value
        predecessor = current.value
        current = current.right
      elsif value < current.value
        current = current.left
      else
        break
      end
    end
    
    predecessor
  end

  # 查找后继节点（大于给定值的最小值）
  # 时间复杂度：平均 O(log n)，最坏 O(n)
  def successor(value)
    node = search(value)
    return nil if node.nil?
    
    # 如果有右子树，后继是右子树的最小值
    if node.right
      return min(node.right)
    end
    
    # 否则，后继是某个祖先节点
    successor = nil
    current = @root
    
    while current
      if value < current.value
        successor = current.value
        current = current.left
      elsif value > current.value
        current = current.right
      else
        break
      end
    end
    
    successor
  end

  # 范围查询：查找在[min_val, max_val]范围内的所有值
  # 时间复杂度：O(k + log n)，k为结果数量
  def range_search(min_val, max_val, node = @root, result = [])
    return result if node.nil?
    
    # 如果当前节点值在范围内，加入结果
    if node.value >= min_val && node.value <= max_val
      result << node.value
    end
    
    # 递归搜索左子树（如果可能有符合条件的值）
    if node.value > min_val
      range_search(min_val, max_val, node.left, result)
    end
    
    # 递归搜索右子树（如果可能有符合条件的值）
    if node.value < max_val
      range_search(min_val, max_val, node.right, result)
    end
    
    result.sort
  end

  # 查找第k小的元素（k从1开始）
  # 时间复杂度：O(n)
  def kth_smallest(k)
    return nil if k <= 0 || k > @size
    
    count = 0
    result = nil
    
    inorder_traversal do |value|
      count += 1
      if count == k
        result = value
        break
      end
    end
    
    result
  end

  # 查找第k大的元素（k从1开始）
  def kth_largest(k)
    kth_smallest(@size - k + 1)
  end

  # 验证是否为有效的二叉搜索树
  def valid_bst?(node = @root, min_val = nil, max_val = nil)
    return true if node.nil?
    
    # 检查当前节点是否违反BST性质
    return false if min_val && node.value <= min_val
    return false if max_val && node.value >= max_val
    
    # 递归检查左右子树
    valid_bst?(node.left, min_val, node.value) && 
    valid_bst?(node.right, node.value, max_val)
  end

  # 平衡因子（左子树高度 - 右子树高度）
  def balance_factor(node = @root)
    return 0 if node.nil?
    
    left_height = node.left ? height(node.left) : -1
    right_height = node.right ? height(node.right) : -1
    left_height - right_height
  end

  # 检查树是否平衡（所有节点的平衡因子都在[-1, 1]范围内）
  def balanced?(node = @root)
    return true if node.nil?
    
    bf = balance_factor(node)
    return false if bf.abs > 1
    
    balanced?(node.left) && balanced?(node.right)
  end

  # 从有序数组构建平衡BST
  def self.from_sorted_array(array)
    bst = BinarySearchTree.new
    bst.instance_variable_set(:@root, build_balanced_bst(array, 0, array.length - 1))
    bst.instance_variable_set(:@size, array.length)
    bst
  end

  # 转换为有序数组
  def to_sorted_array
    inorder_traversal
  end

  # 重新平衡树
  def rebalance!
    sorted_values = to_sorted_array
    @root = self.class.build_balanced_bst(sorted_values, 0, sorted_values.length - 1)
    self
  end

  # 返回平衡后的新树
  def rebalance
    self.class.from_sorted_array(to_sorted_array)
  end

  # 计算树的不平衡程度
  def imbalance_score(node = @root)
    return 0 if node.nil?
    
    bf = balance_factor(node).abs
    left_score = imbalance_score(node.left)
    right_score = imbalance_score(node.right)
    
    bf + left_score + right_score
  end

  private

  # 插入节点的递归实现
  def insert_node(node, value)
    return TreeNode.new(value) if node.nil?
    
    if value < node.value
      node.left = insert_node(node.left, value)
    elsif value > node.value
      node.right = insert_node(node.right, value)
    end
    # 如果值相等，不插入重复值
    
    node
  end

  # 删除节点的递归实现
  def delete_node(node, value)
    return node if node.nil?
    
    if value < node.value
      node.left = delete_node(node.left, value)
    elsif value > node.value
      node.right = delete_node(node.right, value)
    else
      # 找到要删除的节点
      
      # 情况1：叶子节点
      if node.left.nil? && node.right.nil?
        return nil
      end
      
      # 情况2：只有一个子节点
      if node.left.nil?
        return node.right
      elsif node.right.nil?
        return node.left
      end
      
      # 情况3：有两个子节点
      # 找到右子树的最小值（后继节点）
      successor_value = min(node.right)
      node.value = successor_value
      node.right = delete_node(node.right, successor_value)
    end
    
    node
  end

  # 从有序数组构建平衡BST的递归实现
  def self.build_balanced_bst(array, start, end_idx)
    return nil if start > end_idx
    
    mid = (start + end_idx) / 2
    node = TreeNode.new(array[mid])
    
    node.left = build_balanced_bst(array, start, mid - 1)
    node.right = build_balanced_bst(array, mid + 1, end_idx)
    
    node
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== BinarySearchTree 使用示例 ==="
  
  # 创建BST并插入数据
  bst = BinarySearchTree.new
  values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
  
  puts "插入值: #{values}"
  values.each { |val| bst.insert(val) }
  
  puts "\nBST结构:"
  bst.print_tree
  
  puts "\n基本信息:"
  puts "节点数: #{bst.size}"
  puts "高度: #{bst.height}"
  puts "是否为有效BST: #{bst.valid_bst?}"
  puts "是否平衡: #{bst.balanced?}"
  puts "不平衡分数: #{bst.imbalance_score}"
  
  puts "\n查找操作:"
  puts "最小值: #{bst.min}"
  puts "最大值: #{bst.max}"
  puts "查找40: #{bst.search(40) ? '找到' : '未找到'}"
  puts "查找90: #{bst.search(90) ? '找到' : '未找到'}"
  
  puts "\n前驱和后继:"
  puts "40的前驱: #{bst.predecessor(40)}"
  puts "40的后继: #{bst.successor(40)}"
  
  puts "\n排序和选择:"
  puts "有序遍历: #{bst.inorder_traversal}"
  puts "第3小的元素: #{bst.kth_smallest(3)}"
  puts "第3大的元素: #{bst.kth_largest(3)}"
  
  puts "\n范围查询:"
  puts "[25, 55]范围内的值: #{bst.range_search(25, 55)}"
  
  puts "\n删除操作:"
  puts "删除30前: #{bst.inorder_traversal}"
  bst.delete(30)
  puts "删除30后: #{bst.inorder_traversal}"
  
  puts "\n=== 平衡BST示例 ==="
  
  # 从有序数组构建平衡BST
  sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  balanced_bst = BinarySearchTree.from_sorted_array(sorted_array)
  
  puts "从有序数组构建的平衡BST:"
  balanced_bst.print_tree
  puts "是否平衡: #{balanced_bst.balanced?}"
  puts "高度: #{balanced_bst.height}"
  
  # 重新平衡不平衡的树
  puts "\n重新平衡原BST:"
  rebalanced_bst = bst.rebalance
  rebalanced_bst.print_tree
  puts "重新平衡后高度: #{rebalanced_bst.height}"
end