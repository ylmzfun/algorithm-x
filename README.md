<!--
 * @Author: ylmzfun ylmzfun@foxmail.com
 * @Date: 2025-08-07 14:46:34
 * @LastEditors: ylmzfun ylmzfun@foxmail.com
 * @LastEditTime: 2025-08-07 18:00:06
 * @FilePath: /ruby-algorithm/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# Ruby 数据结构实现项目

[![Ruby Version](https://img.shields.io/badge/ruby-%3E%3D%202.7.0-red.svg)](https://www.ruby-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code_style-rubocop-brightgreen.svg)](https://github.com/rubocop/rubocop)

此项目使用 Ruby 语言实现了各种常见的数据结构与算法，包括详细的思路解释、作用说明以及实际应用场景。每个数据结构/算法都包含完整的实现、详细的注释、时间复杂度分析和实际应用示例。

## 🚀 特性

- **完整实现**: 11种核心数据结构 + 6大算法模块
- **详细注释**: 每个类和方法都有详细的中文注释
- **性能分析**: 包含时间复杂度和空间复杂度分析
- **实际应用**: 提供真实业务场景的应用示例
- **测试覆盖**: 94个测试用例，100%通过率
- **代码规范**: 遵循 RuboCop 代码规范

## 项目结构

```
ruby-algorithm/
├── README.md                 # 项目说明文档
├── lib/                      # 核心实现目录
│   ├── linear/              # 线性数据结构
│   │   ├── array_list.rb    # 动态数组
│   │   ├── linked_list.rb   # 链表
│   │   ├── stack.rb         # 栈
│   │   └── queue.rb         # 队列
│   ├── tree/                # 树形数据结构
│   │   ├── binary_tree.rb   # 二叉树
│   │   ├── bst.rb           # 二叉搜索树
│   │   ├── avl_tree.rb      # AVL树
│   │   └── heap.rb          # 堆
│   ├── graph/               # 图数据结构
│   │   ├── graph.rb         # 图的基本实现
│   │   └── weighted_graph.rb # 加权图
│   ├── hash/                # 哈希相关
│   │   ├── hash_table.rb    # 哈希表
│   │   └── bloom_filter.rb  # 布隆过滤器
│   ├── data_structures/     # 新增数据结构
│   │   ├── trie.rb          # 字典树 (Trie)
│   │   └── union_find.rb    # 并查集 (Union-Find)
│   └── algorithms/          # 算法模块
│       ├── sorting.rb       # 排序算法 (13种)
│       ├── searching.rb     # 搜索算法 (11种)
│       ├── string.rb        # 字符串匹配算法
│       └── dynamic_programming.rb # 动态规划
├── examples/                # 使用示例
└── tests/                   # 测试文件
    ├── test_runner.rb       # 数据结构测试 (35个)
    └── algorithms_test.rb   # 算法测试 (59个)
```

## 数据结构概览

### 线性数据结构
- **动态数组 (ArrayList)**: 可变长度的数组实现
- **链表 (LinkedList)**: 单向链表和双向链表
- **栈 (Stack)**: 后进先出 (LIFO) 数据结构
- **队列 (Queue)**: 先进先出 (FIFO) 数据结构

### 树形数据结构
- **二叉树 (BinaryTree)**: 基础二叉树实现
- **二叉搜索树 (BST)**: 有序二叉树
- **AVL树**: 自平衡二叉搜索树
- **堆 (Heap)**: 完全二叉树实现的优先队列

### 图数据结构
- **图 (Graph)**: 邻接表和邻接矩阵实现
- **加权图 (WeightedGraph)**: 带权重的图结构

### 哈希数据结构
- **哈希表 (HashTable)**: 键值对存储结构
- **布隆过滤器 (BloomFilter)**: 概率性数据结构

### 新增数据结构
- **字典树 (Trie)**: 前缀树，高效字符串存储和检索
- **并查集 (Union-Find)**: 不相交集合的合并与查询

## 算法概览

### 排序算法 (13种)
- **比较排序 O(n²)**: 冒泡排序、选择排序、插入排序、希尔排序
- **比较排序 O(n log n)**: 归并排序、快速排序、三路快排、堆排序、Tim排序
- **非比较排序**: 计数排序、桶排序、基数排序
- **特殊排序**: 鸡尾酒排序
- **工具方法**: 快速选择（第k小元素）、部分排序

### 搜索算法 (11种)
- **基本搜索**: 线性搜索、二分搜索（迭代/递归）
- **边界搜索**: lower_bound、upper_bound、search_range
- **高级搜索**: 跳跃搜索、指数搜索、插值搜索、斐波那契搜索
- **场景搜索**: 旋转数组搜索、二维矩阵搜索、峰值查找

### 字符串算法
- **匹配算法**: Brute Force、KMP、Rabin-Karp、Boyer-Moore、Z-Algorithm
- **字符串操作**: 最长公共子串、编辑距离、最长回文子串（Manacher）

### 动态规划
- **背包问题**: 0/1背包、完全背包
- **序列问题**: LCS、LIS、最大子数组和
- **硬币问题**: 最少硬币数、硬币组合数
- **路径问题**: 网格路径、最小路径和
- **经典DP**: 斐波那契、爬楼梯、打家劫舍、分割等和子集
- **区间DP**: 矩阵链乘法、戳气球

## 📦 安装

### 环境要求

- Ruby >= 2.7.0
- Bundler (可选，用于依赖管理)

### 克隆项目

```bash
git clone https://github.com/your-username/ruby-algorithm.git
cd ruby-algorithm
```

### 安装依赖（可选）

```bash
bundle install
```

## 🚀 快速开始

### 基本使用

```ruby
# 引入所需的数据结构
require_relative 'lib/linear/stack'
require_relative 'lib/tree/bst'
require_relative 'lib/hash/hash_table'

# 使用栈
stack = Stack.new
stack.push(1)
stack.push(2)
puts stack.pop  # 输出: 2

# 使用二叉搜索树
bst = BinarySearchTree.new
[50, 30, 70, 20, 40].each { |val| bst.insert(val) }
puts bst.inorder_traversal  # 输出: [20, 30, 40, 50, 70]

# 使用哈希表
hash_table = HashTable.new
hash_table.put("name", "Alice")
puts hash_table.get("name")  # 输出: Alice
```

### 运行演示程序

```bash
# 运行基本演示
ruby demo.rb

# 运行实际应用示例
ruby examples/data_structure_examples.rb

# 运行测试套件
ruby tests/test_runner.rb

# 运行性能测试
ruby tests/performance_test.rb
```

## 📚 使用方法

每个数据结构都包含详细的注释和使用示例。主要特点：

- **完整的API**: 每个数据结构都提供了完整的操作方法
- **详细注释**: 包含中文注释和使用说明
- **时间复杂度**: 标注了每个操作的时间复杂度
- **应用场景**: 说明了适用的业务场景

## 🎯 应用场景

每个数据结构的实现文件都包含了详细的应用场景说明：

### 业务应用
- **电商系统**: 购物车、订单处理、商品分类
- **社交网络**: 用户关系图、消息队列
- **缓存系统**: LRU缓存、多级缓存
- **搜索引擎**: 倒排索引、布隆过滤器

### 技术特点
- 适用的业务场景分析
- 设计模式中的应用
- 性能特点和时间复杂度
- 实际项目中的使用案例

## 🧪 测试

项目包含完整的测试套件：

```bash
# 运行所有数据结构测试
ruby tests/test_runner.rb

# 运行算法测试
ruby tests/algorithms_test.rb

# 运行性能测试
ruby tests/performance_test.rb

# 使用RuboCop检查代码风格
bundle exec rubocop
```

测试覆盖：
- 功能正确性测试
- 边界条件测试
- 性能基准测试
- 内存使用测试
- 总计94个测试用例，100%通过

## 📈 性能特点

| 数据结构   | 插入      | 删除      | 查找      | 空间复杂度 |
| ---------- | --------- | --------- | --------- | ---------- |
| ArrayList  | O(1)*     | O(n)      | O(n)      | O(n)       |
| LinkedList | O(1)      | O(n)      | O(n)      | O(n)       |
| Stack      | O(1)      | O(1)      | -         | O(n)       |
| Queue      | O(1)      | O(1)      | -         | O(n)       |
| BST        | O(log n)* | O(log n)* | O(log n)* | O(n)       |
| AVL Tree   | O(log n)  | O(log n)  | O(log n)  | O(n)       |
| Heap       | O(log n)  | O(log n)  | O(n)      | O(n)       |
| HashTable  | O(1)*     | O(1)*     | O(1)*     | O(n)       |
| Graph      | O(1)      | O(V+E)    | O(V+E)    | O(V+E)     |

*平均情况下的时间复杂度

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 RuboCop 代码规范
- 添加适当的注释和文档
- 为新功能编写测试
- 确保所有测试通过

### 提交信息规范

- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有贡献者的努力
- 参考了经典的数据结构教材和算法实现
- 受到开源社区的启发和支持

## 📞 联系方式

如果您有任何问题或建议，请通过以下方式联系：

- 提交 Issue: [GitHub Issues](https://github.com/your-username/ruby-algorithm/issues)
- 邮箱: your-email@example.com
- 项目主页: [GitHub Repository](https://github.com/your-username/ruby-algorithm)

---

⭐ 如果这个项目对您有帮助，请给它一个星标！