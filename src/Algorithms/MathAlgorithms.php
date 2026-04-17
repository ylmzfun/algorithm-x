<?php

namespace DataStructures\Algorithms;

/**
 * 数学算法集合
 * 包含经典的数学算法和数论算法
 */
class MathAlgorithms
{
    /**
     * 最大公约数（欧几里得算法）
     * 时间复杂度: O(log(min(a,b))), 空间复杂度: O(1)
     */
    public static function gcd(int $a, int $b): int
    {
        while ($b !== 0) {
            $temp = $b;
            $b = $a % $b;
            $a = $temp;
        }
        return abs($a);
    }
    
    /**
     * 最小公倍数
     * 时间复杂度: O(log(min(a,b))), 空间复杂度: O(1)
     */
    public static function lcm(int $a, int $b): int
    {
        return abs($a * $b) / self::gcd($a, $b);
    }
    
    /**
     * 判断是否为质数
     * 时间复杂度: O(sqrt(n)), 空间复杂度: O(1)
     */
    public static function isPrime(int $n): bool
    {
        if ($n < 2) return false;
        if ($n === 2) return true;
        if ($n % 2 === 0) return false;
        
        for ($i = 3; $i * $i <= $n; $i += 2) {
            if ($n % $i === 0) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * 埃拉托斯特尼筛法生成质数
     * 时间复杂度: O(n log log n), 空间复杂度: O(n)
     */
    public static function sieveOfEratosthenes(int $n): array
    {
        if ($n < 2) return [];
        
        $isPrime = array_fill(0, $n + 1, true);
        $isPrime[0] = $isPrime[1] = false;
        
        for ($i = 2; $i * $i <= $n; $i++) {
            if ($isPrime[$i]) {
                for ($j = $i * $i; $j <= $n; $j += $i) {
                    $isPrime[$j] = false;
                }
            }
        }
        
        $primes = [];
        for ($i = 2; $i <= $n; $i++) {
            if ($isPrime[$i]) {
                $primes[] = $i;
            }
        }
        
        return $primes;
    }
    
    /**
     * 快速幂算法
     * 时间复杂度: O(log n), 空间复杂度: O(1)
     */
    public static function fastPower(int $base, int $exp, int $mod = null): int
    {
        $result = 1;
        $base = $base % ($mod ?? PHP_INT_MAX);
        
        while ($exp > 0) {
            if ($exp % 2 === 1) {
                $result = ($result * $base) % ($mod ?? PHP_INT_MAX);
            }
            $exp = intval($exp / 2);
            $base = ($base * $base) % ($mod ?? PHP_INT_MAX);
        }
        
        return $result;
    }
    
    /**
     * 扩展欧几里得算法
     * 求解 ax + by = gcd(a, b)
     */
    public static function extendedGcd(int $a, int $b): array
    {
        if ($b === 0) {
            return ['gcd' => $a, 'x' => 1, 'y' => 0];
        }
        
        $result = self::extendedGcd($b, $a % $b);
        $x = $result['y'];
        $y = $result['x'] - intval($a / $b) * $result['y'];
        
        return ['gcd' => $result['gcd'], 'x' => $x, 'y' => $y];
    }
    
    /**
     * 模逆元
     * 时间复杂度: O(log m), 空间复杂度: O(1)
     */
    public static function modInverse(int $a, int $m): ?int
    {
        $result = self::extendedGcd($a, $m);
        
        if ($result['gcd'] !== 1) {
            return null; // 模逆元不存在
        }
        
        return ($result['x'] % $m + $m) % $m;
    }
    
    /**
     * 阶乘
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function factorial(int $n): int
    {
        if ($n < 0) return 0;
        if ($n <= 1) return 1;
        
        $result = 1;
        for ($i = 2; $i <= $n; $i++) {
            $result *= $i;
        }
        
        return $result;
    }
    
    /**
     * 组合数 C(n, k)
     * 时间复杂度: O(k), 空间复杂度: O(1)
     */
    public static function combination(int $n, int $k): int
    {
        if ($k > $n || $k < 0) return 0;
        if ($k === 0 || $k === $n) return 1;
        
        $k = min($k, $n - $k); // 利用对称性
        
        $result = 1;
        for ($i = 0; $i < $k; $i++) {
            $result = $result * ($n - $i) / ($i + 1);
        }
        
        return intval($result);
    }
    
    /**
     * 排列数 P(n, k)
     * 时间复杂度: O(k), 空间复杂度: O(1)
     */
    public static function permutation(int $n, int $k): int
    {
        if ($k > $n || $k < 0) return 0;
        if ($k === 0) return 1;
        
        $result = 1;
        for ($i = 0; $i < $k; $i++) {
            $result *= ($n - $i);
        }
        
        return $result;
    }
    
    /**
     * 卡塔兰数
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function catalan(int $n): int
    {
        if ($n <= 1) return 1;
        
        $result = 0;
        for ($i = 0; $i < $n; $i++) {
            $result += self::catalan($i) * self::catalan($n - 1 - $i);
        }
        
        return $result;
    }
    
    /**
     * 卡塔兰数（动态规划版本）
     * 时间复杂度: O(n²), 空间复杂度: O(n)
     */
    public static function catalanDP(int $n): int
    {
        if ($n <= 1) return 1;
        
        $catalan = array_fill(0, $n + 1, 0);
        $catalan[0] = $catalan[1] = 1;
        
        for ($i = 2; $i <= $n; $i++) {
            for ($j = 0; $j < $i; $j++) {
                $catalan[$i] += $catalan[$j] * $catalan[$i - 1 - $j];
            }
        }
        
        return $catalan[$n];
    }
    
    /**
     * 平方根（牛顿法）
     * 时间复杂度: O(log n), 空间复杂度: O(1)
     */
    public static function sqrt(float $x, float $precision = 1e-10): float
    {
        if ($x < 0) return NAN;
        if ($x === 0) return 0;
        
        $guess = $x / 2;
        
        while (abs($guess * $guess - $x) > $precision) {
            $guess = ($guess + $x / $guess) / 2;
        }
        
        return $guess;
    }
    
    /**
     * 整数平方根
     * 时间复杂度: O(log n), 空间复杂度: O(1)
     */
    public static function intSqrt(int $x): int
    {
        if ($x < 0) return -1;
        if ($x < 2) return $x;
        
        $left = 1;
        $right = intval($x / 2) + 1;
        
        while ($left <= $right) {
            $mid = $left + intval(($right - $left) / 2);
            $square = $mid * $mid;
            
            if ($square === $x) {
                return $mid;
            } elseif ($square < $x) {
                $left = $mid + 1;
            } else {
                $right = $mid - 1;
            }
        }
        
        return $right;
    }
    
    /**
     * 判断完全平方数
     * 时间复杂度: O(log n), 空间复杂度: O(1)
     */
    public static function isPerfectSquare(int $num): bool
    {
        if ($num < 0) return false;
        
        $sqrt = self::intSqrt($num);
        return $sqrt * $sqrt === $num;
    }
    
    /**
     * 数字反转
     * 时间复杂度: O(log n), 空间复杂度: O(1)
     */
    public static function reverseInteger(int $x): int
    {
        $result = 0;
        $sign = $x < 0 ? -1 : 1;
        $x = abs($x);
        
        while ($x > 0) {
            $result = $result * 10 + $x % 10;
            $x = intval($x / 10);
        }
        
        $result *= $sign;
        
        // 检查32位整数溢出
        if ($result < -2147483648 || $result > 2147483647) {
            return 0;
        }
        
        return $result;
    }
    
    /**
     * 判断回文数
     * 时间复杂度: O(log n), 空间复杂度: O(1)
     */
    public static function isPalindrome(int $x): bool
    {
        if ($x < 0) return false;
        
        return $x === self::reverseInteger($x);
    }
    
    /**
     * 计算数字的各位数字之和
     * 时间复杂度: O(log n), 空间复杂度: O(1)
     */
    public static function digitSum(int $n): int
    {
        $sum = 0;
        $n = abs($n);
        
        while ($n > 0) {
            $sum += $n % 10;
            $n = intval($n / 10);
        }
        
        return $sum;
    }
    
    /**
     * 计算数字的位数
     * 时间复杂度: O(log n), 空间复杂度: O(1)
     */
    public static function countDigits(int $n): int
    {
        if ($n === 0) return 1;
        
        $count = 0;
        $n = abs($n);
        
        while ($n > 0) {
            $count++;
            $n = intval($n / 10);
        }
        
        return $count;
    }
    
    /**
     * 约瑟夫问题
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function josephus(int $n, int $k): int
    {
        $result = 0;
        
        for ($i = 2; $i <= $n; $i++) {
            $result = ($result + $k) % $i;
        }
        
        return $result + 1; // 转换为1-based索引
    }
    
    /**
     * 计算两点间距离
     * 时间复杂度: O(1), 空间复杂度: O(1)
     */
    public static function distance(array $point1, array $point2): float
    {
        $dx = $point1[0] - $point2[0];
        $dy = $point1[1] - $point2[1];
        
        return sqrt($dx * $dx + $dy * $dy);
    }
    
    /**
     * 判断三点是否共线
     * 时间复杂度: O(1), 空间复杂度: O(1)
     */
    public static function areCollinear(array $p1, array $p2, array $p3): bool
    {
        // 使用叉积判断
        $area = ($p2[0] - $p1[0]) * ($p3[1] - $p1[1]) - ($p3[0] - $p1[0]) * ($p2[1] - $p1[1]);
        return abs($area) < 1e-10;
    }
}