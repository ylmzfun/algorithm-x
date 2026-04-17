<?php

/**
 * 代码生成器工具
 * 用于自动生成新的数据结构和算法模板
 */

require_once __DIR__ . '/../vendor/autoload.php';

class CodeGenerator
{
    private $templatesDir;
    private $outputDir;
    
    public function __construct()
    {
        $this->templatesDir = __DIR__ . '/templates/';
        $this->outputDir = __DIR__ . '/../src/';
        
        // 确保模板目录存在
        if (!is_dir($this->templatesDir)) {
            mkdir($this->templatesDir, 0755, true);
        }
    }
    
    /**
     * 生成数据结构类
     */
    public function generateDataStructure(string $name, string $type = 'linear'): void
    {
        $className = ucfirst($name);
        $namespace = $this->getNamespaceByType($type);
        $template = $this->getDataStructureTemplate($type);
        
        $content = str_replace(
            ['{{CLASS_NAME}}', '{{NAMESPACE}}', '{{DESCRIPTION}}'],
            [$className, $namespace, $this->generateDescription($name, 'data structure')],
            $template
        );
        
        $filePath = $this->outputDir . $this->getDirectoryByType($type) . '/' . $className . '.php';
        $this->ensureDirectoryExists(dirname($filePath));
        
        file_put_contents($filePath, $content);
        echo "数据结构类已生成: {$filePath}\n";
    }
    
    /**
     * 生成算法类
     */
    public function generateAlgorithm(string $name, string $category = 'general'): void
    {
        $className = ucfirst($name) . 'Algorithm';
        $namespace = 'DataStructures\\Algorithms';
        $template = $this->getAlgorithmTemplate();
        
        $content = str_replace(
            ['{{CLASS_NAME}}', '{{NAMESPACE}}', '{{DESCRIPTION}}', '{{ALGORITHM_NAME}}'],
            [$className, $namespace, $this->generateDescription($name, 'algorithm'), $name],
            $template
        );
        
        $filePath = $this->outputDir . 'Algorithms/' . $className . '.php';
        $this->ensureDirectoryExists(dirname($filePath));
        
        file_put_contents($filePath, $content);
        echo "算法类已生成: {$filePath}\n";
    }
    
    /**
     * 生成测试类
     */
    public function generateTest(string $className, string $type = 'unit'): void
    {
        $testClassName = $className . 'Test';
        $template = $this->getTestTemplate();
        
        $content = str_replace(
            ['{{TEST_CLASS_NAME}}', '{{CLASS_NAME}}', '{{DESCRIPTION}}'],
            [$testClassName, $className, $this->generateDescription($className, 'test')],
            $template
        );
        
        $filePath = __DIR__ . '/../tests/' . $testClassName . '.php';
        $this->ensureDirectoryExists(dirname($filePath));
        
        file_put_contents($filePath, $content);
        echo "测试类已生成: {$filePath}\n";
    }
    
    /**
     * 生成示例文件
     */
    public function generateExample(string $name, string $description = ''): void
    {
        $fileName = ucfirst($name) . 'Example';
        $template = $this->getExampleTemplate();
        
        $content = str_replace(
            ['{{FILE_NAME}}', '{{DESCRIPTION}}', '{{EXAMPLE_NAME}}'],
            [$fileName, $description ?: $this->generateDescription($name, 'example'), $name],
            $template
        );
        
        $filePath = __DIR__ . '/../examples/' . $fileName . '.php';
        $this->ensureDirectoryExists(dirname($filePath));
        
        file_put_contents($filePath, $content);
        echo "示例文件已生成: {$filePath}\n";
    }
    
    /**
     * 获取数据结构模板
     */
    private function getDataStructureTemplate(string $type): string
    {
        switch ($type) {
            case 'linear':
                return $this->getLinearDataStructureTemplate();
            case 'tree':
                return $this->getTreeDataStructureTemplate();
            case 'graph':
                return $this->getGraphDataStructureTemplate();
            case 'hash':
                return $this->getHashDataStructureTemplate();
            default:
                return $this->getGenericDataStructureTemplate();
        }
    }
    
