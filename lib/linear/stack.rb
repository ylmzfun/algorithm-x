# 栈 (Stack) 实现
# 
# 思路：
# 栈是一种后进先出（LIFO - Last In First Out）的线性数据结构。
# 只能在栈顶进行插入（push）和删除（pop）操作。
# 可以用数组或链表作为底层实现。
# 
# 作用：
# 1. 函数调用管理：程序运行时的函数调用栈
# 2. 表达式求值：中缀表达式转后缀表达式
# 3. 括号匹配：检查括号是否正确配对
# 4. 撤销操作：编辑器的撤销功能
# 5. 深度优先搜索：DFS算法的实现
# 
# 应用场景：
# 1. 编译器：语法分析、词法分析
# 2. 浏览器：前进后退历史记录
# 3. 游戏开发：状态管理、场景切换
# 4. 算法：递归算法的迭代实现
# 5. 设计模式：命令模式中的撤销操作
# 6. Web开发：路由栈、中间件栈

class Stack
  attr_reader :size

  def initialize
    @items = []
    @size = 0
  end

  # 入栈操作
  # 时间复杂度：O(1)
  def push(item)
    @items[@size] = item
    @size += 1
    self
  end
  alias_method :<<, :push

  # 出栈操作
  # 时间复杂度：O(1)
  def pop
    raise RuntimeError, "Stack is empty" if empty?
    
    @size -= 1
    item = @items[@size]
    @items[@size] = nil  # 清除引用
    item
  end

  # 查看栈顶元素（不删除）
  # 时间复杂度：O(1)
  def peek
    raise RuntimeError, "Stack is empty" if empty?
    @items[@size - 1]
  end
  alias_method :top, :peek

  # 检查栈是否为空
  def empty?
    @size == 0
  end

  # 清空栈
  def clear
    @items.clear
    @size = 0
    self
  end

  # 搜索元素（返回距离栈顶的距离，栈顶为1）
  # 时间复杂度：O(n)
  def search(item)
    (@size - 1).downto(0) do |i|
      return @size - i if @items[i] == item
    end
    -1  # 未找到
  end

  # 转换为数组（栈顶在数组末尾）
  def to_a
    @items[0, @size]
  end

  # 迭代器（从栈顶到栈底）
  def each
    return enum_for(:each) unless block_given?
    
    (@size - 1).downto(0) do |i|
      yield @items[i]
    end
    self
  end

  # 字符串表示
  def to_s
    "Stack[#{to_a.join(', ')}] (top: #{empty? ? 'empty' : peek})"
  end

  def inspect
    "#<Stack:#{object_id} size=#{@size} top=#{empty? ? 'nil' : peek.inspect}>"
  end
end

# 基于链表的栈实现（可选）
class LinkedStack
  attr_reader :size

  # 栈节点
  class StackNode
    attr_accessor :data, :next

    def initialize(data, next_node = nil)
      @data = data
      @next = next_node
    end
  end

  def initialize
    @top = nil
    @size = 0
  end

  # 入栈操作
  # 时间复杂度：O(1)
  def push(item)
    @top = StackNode.new(item, @top)
    @size += 1
    self
  end

  # 出栈操作
  # 时间复杂度：O(1)
  def pop
    raise RuntimeError, "Stack is empty" if empty?
    
    item = @top.data
    @top = @top.next
    @size -= 1
    item
  end

  # 查看栈顶元素
  # 时间复杂度：O(1)
  def peek
    raise RuntimeError, "Stack is empty" if empty?
    @top.data
  end

  # 检查栈是否为空
  def empty?
    @top.nil?
  end

  # 清空栈
  def clear
    @top = nil
    @size = 0
    self
  end

  # 转换为数组
  def to_a
    result = []
    current = @top
    while current
      result << current.data
      current = current.next
    end
    result.reverse
  end

  # 迭代器（从栈顶到栈底）
  def each
    return enum_for(:each) unless block_given?
    
    current = @top
    while current
      yield current.data
      current = current.next
    end
    self
  end

  def to_s
    "LinkedStack[#{to_a.join(', ')}] (top: #{empty? ? 'empty' : peek})"
  end
end

