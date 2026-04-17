<?php

namespace DataStructures\Algorithms;

/**
 * 字符串算法集合
 * 包含常见的字符串处理和模式匹配算法
 */
class StringAlgorithms
{
    /**
     * KMP (Knuth-Morris-Pratt) 字符串匹配算法
     * 时间复杂度: O(n + m)
     * 空间复杂度: O(m)
     */
    public static function kmpSearch(string $text, string $pattern): array
    {
        $n = strlen($text);
        $m = strlen($pattern);
        
        if ($m === 0) return [];
        
        $lps = self::computeLPS($pattern);
        $matches = [];
        
        $i = 0; // text的索引
        $j = 0; // pattern的索引
        
        while ($i < $n) {
            if ($text[$i] === $pattern[$j]) {
                $i++;
                $j++;
            }
            
            if ($j === $m) {
                $matches[] = $i - $j;
                $j = $lps[$j - 1];
            } elseif ($i < $n && $text[$i] !== $pattern[$j]) {
                if ($j !== 0) {
                    $j = $lps[$j - 1];
                } else {
                    $i++;
                }
            }
        }
        
        return $matches;
    }
    
    /**
     * 计算LPS (Longest Proper Prefix which is also Suffix) 数组
     */
    private static function computeLPS(string $pattern): array
    {
        $m = strlen($pattern);
        $lps = array_fill(0, $m, 0);
        $len = 0;
        $i = 1;
        
        while ($i < $m) {
            if ($pattern[$i] === $pattern[$len]) {
                $len++;
                $lps[$i] = $len;
                $i++;
            } else {
                if ($len !== 0) {
                    $len = $lps[$len - 1];
                } else {
                    $lps[$i] = 0;
                    $i++;
                }
            }
        }
        
        return $lps;
    }
    
    /**
     * Rabin-Karp 字符串匹配算法
     * 时间复杂度: 平均 O(n + m), 最坏 O(nm)
     * 空间复杂度: O(1)
     */
    public static function rabinKarpSearch(string $text, string $pattern): array
    {
        $n = strlen($text);
        $m = strlen($pattern);
        $prime = 101; // 质数
        $base = 256; // 字符集大小
        
        if ($m > $n) return [];
        
        $matches = [];
        $patternHash = 0;
        $textHash = 0;
        $h = 1;
        
        // 计算 base^(m-1) % prime
        for ($i = 0; $i < $m - 1; $i++) {
            $h = ($h * $base) % $prime;
        }
        
        // 计算模式和第一个窗口的哈希值
        for ($i = 0; $i < $m; $i++) {
            $patternHash = ($base * $patternHash + ord($pattern[$i])) % $prime;
            $textHash = ($base * $textHash + ord($text[$i])) % $prime;
        }
        
        // 滑动窗口
        for ($i = 0; $i <= $n - $m; $i++) {
            if ($patternHash === $textHash) {
                // 哈希值匹配，验证字符串
                if (substr($text, $i, $m) === $pattern) {
                    $matches[] = $i;
                }
            }
            
            // 计算下一个窗口的哈希值
            if ($i < $n - $m) {
                $textHash = ($base * ($textHash - ord($text[$i]) * $h) + ord($text[$i + $m])) % $prime;
                if ($textHash < 0) {
                    $textHash += $prime;
                }
            }
        }
        
        return $matches;
    }
    
    /**
     * Boyer-Moore 字符串匹配算法
     * 时间复杂度: 平均 O(n/m), 最坏 O(nm)
     * 空间复杂度: O(σ) σ为字符集大小
     */
    public static function boyerMooreSearch(string $text, string $pattern): array
    {
        $n = strlen($text);
        $m = strlen($pattern);
        
        if ($m === 0) return [];
        
        $badChar = self::buildBadCharTable($pattern);
        $matches = [];
        $s = 0; // 模式相对于文本的偏移
        
        while ($s <= $n - $m) {
            $j = $m - 1;
            
            // 从右到左匹配
            while ($j >= 0 && $pattern[$j] === $text[$s + $j]) {
                $j--;
            }
            
            if ($j < 0) {
                $matches[] = $s;
                $s += ($s + $m < $n) ? $m - ($badChar[ord($text[$s + $m])] ?? -1) : 1;
            } else {
                $s += max(1, $j - ($badChar[ord($text[$s + $j])] ?? -1));
            }
        }
        
        return $matches;
    }
    