    /**
     * 线性数据结构模板
     */
    private function getLinearDataStructureTemplate(): string
    {
        return <<<'PHP'
<?php

namespace {{NAMESPACE}};

use DataStructures\Interfaces\DataStructureInterface;
use DataStructures\Exceptions\EmptyDataStructureException;
use DataStructures\Exceptions\IndexOutOfBoundsException;

/**
 * {{DESCRIPTION}}
 */
class {{CLASS_NAME}} implements DataStructureInterface
{
    private array $data = [];
    private int $size = 0;
    
    /**
     * 添加元素
     */
    public function add($element): void
    {
        $this->data[] = $element;
        $this->size++;
    }
    
    /**
     * 移除元素
     */
    public function remove($element): bool
    {
        $index = array_search($element, $this->data, true);
        if ($index !== false) {
            array_splice($this->data, $index, 1);
            $this->size--;
            return true;
        }
        return false;
    }
    
    /**
     * 检查是否包含元素
     */
    public function contains($element): bool
    {
        return in_array($element, $this->data, true);
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 检查是否为空
     */
    public function isEmpty(): bool
    {
        return $this->size === 0;
    }
    
    /**
     * 清空数据结构
     */
    public function clear(): void
    {
        $this->data = [];
        $this->size = 0;
    }
    
    /**
     * 转换为数组
     */
    public function toArray(): array
    {
        return $this->data;
    }
    
    /**
     * 获取迭代器
     */
    public function getIterator(): \Iterator
    {
        return new \ArrayIterator($this->data);
    }
}
PHP;
    }
    
    /**
     * 算法模板
     */
    private function getAlgorithmTemplate(): string
    {
        return <<<'PHP'
<?php

namespace {{NAMESPACE}};

/**
 * {{DESCRIPTION}}
 */
class {{CLASS_NAME}}
{
    /**
     * {{ALGORITHM_NAME}}算法实现
     * 
     * @param array $data 输入数据
     * @return mixed 算法结果
     */
    public static function execute(array $data)
    {
        // TODO: 实现{{ALGORITHM_NAME}}算法
        throw new \RuntimeException('Algorithm not implemented yet');
    }
    
    /**
     * 算法的时间复杂度
     */
    public static function getTimeComplexity(): string
    {
        return 'O(n)'; // TODO: 更新实际的时间复杂度
    }
    
    /**
     * 算法的空间复杂度
     */
    public static function getSpaceComplexity(): string
    {
        return 'O(1)'; // TODO: 更新实际的空间复杂度
    }
    
    /**
     * 算法描述
     */
    public static function getDescription(): string
    {
        return '{{DESCRIPTION}}';
    }
}
PHP;
    }
    
    /**
     * 测试模板
     */
    private function getTestTemplate(): string
    {
        return <<<'PHP'
<?php

namespace DataStructures\Tests;

use PHPUnit\Framework\TestCase;
use DataStructures\{{CLASS_NAME}};

/**
 * {{DESCRIPTION}}
 */
class {{TEST_CLASS_NAME}} extends TestCase
{
    private {{CLASS_NAME}} $instance;
    
    protected function setUp(): void
    {
        $this->instance = new {{CLASS_NAME}}();
    }
    
    protected function tearDown(): void
    {
        $this->instance = null;
    }
    
    /**
     * 测试基本功能
     */
    public function testBasicFunctionality(): void
    {
        // TODO: 实现基本功能测试
        $this->assertTrue(true);
    }
    
    /**
     * 测试边界条件
     */
    public function testEdgeCases(): void
    {
        // TODO: 实现边界条件测试
        $this->assertTrue(true);
    }
    
    /**
     * 测试异常情况
     */
    public function testExceptions(): void
    {
        // TODO: 实现异常情况测试
        $this->assertTrue(true);
    }
    
    /**
     * 测试性能
     */
    public function testPerformance(): void
    {
        // TODO: 实现性能测试
        $this->assertTrue(true);
    }
}
PHP;
    }
    
    /**
     * 示例模板
     */
    private function getExampleTemplate(): string
    {
        return <<<'PHP'
<?php

/**
 * {{DESCRIPTION}}
 */

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Utils\Utils;

echo "\n=== {{EXAMPLE_NAME}}示例 ===\n";

// TODO: 实现示例代码

echo "\n示例执行完成!\n";
PHP;
    }
    
    /**
     * 通用数据结构模板
     */
    private function getGenericDataStructureTemplate(): string
    {
        return <<<'PHP'
<?php

namespace {{NAMESPACE}};

use DataStructures\Interfaces\DataStructureInterface;

/**
 * {{DESCRIPTION}}
 */
class {{CLASS_NAME}} implements DataStructureInterface
{
    /**
     * 构造函数
     */
    public function __construct()
    {
        // TODO: 初始化数据结构
    }
    
    /**
     * 添加元素
     */
    public function add($element): void
    {
        // TODO: 实现添加元素
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 移除元素
     */
    public function remove($element): bool
    {
        // TODO: 实现移除元素
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 检查是否包含元素
     */
    public function contains($element): bool
    {
        // TODO: 实现包含检查
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        // TODO: 实现大小获取
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 检查是否为空
     */
    public function isEmpty(): bool
    {
        return $this->size() === 0;
    }
    
    /**
     * 清空数据结构
     */
    public function clear(): void
    {
        // TODO: 实现清空操作
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 转换为数组
     */
    public function toArray(): array
    {
        // TODO: 实现数组转换
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 获取迭代器
     */
    public function getIterator(): \Iterator
    {
        // TODO: 实现迭代器
        throw new \RuntimeException('Method not implemented yet');
    }
}
PHP;
    }
    
    /**
     * 树形数据结构模板
     */
    private function getTreeDataStructureTemplate(): string
    {
        return str_replace('{{ADDITIONAL_METHODS}}', $this->getTreeMethods(), $this->getGenericDataStructureTemplate());
    }
    
    /**
     * 图数据结构模板
     */
    private function getGraphDataStructureTemplate(): string
    {
        return str_replace('{{ADDITIONAL_METHODS}}', $this->getGraphMethods(), $this->getGenericDataStructureTemplate());
    }
    
    /**
     * 哈希数据结构模板
     */
    private function getHashDataStructureTemplate(): string
    {
        return str_replace('{{ADDITIONAL_METHODS}}', $this->getHashMethods(), $this->getGenericDataStructureTemplate());
    }
    
    /**
     * 获取树方法
     */
    private function getTreeMethods(): string
    {
        return <<<'PHP'
    
    /**
     * 获取根节点
     */
    public function getRoot()
    {
        // TODO: 实现获取根节点
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 获取高度
     */
    public function getHeight(): int
    {
        // TODO: 实现获取高度
        throw new \RuntimeException('Method not implemented yet');
    }
PHP;
    }
    
    /**
     * 获取图方法
     */
    private function getGraphMethods(): string
    {
        return <<<'PHP'
    
    /**
     * 添加顶点
     */
    public function addVertex($vertex): void
    {
        // TODO: 实现添加顶点
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 添加边
     */
    public function addEdge($from, $to, $weight = 1): void
    {
        // TODO: 实现添加边
        throw new \RuntimeException('Method not implemented yet');
    }
PHP;
    }
    
    /**
     * 获取哈希方法
     */
    private function getHashMethods(): string
    {
        return <<<'PHP'
    
    /**
     * 获取值
     */
    public function get($key)
    {
        // TODO: 实现获取值
        throw new \RuntimeException('Method not implemented yet');
    }
    
    /**
     * 设置值
     */
    public function put($key, $value): void
    {
        // TODO: 实现设置值
        throw new \RuntimeException('Method not implemented yet');
    }
PHP;
    }
    
    /**
     * 根据类型获取命名空间
     */
    private function getNamespaceByType(string $type): string
    {
        $namespaces = [
            'linear' => 'DataStructures\\Linear',
            'tree' => 'DataStructures\\Tree',
            'graph' => 'DataStructures\\Graph',
            'hash' => 'DataStructures\\Hash',
            'advanced' => 'DataStructures\\Advanced'
        ];
        
        return $namespaces[$type] ?? 'DataStructures';
    }
    
    /**
     * 根据类型获取目录
     */
    private function getDirectoryByType(string $type): string
    {
        $directories = [
            'linear' => 'Linear',
            'tree' => 'Trees',
            'graph' => 'Graphs',
            'hash' => 'Hash',
            'advanced' => 'Advanced'
        ];
        
        return $directories[$type] ?? '';
    }
    
    /**
     * 生成描述
     */
    private function generateDescription(string $name, string $type): string
    {
        return ucfirst($name) . ' ' . $type . ' implementation';
    }
    
    /**
     * 确保目录存在
     */
    private function ensureDirectoryExists(string $directory): void
    {
        if (!is_dir($directory)) {
            mkdir($directory, 0755, true);
        }
    }
    
    /**
     * 显示帮助信息
     */
    public function showHelp(): void
    {
        echo <<<'HELP'
代码生成器工具

用法:
  php generator.php <command> <name> [options]

命令:
  data-structure <name> [type]  生成数据结构类
  algorithm <name> [category]   生成算法类
  test <class_name>            生成测试类
  example <name> [description] 生成示例文件

选项:
  type: linear, tree, graph, hash, advanced
  category: sorting, search, graph, string, dp, greedy, backtrack, math

示例:
  php generator.php data-structure MyStack linear
  php generator.php algorithm QuickSort sorting
  php generator.php test MyStack
  php generator.php example MyStackDemo "Stack demonstration"

HELP;
    }
}

// 命令行处理
if (basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    $generator = new CodeGenerator();
    
    if ($argc < 2) {
        $generator->showHelp();
        exit(1);
    }
    
    $command = $argv[1];
    
    switch ($command) {
        case 'data-structure':
            if ($argc < 3) {
                echo "错误: 请提供数据结构名称\n";
                exit(1);
            }
            $name = $argv[2];
            $type = $argv[3] ?? 'linear';
            $generator->generateDataStructure($name, $type);
            break;
            
        case 'algorithm':
            if ($argc < 3) {
                echo "错误: 请提供算法名称\n";
                exit(1);
            }
            $name = $argv[2];
            $category = $argv[3] ?? 'general';
            $generator->generateAlgorithm($name, $category);
            break;
            
        case 'test':
            if ($argc < 3) {
                echo "错误: 请提供类名\n";
                exit(1);
            }
            $className = $argv[2];
            $generator->generateTest($className);
            break;
            
        case 'example':
            if ($argc < 3) {
                echo "错误: 请提供示例名称\n";
                exit(1);
            }
            $name = $argv[2];
            $description = $argv[3] ?? '';
            $generator->generateExample($name, $description);
            break;
            
        case 'help':
        case '--help':
        case '-h':
            $generator->showHelp();
            break;
            
        default:
            echo "错误: 未知命令 '{$command}'\n";
            $generator->showHelp();
            exit(1);
    }
}