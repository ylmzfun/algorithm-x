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

    // ==================== 中国剩余定理 ====================

    /**
     * 中国剩余定理 (CRT)
     * 求解同余方程组: x ≡ remainders[i] (mod moduli[i])
     * 要求所有模数两两互质。
     *
     * 时间复杂度: O(n log M)，M = 所有模数乘积
     *
     * @param array $remainders 余数列表
     * @param array $moduli 模数列表（两两互质）
     * @return int|null 最小非负整数解，无解返回 null
     */
    public static function chineseRemainderTheorem(array $remainders, array $moduli): ?int
    {
        $n = count($remainders);
        if ($n === 0 || $n !== count($moduli)) {
            return null;
        }

        // 计算所有模数的乘积 M
        $M = 1;
        foreach ($moduli as $m) {
            $M *= $m;
        }

        $result = 0;
        for ($i = 0; $i < $n; $i++) {
            $Mi = $M / $moduli[$i];
            $inv = self::modInverse((int)$Mi, (int)$moduli[$i]);

            if ($inv === null) {
                return null; // 模逆不存在
            }

            $result = ($result + $remainders[$i] * $Mi * $inv) % $M;
        }

        // 确保非负
        $result = (int)$result;
        return $result < 0 ? $result + $M : $result;
    }

    /**
     * 扩展中国剩余定理（模数不一定互质）
     * 求解 x ≡ remainders[i] (mod moduli[i])
     *
     * @param array $remainders
     * @param array $moduli
     * @return int|null
     */
    public static function extendedCRT(array $remainders, array $moduli): ?int
    {
        $n = count($remainders);
        if ($n === 0) {
            return null;
        }

        $r0 = $remainders[0];
        $m0 = $moduli[0];

        for ($i = 1; $i < $n; $i++) {
            $r1 = $remainders[$i];
            $m1 = $moduli[$i];

            // 使用扩展欧几里得求解: m0 * x + m1 * y = r1 - r0
            $g = self::extendedGcd($m0, $m1);
            $gcd = $g['gcd'];

            if (($r1 - $r0) % $gcd !== 0) {
                return null; // 无解
            }

            $x = $g['x'];
            $lcm = $m0 / $gcd * $m1;

            // x ≡ r0 + m0 * (r1 - r0) / gcd * x (mod lcm)
            $r0 = ($r0 + $m0 * (($r1 - $r0) / $gcd) * $x) % $lcm;
            $r0 = ($r0 + $lcm) % $lcm;
            $m0 = (int)$lcm;
        }

        return (int)$r0;
    }

    // ==================== 矩阵快速幂 ====================

    /**
     * 矩阵快速幂
     * 计算矩阵 mat 的 exp 次幂
     * 时间复杂度: O(n³ log exp)
     *
     * @param array $mat 方阵（二维数组）
     * @param int $exp 指数
     * @param int|null $mod 可选模数
     * @return array
     */
    public static function matrixPower(array $mat, int $exp, ?int $mod = null): array
    {
        $n = count($mat);
        if ($n === 0 || $exp < 0) {
            return [];
        }

        // 初始化为单位矩阵
        $result = [];
        for ($i = 0; $i < $n; $i++) {
            $result[$i] = array_fill(0, $n, 0);
            $result[$i][$i] = 1;
        }

        $base = $mat;

        while ($exp > 0) {
            if ($exp & 1) {
                $result = self::matrixMultiply($result, $base, $mod);
            }
            $base = self::matrixMultiply($base, $base, $mod);
            $exp >>= 1;
        }

        return $result;
    }

    /**
     * 矩阵乘法
     *
     * @param array $a
     * @param array $b
     * @param int|null $mod
     * @return array
     */
    private static function matrixMultiply(array $a, array $b, ?int $mod = null): array
    {
        $n = count($a);
        $m = count($b[0] ?? []);
        $p = count($b);
        $result = [];

        for ($i = 0; $i < $n; $i++) {
            $result[$i] = array_fill(0, $m, 0);
            for ($j = 0; $j < $m; $j++) {
                for ($k = 0; $k < $p; $k++) {
                    $result[$i][$j] += $a[$i][$k] * $b[$k][$j];
                    if ($mod !== null) {
                        $result[$i][$j] %= $mod;
                    }
                }
            }
        }

        return $result;
    }

    /**
     * 斐波那契数列（矩阵快速幂版）
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     *
     * @param int $n 第 n 项（0-indexed）
     * @param int|null $mod 可选模数
     * @return int
     */
    public static function fibonacciMatrix(int $n, ?int $mod = null): int
    {
        if ($n <= 1) {
            return $n;
        }

        $base = [[1, 1], [1, 0]];
        $result = self::matrixPower($base, $n - 1, $mod);

        $fib = $result[0][0];
        if ($mod !== null) {
            $fib %= $mod;
        }

        return (int)$fib;
    }

    /**
     * 线性递推（矩阵快速幂求解）
     * 对形如 a[n] = c0*a[n-1] + c1*a[n-2] + ... + c[k-1]*a[n-k] 的递推式，
     * 给定前 k 项初值，求第 n 项。
     *
     * @param array $coeffs 系数 [c0, c1, ..., c[k-1]]，对应 a[n-1], a[n-2], ...
     * @param array $init 初始值 [a[0], a[1], ..., a[k-1]]（共 k 项）
     * @param int $n 目标项索引
     * @param int|null $mod 可选模数
     * @return int
     */
    public static function linearRecurrence(array $coeffs, array $init, int $n, ?int $mod = null): int
    {
        $k = count($coeffs);

        if ($n < $k) {
            return $init[$n];
        }

        // 构建转移矩阵
        $matrix = [];
        for ($i = 0; $i < $k; $i++) {
            $matrix[$i] = array_fill(0, $k, 0);
            if ($i === 0) {
                for ($j = 0; $j < $k; $j++) {
                    $matrix[$i][$j] = $coeffs[$j];
                }
            } else {
                $matrix[$i][$i - 1] = 1;
            }
        }

        $powered = self::matrixPower($matrix, $n - $k + 1, $mod);

        // 结果 = powered * init_vector（取第一行点积）
        $result = 0;
        for ($j = 0; $j < $k; $j++) {
            $result += $powered[0][$j] * $init[$k - 1 - $j];
            if ($mod !== null) {
                $result %= $mod;
            }
        }

        return (int)$result;
    }

    // ==================== 博弈论 ====================

    /**
     * Nim 游戏判定
     * 有 n 堆石子，每堆有 stones[i] 个。
     * 两人轮流取石子，每次可以从任一堆中取任意数量的石子（至少1个）。
     * 无法取石子者输。判断先手是否必胜。
     *
     * 结论：所有堆石子数的异或和不为0时先手必胜。
     *
     * 时间复杂度: O(n)
     *
     * @param array $stones 每堆石子数量
     * @return bool 先手是否必胜
     */
    public static function nimGame(array $stones): bool
    {
        $xor = 0;
        foreach ($stones as $s) {
            $xor ^= $s;
        }
        return $xor !== 0;
    }

    /**
     * Nim 游戏求必胜策略的第一步
     *
     * @param array $stones 每堆石子数量
     * @return array|null 必胜策略: ['pile' => index, 'take' => count]，无可胜策略返回 null
     */
    public static function nimWinningMove(array $stones): ?array
    {
        $xor = 0;
        foreach ($stones as $s) {
            $xor ^= $s;
        }

        if ($xor === 0) {
            return null; // 必败局面
        }

        foreach ($stones as $i => $s) {
            $target = $s ^ $xor;
            if ($target < $s) {
                return ['pile' => $i, 'take' => $s - $target];
            }
        }

        return null;
    }

    /**
     * SG 函数（Sprague-Grundy）
     * 对有向图游戏，计算一个状态的 SG 值。
     *
     * @param int $state 当前状态值
     * @param callable $transitions 转移函数: f(state) => [next_state1, next_state2, ...]
     * @param array &$memo 记忆化缓存
     * @return int SG 值
     */
    public static function sgFunction(int $state, callable $transitions, array &$memo = []): int
    {
        if (isset($memo[$state])) {
            return $memo[$state];
        }

        $nextStates = $transitions($state);
        $reachable = [];

        foreach ($nextStates as $next) {
            $sg = self::sgFunction($next, $transitions, $memo);
            $reachable[$sg] = true;
        }

        // mex: 最小的不在集合中的非负整数
        $g = 0;
        while (isset($reachable[$g])) {
            $g++;
        }

        $memo[$state] = $g;
        return $g;
    }

    /**
     * SG 定理：组合游戏的 SG 值等于各子游戏 SG 值的异或
     *
     * @param array $positions 各子游戏的位置
     * @param callable $transitions 转移函数
     * @return int 组合 SG 值
     */
    public static function sgComposite(array $positions, callable $transitions): int
    {
        $xor = 0;
        foreach ($positions as $pos) {
            $xor ^= self::sgFunction($pos, $transitions);
        }
        return $xor;
    }

    /**
     * 判断 SG 组合游戏中先手是否必胜
     *
     * @param array $positions
     * @param callable $transitions
     * @return bool
     */
    public static function sgIsWinning(array $positions, callable $transitions): bool
    {
        return self::sgComposite($positions, $transitions) !== 0;
    }

    // ==================== 线性同余方程 ====================

    /**
     * 求解线性同余方程: a * x ≡ b (mod m)
     * 返回最小非负整数解，无解返回 null
     *
     * 时间复杂度: O(log m)
     *
     * @param int $a
     * @param int $b
     * @param int $m
     * @return int|null
     */
    public static function linearCongruence(int $a, int $b, int $m): ?int
    {
        $a = (($a % $m) + $m) % $m;
        $b = (($b % $m) + $m) % $m;

        if ($a === 0) {
            return $b === 0 ? 0 : null;
        }

        $g = self::extendedGcd($a, $m);
        $gcd = $g['gcd'];

        if ($b % $gcd !== 0) {
            return null;
        }

        $x0 = $g['x'] * ($b / $gcd);
        $mod = $m / $gcd;

        $x0 = (int)(($x0 % $mod + $mod) % $mod);
        return $x0;
    }

    /**
     * 求解线性丢番图方程: a*x + b*y = c
     * 返回一组特解 ['x' => int, 'y' => int] 或 null
     *
     * @param int $a
     * @param int $b
     * @param int $c
     * @return array|null
     */
    public static function linearDiophantine(int $a, int $b, int $c): ?array
    {
        $g = self::extendedGcd(abs($a), abs($b));
        $gcd = $g['gcd'];

        if ($c % $gcd !== 0) {
            return null;
        }

        $x0 = $g['x'] * ($c / $gcd);
        $y0 = $g['y'] * ($c / $gcd);

        if ($a < 0) {
            $x0 = -$x0;
        }
        if ($b < 0) {
            $y0 = -$y0;
        }

        return ['x' => (int)$x0, 'y' => (int)$y0];
    }

    // ==================== 概率算法 ====================

    /**
     * Miller-Rabin 素性测试（概率算法）
     *
     * 判断 n 是否可能为素数。经过 k 轮测试后，错误概率 ≤ 1/4^k。
     * 对于 n < 2^64，使用特定底数集合可确定性地判定。
     *
     * 时间复杂度: O(k log³ n)
     *
     * @param int $n
     * @param int $k 测试轮数（默认10，错误率 ~ 1/10^6）
     * @return bool true = 很可能是素数, false = 一定不是素数
     */
    public static function millerRabin(int $n, int $k = 10): bool
    {
        if ($n < 2) {
            return false;
        }
        if ($n === 2 || $n === 3) {
            return true;
        }
        if ($n % 2 === 0) {
            return false;
        }

        // 写 n-1 = d * 2^s
        $d = $n - 1;
        $s = 0;
        while ($d % 2 === 0) {
            $d = (int)($d / 2);
            $s++;
        }

        // 确定性底数集合（对 n < 2^64 有效）
        $deterministicBases = [2, 3, 5, 7, 11, 13, 17];
        $bases = ($n < PHP_INT_MAX) ? $deterministicBases : [];

        for ($i = 0; $i < $k && (empty($bases) || $i < count($bases)); $i++) {
            $a = !empty($bases) ? $bases[$i] : random_int(2, min($n - 2, PHP_INT_MAX));
            if ($a >= $n) {
                continue;
            }

            $x = self::modPow($a, $d, $n);
            if ($x === 1 || $x === $n - 1) {
                continue;
            }

            $composite = true;
            for ($r = 0; $r < $s - 1; $r++) {
                $x = self::modMul($x, $x, $n);
                if ($x === $n - 1) {
                    $composite = false;
                    break;
                }
            }

            if ($composite) {
                return false;
            }
        }

        return true;
    }

    /**
     * 蒙特卡洛方法估算 π
     *
     * @param int $samples 采样点数
     * @return float π 的估计值
     */
    public static function monteCarloPi(int $samples = 100000): float
    {
        $inside = 0;
        for ($i = 0; $i < $samples; $i++) {
            $x = mt_rand() / mt_getrandmax();
            $y = mt_rand() / mt_getrandmax();
            if ($x * $x + $y * $y <= 1.0) {
                $inside++;
            }
        }
        return 4.0 * $inside / $samples;
    }

    /**
     * 模乘 (a * b) % mod，安全处理溢出
     */
    private static function modMul(int $a, int $b, int $mod): int
    {
        $result = 0;
        $a %= $mod;
        $b %= $mod;
        while ($b > 0) {
            if ($b & 1) {
                $result = ($result + $a) % $mod;
            }
            $a = ($a * 2) % $mod;
            $b >>= 1;
        }
        return $result;
    }

    /**
     * 模幂运算 (base^exp) % mod
     */
    private static function modPow(int $base, int $exp, int $mod): int
    {
        $result = 1;
        $base %= $mod;
        while ($exp > 0) {
            if ($exp & 1) {
                $result = self::modMul($result, $base, $mod);
            }
            $base = self::modMul($base, $base, $mod);
            $exp >>= 1;
        }
        return $result;
    }

    // ==================== 随机化算法 ====================

    /**
     * Fisher-Yates 洗牌算法
     *
     * 时间复杂度: O(n)，空间复杂度: O(1)
     *
     * @param array $arr
     * @return array 随机排列后的数组
     */
    public static function shuffle(array $arr): array
    {
        $n = count($arr);
        for ($i = $n - 1; $i > 0; $i--) {
            $j = random_int(0, $i);
            [$arr[$i], $arr[$j]] = [$arr[$j], $arr[$i]];
        }
        return $arr;
    }

    /**
     * 随机化快速选择 — 查找第 k 小的元素（k 为 0-indexed）
     *
     * O(n) 期望时间
     *
     * @param array $arr
     * @param int $k
     * @return mixed
     */
    public static function quickSelect(array $arr, int $k)
    {
        $n = count($arr);
        if ($n === 0 || $k < 0 || $k >= $n) {
            return null;
        }

        $left = 0;
        $right = $n - 1;

        while ($left <= $right) {
            $pivotIdx = random_int($left, $right);
            [$arr[$pivotIdx], $arr[$right]] = [$arr[$right], $arr[$pivotIdx]];
            $pivot = $arr[$right];

            $i = $left;
            for ($j = $left; $j < $right; $j++) {
                if ($arr[$j] <= $pivot) {
                    [$arr[$i], $arr[$j]] = [$arr[$j], $arr[$i]];
                    $i++;
                }
            }
            [$arr[$i], $arr[$right]] = [$arr[$right], $arr[$i]];

            if ($i === $k) {
                return $arr[$i];
            } elseif ($i < $k) {
                $left = $i + 1;
            } else {
                $right = $i - 1;
            }
        }

        return null;
    }

    /**
     * 蓄水池抽样 — 从长度未知的数据流中随机等概率选取 k 个元素
     *
     * @param array $stream 数据流（模拟）
     * @param int $k
     * @return array
     */
    public static function reservoirSampling(array $stream, int $k): array
    {
        $reservoir = [];
        $n = count($stream);

        for ($i = 0; $i < $n; $i++) {
            if ($i < $k) {
                $reservoir[$i] = $stream[$i];
            } else {
                $j = random_int(0, $i);
                if ($j < $k) {
                    $reservoir[$j] = $stream[$i];
                }
            }
        }

        return $reservoir;
    }
}