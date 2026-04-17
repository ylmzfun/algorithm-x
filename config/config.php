<?php

/**
 * 项目配置文件
 * 包含项目的各种配置参数和常量定义
 */

namespace DataStructures\Config;

/**
 * 项目配置类
 */
class Config
{
    /**
     * 项目基本信息
     */
    public const PROJECT_NAME = 'PHP Data Structures & Algorithms';
    public const PROJECT_VERSION = '2.0.0';
    public const PROJECT_AUTHOR = 'PHP Algorithm Team';
    public const PROJECT_DESCRIPTION = 'A comprehensive PHP library for data structures and algorithms';
    
    /**
     * 性能测试配置
     */
    public const PERFORMANCE_TEST_SIZES = [100, 500, 1000, 5000, 10000];
    public const PERFORMANCE_TEST_ITERATIONS = 3;
    public const PERFORMANCE_MEMORY_LIMIT = '512M';
    public const PERFORMANCE_TIME_LIMIT = 300; // 5分钟
    
    /**
     * 算法配置
     */
    public const DEFAULT_ARRAY_SIZE = 1000;
    public const MAX_ARRAY_SIZE = 100000;
    public const MIN_ARRAY_VALUE = 1;
    public const MAX_ARRAY_VALUE = 10000;
    
    /**
     * 图算法配置
     */
    public const MAX_VERTICES = 1000;
    public const DEFAULT_GRAPH_DENSITY = 0.3; // 30%的边密度
    
    /**
     * 字符串算法配置
     */
    public const MAX_STRING_LENGTH = 10000;
    public const DEFAULT_ALPHABET_SIZE = 256; // ASCII字符集
    
    /**
     * 动态规划配置
     */
    public const DP_MAX_CACHE_SIZE = 10000;
    public const DP_FIBONACCI_MAX = 50;
    public const DP_KNAPSACK_MAX_WEIGHT = 1000;
    
    /**
     * 数学算法配置
     */
    public const PRIME_SIEVE_MAX = 1000000;
    public const FAST_POWER_MOD = 1000000007;
    public const GCD_MAX_ITERATIONS = 1000;
    
    /**
     * 测试配置
     */
    public const TEST_DATA_DIR = __DIR__ . '/../tests/data/';
    public const TEST_OUTPUT_DIR = __DIR__ . '/../tests/output/';
    public const TEST_TIMEOUT = 30; // 30秒
    
    /**
     * 日志配置
     */
    public const LOG_LEVEL_DEBUG = 0;
    public const LOG_LEVEL_INFO = 1;
    public const LOG_LEVEL_WARNING = 2;
    public const LOG_LEVEL_ERROR = 3;
    public const DEFAULT_LOG_LEVEL = self::LOG_LEVEL_INFO;
    
    /**
     * 缓存配置
     */
    public const CACHE_ENABLED = true;
    public const CACHE_TTL = 3600; // 1小时
    public const CACHE_MAX_SIZE = 1000;
    
    /**
     * 输出格式配置
     */
    public const OUTPUT_FORMAT_TEXT = 'text';
    public const OUTPUT_FORMAT_JSON = 'json';
    public const OUTPUT_FORMAT_XML = 'xml';
    public const DEFAULT_OUTPUT_FORMAT = self::OUTPUT_FORMAT_TEXT;
    
    /**
     * 错误处理配置
     */
    public const ERROR_REPORTING_LEVEL = E_ALL;
    public const DISPLAY_ERRORS = true;
    public const LOG_ERRORS = true;
    
    /**
     * 获取所有配置
     */
    public static function getAll(): array
    {
        $reflection = new \ReflectionClass(self::class);
        return $reflection->getConstants();
    }
    
    /**
     * 获取项目信息
     */
    public static function getProjectInfo(): array
    {
        return [
            'name' => self::PROJECT_NAME,
            'version' => self::PROJECT_VERSION,
            'author' => self::PROJECT_AUTHOR,
            'description' => self::PROJECT_DESCRIPTION,
            'php_version' => PHP_VERSION,
            'memory_limit' => ini_get('memory_limit'),
            'max_execution_time' => ini_get('max_execution_time')
        ];
    }
    
    /**
     * 获取性能测试配置
     */
    public static function getPerformanceConfig(): array
    {
        return [
            'test_sizes' => self::PERFORMANCE_TEST_SIZES,
            'iterations' => self::PERFORMANCE_TEST_ITERATIONS,
            'memory_limit' => self::PERFORMANCE_MEMORY_LIMIT,
            'time_limit' => self::PERFORMANCE_TIME_LIMIT
        ];
    }
    
    /**
     * 获取算法配置
     */
    public static function getAlgorithmConfig(): array
    {
        return [
            'default_array_size' => self::DEFAULT_ARRAY_SIZE,
            'max_array_size' => self::MAX_ARRAY_SIZE,
            'array_value_range' => [self::MIN_ARRAY_VALUE, self::MAX_ARRAY_VALUE],
            'max_vertices' => self::MAX_VERTICES,
            'graph_density' => self::DEFAULT_GRAPH_DENSITY,
            'max_string_length' => self::MAX_STRING_LENGTH,
            'alphabet_size' => self::DEFAULT_ALPHABET_SIZE
        ];
    }
    
    /**
     * 设置PHP运行时配置
     */
    public static function setupRuntime(): void
    {
        // 设置错误报告
        error_reporting(self::ERROR_REPORTING_LEVEL);
        ini_set('display_errors', self::DISPLAY_ERRORS ? '1' : '0');
        ini_set('log_errors', self::LOG_ERRORS ? '1' : '0');
        
        // 设置内存限制
        ini_set('memory_limit', self::PERFORMANCE_MEMORY_LIMIT);
        
        // 设置执行时间限制
        set_time_limit(self::PERFORMANCE_TIME_LIMIT);
        
        // 设置时区
        date_default_timezone_set('Asia/Shanghai');
    }
    
    /**
     * 验证配置
     */
    public static function validate(): array
    {
        $errors = [];
        
        // 检查内存限制
        $memoryLimit = ini_get('memory_limit');
        if ($memoryLimit !== '-1' && self::parseMemoryLimit($memoryLimit) < self::parseMemoryLimit(self::PERFORMANCE_MEMORY_LIMIT)) {
            $errors[] = "Memory limit too low: {$memoryLimit} < " . self::PERFORMANCE_MEMORY_LIMIT;
        }
        
        // 检查PHP版本
        if (version_compare(PHP_VERSION, '7.4.0', '<')) {
            $errors[] = "PHP version too old: " . PHP_VERSION . " < 7.4.0";
        }
        
        // 检查必要的扩展
        $requiredExtensions = ['json', 'mbstring'];
        foreach ($requiredExtensions as $ext) {
            if (!extension_loaded($ext)) {
                $errors[] = "Required extension not loaded: {$ext}";
            }
        }
        
        return $errors;
    }
    
    /**
     * 解析内存限制字符串
     */
    private static function parseMemoryLimit(string $limit): int
    {
        $limit = trim($limit);
        $last = strtolower($limit[strlen($limit) - 1]);
        $value = (int) $limit;
        
        switch ($last) {
            case 'g':
                $value *= 1024;
            case 'm':
                $value *= 1024;
            case 'k':
                $value *= 1024;
        }
        
        return $value;
    }
}

// 自动设置运行时配置
Config::setupRuntime();