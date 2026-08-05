# 二叉树 (Binary Tree) 实现
# 
# 思路：
# 二叉树是一种树形数据结构，每个节点最多有两个子节点，通常称为左子节点和右子节点。
# 二叉树具有递归的性质，每个子树也是一个二叉树。
# 
# 作用：
# 1. 层次化数据组织：文件系统、组织架构
# 2. 表达式解析：数学表达式的语法树
# 3. 决策过程：决策树算法
# 4. 搜索和排序：二叉搜索树的基础
# 5. 堆的实现：优先队列的底层结构
# 
# 应用场景：
# 1. 编译器：抽象语法树(AST)
# 2. 数据库：B树索引的基础
# 3. 游戏开发：场景图、碰撞检测
# 4. 机器学习：决策树、随机森林
# 5. 网络路由：路由表的组织
# 6. 图形学：空间分割树

# 二叉树节点类
class TreeNode
  attr_accessor :value, :left, :right

  def initialize(value, left = nil, right = nil)
    @value = value
    @left = left
    @right = right
  end

  # 检查是否为叶子节点
  def leaf?
    @left.nil? && @right.nil?
  end

  # 检查是否有左子节点
  def has_left?
    !@left.nil?
  end

  # 检查是否有右子节点
  def has_right?
    !@right.nil?
  end

  # 获取子节点数量
  def children_count
    count = 0
    count += 1 if @left
    count += 1 if @right
    count
  end

  def to_s
    @value.to_s
  end

  def inspect
    "#<TreeNode:#{object_id} value=#{@value.inspect} left=#{@left ? @left.value : 'nil'} right=#{@right ? @right.value : 'nil'}>"
  end
end