    /**
     * 构建坏字符表
     */
    private static function buildBadCharTable(string $pattern): array
    {
        $m = strlen($pattern);
        $badChar = [];
        
        for ($i = 0; $i < $m; $i++) {
            $badChar[ord($pattern[$i])] = $i;
        }
        
        return $badChar;
    }
    
    /**
     * 最长公共子序列 (LCS)
     * 时间复杂度: O(mn)
     * 空间复杂度: O(mn)
     */
    public static function longestCommonSubsequence(string $str1, string $str2): string
    {
        $m = strlen($str1);
        $n = strlen($str2);
        
        $dp = array_fill(0, $m + 1, array_fill(0, $n + 1, 0));
        
        // 填充DP表
        for ($i = 1; $i <= $m; $i++) {
            for ($j = 1; $j <= $n; $j++) {
                if ($str1[$i - 1] === $str2[$j - 1]) {
                    $dp[$i][$j] = $dp[$i - 1][$j - 1] + 1;
                } else {
                    $dp[$i][$j] = max($dp[$i - 1][$j], $dp[$i][$j - 1]);
                }
            }
        }
        
        // 重构LCS
        $lcs = '';
        $i = $m;
        $j = $n;
        
        while ($i > 0 && $j > 0) {
            if ($str1[$i - 1] === $str2[$j - 1]) {
                $lcs = $str1[$i - 1] . $lcs;
                $i--;
                $j--;
            } elseif ($dp[$i - 1][$j] > $dp[$i][$j - 1]) {
                $i--;
            } else {
                $j--;
            }
        }
        
        return $lcs;
    }
    
    /**
     * 编辑距离 (Levenshtein Distance)
     * 时间复杂度: O(mn)
     * 空间复杂度: O(mn)
     */
    public static function editDistance(string $str1, string $str2): int
    {
        $m = strlen($str1);
        $n = strlen($str2);
        
        $dp = array_fill(0, $m + 1, array_fill(0, $n + 1, 0));
        
        // 初始化边界
        for ($i = 0; $i <= $m; $i++) {
            $dp[$i][0] = $i;
        }
        for ($j = 0; $j <= $n; $j++) {
            $dp[0][$j] = $j;
        }
        
        // 填充DP表
        for ($i = 1; $i <= $m; $i++) {
            for ($j = 1; $j <= $n; $j++) {
                if ($str1[$i - 1] === $str2[$j - 1]) {
                    $dp[$i][$j] = $dp[$i - 1][$j - 1];
                } else {
                    $dp[$i][$j] = 1 + min(
                        $dp[$i - 1][$j],     // 删除
                        $dp[$i][$j - 1],     // 插入
                        $dp[$i - 1][$j - 1]  // 替换
                    );
                }
            }
        }
        
        return $dp[$m][$n];
    }
    
    /**
     * 最长回文子串 (Manacher算法)
     * 时间复杂度: O(n)
     * 空间复杂度: O(n)
     */
    public static function longestPalindrome(string $s): string
    {
        if (empty($s)) return '';
        
        // 预处理字符串
        $processed = '#' . implode('#', str_split($s)) . '#';
        $n = strlen($processed);
        $p = array_fill(0, $n, 0);
        $center = 0;
        $right = 0;
        $maxLen = 0;
        $centerIndex = 0;
        
        for ($i = 0; $i < $n; $i++) {
            $mirror = 2 * $center - $i;
            
            if ($i < $right) {
                $p[$i] = min($right - $i, $p[$mirror]);
            }
            
            // 尝试扩展回文
            while ($i + $p[$i] + 1 < $n && $i - $p[$i] - 1 >= 0 && 
                   $processed[$i + $p[$i] + 1] === $processed[$i - $p[$i] - 1]) {
                $p[$i]++;
            }
            
            // 更新中心和右边界
            if ($i + $p[$i] > $right) {
                $center = $i;
                $right = $i + $p[$i];
            }
            
            // 更新最长回文
            if ($p[$i] > $maxLen) {
                $maxLen = $p[$i];
                $centerIndex = $i;
            }
        }
        
        $start = ($centerIndex - $maxLen) / 2;
        return substr($s, $start, $maxLen);
    }
    
