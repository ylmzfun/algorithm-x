<?php

/**
 * 文档生成器
 * 自动生成项目API文档
 */

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Config\Config;

class DocumentationGenerator
{
    private $sourceDir;
    private $outputDir;
    private $projectInfo;
    
    public function __construct()
    {
        $this->sourceDir = __DIR__ . '/../src/';
        $this->outputDir = __DIR__ . '/../docs/';
        $this->projectInfo = Config::getProjectInfo();
        
        // 确保输出目录存在
        if (!is_dir($this->outputDir)) {
            mkdir($this->outputDir, 0755, true);
        }
    }
    
    /**
     * 生成所有文档
     */
    public function generateAll(): void
    {
        echo "开始生成项目文档...\n";
        
        $this->generateIndex();
        $this->generateApiDocs();
        $this->generateAlgorithmDocs();
        $this->generateDataStructureDocs();
        $this->generateExampleDocs();
        $this->generateChangeLog();
        
        echo "文档生成完成！\n";
        echo "文档位置: {$this->outputDir}\n";
    }
    
    /**
     * 生成首页文档
     */
    private function generateIndex(): void
    {
        $content = $this->generateMarkdownHeader('项目文档', 1);
        
        $content .= $this->generateProjectInfo();
        $content .= $this->generateTableOfContents();
        $content .= $this->generateQuickStart();
        
        file_put_contents($this->outputDir . 'index.md', $content);
        echo "✓ 生成首页文档\n";
    }
    
    /**
     * 生成API文档
     */
    private function generateApiDocs(): void
    {
        $apiDir = $this->outputDir . 'api/';
        if (!is_dir($apiDir)) {
            mkdir($apiDir, 0755, true);
        }
        
        $classes = $this->scanClasses($this->sourceDir);
        
        foreach ($classes as $class) {
            $this->generateClassDoc($class, $apiDir);
        }
        
        $this->generateApiIndex($classes, $apiDir);
        echo "✓ 生成API文档 (" . count($classes) . " 个类)\n";
    }
    
    /**
     * 生成算法文档
     */
    private function generateAlgorithmDocs(): void
    {
        $content = $this->generateMarkdownHeader('算法文档', 1);
        
        $algorithmCategories = [
            'Sorting' => '排序算法',
            'SearchAlgorithms' => '搜索算法',
            'DynamicProgramming' => '动态规划算法',
            'GreedyAlgorithms' => '贪心算法',
            'BacktrackingAlgorithms' => '回溯算法',
            'MathAlgorithms' => '数学算法',
            'GraphAlgorithms' => '图算法',
            'StringAlgorithms' => '字符串算法'
        ];
        
        foreach ($algorithmCategories as $className => $title) {
            $filePath = $this->sourceDir . 'Algorithms/' . $className . '.php';
            if (file_exists($filePath)) {
                $content .= $this->generateAlgorithmCategoryDoc($className, $title, $filePath);
            }
        }
        
        file_put_contents($this->outputDir . 'algorithms.md', $content);
        echo "✓ 生成算法文档\n";
    }
    
    /**
     * 生成数据结构文档
     */
    private function generateDataStructureDocs(): void
    {
        $content = $this->generateMarkdownHeader('数据结构文档', 1);
        
        $categories = [
            'Linear' => '线性数据结构',
            'Trees' => '树形数据结构',
            'Graphs' => '图数据结构',
            'Hash' => '哈希数据结构',
            'Advanced' => '高级数据结构'
        ];
        
        foreach ($categories as $dir => $title) {
            $categoryDir = $this->sourceDir . $dir . '/';
            if (is_dir($categoryDir)) {
                $content .= $this->generateDataStructureCategoryDoc($dir, $title, $categoryDir);
            }
        }
        
        file_put_contents($this->outputDir . 'data-structures.md', $content);
        echo "✓ 生成数据结构文档\n";
    }
    