# 二叉树类
class BinaryTree
  attr_accessor :root
  attr_reader :size

  def initialize(root_value = nil)
    @root = root_value ? TreeNode.new(root_value) : nil
    @size = @root ? 1 : 0
  end

  # 检查树是否为空
  def empty?
    @root.nil?
  end

  # 清空树
  def clear
    @root = nil
    @size = 0
    self
  end

  # 计算树的高度（深度）
  # 时间复杂度：O(n)
  def height(node = @root)
    return -1 if node.nil?  # 空树高度为-1
    return 0 if node.leaf?  # 叶子节点高度为0
    
    left_height = height(node.left)
    right_height = height(node.right)
    [left_height, right_height].max + 1
  end
  alias_method :depth, :height

  # 计算树的节点数量
  # 时间复杂度：O(n)
  def count_nodes(node = @root)
    return 0 if node.nil?
    1 + count_nodes(node.left) + count_nodes(node.right)
  end

  # 计算叶子节点数量
  # 时间复杂度：O(n)
  def count_leaves(node = @root)
    return 0 if node.nil?
    return 1 if node.leaf?
    count_leaves(node.left) + count_leaves(node.right)
  end

  # 检查树是否平衡（每个节点的左右子树高度差不超过1）
  # 时间复杂度：O(n)
  def balanced?(node = @root)
    return true if node.nil?

    left_height = height(node.left)
    right_height = height(node.right)

    return false if (left_height - right_height).abs > 1

    balanced?(node.left) && balanced?(node.right)
  end
  alias_method :is_balanced?, :balanced?

  # 前序遍历 (根 -> 左 -> 右)
  # 时间复杂度：O(n)
  def preorder_traversal(node = @root, &block)
    result = []
    preorder_helper(node, result, &block)
    block_given? ? self : result
  end

  # 中序遍历 (左 -> 根 -> 右)
  # 时间复杂度：O(n)
  def inorder_traversal(node = @root, &block)
    result = []
    inorder_helper(node, result, &block)
    block_given? ? self : result
  end

  # 后序遍历 (左 -> 右 -> 根)
  # 时间复杂度：O(n)
  def postorder_traversal(node = @root, &block)
    result = []
    postorder_helper(node, result, &block)
    block_given? ? self : result
  end

  # 层序遍历（广度优先）
  # 时间复杂度：O(n)
  def level_order_traversal(&block)
    result = []
    return result if @root.nil?
    
    queue = [@root]
    
    while !queue.empty?
      node = queue.shift
      
      if block_given?
        yield node.value
      else
        result << node.value
      end
      
      queue << node.left if node.left
      queue << node.right if node.right
    end
    
    block_given? ? self : result
  end
  alias_method :breadth_first_traversal, :level_order_traversal

  # 按层级返回节点（每层一个数组）
  def level_order_by_levels
    return [] if @root.nil?
    
    result = []
    current_level = [@root]
    
    while !current_level.empty?
      level_values = current_level.map(&:value)
      result << level_values
      
      next_level = []
      current_level.each do |node|
        next_level << node.left if node.left
        next_level << node.right if node.right
      end
      
      current_level = next_level
    end
    
    result
  end

  # 查找节点
  # 时间复杂度：O(n)
  def find(value, node = @root)
    return nil if node.nil?
    return node if node.value == value
    
    # 在左子树中查找
    left_result = find(value, node.left)
    return left_result if left_result
    
    # 在右子树中查找
    find(value, node.right)
  end

  # 检查是否包含某个值
  def include?(value)
    !find(value).nil?
  end
  alias_method :contains?, :include?

  # 获取某个节点的路径（从根到该节点）
  def path_to(value, node = @root, current_path = [])
    return nil if node.nil?
    
    current_path = current_path + [node.value]
    
    return current_path if node.value == value
    
    # 在左子树中查找
    left_path = path_to(value, node.left, current_path)
    return left_path if left_path
    
    # 在右子树中查找
    path_to(value, node.right, current_path)
  end

  # 检查两个树是否相等
  def ==(other)
    return false unless other.is_a?(BinaryTree)
    trees_equal?(@root, other.root)
  end

  # 复制树
  def clone
    new_tree = BinaryTree.new
    new_tree.root = clone_node(@root)
    new_tree.instance_variable_set(:@size, @size)
    new_tree
  end
  alias_method :dup, :clone

  # 镜像翻转树
  def mirror!
    mirror_node!(@root)
    self
  end

  # 返回镜像树（不修改原树）
  def mirror
    clone.mirror!
  end

  # 检查是否为对称树
  def symmetric?
    return true if @root.nil?
    is_symmetric?(@root.left, @root.right)
  end

  # 获取最大宽度（某一层的最大节点数）
  def max_width
    return 0 if @root.nil?
    
    max_width = 0
    current_level = [@root]
    
    while !current_level.empty?
      max_width = [max_width, current_level.size].max
      
      next_level = []
      current_level.each do |node|
        next_level << node.left if node.left
        next_level << node.right if node.right
      end
      
      current_level = next_level
    end
    
    max_width
  end

  # 从数组构建完全二叉树
  def self.from_array(array)
    return BinaryTree.new if array.empty?
    
    tree = BinaryTree.new
    tree.root = build_from_array(array, 0)
    tree.instance_variable_set(:@size, array.size)
    tree
  end

  # 转换为数组（层序遍历）
  def to_a
    level_order_traversal
  end

  # 可视化打印树结构
  def print_tree(node = @root, prefix = "", is_last = true)
    return if node.nil?
    
    puts "#{prefix}#{is_last ? '└── ' : '├── '}#{node.value}"
    
    children = [node.left, node.right].compact
    children.each_with_index do |child, index|
      is_last_child = index == children.size - 1
      new_prefix = prefix + (is_last ? "    " : "│   ")
      print_tree(child, new_prefix, is_last_child)
    end
  end

  # 字符串表示
  def to_s
    return "BinaryTree[empty]" if empty?
    "BinaryTree[root: #{@root.value}, height: #{height}, nodes: #{count_nodes}]"
  end

  def inspect
    "#<BinaryTree:#{object_id} root=#{@root ? @root.value : 'nil'} size=#{@size}>"
  end

  private

  # 前序遍历辅助方法
  def preorder_helper(node, result, &block)
    return if node.nil?
    
    if block_given?
      yield node.value
    else
      result << node.value
    end
    
    preorder_helper(node.left, result, &block)
    preorder_helper(node.right, result, &block)
  end

  # 中序遍历辅助方法
  def inorder_helper(node, result, &block)
    return if node.nil?
    
    inorder_helper(node.left, result, &block)
    
    if block_given?
      yield node.value
    else
      result << node.value
    end
    
    inorder_helper(node.right, result, &block)
  end

  # 后序遍历辅助方法
  def postorder_helper(node, result, &block)
    return if node.nil?
    
    postorder_helper(node.left, result, &block)
    postorder_helper(node.right, result, &block)
    
    if block_given?
      yield node.value
    else
      result << node.value
    end
  end

  # 检查两个子树是否相等
  def trees_equal?(node1, node2)
    return true if node1.nil? && node2.nil?
    return false if node1.nil? || node2.nil?
    return false if node1.value != node2.value
    
    trees_equal?(node1.left, node2.left) && trees_equal?(node1.right, node2.right)
  end

  # 克隆节点
  def clone_node(node)
    return nil if node.nil?
    
    new_node = TreeNode.new(node.value)
    new_node.left = clone_node(node.left)
    new_node.right = clone_node(node.right)
    new_node
  end

  # 镜像翻转节点
  def mirror_node!(node)
    return if node.nil?
    
    node.left, node.right = node.right, node.left
    mirror_node!(node.left)
    mirror_node!(node.right)
  end

  # 检查是否对称
  def is_symmetric?(left, right)
    return true if left.nil? && right.nil?
    return false if left.nil? || right.nil?
    return false if left.value != right.value
    
    is_symmetric?(left.left, right.right) && is_symmetric?(left.right, right.left)
  end

  # 从数组构建树的辅助方法
  def self.build_from_array(array, index)
    return nil if index >= array.size || array[index].nil?
    
    node = TreeNode.new(array[index])
    node.left = build_from_array(array, 2 * index + 1)
    node.right = build_from_array(array, 2 * index + 2)
    node
  end
