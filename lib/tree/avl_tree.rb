# frozen_string_literal: true

# AVL树（自平衡二叉搜索树）实现
#
# AVL树是一种自平衡的二叉搜索树，由Adelson-Velsky和Landis在1962年发明。
# 它保证任何节点的两个子树的高度差不超过1，从而确保树的平衡性。
#
# 特点：
# 1. 是一种二叉搜索树
# 2. 任何节点的左右子树高度差不超过1
# 3. 插入和删除操作会自动维护平衡
# 4. 查找、插入、删除的时间复杂度都是O(log n)
#
# 应用场景：
# 1. 需要频繁查找的数据结构
# 2. 数据库索引
# 3. 内存管理
# 4. 编译器中的符号表
# 5. 操作系统中的进程调度

# AVL树节点
class AVLNode
  attr_accessor :value, :left, :right, :height

  def initialize(value)
    @value = value
    @left = nil
    @right = nil
    @height = 1
  end

  def to_s
    "AVLNode(#{@value})"
  end
end

# AVL树实现
class AVLTree
  attr_reader :root, :size

  def initialize
    @root = nil
    @size = 0
  end

  # 插入值
  def insert(value)
    @root = insert_recursive(@root, value)
    @size += 1
  end

  # 删除值
  def delete(value)
    return false unless include?(value)
    
    @root = delete_recursive(@root, value)
    @size -= 1
    true
  end

  # 查找值
  def search(value)
    search_recursive(@root, value)
  end

  # 检查是否包含值
  def include?(value)
    !search(value).nil?
  end

  # 获取最小值
  def min
    return nil if @root.nil?

    find_min(@root).value
  end

  # 获取最大值
  def max
    return nil if @root.nil?

    find_max(@root).value
  end

  # 中序遍历（返回有序数组）
  def inorder_traversal
    result = []
    inorder_recursive(@root, result)
    result
  end

  # 前序遍历
  def preorder_traversal
    result = []
    preorder_recursive(@root, result)
    result
  end

  # 后序遍历
  def postorder_traversal
    result = []
    postorder_recursive(@root, result)
    result
  end

  # 层序遍历
  def level_order_traversal
    return [] if @root.nil?

    result = []
    queue = [@root]

    until queue.empty?
      node = queue.shift
      result << node.value

      queue << node.left if node.left
      queue << node.right if node.right
    end

    result
  end

  # 获取树的高度
  def height
    get_height(@root)
  end

  # 检查树是否为空
  def empty?
    @root.nil?
  end

  # 清空树
  def clear
    @root = nil
    @size = 0
  end

  # 获取平衡因子
  def balance_factor(node = @root)
    return 0 if node.nil?

    get_height(node.left) - get_height(node.right)
  end

  # 检查树是否平衡
  def balanced?
    check_balance(@root)
  end

  # 转换为数组
  def to_a
    inorder_traversal
  end

  # 打印树结构
  def print_tree
    return puts 'Empty tree' if @root.nil?

    print_tree_recursive(@root, '', true)
  end

  private

  # 递归插入
  def insert_recursive(node, value)
    # 标准BST插入
    if node.nil?
      return AVLNode.new(value)
    elsif value < node.value
      node.left = insert_recursive(node.left, value)
    elsif value > node.value
      node.right = insert_recursive(node.right, value)
    else
      # 值已存在，不插入重复值
      @size -= 1  # 撤销size增加
      return node
    end

    # 更新高度
    update_height(node)

    # 获取平衡因子
    balance = get_balance(node)

    # 执行旋转以维护平衡
    # Left Left Case
    if balance > 1 && value < node.left.value
      return rotate_right(node)
    end

    # Right Right Case
    if balance < -1 && value > node.right.value
      return rotate_left(node)
    end

    # Left Right Case
    if balance > 1 && value > node.left.value
      node.left = rotate_left(node.left)
      return rotate_right(node)
    end

    # Right Left Case
    if balance < -1 && value < node.right.value
      node.right = rotate_right(node.right)
      return rotate_left(node)
    end

    node
  end

  # 递归删除
  def delete_recursive(node, value)
    return node if node.nil?

    if value < node.value
      node.left = delete_recursive(node.left, value)
    elsif value > node.value
      node.right = delete_recursive(node.right, value)
    else
      # 找到要删除的节点
      if node.left.nil?
        return node.right
      elsif node.right.nil?
        return node.left
      else
        # 节点有两个子节点
        successor = find_min(node.right)
        node.value = successor.value
        node.right = delete_recursive(node.right, successor.value)
      end
    end

    return node if node.nil?

    # 更新高度
    update_height(node)

    # 获取平衡因子
    balance = get_balance(node)

    # 执行旋转以维护平衡
    # Left Left Case
    if balance > 1 && get_balance(node.left) >= 0
      return rotate_right(node)
    end

    # Left Right Case
    if balance > 1 && get_balance(node.left) < 0
      node.left = rotate_left(node.left)
      return rotate_right(node)
    end

    # Right Right Case
    if balance < -1 && get_balance(node.right) <= 0
      return rotate_left(node)
    end

    # Right Left Case
    if balance < -1 && get_balance(node.right) > 0
      node.right = rotate_right(node.right)
      return rotate_left(node)
    end

    node
  end

  # 递归查找
  def search_recursive(node, value)
    return nil if node.nil?
    return node if node.value == value

    if value < node.value
      search_recursive(node.left, value)
    else
      search_recursive(node.right, value)
    end
  end

  # 获取节点高度
  def get_height(node)
    return 0 if node.nil?

    node.height
  end

  # 更新节点高度
  def update_height(node)
    return if node.nil?

    node.height = [get_height(node.left), get_height(node.right)].max + 1
  end

  # 获取平衡因子
  def get_balance(node)
    return 0 if node.nil?

    get_height(node.left) - get_height(node.right)
  end

  # 右旋转
  def rotate_right(y)
    x = y.left
    t2 = x.right

    # 执行旋转
    x.right = y
    y.left = t2

    # 更新高度
    update_height(y)
    update_height(x)

    x
  end

  # 左旋转
  def rotate_left(x)
    y = x.right
    t2 = y.left

    # 执行旋转
    y.left = x
    x.right = t2

    # 更新高度
    update_height(x)
    update_height(y)

    y
  end

  # 查找最小值节点
  def find_min(node)
    while node.left
      node = node.left
    end
    node
  end

  # 查找最大值节点
  def find_max(node)
    while node.right
      node = node.right
    end
    node
  end

  # 中序遍历递归
  def inorder_recursive(node, result)
    return if node.nil?

    inorder_recursive(node.left, result)
    result << node.value
    inorder_recursive(node.right, result)
  end

  # 前序遍历递归
  def preorder_recursive(node, result)
    return if node.nil?

    result << node.value
    preorder_recursive(node.left, result)
    preorder_recursive(node.right, result)
  end

  # 后序遍历递归
  def postorder_recursive(node, result)
    return if node.nil?

    postorder_recursive(node.left, result)
    postorder_recursive(node.right, result)
    result << node.value
  end

  # 检查平衡性
  def check_balance(node)
    return true if node.nil?

    left_height = get_height(node.left)
    right_height = get_height(node.right)

    return false if (left_height - right_height).abs > 1

    check_balance(node.left) && check_balance(node.right)
  end

  # 打印树结构（递归）
  def print_tree_recursive(node, prefix, is_last)
    return if node.nil?

    puts "#{prefix}#{is_last ? '└── ' : '├── '}#{node.value} (h:#{node.height})"

    children = [node.left, node.right].compact
    children.each_with_index do |child, index|
      is_last_child = index == children.length - 1
      new_prefix = prefix + (is_last ? '    ' : '│   ')
      print_tree_recursive(child, new_prefix, is_last_child)
    end
  end
