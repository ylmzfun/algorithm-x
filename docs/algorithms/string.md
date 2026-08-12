# 字符串算法专题（`algorithm_x/string/`）

本文档覆盖 `include/algorithm_x/string/` 下的 8 个头文件：单模式匹配（KMP、Boyer-Moore、
Rabin-Karp）、多模式匹配（Aho-Corasick 自动机）、回文（Manacher）、循环移位最小表示（Booth）、
编辑距离与最长公共子序列、后缀自动机（SAM）、后缀数组（含 LCP）。
除 `AhoCorasick`、`SuffixAutomaton`、`SuffixArray` 为类外，其余均为 `inline` 自由函数；
所有符号位于命名空间 `algorithm_x::string`，头文件统一以 `#include "string/xxx.h"` 引入。

---

### `string/aho_corasick.h` — Aho-Corasick 多模式匹配自动机

**用途**：在文本中一次扫描同时找出所有模式串的所有出现位置，是 KMP 从单模式到多模式的推广。

**原理**：把所有模式串插入 Trie 后，BFS 构建 fail 指针：失配时沿 fail 链跳到最长可匹配前缀对应的节点，并把 fail 链上节点的 output 合并进当前节点，使每个状态都能立刻枚举以当前位置结尾的所有模式。匹配时逐字符走 `next`，收集每个 `{pattern_id, start_position}` 即可。

**主要 API**：
```cpp
class AhoCorasick {
public:
    AhoCorasick();
    int insert(const std::string& pattern);                       // 插入模式，返回其 id（0 基）
    void build();                                                 // 全部插入后构建 fail 指针
    std::vector<std::pair<int, std::size_t>> search(const std::string& text);
    // 返回 {模式 id, 出现起始位置} 的列表
};
```

**复杂度**：插入单串 `O(m)`；`build` `O(26 × 节点数)`（每个节点扫描 26 个转移）；匹配 `O(n + 匹配总数)`；空间 `O(26 × 总模式长度)`。仅支持小写字母 a-z。

**使用场景**：
- 敏感词过滤、字典多关键词扫描（一次遍历报告全部命中）。
- 文本中大量模式串的统计与定位。

**使用示例**：
```cpp
#include "string/aho_corasick.h"
using namespace algorithm_x::string;

AhoCorasick ac;
int she = ac.insert("she");
int hers = ac.insert("hers");
ac.build();
auto matches = ac.search("ushers");    // {{she,1}, {hers,2}}：位置与模式一一对应
```

---

### `string/boyer_moore.h` — Boyer-Moore 字符串匹配（坏字符规则）

**用途**：单模式串匹配，模式越长、文本字符集越大时平均性能越好，常用于大文本扫描。

**原理**：从模式末尾向前比较（从右向左匹配），失配时用"坏字符"规则计算跳转量：若失配字符在模式中出现，则把模式中该字符最后一次出现的位置对齐到文本失配处；否则整个模式越过该字符。匹配成功时用文本后一个字符的坏字符表决定下一次移位。本实现只实现了坏字符规则（未含好后缀规则），匹配成功后可能回退，故最坏 `O(nm)`。

**主要 API**：
```cpp
// 返回所有匹配起始位置（0 基），空模式或 m > n 返回空
std::vector<std::size_t> boyer_moore_search(const std::string& text,
                                            const std::string& pattern);
```

**复杂度**：平均 `O(n/m)`，最坏 `O(nm)`；空间 `O(256)`（ASCII 坏字符表）。

**使用场景**：
- 模式较长、字符集较大（如英文文本）时的单模式搜索。
- 与 KMP 对照学习"坏字符 + 好后缀"两类启发式。

**使用示例**：
```cpp
#include "string/boyer_moore.h"
using namespace algorithm_x::string;

auto pos = boyer_moore_search("ababcabcabababd", "ababd");
// pos == {9}，仅一处匹配
```

---

### `string/edit_distance.h` — 编辑距离与最长公共子序列

**用途**：计算两个字符串的莱文斯坦编辑距离（插入/删除/替换各计 1 代价）、LCS 长度与 LCS 具体序列。

**原理**：经典二维 DP：`edit_distance` 用 `dp[i][j]` 表示 `a[0..i)` 到 `b[0..j)` 的最小编辑代价，转移取 `min(删除、插入、替换)`，只保留上一行实现 `O(m)` 空间；`lcs_length` 字符相等则 `dp[i-1][j-1]+1`，否则取两侧较大者；`lcs_string` 保留完整 dp 表后从右下角回溯拼接再反转。

