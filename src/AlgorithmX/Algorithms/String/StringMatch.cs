namespace AlgorithmX.Algorithms.String;

/// <summary>
/// 字符串匹配算法集合。
/// </summary>
public static class StringMatch
{
    // ═══════════════════════════════════════════
    // KMP (Knuth-Morris-Pratt)
    // ═══════════════════════════════════════════

    /// <summary>
    /// KMP 字符串匹配。返回 pattern 在 text 中所有匹配的起始位置。O(m+n)。
    /// </summary>
    public static IList<int> KmpSearch(string text, string pattern)
    {
        var result = new List<int>();
        if (string.IsNullOrEmpty(pattern)) return result;

        int[] lps = BuildLps(pattern);
        int i = 0, j = 0;

        while (i < text.Length)
        {
            if (text[i] == pattern[j])
            {
                i++;
                j++;
            }
            if (j == pattern.Length)
            {
                result.Add(i - j);
                j = lps[j - 1];
            }
            else if (i < text.Length && text[i] != pattern[j])
            {
                if (j != 0)
                    j = lps[j - 1];
                else
                    i++;
            }
        }
        return result;
    }

    /// <summary>
    /// 构建 LPS (Longest Proper Prefix which is also Suffix) 数组。
    /// </summary>
    public static int[] BuildLps(string pattern)
    {
        int m = pattern.Length;
        int[] lps = new int[m];
        int len = 0, i = 1;

        while (i < m)
        {
            if (pattern[i] == pattern[len])
            {
                len++;
                lps[i] = len;
                i++;
            }
            else
            {
                if (len != 0)
                    len = lps[len - 1];
                else
                {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    // ═══════════════════════════════════════════
    // Rabin-Karp (滚动哈希)
    // ═══════════════════════════════════════════

    /// <summary>
    /// Rabin-Karp 字符串匹配。返回 pattern 在 text 中所有匹配的起始位置。
    /// 平均 O(m+n)，最坏 O(mn)（哈希冲突时）。
    /// </summary>
    public static IList<int> RabinKarpSearch(string text, string pattern)
    {
        var result = new List<int>();
        int n = text.Length, m = pattern.Length;
        if (m == 0 || m > n) return result;

        const long mod = 1_000_000_007;
        const long base_ = 256;

        long patternHash = 0, textHash = 0;
        long highestPower = 1;
        for (int i = 0; i < m - 1; i++)
            highestPower = (highestPower * base_) % mod;

        for (int i = 0; i < m; i++)
        {
            patternHash = (patternHash * base_ + pattern[i]) % mod;
            textHash = (textHash * base_ + text[i]) % mod;
        }

        for (int i = 0; i <= n - m; i++)
        {
            if (patternHash == textHash && text.AsSpan(i, m).SequenceEqual(pattern))
                result.Add(i);

            if (i < n - m)
            {
                textHash = (base_ * (textHash - text[i] * highestPower % mod + mod) % mod + text[i + m]) % mod;
            }
        }
        return result;
    }

    // ═══════════════════════════════════════════
    // Manacher — 最长回文子串 O(n)
    // ═══════════════════════════════════════════

    /// <summary>
    /// Manacher 算法求最长回文子串。O(n)。
    /// </summary>
    public static string LongestPalindrome(string s)
    {
        if (string.IsNullOrEmpty(s)) return "";

        // 预处理：插入 # 分隔符
        var t = new char[s.Length * 2 + 3];
        t[0] = '^';
        int idx = 1;
        foreach (char c in s)
        {
            t[idx++] = '#';
            t[idx++] = c;
        }
        t[idx++] = '#';
        t[idx] = '$';

        int n = idx + 1;
        var p = new int[n];
        int center = 0, right = 0;
        int maxLen = 0, maxCenter = 0;

        for (int i = 1; i < n - 1; i++)
        {
            int mirror = 2 * center - i;
            if (i < right)
                p[i] = Math.Min(right - i, p[mirror]);

            while (t[i + p[i] + 1] == t[i - p[i] - 1])
                p[i]++;

            if (i + p[i] > right)
            {
                center = i;
                right = i + p[i];
            }

            if (p[i] > maxLen)
            {
                maxLen = p[i];
                maxCenter = i;
            }
        }

        int start = (maxCenter - maxLen - 1) / 2;
        return s.Substring(start, maxLen);
    }
}