    /**
     * 生成示例文档
     */
    private function generateExampleDocs(): void
    {
        $content = $this->generateMarkdownHeader('使用示例', 1);
        
        $examplesDir = __DIR__ . '/../examples/';
        $examples = glob($examplesDir . '*.php');
        
        foreach ($examples as $example) {
            $content .= $this->generateExampleDoc($example);
        }
        
        file_put_contents($this->outputDir . 'examples.md', $content);
        echo "✓ 生成示例文档\n";
    }
    
    /**
     * 生成变更日志
     */
    private function generateChangeLog(): void
    {
        $content = $this->generateMarkdownHeader('变更日志', 1);
        
        $content .= $this->generateMarkdownHeader('版本 2.0.0', 2);
        $content .= "发布日期: " . date('Y-m-d') . "\n\n";
        
        $content .= $this->generateMarkdownHeader('新增功能', 3);
        $content .= "- 动态规划算法模块\n";
        $content .= "- 贪心算法模块\n";
        $content .= "- 回溯算法模块\n";
        $content .= "- 数学算法模块\n";
        $content .= "- 性能测试工具\n";
        $content .= "- 基准测试工具\n";
        $content .= "- 代码生成器\n";
        $content .= "- 配置管理系统\n";
        $content .= "- 自动文档生成\n\n";
        
        $content .= $this->generateMarkdownHeader('改进', 3);
        $content .= "- 完善的单元测试覆盖\n";
        $content .= "- 更好的错误处理\n";
        $content .= "- 性能优化\n";
        $content .= "- 代码质量提升\n\n";
        
        file_put_contents($this->outputDir . 'CHANGELOG.md', $content);
        echo "✓ 生成变更日志\n";
    }
    