end

# AVL树应用示例
module AVLTreeApplications
  # 范围查询
  def self.range_query(avl_tree, min_val, max_val)
    result = []
    range_query_recursive(avl_tree.root, min_val, max_val, result)
    result
  end

  # 第k小元素
  def self.kth_smallest(avl_tree, k)
    return nil if k <= 0 || k > avl_tree.size

    sorted_values = avl_tree.inorder_traversal
    sorted_values[k - 1]
  end

  # 查找前驱
  def self.predecessor(avl_tree, value)
    node = avl_tree.search(value)
    return nil if node.nil?

    if node.left
      # 如果有左子树，前驱是左子树的最大值
      current = node.left
      current = current.right while current.right
      return current.value
    end

    # 否则向上查找
    predecessor_value = nil
    current = avl_tree.root

    while current
      if value > current.value
        predecessor_value = current.value
        current = current.right
      else
        current = current.left
      end
    end

    predecessor_value
  end

  # 查找后继
  def self.successor(avl_tree, value)
    node = avl_tree.search(value)
    return nil if node.nil?

    if node.right
      # 如果有右子树，后继是右子树的最小值
      current = node.right
      current = current.left while current.left
      return current.value
    end

    # 否则向上查找
    successor_value = nil
    current = avl_tree.root

    while current
      if value < current.value
        successor_value = current.value
        current = current.left
      else
        current = current.right
      end
    end

    successor_value
  end

  private

  def self.range_query_recursive(node, min_val, max_val, result)
    return if node.nil?

    # 如果当前节点值在范围内，添加到结果
    result << node.value if node.value >= min_val && node.value <= max_val

    # 递归搜索左子树（如果可能包含范围内的值）
    range_query_recursive(node.left, min_val, max_val, result) if node.value > min_val

    # 递归搜索右子树（如果可能包含范围内的值）
    range_query_recursive(node.right, min_val, max_val, result) if node.value < max_val
  end
end

# 使用示例
if __FILE__ == $PROGRAM_NAME
  puts "=== AVL树演示 ==="

  avl = AVLTree.new
  values = [10, 20, 30, 40, 50, 25]

  puts "插入值: #{values}"
  values.each { |val| avl.insert(val) }

  puts "\n树结构:"
  avl.print_tree

  puts "\n中序遍历: #{avl.inorder_traversal}"
  puts "树高度: #{avl.height}"
  puts "是否平衡: #{avl.balanced?}"
  puts "最小值: #{avl.min}, 最大值: #{avl.max}"

  puts "\n查找测试:"
  puts "查找25: #{avl.include?(25) ? '找到' : '未找到'}"
  puts "查找35: #{avl.include?(35) ? '找到' : '未找到'}"

  puts "\n删除30后:"
  avl.delete(30)
  puts "中序遍历: #{avl.inorder_traversal}"
  puts "是否平衡: #{avl.balanced?}"

  puts "\n应用示例:"
  puts "范围查询[20,40]: #{AVLTreeApplications.range_query(avl, 20, 40)}"
  puts "第2小的元素: #{AVLTreeApplications.kth_smallest(avl, 2)}"
  puts "25的前驱: #{AVLTreeApplications.predecessor(avl, 25)}"
  puts "25的后继: #{AVLTreeApplications.successor(avl, 25)}"
end