end

# 二叉树的实际应用示例
module BinaryTreeApplications
  # 表达式树
  class ExpressionTree < BinaryTree
    def initialize(expression = nil)
      super()
      build_from_postfix(expression) if expression
    end

    # 从后缀表达式构建表达式树
    def build_from_postfix(postfix_expr)
      stack = []
      operators = ['+', '-', '*', '/', '^']
      
      postfix_expr.split.each do |token|
        if operators.include?(token)
          right = stack.pop
          left = stack.pop
          node = TreeNode.new(token)
          node.left = left
          node.right = right
          stack.push(node)
        else
          stack.push(TreeNode.new(token.to_f))
        end
      end
      
      @root = stack.pop
    end

    # 计算表达式的值
    def evaluate(node = @root)
      return node.value if node.leaf?
      
      left_val = evaluate(node.left)
      right_val = evaluate(node.right)
      
      case node.value
      when '+'
        left_val + right_val
      when '-'
        left_val - right_val
      when '*'
        left_val * right_val
      when '/'
        left_val / right_val
      when '^'
        left_val ** right_val
      end
    end

    # 转换为中缀表达式
    def to_infix(node = @root)
      return node.value.to_s if node.leaf?
      
      left_expr = to_infix(node.left)
      right_expr = to_infix(node.right)
      "(#{left_expr} #{node.value} #{right_expr})"
    end
  end

  # 决策树节点
  class DecisionNode < TreeNode
    attr_accessor :condition, :true_branch, :false_branch

    def initialize(condition, true_branch = nil, false_branch = nil)
      @condition = condition
      @true_branch = true_branch
      @false_branch = false_branch
    end

    def evaluate(data)
      if @condition.call(data)
        @true_branch ? @true_branch.evaluate(data) : true
      else
        @false_branch ? @false_branch.evaluate(data) : false
      end
    end
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== BinaryTree 使用示例 ==="
  
  # 手动构建二叉树
  tree = BinaryTree.new(1)
  tree.root.left = TreeNode.new(2)
  tree.root.right = TreeNode.new(3)
  tree.root.left.left = TreeNode.new(4)
  tree.root.left.right = TreeNode.new(5)
  tree.root.right.left = TreeNode.new(6)
  tree.root.right.right = TreeNode.new(7)
  
  puts "二叉树结构:"
  tree.print_tree
  
  puts "\n树的基本信息:"
  puts "高度: #{tree.height}"
  puts "节点数: #{tree.count_nodes}"
  puts "叶子节点数: #{tree.count_leaves}"
  puts "最大宽度: #{tree.max_width}"
  
  puts "\n遍历方式:"
  puts "前序遍历: #{tree.preorder_traversal}"
  puts "中序遍历: #{tree.inorder_traversal}"
  puts "后序遍历: #{tree.postorder_traversal}"
  puts "层序遍历: #{tree.level_order_traversal}"
  
  puts "\n按层级遍历:"
  tree.level_order_by_levels.each_with_index do |level, index|
    puts "第#{index}层: #{level}"
  end
  
  puts "\n查找操作:"
  puts "查找值5: #{tree.find(5) ? '找到' : '未找到'}"
  puts "查找值8: #{tree.find(8) ? '找到' : '未找到'}"
  puts "到节点5的路径: #{tree.path_to(5)}"
  
  puts "\n=== 从数组构建二叉树 ==="
  
  array_tree = BinaryTree.from_array([1, 2, 3, 4, 5, 6, 7, 8, 9])
  puts "从数组 [1,2,3,4,5,6,7,8,9] 构建的树:"
  array_tree.print_tree
  
  puts "\n=== 树的操作 ==="
  
  # 克隆树
  cloned_tree = tree.clone
  puts "原树和克隆树相等: #{tree == cloned_tree}"
  
  # 镜像翻转
  mirrored_tree = tree.mirror
  puts "\n镜像后的树:"
  mirrored_tree.print_tree
  
  # 对称性检查
  symmetric_tree = BinaryTree.new(1)
  symmetric_tree.root.left = TreeNode.new(2)
  symmetric_tree.root.right = TreeNode.new(2)
  symmetric_tree.root.left.left = TreeNode.new(3)
  symmetric_tree.root.left.right = TreeNode.new(4)
  symmetric_tree.root.right.left = TreeNode.new(4)
  symmetric_tree.root.right.right = TreeNode.new(3)
  
  puts "\n对称树检查: #{symmetric_tree.symmetric?}"
  
  puts "\n=== 表达式树示例 ==="
  
  # 表达式树：(3 + 4) * 2
  expr_tree = BinaryTreeApplications::ExpressionTree.new("3 4 + 2 *")
  puts "后缀表达式 '3 4 + 2 *' 构建的表达式树:"
  expr_tree.print_tree
  puts "中缀表达式: #{expr_tree.to_infix}"
  puts "计算结果: #{expr_tree.evaluate}"
  
  puts "\n=== 性能测试 ==="
  
  # 构建大型二叉树
  large_array = (1..1000).to_a
  start_time = Time.now
  large_tree = BinaryTree.from_array(large_array)
  end_time = Time.now
  
  puts "构建1000节点的树耗时: #{((end_time - start_time) * 1000).round(2)}ms"
  puts "树高度: #{large_tree.height}"
  
  # 遍历性能测试
  start_time = Time.now
  large_tree.inorder_traversal
  end_time = Time.now
  
  puts "中序遍历1000节点耗时: #{((end_time - start_time) * 1000).round(2)}ms"
end