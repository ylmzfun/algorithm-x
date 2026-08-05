<?php

namespace DataStructures\Algorithms;

/**
 * SuffixAutomaton - 后缀自动机 (SAM)
 *
 * 思路：
 * 1. 最小化确定性有限自动机，接受字符串的所有后缀
 * 2. 在线构建：逐个字符添加，维护 last 状态
 * 3. 状态转移通过字符边，每个状态有一组 endpos 等价类
 * 4. 通过 link 指针构成 parent 树（后缀链接树）
 *
 * 作用：
 * - 高效处理子串相关问题
 * - 在 O(n) 时间内接受字符串所有子串
 * - 状态数和转移数均为 O(n)
 *
 * 业务场景：
 * 1. 文本编辑器：子串高亮匹配
 * 2. 生物信息学：DNA序列中的重复模式发现
 * 3. 搜索引擎：子串索引
 * 4. 代码分析：公共子表达式检测
 * 5. 数据压缩：LZ77/LZ78的加速
 * 6. 抄袭检测：最长公共子串
 * 7. 拼写检查：模糊匹配
 * 8. 自然语言处理：词干提取
 * 9. 密码学：周期性分析
 * 10. 音乐检索：旋律匹配
 *
 * 时间复杂度：
 * - 构建: O(n)
 * - 状态数: ≤ 2n - 1
 * - 转移数: ≤ 3n - 4
 */
class SuffixAutomaton
{
    private array $states;
    private int $last;
    private int $size;

    /**
     * @param string $s 构建自动机的字符串
     */
    public function __construct(string $s)
    {
        $this->states = [];
        $this->size = 0;
        $this->last = 0;

        // 初始状态
        $this->states[0] = ['len' => 0, 'link' => -1, 'next' => []];
        $this->size = 1;

        $len = strlen($s);
        for ($i = 0; $i < $len; $i++) {
            $this->extend($s[$i]);
        }
    }

    /**
     * 添加一个字符，在线扩展自动机
     */
    private function extend(string $c): void
    {
        $cur = $this->size++;
        $this->states[$cur] = [
            'len' => $this->states[$this->last]['len'] + 1,
            'link' => 0,
            'next' => [],
        ];

        $p = $this->last;
        while ($p !== -1 && !isset($this->states[$p]['next'][$c])) {
            $this->states[$p]['next'][$c] = $cur;
            $p = $this->states[$p]['link'];
        }

        if ($p === -1) {
            $this->states[$cur]['link'] = 0;
        } else {
            $q = $this->states[$p]['next'][$c];
            if ($this->states[$p]['len'] + 1 === $this->states[$q]['len']) {
                $this->states[$cur]['link'] = $q;
            } else {
                $clone = $this->size++;
                $this->states[$clone] = [
                    'len' => $this->states[$p]['len'] + 1,
                    'link' => $this->states[$q]['link'],
                    'next' => $this->states[$q]['next'],
                ];

                while ($p !== -1 && isset($this->states[$p]['next'][$c]) && $this->states[$p]['next'][$c] === $q) {
                    $this->states[$p]['next'][$c] = $clone;
                    $p = $this->states[$p]['link'];
                }

                $this->states[$q]['link'] = $clone;
                $this->states[$cur]['link'] = $clone;
            }
        }

        $this->last = $cur;
    }

    /**
     * 检查 t 是否是原串的子串
     *
     * @param string $t
     * @return bool
     */
    public function contains(string $t): bool
    {
        $state = 0;
        $len = strlen($t);

        for ($i = 0; $i < $len; $i++) {
            $c = $t[$i];
            if (!isset($this->states[$state]['next'][$c])) {
                return false;
            }
            $state = $this->states[$state]['next'][$c];
        }

        return true;
    }

    /**
     * 统计子串 t 在原串中的出现次数
     *
     * @param string $t
     * @return int
     */
    public function countOccurrences(string $t): int
    {
        $state = 0;
        $len = strlen($t);

        for ($i = 0; $i < $len; $i++) {
            $c = $t[$i];
            if (!isset($this->states[$state]['next'][$c])) {
                return 0;
            }
            $state = $this->states[$state]['next'][$c];
        }

        // 计算该状态的 endpos 集合大小
        // 需要预处理 cnt
        $cnt = $this->computeEndposSize();
        return $cnt[$state];
    }

    /**
     * 所有不同子串的数量
     *
     * @return int
     */
    public function countDistinctSubstrings(): int
    {
        $total = 0;
        for ($i = 1; $i < $this->size; $i++) {
            $total += $this->states[$i]['len'] - $this->states[$this->states[$i]['link']]['len'];
        }
        return $total;
    }

    /**
     * 最长公共子串（与另一字符串）
     *
     * @param string $t
     * @return string
     */
    public function longestCommonSubstring(string $t): string
    {
        $state = 0;
        $length = 0;
        $bestLength = 0;
        $bestEnd = 0;

        $len = strlen($t);
        for ($i = 0; $i < $len; $i++) {
            $c = $t[$i];

            while ($state > 0 && !isset($this->states[$state]['next'][$c])) {
                $state = $this->states[$state]['link'];
                $length = $this->states[$state]['len'];
            }

            if (isset($this->states[$state]['next'][$c])) {
                $state = $this->states[$state]['next'][$c];
                $length++;
            }

            if ($length > $bestLength) {
                $bestLength = $length;
                $bestEnd = $i;
            }
        }

        return substr($t, $bestEnd - $bestLength + 1, $bestLength);
    }

    /**
     * 所有出现次数大于等于 k 的子串中，最长子串的长度
     *
     * @param int $k 最少出现次数
     * @return int
     */
    public function longestRepeatedSubstring(int $k = 2): int
    {
        $cnt = $this->computeEndposSize();
        $maxLen = 0;

        for ($i = 1; $i < $this->size; $i++) {
            if ($cnt[$i] >= $k) {
                $maxLen = max($maxLen, $this->states[$i]['len']);
            }
        }

        return $maxLen;
    }

    /**
     * 获取自动机大小（状态数）
     */
    public function getSize(): int
    {
        return $this->size;
    }

    /**
     * 计算每个状态的 endpos 集合大小
     */
    private function computeEndposSize(): array
    {
        $cnt = array_fill(0, $this->size, 0);

        // 标记所有非克隆状态（原串前缀对应的状态）
        $state = 0;
        // 遍历所有状态，标记那些在原串中有endpos的状态
        // 实际做法：从last回溯到0，标记cnt
        // 更稳健的做法：给每个非克隆状态初始cnt=1
        $isClone = array_fill(0, $this->size, false);

        // 克隆状态的特征：link指向它，并且len是连续的
        // 简化：通过后缀链接树拓扑排序
        // 先给所有状态分配初始cnt，然后按长度排序
        $order = range(0, $this->size - 1);
        usort($order, function($a, $b) {
            return $this->states[$b]['len'] - $this->states[$a]['len'];
        });

        // 非克隆状态：在原串中每添加一个字符就产生一个新状态
        // 从0出发按序走原串可标记所有非克隆状态
        // 这里采用更直接的方法：从last走link树回溯
        $p = $this->last;
        while ($p > 0) {
            $cnt[$p] = 1;
            $p = $this->states[$p]['link'];
        }

        // 按长度降序传播cnt到link
        foreach ($order as $v) {
            if ($this->states[$v]['link'] !== -1) {
                $cnt[$this->states[$v]['link']] += $cnt[$v];
            }
        }

        return $cnt;
    }
}