**主要 API**：
```cpp
inline int edit_distance(const std::string& a, const std::string& b);  // Levenshtein 距离
inline int lcs_length(const std::string& a, const std::string& b);     // LCS 长度
inline std::string lcs_string(const std::string& a, const std::string& b); // LCS 序列
```

**复杂度**：三个函数时间均 `O(nm)`；`edit_distance`/`lcs_length` 空间 `O(m)`（滚动数组），`lcs_string` 空间 `O(nm)`（需完整表回溯）。

**使用场景**：
- 拼写纠错、基因序列比对、diff 的最小编辑代价。
- 文本相似度与"最长公共子序列"类问题（注意：是子序列，不是连续子串）。

**使用示例**：
```cpp
#include "string/edit_distance.h"
using namespace algorithm_x::string;

int d = edit_distance("kitten", "sitting");   // 3
int l = lcs_length("abcde", "ace");           // 3
std::string s = lcs_string("abcde", "ace");   // "ace"
```

---

### `string/manacher.h` — Manacher 最长回文子串

**用途**：线性时间求出任意字符串的最长回文子串（同时覆盖奇偶长度回文）。

**原理**：在字符间插入 `#` 将原串变换为 `^#a#b#c#$` 形式，使所有回文变成奇数长度；维护当前回文覆盖的最右边界 `right` 与中心 `center`，`p[i]` 记录以 `i` 为中心的回文半径，可利用对称性 `p[i] = min(right - i, p[2*center - i])` 复用已算结果，再中心扩展。最终最长半径对应的中心还原出原串下标 `(max_center - max_len) / 2`。

**主要 API**：
```cpp
// 返回最长回文子串本身；空串返回 ""
std::string longest_palindrome(const std::string& s);
```

**复杂度**：时间 `O(n)`（每个中心最多扩展一次），空间 `O(n)`（变换串与半径数组）。

**使用场景**：
- 求最长回文子串、回文子串计数等回文类问题。
- 需要 `O(n)` 实时性的长文本回文检测。

**使用示例**：
```cpp
#include "string/manacher.h"
using namespace algorithm_x::string;

std::string p = longest_palindrome("babad");   // "bab" 或 "aba"（首现为准）
std::string q = longest_palindrome("cbbd");    // "bb"
```

---

### `string/min_representation.h` — 最小表示法（Booth 算法）

**用途**：找出循环同构串中字典序最小的那个，并返回其完整字符串，是解决"循环移位最小字典序"问题的标准算法。

**原理**：双指针 `i`、`j` 各自代表一个候选起始位置，`k` 为已比较相等的长度；逐字符比较 `s[(i+k)%n]` 与 `s[(j+k)%n]`，不等时失败较大的一方直接跳过 `k+1` 个候选（因为那段内的所有起点都不可能最优），最终 `min(i, j)` 即最小表示的起点。复杂度线性。

**主要 API**：
```cpp
// 返回字典序最小的循环移位；空串返回 ""
std::string min_representation(const std::string& s);
```

**复杂度**：时间 `O(n)`，额外空间 `O(1)`（不含返回值）。

**使用场景**：
- 项链/手环类问题：循环同构串去重与最小字典序表示。
- 字符串周期性与"最小起始点"判定。

**使用示例**：
```cpp
#include "string/min_representation.h"
using namespace algorithm_x::string;

std::string r = min_representation("bcda");   // "abcd"（循环移位中的最小者）
```

---

### `string/sam.h` — 后缀自动机（SAM）

**用途**：在线构建字符串的后缀自动机，支持 `O(|t|)` 判断任意串 t 是否为 s 的子串，状态数线性于字符串长度。

**原理**：SAM 是接受 s 全部子串的最小 DFA：`extend(c)` 每次追加一个字符，沿 `link`（后缀链接）链补边，必要时克隆节点 `q` 以保持"每个状态代表一段连续长度的 endpos 等价类"这一不变量；`link` 链上父状态长度恰好是子状态长度区间下限。本实现转移用 `std::map<char,int>` 存储，节省空间但单步转移 `O(log Σ)`。

**主要 API**：
```cpp
class SuffixAutomaton {
public:
    void build(const std::string& s);                 // 在线构建
    bool contains(const std::string& t) const;        // t 是否为 s 的子串
    std::size_t state_count() const;                  // 状态数（≤ 2n-1）
};
```

**复杂度**：构建均摊 `O(n log Σ)`（Σ 为字符集大小，map 转移），状态数 ≤ `2n - 1`；`contains` 时间 `O(|t| log Σ)`。

**使用场景**：
- 海量子串存在性查询（构建一次、反复查询）。
- 进一步扩展可实现子串出现次数统计、本质不同子串数等（本实现仅提供基础能力）。

