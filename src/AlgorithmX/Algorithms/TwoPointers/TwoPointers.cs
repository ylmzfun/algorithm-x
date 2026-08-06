namespace AlgorithmX.Algorithms.TwoPointers;

/// <summary>
/// 双指针与滑动窗口算法。
/// </summary>
public static class TwoPointers
{
    // ═══════════════════════════════════════════
    // 对撞指针
    // ═══════════════════════════════════════════

    /// <summary>
    /// 有序数组的两数之和 — 返回和为 target 的两个数的索引（1-based）。
    /// O(n)。
    /// </summary>
    public static int[] TwoSumSorted(int[] numbers, int target)
    {
        int left = 0, right = numbers.Length - 1;
        while (left < right)
        {
            int sum = numbers[left] + numbers[right];
            if (sum == target)
                return new[] { left + 1, right + 1 };
            if (sum < target) left++;
            else right--;
        }
        return Array.Empty<int>();
    }

    /// <summary>
    /// 三数之和 — 找出所有和为 0 的不重复三元组。O(n²)。
    /// </summary>
    public static IList<IList<int>> ThreeSum(int[] nums)
    {
        Array.Sort(nums);
        var result = new List<IList<int>>();
        int n = nums.Length;

        for (int i = 0; i < n - 2; i++)
        {
            if (i > 0 && nums[i] == nums[i - 1]) continue; // 跳过重复
            int left = i + 1, right = n - 1;
            while (left < right)
            {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0)
                {
                    result.Add(new List<int> { nums[i], nums[left], nums[right] });
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    left++;
                    right--;
                }
                else if (sum < 0) left++;
                else right--;
            }
        }
        return result;
    }

    /// <summary>
    /// 盛最多水的容器。O(n)。
    /// </summary>
    public static int MaxArea(int[] height)
    {
        int left = 0, right = height.Length - 1;
        int maxArea = 0;
        while (left < right)
        {
            int area = Math.Min(height[left], height[right]) * (right - left);
            maxArea = Math.Max(maxArea, area);
            if (height[left] < height[right]) left++;
            else right--;
        }
        return maxArea;
    }

    // ═══════════════════════════════════════════
    // 滑动窗口
    // ═══════════════════════════════════════════

    /// <summary>
    /// 无重复字符的最长子串长度。O(n)。
    /// </summary>
    public static int LengthOfLongestSubstring(string s)
    {
        var seen = new Dictionary<char, int>();
        int left = 0, maxLen = 0;
        for (int right = 0; right < s.Length; right++)
        {
            if (seen.TryGetValue(s[right], out int prevIndex) && prevIndex >= left)
            {
                left = prevIndex + 1;
            }
            seen[s[right]] = right;
            maxLen = Math.Max(maxLen, right - left + 1);
        }
        return maxLen;
    }

    /// <summary>
    /// 最小覆盖子串 — s 中涵盖 t 中所有字符的最小子串。O(m+n)。
    /// </summary>
    public static string MinWindow(string s, string t)
    {
        if (string.IsNullOrEmpty(s) || string.IsNullOrEmpty(t)) return "";

        var need = new Dictionary<char, int>();
        foreach (char c in t)
            need[c] = need.GetValueOrDefault(c) + 1;

        var window = new Dictionary<char, int>();
        int left = 0, matched = 0;
        int minStart = 0, minLen = int.MaxValue;

        for (int right = 0; right < s.Length; right++)
        {
            char c = s[right];
            window[c] = window.GetValueOrDefault(c) + 1;
            if (need.ContainsKey(c) && window[c] == need[c])
                matched++;

            while (matched == need.Count)
            {
                if (right - left + 1 < minLen)
                {
                    minLen = right - left + 1;
                    minStart = left;
                }
                char leftChar = s[left];
                window[leftChar]--;
                if (need.ContainsKey(leftChar) && window[leftChar] < need[leftChar])
                    matched--;
                left++;
            }
        }
        return minLen == int.MaxValue ? "" : s.Substring(minStart, minLen);
    }

    /// <summary>
    /// 找到字符串中所有字母异位词的起始索引。O(n)。
    /// </summary>
    public static IList<int> FindAnagrams(string s, string p)
    {
        var result = new List<int>();
        if (s.Length < p.Length) return result;

        var need = new int[26];
        var window = new int[26];
        for (int i = 0; i < p.Length; i++)
        {
            need[p[i] - 'a']++;
            window[s[i] - 'a']++;
        }
        if (WindowMatches(need, window)) result.Add(0);

        for (int i = p.Length; i < s.Length; i++)
        {
            window[s[i] - 'a']++;
            window[s[i - p.Length] - 'a']--;
            if (WindowMatches(need, window)) result.Add(i - p.Length + 1);
        }
        return result;
    }

    private static bool WindowMatches(int[] need, int[] window)
    {
        for (int i = 0; i < 26; i++)
            if (need[i] != window[i]) return false;
        return true;
    }
}