    /**
     * Z算法 (线性时间字符串匹配)
     * 时间复杂度: O(n + m)
     * 空间复杂度: O(n + m)
     */
    public static function zAlgorithm(string $text, string $pattern): array
    {
        $concat = $pattern . '$' . $text;
        $n = strlen($concat);
        $z = array_fill(0, $n, 0);
        $l = 0;
        $r = 0;
        
        for ($i = 1; $i < $n; $i++) {
            if ($i <= $r) {
                $z[$i] = min($r - $i + 1, $z[$i - $l]);
            }
            
            while ($i + $z[$i] < $n && $concat[$z[$i]] === $concat[$i + $z[$i]]) {
                $z[$i]++;
            }
            
            if ($i + $z[$i] - 1 > $r) {
                $l = $i;
                $r = $i + $z[$i] - 1;
            }
        }
        
        $matches = [];
        $patternLen = strlen($pattern);
        
        for ($i = $patternLen + 1; $i < $n; $i++) {
            if ($z[$i] === $patternLen) {
                $matches[] = $i - $patternLen - 1;
            }
        }
        
        return $matches;
    }
    
    /**
     * 字符串哈希 (Rolling Hash)
     * 时间复杂度: O(n)
     * 空间复杂度: O(1)
     */
    public static function rollingHash(string $s, int $base = 256, int $mod = 1000000007): int
    {
        $hash = 0;
        $n = strlen($s);
        
        for ($i = 0; $i < $n; $i++) {
            $hash = ($hash * $base + ord($s[$i])) % $mod;
        }
        
        return $hash;
    }
    
    /**
     * 字符串的所有排列
     * 时间复杂度: O(n!)
     * 空间复杂度: O(n)
     */
    public static function permutations(string $s): array
    {
        $result = [];
        $chars = str_split($s);
        self::permuteHelper($chars, 0, $result);
        return $result;
    }
    
    private static function permuteHelper(array &$chars, int $start, array &$result): void
    {
        if ($start === count($chars)) {
            $result[] = implode('', $chars);
            return;
        }
        
        for ($i = $start; $i < count($chars); $i++) {
            // 交换
            $temp = $chars[$start];
            $chars[$start] = $chars[$i];
            $chars[$i] = $temp;
            
            self::permuteHelper($chars, $start + 1, $result);
            
            // 回溯
            $temp = $chars[$start];
            $chars[$start] = $chars[$i];
            $chars[$i] = $temp;
        }
    }
    
    /**
     * 检查字符串是否为回文
     * 时间复杂度: O(n)
     * 空间复杂度: O(1)
     */
    public static function isPalindrome(string $s): bool
    {
        $left = 0;
        $right = strlen($s) - 1;
        
        while ($left < $right) {
            if ($s[$left] !== $s[$right]) {
                return false;
            }
            $left++;
            $right--;
        }
        
        return true;
    }
    
    /**
     * 字符串压缩 (Run Length Encoding)
     * 时间复杂度: O(n)
     * 空间复杂度: O(n)
     */
    public static function compress(string $s): string
    {
        if (empty($s)) return '';
        
        $result = '';
        $count = 1;
        $current = $s[0];
        
        for ($i = 1; $i < strlen($s); $i++) {
            if ($s[$i] === $current) {
                $count++;
            } else {
                $result .= $current . ($count > 1 ? $count : '');
                $current = $s[$i];
                $count = 1;
            }
        }
        
        $result .= $current . ($count > 1 ? $count : '');
        
        return strlen($result) < strlen($s) ? $result : $s;
    }
    
    /**
     * 字符串解压缩
     * 时间复杂度: O(n)
     * 空间复杂度: O(n)
     */
    public static function decompress(string $compressed): string
    {
        $result = '';
        $i = 0;
        $n = strlen($compressed);
        
        while ($i < $n) {
            $char = $compressed[$i];
            $i++;
            
            $count = '';
            while ($i < $n && is_numeric($compressed[$i])) {
                $count .= $compressed[$i];
                $i++;
            }
            
            $repeat = $count === '' ? 1 : intval($count);
            $result .= str_repeat($char, $repeat);
        }
        
        return $result;
    }
}