# 栈的实际应用示例
module StackApplications
  # 括号匹配检查
  def self.balanced_parentheses?(str)
    stack = Stack.new
    pairs = { '(' => ')', '[' => ']', '{' => '}' }
    
    str.each_char do |char|
      if pairs.key?(char)
        stack.push(char)
      elsif pairs.value?(char)
        return false if stack.empty?
        return false if pairs[stack.pop] != char
      end
    end
    
    stack.empty?
  end

  # 中缀表达式转后缀表达式（逆波兰表示法）
  def self.infix_to_postfix(expression)
    stack = Stack.new
    result = []
    precedence = { '+' => 1, '-' => 1, '*' => 2, '/' => 2, '^' => 3 }
    
    expression.split.each do |token|
      if token.match?(/\d+/)  # 数字
        result << token
      elsif token == '('
        stack.push(token)
      elsif token == ')'
        while !stack.empty? && stack.peek != '('
          result << stack.pop
        end
        stack.pop  # 移除 '('
      elsif precedence.key?(token)  # 操作符
        while !stack.empty? && stack.peek != '(' && 
              precedence[stack.peek] && precedence[stack.peek] >= precedence[token]
          result << stack.pop
        end
        stack.push(token)
      end
    end
    
    while !stack.empty?
      result << stack.pop
    end
    
    result.join(' ')
  end

  # 计算后缀表达式
  def self.evaluate_postfix(expression)
    stack = Stack.new
    
    expression.split.each do |token|
      if token.match?(/\d+/)
        stack.push(token.to_i)
      else
        b = stack.pop
        a = stack.pop
        case token
        when '+'
          stack.push(a + b)
        when '-'
          stack.push(a - b)
        when '*'
          stack.push(a * b)
        when '/'
          stack.push(a / b)
        when '^'
          stack.push(a ** b)
        end
      end
    end
    
    stack.pop
  end

  # 十进制转其他进制
  def self.decimal_to_base(number, base)
    return "0" if number == 0
    
    stack = Stack.new
    digits = "0123456789ABCDEF"
    
    while number > 0
      stack.push(digits[number % base])
      number /= base
    end
    
    result = ""
    while !stack.empty?
      result += stack.pop
    end
    
    result
  end

  # 简单的撤销/重做功能实现
  class UndoRedoManager
    def initialize
      @undo_stack = Stack.new
      @redo_stack = Stack.new
    end

    def execute_command(command)
      @undo_stack.push(command)
      @redo_stack.clear  # 执行新命令后清空重做栈
      command.execute
    end

    def undo
      return false if @undo_stack.empty?
      
      command = @undo_stack.pop
      @redo_stack.push(command)
      command.undo
      true
    end

    def redo
      return false if @redo_stack.empty?
      
      command = @redo_stack.pop
      @undo_stack.push(command)
      command.execute
      true
    end

    def can_undo?
      !@undo_stack.empty?
    end

    def can_redo?
      !@redo_stack.empty?
    end
  end
end

# 使用示例和测试
if __FILE__ == $0
  puts "=== Stack 使用示例 ==="
  
  # 基本栈操作
  stack = Stack.new
  puts "创建空栈: #{stack}"
  
  # 入栈操作
  stack.push(1).push(2).push(3)
  puts "入栈后: #{stack}"
  
  # 查看栈顶
  puts "栈顶元素: #{stack.peek}"
  
  # 出栈操作
  popped = stack.pop
  puts "出栈元素 #{popped}: #{stack}"
  
  # 搜索元素
  puts "元素2距离栈顶的距离: #{stack.search(2)}"
  
  # 遍历栈
  print "从栈顶到栈底遍历: "
  stack.each { |item| print "#{item} " }
  puts
  
  puts "\n=== LinkedStack 使用示例 ==="
  
  linked_stack = LinkedStack.new
  linked_stack.push('a').push('b').push('c')
  puts "链表栈: #{linked_stack}"
  
  puts "\n=== 栈的应用示例 ==="
  
  # 括号匹配
  test_strings = ["((()))", "([{}])", "((()]", "({[}])"]
  test_strings.each do |str|
    result = StackApplications.balanced_parentheses?(str)
    puts "#{str} 括号匹配: #{result}"
  end
  
  # 表达式转换和计算
  infix = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
  postfix = StackApplications.infix_to_postfix(infix)
  puts "\n中缀表达式: #{infix}"
  puts "后缀表达式: #{postfix}"
  
  simple_postfix = "3 4 + 2 *"
  result = StackApplications.evaluate_postfix(simple_postfix)
  puts "计算 '#{simple_postfix}' = #{result}"
  
  # 进制转换
  number = 255
  puts "\n十进制 #{number} 转换:"
  puts "二进制: #{StackApplications.decimal_to_base(number, 2)}"
  puts "八进制: #{StackApplications.decimal_to_base(number, 8)}"
  puts "十六进制: #{StackApplications.decimal_to_base(number, 16)}"
  
  puts "\n=== 性能测试 ==="
  
  # 性能测试
  large_stack = Stack.new
  start_time = Time.now
  
  # 入栈100000个元素
  100000.times { |i| large_stack.push(i) }
  
  # 出栈100000个元素
  100000.times { large_stack.pop }
  
  end_time = Time.now
  puts "100000次入栈+出栈操作耗时: #{((end_time - start_time) * 1000).round(2)}ms"
end