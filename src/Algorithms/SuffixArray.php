<?php

namespace DataStructures\Algorithms;

/**
 * SuffixArray - 后缀数组
 *
 * 思路：
 * 1. 字符串所有后缀按字典序排序后的索引数组
 * 2. 使用倍增法 O(n log n) 构建
 * 3. 配合 LCP 数组处理子串相关问题
 * 4. 比后缀树更省空间，实现更简单
 *
 * 作用：
 * - 子串查找、最长重复子串
 * - 最长公共子串（两串）
 * - 不同子串计数
 *
 * 业务场景：
 * 1. 生物信息学：DNA序列比对
 * 2. 全文搜索：子串索引
 * 3. 数据压缩：Burrows-Wheeler变换
 * 4. 抄袭检测：最长公共子串
 * 5. 音乐检索：旋律匹配
 *
 * 时间复杂度：构建 O(n log n)，查询 O(m log n)
 */
class SuffixArray
{
    private string $text;
    private array $sa;      // 后缀数组
    private array $rank;    // 排名数组
    private array $lcp;     // LCP数组

    /**
     * @param string $s 原始字符串
     */
    public function __construct(string $s)
    {
        $this->text = $s;
        $this->buildSA();
        $this->buildLCP();
    }

    /**
     * 倍增法构建后缀数组
     */
    private function buildSA(): void
    {
        $n = strlen($this->text);
        $sa = range(0, $n - 1);
        $rank = [];
        $tmp = [];

        // 初始按首字符排序
        for ($i = 0; $i < $n; $i++) {
            $rank[$i] = ord($this->text[$i]);
        }

        $k = 1;
        while ($k < $n) {
            // 按 (rank[i], rank[i+k]) 排序
            $key = $rank;
            usort($sa, function($a, $b) use ($key, $k, $n) {
                $ra = $key[$a];
                $rb = $key[$b];
                $ra2 = ($a + $k < $n) ? $key[$a + $k] : -1;
                $rb2 = ($b + $k < $n) ? $key[$b + $k] : -1;
                return $ra !== $rb ? $ra - $rb : $ra2 - $rb2;
            });

            $tmp[$sa[0]] = 0;
            for ($i = 1; $i < $n; $i++) {
                $a = $sa[$i];
                $b = $sa[$i - 1];
                $same = ($key[$a] === $key[$b])
                    && (($a + $k < $n ? $key[$a + $k] : -1) === ($b + $k < $n ? $key[$b + $k] : -1));
                $tmp[$a] = $tmp[$b] + ($same ? 0 : 1);
            }

            $rank = $tmp;
            if ($rank[$sa[$n - 1]] === $n - 1) {
                break;
            }
            $k <<= 1;
        }

        $this->sa = $sa;
        $this->rank = $rank;
    }

    /**
     * Kasai 算法构建 LCP 数组
     */
    private function buildLCP(): void
    {
        $n = strlen($this->text);
        $lcp = array_fill(0, $n, 0);
        $h = 0;

        for ($i = 0; $i < $n; $i++) {
            $r = $this->rank[$i];
            if ($r === 0) {
                continue;
            }

            $j = $this->sa[$r - 1];
            while ($i + $h < $n && $j + $h < $n && $this->text[$i + $h] === $this->text[$j + $h]) {
                $h++;
            }

            $lcp[$r] = $h;
            if ($h > 0) {
                $h--;
            }
        }

        $this->lcp = $lcp;
    }

    /**
     * 在后缀数组中二分查找模式串
     *
     * @return array 所有匹配位置
     */
    public function search(string $pattern): array
    {
        $n = strlen($this->text);
        $m = strlen($pattern);

        // 找下界
        $low = 0;
        $high = $n;
        while ($low < $high) {
            $mid = intdiv($low + $high, 2);
            $cmp = substr_compare($this->text, $pattern, $this->sa[$mid], $m);
            if ($cmp < 0) {
                $low = $mid + 1;
            } else {
                $high = $mid;
            }
        }
        $first = $low;

        // 找上界
        $high = $n;
        while ($low < $high) {
            $mid = intdiv($low + $high, 2);
            $cmp = substr_compare($this->text, $pattern, $this->sa[$mid], $m);
            if ($cmp <= 0) {
                $low = $mid + 1;
            } else {
                $high = $mid;
            }
        }
        $last = $low;

        $result = [];
        for ($i = $first; $i < $last; $i++) {
            $result[] = $this->sa[$i];
        }
        sort($result);
        return $result;
    }

    /**
     * 检查 pattern 是否为子串
     */
    public function contains(string $pattern): bool
    {
        return !empty($this->search($pattern));
    }

    /**
     * 最长重复子串
     */
    public function longestRepeatedSubstring(): string
    {
        $maxLen = 0;
        $maxIdx = 0;

        for ($i = 1; $i < count($this->lcp); $i++) {
            if ($this->lcp[$i] > $maxLen) {
                $maxLen = $this->lcp[$i];
                $maxIdx = $this->sa[$i];
            }
        }

        return substr($this->text, $maxIdx, $maxLen);
    }

    /**
     * 与另一字符串的最长公共子串
     */
    public function longestCommonSubstring(string $other): string
    {
        $combined = $this->text . "\0" . $other;
        $sa = new SuffixArray($combined);

        $n1 = strlen($this->text);
        $maxLen = 0;
        $maxIdx = 0;

        for ($i = 1; $i < $sa->getLength(); $i++) {
            $a = $sa->sa[$i - 1];
            $b = $sa->sa[$i];

            // 检查两个后缀分别来自不同串
            if (($a < $n1 && $b > $n1) || ($a > $n1 && $b < $n1)) {
                if ($sa->lcp[$i] > $maxLen) {
                    $maxLen = $sa->lcp[$i];
                    $maxIdx = $sa->sa[$i];
                }
            }
        }

        return substr($combined, $maxIdx, $maxLen);
    }

    /**
     * 不同子串数量
     */
    public function countDistinctSubstrings(): int
    {
        $n = strlen($this->text);
        $total = $n * ($n + 1) / 2;
        $lcpSum = array_sum($this->lcp);
        return $total - $lcpSum;
    }

    public function getSA(): array { return $this->sa; }
    public function getRank(): array { return $this->rank; }
    public function getLCP(): array { return $this->lcp; }
    public function getLength(): int { return count($this->sa); }
}