    /**
     * 扫描类文件
     */
    private function scanClasses(string $directory): array
    {
        $classes = [];
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($directory)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile() && $file->getExtension() === 'php') {
                $relativePath = str_replace($directory, '', $file->getPathname());
                $className = $this->extractClassName($file->getPathname());
                if ($className) {
                    $classes[] = [
                        'name' => $className,
                        'file' => $file->getPathname(),
                        'relative_path' => $relativePath
                    ];
                }
            }
        }
        
        return $classes;
    }
    
    /**
     * 提取类名
     */
    private function extractClassName(string $filePath): ?string
    {
        $content = file_get_contents($filePath);
        if (preg_match('/class\s+([A-Za-z_][A-Za-z0-9_]*)/', $content, $matches)) {
            return $matches[1];
        }
        return null;
    }
    
    /**
     * 生成类文档
     */
    private function generateClassDoc(array $classInfo, string $outputDir): void
    {
        $content = $this->generateMarkdownHeader($classInfo['name'], 1);
        
        $reflection = $this->getClassReflection($classInfo['file']);
        if ($reflection) {
            $content .= $this->generateClassInfo($reflection);
            $content .= $this->generateMethodDocs($reflection);
        }
        
        $fileName = $classInfo['name'] . '.md';
        file_put_contents($outputDir . $fileName, $content);
    }
    
    /**
     * 获取类反射
     */
    private function getClassReflection(string $filePath): ?ReflectionClass
    {
        try {
            require_once $filePath;
            $className = $this->extractClassName($filePath);
            if ($className) {
                // 尝试不同的命名空间
                $namespaces = [
                    'DataStructures\\',
                    'DataStructures\\Linear\\',
                    'DataStructures\\Trees\\',
                    'DataStructures\\Graphs\\',
                    'DataStructures\\Hash\\',
                    'DataStructures\\Advanced\\',
                    'DataStructures\\Algorithms\\',
                    'DataStructures\\Utils\\',
                    'DataStructures\\Interfaces\\',
                    'DataStructures\\Exceptions\\'
                ];
                
                foreach ($namespaces as $namespace) {
                    $fullClassName = $namespace . $className;
                    if (class_exists($fullClassName) || interface_exists($fullClassName)) {
                        return new ReflectionClass($fullClassName);
                    }
                }
            }
        } catch (Exception $e) {
            // 忽略错误
        }
        
        return null;
    }
    
    /**
     * 生成项目信息
     */
    private function generateProjectInfo(): string
    {
        $content = $this->generateMarkdownHeader('项目信息', 2);
        $content .= "- **项目名称**: {$this->projectInfo['name']}\n";
        $content .= "- **版本**: {$this->projectInfo['version']}\n";
        $content .= "- **作者**: {$this->projectInfo['author']}\n";
        $content .= "- **描述**: {$this->projectInfo['description']}\n";
        $content .= "- **PHP版本**: {$this->projectInfo['php_version']}\n\n";
        
        return $content;
    }
    
    /**
     * 生成目录
     */
    private function generateTableOfContents(): string
    {
        $content = $this->generateMarkdownHeader('目录', 2);
        $content .= "- [API文档](api/index.md)\n";
        $content .= "- [算法文档](algorithms.md)\n";
        $content .= "- [数据结构文档](data-structures.md)\n";
        $content .= "- [使用示例](examples.md)\n";
        $content .= "- [变更日志](CHANGELOG.md)\n\n";
        
        return $content;
    }
    
    /**
     * 生成快速开始
     */
    private function generateQuickStart(): string
    {
        $content = $this->generateMarkdownHeader('快速开始', 2);
        $content .= "```bash\n";
        $content .= "# 安装依赖\n";
        $content .= "composer install\n\n";
        $content .= "# 运行示例\n";
        $content .= "composer demo\n\n";
        $content .= "# 运行测试\n";
        $content .= "composer test\n\n";
        $content .= "# 性能测试\n";
        $content .= "composer benchmark\n";
        $content .= "```\n\n";
        
        return $content;
    }
    
    /**
     * 生成Markdown标题
     */
    private function generateMarkdownHeader(string $title, int $level): string
    {
        return str_repeat('#', $level) . ' ' . $title . "\n\n";
    }
    
    /**
     * 生成类信息
     */
    private function generateClassInfo(ReflectionClass $reflection): string
    {
        $content = "**命名空间**: `{$reflection->getNamespaceName()}`\n\n";
        
        $docComment = $reflection->getDocComment();
        if ($docComment) {
            $description = $this->extractDescription($docComment);
            if ($description) {
                $content .= "**描述**: {$description}\n\n";
            }
        }
        
        if ($reflection->isInterface()) {
            $content .= "**类型**: 接口\n\n";
        } elseif ($reflection->isAbstract()) {
            $content .= "**类型**: 抽象类\n\n";
        } else {
            $content .= "**类型**: 类\n\n";
        }
        
        return $content;
    }
    
    /**
     * 生成方法文档
     */
    private function generateMethodDocs(ReflectionClass $reflection): string
    {
        $content = $this->generateMarkdownHeader('方法', 2);
        
        $methods = $reflection->getMethods(ReflectionMethod::IS_PUBLIC);
        
        foreach ($methods as $method) {
            if ($method->getDeclaringClass()->getName() === $reflection->getName()) {
                $content .= $this->generateMethodDoc($method);
            }
        }
        
        return $content;
    }
    
    /**
     * 生成方法文档
     */
    private function generateMethodDoc(ReflectionMethod $method): string
    {
        $content = $this->generateMarkdownHeader($method->getName(), 3);
        
        $docComment = $method->getDocComment();
        if ($docComment) {
            $description = $this->extractDescription($docComment);
            if ($description) {
                $content .= "{$description}\n\n";
            }
        }
        
        // 方法签名
        $content .= "```php\n";
        $content .= $this->generateMethodSignature($method);
        $content .= "\n```\n\n";
        
        return $content;
    }
    
    /**
     * 生成方法签名
     */
    private function generateMethodSignature(ReflectionMethod $method): string
    {
        $signature = '';
        
        if ($method->isPublic()) {
            $signature .= 'public ';
        } elseif ($method->isProtected()) {
            $signature .= 'protected ';
        } elseif ($method->isPrivate()) {
            $signature .= 'private ';
        }
        
        if ($method->isStatic()) {
            $signature .= 'static ';
        }
        
        $signature .= 'function ' . $method->getName() . '(';
        
        $parameters = [];
        foreach ($method->getParameters() as $param) {
            $paramStr = '';
            if ($param->hasType()) {
                $paramStr .= $param->getType() . ' ';
            }
            $paramStr .= '$' . $param->getName();
            if ($param->isDefaultValueAvailable()) {
                $paramStr .= ' = ' . var_export($param->getDefaultValue(), true);
            }
            $parameters[] = $paramStr;
        }
        
        $signature .= implode(', ', $parameters) . ')';
        
        if ($method->hasReturnType()) {
            $signature .= ': ' . $method->getReturnType();
        }
        
        return $signature;
    }
    
    /**
     * 提取描述
     */
    private function extractDescription(string $docComment): string
    {
        $lines = explode("\n", $docComment);
        $description = '';
        
        foreach ($lines as $line) {
            $line = trim($line, " \t\n\r\0\x0B/*");
            if ($line && !str_starts_with($line, '@')) {
                $description .= $line . ' ';
            }
        }
        
        return trim($description);
    }
    
    /**
     * 生成API索引
     */
    private function generateApiIndex(array $classes, string $outputDir): void
    {
        $content = $this->generateMarkdownHeader('API文档索引', 1);
        
        $categorized = [];
        foreach ($classes as $class) {
            $category = $this->categorizeClass($class['relative_path']);
            $categorized[$category][] = $class;
        }
        
        foreach ($categorized as $category => $classList) {
            $content .= $this->generateMarkdownHeader($category, 2);
            foreach ($classList as $class) {
                $content .= "- [{$class['name']}]({$class['name']}.md)\n";
            }
            $content .= "\n";
        }
        
        file_put_contents($outputDir . 'index.md', $content);
    }
    
    /**
     * 分类类
     */
    private function categorizeClass(string $relativePath): string
    {
        if (str_contains($relativePath, 'Linear')) return '线性数据结构';
        if (str_contains($relativePath, 'Trees')) return '树形数据结构';
        if (str_contains($relativePath, 'Graphs')) return '图数据结构';
        if (str_contains($relativePath, 'Hash')) return '哈希数据结构';
        if (str_contains($relativePath, 'Advanced')) return '高级数据结构';
        if (str_contains($relativePath, 'Algorithms')) return '算法';
        if (str_contains($relativePath, 'Utils')) return '工具类';
        if (str_contains($relativePath, 'Interfaces')) return '接口';
        if (str_contains($relativePath, 'Exceptions')) return '异常类';
        
        return '其他';
    }
    
    /**
     * 生成算法分类文档
     */
    private function generateAlgorithmCategoryDoc(string $className, string $title, string $filePath): string
    {
        $content = $this->generateMarkdownHeader($title, 2);
        
        // 读取文件内容并提取方法
        $fileContent = file_get_contents($filePath);
        preg_match_all('/public static function (\w+)\([^)]*\)/', $fileContent, $matches);
        
        if (!empty($matches[1])) {
            $content .= "**可用方法**:\n\n";
            foreach ($matches[1] as $method) {
                $content .= "- `{$method}()`\n";
            }
            $content .= "\n";
        }
        
        return $content;
    }
    
    /**
     * 生成数据结构分类文档
     */
    private function generateDataStructureCategoryDoc(string $dir, string $title, string $categoryDir): string
    {
        $content = $this->generateMarkdownHeader($title, 2);
        
        $files = glob($categoryDir . '*.php');
        if (!empty($files)) {
            $content .= "**包含的数据结构**:\n\n";
            foreach ($files as $file) {
                $className = basename($file, '.php');
                $content .= "- `{$className}`\n";
            }
            $content .= "\n";
        }
        
        return $content;
    }
    
    /**
     * 生成示例文档
     */
    private function generateExampleDoc(string $exampleFile): string
    {
        $fileName = basename($exampleFile, '.php');
        $content = $this->generateMarkdownHeader($fileName, 2);
        
        $content .= "**文件**: `{$fileName}.php`\n\n";
        $content .= "**运行方式**:\n";
        $content .= "```bash\n";
        $content .= "php examples/{$fileName}.php\n";
        $content .= "```\n\n";
        
        return $content;
    }
}

// 命令行处理
if (basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    $generator = new DocumentationGenerator();
    $generator->generateAll();
}