**使用示例**：
```cpp
#include "string/sam.h"
using namespace algorithm_x::string;

SuffixAutomaton sam;
sam.build("hello");
bool ok1 = sam.contains("ell");   // true
bool ok2 = sam.contains("world"); // false
std::size_t states = sam.state_count();   // "hello" 为 11
```

---

### `string/string_match.h` — 单模式匹配合集（KMP / Rabin-Karp / Z 函数）

**用途**：提供三个最常用的单模式字符串算法：KMP（确定性线性）、Rabin-Karp（滚动哈希、期望线性）、Z 函数（前缀匹配长度数组）。

**原理**：KMP 先对模式求前缀函数 `pi`（`pi[i]` 为 `pattern[0..i]` 的最长真前后缀长度），匹配时失配沿 `pi` 回退，文本指针永不走回头路；Rabin-Karp 用 `BASE=131, MOD=1e9+7` 滚动维护窗口哈希，哈希相等时再做逐字符确认以消除碰撞（最坏仍 `O(nm)`）；Z 函数维护区间 `[l, r]` 复用已匹配信息，`z[i]` 为 `s[i:]` 与 `s` 的最长公共前缀长度。

**主要 API**：
```cpp
std::vector<std::size_t> kmp_search(const std::string& text, const std::string& pattern);
std::vector<std::size_t> rabin_karp(const std::string& text, const std::string& pattern);
std::vector<std::size_t> z_function(const std::string& s);   // z[i] = s[i:] 与 s 的 LCP 长度
```

**复杂度**：`kmp_search` 时间 `O(n + m)`、空间 `O(m)`；`rabin_karp` 期望 `O(n + m)`、最坏 `O(nm)`、空间 `O(1)`；`z_function` 时间 `O(n)`、空间 `O(n)`。

**使用场景**：
- 单模式精确匹配并返回全部出现位置（KMP / Rabin-Karp）。
- 周期串判定（`n % (n - z[n-1]) == 0`）、字符串压缩、后缀结构前处理（Z 函数）。

**使用示例**：
```cpp
#include "string/string_match.h"
using namespace algorithm_x::string;

auto kmp = kmp_search("ababcabcabababd", "ababd");   // {9}
auto rk  = rabin_karp("aaaa", "aa");                 // {0, 1, 2}
auto z   = z_function("aaaa");                       // {0, 3, 2, 1}
```

---

### `string/suffix_array.h` — 后缀数组（Doubling + 基数排序，含 LCP）

**用途**：对字符串构建后缀数组 `sa`、排名 `rank` 与相邻后缀最长公共前缀 `lcp`，是后缀结构类问题（子串查询、重复子串、最长公共子串）的基础设施。

**原理**：倍增法（Doubling）：初始按首字符排序，每轮按"当前排名 + 跨 `2^k` 步的排名"二元组排序，`rank` 重编号直到所有后缀排名互不相同；LCP 用 Kasai 算法，利用 `lcp(rank[i]) ≥ lcp(rank[i-1]) - 1` 的性质在 `O(n)` 内推出（`lcp_[i]` 为 `sa[i-1]` 与 `sa[i]` 的最长公共前缀，`lcp_[0] = 0`）。

**主要 API**：
```cpp
class SuffixArray {
public:
    explicit SuffixArray(const std::string& s);
    const std::vector<std::size_t>& sa() const;     // sa[i] = 字典序第 i 小的后缀起始下标
    const std::vector<std::size_t>& rank() const;   // rank[i] = 后缀 i 的字典序排名
    const std::vector<std::size_t>& lcp() const;    // lcp[i] = sa[i-1] 与 sa[i] 的 LCP 长度
    std::size_t size() const;
};
```

**复杂度**：构建 `O(n log² n)`（每轮 `std::sort` 为 `O(n log n)`，共 `O(log n)` 轮），LCP 构建 `O(n)`；空间 `O(n)`。

**使用场景**：
- 最长重复子串（`max(lcp)`）、不同子串个数（`n(n+1)/2 - Σ lcp[i]`）。
- 多串最长公共子串、子串字典序排名查询等后缀结构问题。

**使用示例**：
```cpp
#include "string/suffix_array.h"
using namespace algorithm_x::string;

SuffixArray sa("banana");
auto s = sa.sa();     // {5, 3, 1, 0, 4, 2}：a, ana, anana, banana, na, nana
auto l = sa.lcp();    // 相邻后缀最长公共前缀长度数组
auto r = sa.rank();   // rank[0] = 3
```
