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

    // ==================== Aho-Corasick 自动机 ====================

    /**
     * Aho-Corasick 多模式匹配算法
     * 构建一个自动机，支持在文本中同时搜索多个模式串。
     * 时间复杂度: 构建 O(m)，搜索 O(n + z)
     *   其中 m = 所有模式串长度之和，n = 文本长度，z = 匹配数量
     * 空间复杂度: O(m)
     *
     * @param array $patterns 模式串列表
     * @return AhoCorasick 自动机对象
     */
    public static function ahoCorasick(array $patterns): AhoCorasick
    {
        return new AhoCorasick($patterns);
    }
}

/**
 * Aho-Corasick 自动机
 *
 * 用途：
 * 1. 敏感词过滤：同时检测多个敏感词
 * 2. 搜索引擎：多关键词高亮
 * 3. 入侵检测：多模式签名匹配
 * 4. DNA 序列分析：多基因片段匹配
 * 5. 拼写检查：词典匹配
 */
class AhoCorasick
{
    private array $trie = [];
    private array $fail = [];
    private array $output = [];
    private int $nodeCount = 0;

    /**
     * @param array $patterns 模式串列表
     */
    public function __construct(array $patterns)
    {
        $this->nodeCount = 1;
        $this->trie = [0 => []];
        $this->fail = [0 => 0];
        $this->output = [0 => []];

        foreach ($patterns as $pattern) {
            $this->insert($pattern);
        }

        $this->buildFailureLinks();
    }

    /**
     * 插入模式串到 Trie 中
     */
    private function insert(string $pattern): void
    {
        $node = 0;
        $len = strlen($pattern);

        for ($i = 0; $i < $len; $i++) {
            $char = $pattern[$i];

            if (!isset($this->trie[$node][$char])) {
                $this->nodeCount++;
                $this->trie[$node][$char] = $this->nodeCount;
                $this->trie[$this->nodeCount] = [];
                $this->fail[$this->nodeCount] = 0;
                $this->output[$this->nodeCount] = [];
            }

            $node = $this->trie[$node][$char];
        }

        $this->output[$node][] = $pattern;
    }

    /**
     * BFS 构建失败链接
     */
    private function buildFailureLinks(): void
    {
        $queue = new \DataStructures\Linear\Queue();

        // 第一层：所有字符边指向根节点
        foreach ($this->trie[0] as $char => $child) {
            $this->fail[$child] = 0;
            $queue->enqueue($child);
        }

        while (!$queue->isEmpty()) {
            $current = $queue->dequeue();

            foreach ($this->trie[$current] as $char => $child) {
                // 计算 child 的失败链接
                $failNode = $this->fail[$current];

                while ($failNode > 0 && !isset($this->trie[$failNode][$char])) {
                    $failNode = $this->fail[$failNode];
                }

                if (isset($this->trie[$failNode][$char])) {
                    $this->fail[$child] = $this->trie[$failNode][$char];
                } else {
                    $this->fail[$child] = 0;
                }

                // 合并输出：child 的输出 = 自己的输出 + 失败链接节点的输出
                $this->output[$child] = array_merge(
                    $this->output[$child],
                    $this->output[$this->fail[$child]]
                );

                $queue->enqueue($child);
            }
        }
    }

    /**
     * 在文本中搜索所有模式串
     *
     * @param string $text
     * @return array 匹配列表: [['pattern' => string, 'position' => int], ...]
     */
    public function search(string $text): array
    {
        $matches = [];
        $node = 0;
        $len = strlen($text);

        for ($i = 0; $i < $len; $i++) {
            $char = $text[$i];

            // 沿失败链接转移，直到可以匹配当前字符
            while ($node > 0 && !isset($this->trie[$node][$char])) {
                $node = $this->fail[$node];
            }

            if (isset($this->trie[$node][$char])) {
                $node = $this->trie[$node][$char];
            } else {
                $node = 0;
            }

            // 检查当前节点的输出
            if (!empty($this->output[$node])) {
                foreach ($this->output[$node] as $pattern) {
                    $matches[] = [
                        'pattern' => $pattern,
                        'position' => $i - strlen($pattern) + 1
                    ];
                }
            }
        }

        return $matches;
    }

    /**
     * 检查文本是否包含任一模式串
     *
     * @param string $text
     * @return bool
     */
    public function containsAny(string $text): bool
    {
        $node = 0;
        $len = strlen($text);

        for ($i = 0; $i < $len; $i++) {
            $char = $text[$i];

            while ($node > 0 && !isset($this->trie[$node][$char])) {
                $node = $this->fail[$node];
            }

            if (isset($this->trie[$node][$char])) {
                $node = $this->trie[$node][$char];
            } else {
                $node = 0;
            }

            if (!empty($this->output[$node])) {
                return true;
            }
        }

        return false;
    }

    /**
     * 过滤文本中的模式串（替换为 ***）
     *
     * @param string $text
     * @param string $replacement
     * @return string
     */
    public function filter(string $text, string $replacement = '***'): string
    {
        $matches = $this->search($text);

        // 按位置排序，从后往前替换避免位置偏移
        usort($matches, function($a, $b) {
            return $b['position'] <=> $a['position'];
        });

        foreach ($matches as $match) {
            $start = $match['position'];
            $len = strlen($match['pattern']);
            $text = substr_replace($text, $replacement, $start, $len);
        }

        return $text;
    }
}