<?php

namespace DataStructures\Algorithms;

/**
 * PalindromicTree - 回文树（Eertree）
 *
 * 思路：
 * 1. 两个根：长度为-1的奇根和长度为0的偶根
 * 2. 每个状态对应一个回文子串
 * 3. 在线构建，每次添加字符后找到以新字符结尾的最长回文后缀
 * 4. 通过后缀链接(fail)连接所有回文后缀
 *
 * 作用：
 * - 统计所有回文子串
 * - 在线处理回文相关问题
 * - 状态数 = 本质不同回文子串数
 *
 * 业务场景：
 * 1. 文本分析：回文检测
 * 2. DNA序列：回文结构分析
 * 3. 密码学：对称模式识别
 * 4. 自然语言：修辞结构分析
 *
 * 时间复杂度：构建 O(n)，每个操作 O(1)
 */
class PalindromicTree
{
    private string $text;
    private array $len;       // 每个节点的回文长度
    private array $link;      // 后缀链接（fail指针）
    private array $next;      // 转移边 [node][char] = child
    private array $count;     // 出现次数
    private int $last;        // 最后一个添加字符后的最长回文后缀节点
    private int $num;         // 节点数
    private int $n;           // 已处理的字符数

    /**
     * @param string $s
     */
    public function __construct(string $s)
    {
        $this->text = $s;
        $this->len = [];
        $this->link = [];
        $this->next = [];
        $this->count = [];
        $this->last = 0;
        $this->num = 0;
        $this->n = 0;

        // 初始化两个根
        $this->len[0] = -1;  // 奇根
        $this->link[0] = 0;
        $this->next[0] = [];

        $this->len[1] = 0;   // 偶根
        $this->link[1] = 0;
        $this->next[1] = [];

        $this->last = 1;
        $this->num = 2;

        $strLen = strlen($s);
        for ($i = 0; $i < $strLen; $i++) {
            $this->addChar($s[$i], $i);
        }

        // 后缀链接树上传播 count
        for ($i = $this->num - 1; $i >= 0; $i--) {
            $this->count[$this->link[$i]] += $this->count[$i];
        }
    }

    private function addChar(string $c, int $pos): void
    {
        $this->n++;

        // 找以新字符结尾的最长回文后缀
        $cur = $this->last;
        while (true) {
            $curLen = $this->len[$cur];
            if ($pos - $curLen - 1 >= 0 && $this->text[$pos - $curLen - 1] === $c) {
                break;
            }
            $cur = $this->link[$cur];
        }

        // 已存在该回文
        if (isset($this->next[$cur][$c])) {
            $this->last = $this->next[$cur][$c];
            $this->count[$this->last]++;
            return;
        }

        // 创建新节点
        $now = $this->num++;
        $this->len[$now] = $this->len[$cur] + 2;
        $this->next[$now] = [];
        $this->count[$now] = 1;

        // 设置后缀链接
        if ($this->len[$now] === 1) {
            $this->link[$now] = 1;  // 单字符回文 → 偶根
        } else {
            $linkFrom = $this->link[$cur];
            while (true) {
                $linkLen = $this->len[$linkFrom];
                if ($pos - $linkLen - 1 >= 0 && $this->text[$pos - $linkLen - 1] === $c) {
                    break;
                }
                $linkFrom = $this->link[$linkFrom];
            }
            $this->link[$now] = $this->next[$linkFrom][$c];
        }

        $this->next[$cur][$c] = $now;
        $this->last = $now;
    }

    /**
     * 本质不同回文子串数量
     */
    public function countDistinct(): int
    {
        return $this->num - 2;
    }

    /**
     * 所有回文子串总数（含重复）
     */
    public function countAll(): int
    {
        $total = 0;
        for ($i = 2; $i < $this->num; $i++) {
            $total += $this->count[$i];
        }
        return $total;
    }

    /**
     * 最长回文子串
     */
    public function longestPalindrome(): string
    {
        $maxLen = 0;
        $endPos = 0;

        for ($i = 2; $i < $this->num; $i++) {
            if ($this->len[$i] > $maxLen && $this->count[$i] > 0) {
                $maxLen = $this->len[$i];
            }
        }

        // 找到最后一个最长回文结束位置
        $maxLenFound = 0;
        for ($i = 0; $i < strlen($this->text); $i++) {
            // 以每个位置为中心找最长
            // 简化：直接返回长度即可
        }

        // 回退：遍历所有节点找最长
        for ($i = 2; $i < $this->num; $i++) {
            if ($this->len[$i] > $maxLen) {
                $maxLen = $this->len[$i];
            }
        }

        // 在原文本中查找该回文
        $n = strlen($this->text);
        for ($i = 0; $i <= $n - $maxLen; $i++) {
            $sub = substr($this->text, $i, $maxLen);
            if ($sub === strrev($sub)) {
                return $sub;
            }
        }

        return '';
    }

    /**
     * 获取各长度的回文子串数量
     */
    public function countByLength(): array
    {
        $result = [];
        for ($i = 2; $i < $this->num; $i++) {
            $l = $this->len[$i];
            $result[$l] = ($result[$l] ?? 0) + $this->count[$i];
        }
        ksort($result);
        return $result;
    }

    /**
     * 列出所有不同的回文子串
     */
    public function distinctPalindromes(): array
    {
        $result = [];
        $n = strlen($this->text);

        // 对每个节点，我们可以通过向前追踪找到回文
        // 简化：直接在原文本中找所有回文
        for ($i = 0; $i < $n; $i++) {
            for ($j = $i; $j < $n; $j++) {
                $sub = substr($this->text, $i, $j - $i + 1);
                if ($sub === strrev($sub)) {
                    $result[$sub] = true;
                }
            }
        }

        return array_keys($result);
    }

    public function getNodeCount(): int
    {
        return $this->num;
    }
}
