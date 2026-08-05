package com.algorithmx.foundation.array;

import java.util.*;

/**
 * 数组核心技巧：双指针、前缀和、差分数组、滑动窗口
 */
public class ArrayTechniques {

    // ==================== 双指针 ====================

    /** 两数之和 II — 有序数组，相向双指针 */
    public static int[] twoSum(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int sum = nums[left] + nums[right];
            if (sum == target) return new int[]{left, right};
            if (sum < target) left++;
            else right--;
        }
        return new int[]{-1, -1};
    }

    /** 三数之和 — 排序 + 双指针去重 */
    public static List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        int n = nums.length;
        for (int i = 0; i < n - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int left = i + 1, right = n - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    res.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    left++; right--;
                } else if (sum < 0) left++;
                else right--;
            }
        }
        return res;
    }

    /** 接雨水 — 相向双指针 */
    public static int trap(int[] height) {
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0, water = 0;
        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) leftMax = height[left];
                else water += leftMax - height[left];
                left++;
            } else {
                if (height[right] >= rightMax) rightMax = height[right];
                else water += rightMax - height[right];
                right--;
            }
        }
        return water;
    }

    /** 盛最多水的容器 — 相向双指针 */
    public static int maxArea(int[] height) {
        int left = 0, right = height.length - 1, max = 0;
        while (left < right) {
            int area = Math.min(height[left], height[right]) * (right - left);
            max = Math.max(max, area);
            if (height[left] < height[right]) left++;
            else right--;
        }
        return max;
    }

    // ==================== 前缀和 ====================

    /** 区域和检索 — 前缀和 */
    public static class PrefixSum {
        private final int[] preSum;

        public PrefixSum(int[] nums) {
            preSum = new int[nums.length + 1];
            for (int i = 0; i < nums.length; i++) preSum[i + 1] = preSum[i] + nums[i];
        }

        public int sumRange(int left, int right) {
            return preSum[right + 1] - preSum[left];
        }
    }

    /** 和为 K 的子数组个数 — 前缀和 + HashMap */
    public static int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, 1);
        int sum = 0, count = 0;
        for (int x : nums) {
            sum += x;
            count += map.getOrDefault(sum - k, 0);
            map.merge(sum, 1, Integer::sum);
        }
        return count;
    }

    // ==================== 差分数组 ====================

    /** 差分数组 — 区间增减 O(1)，最终还原 O(n) */
    public static class DifferenceArray {
        private final int[] diff;

        public DifferenceArray(int[] nums) {
            diff = new int[nums.length];
            diff[0] = nums[0];
            for (int i = 1; i < nums.length; i++) diff[i] = nums[i] - nums[i - 1];
        }

        /** 区间 [l, r] 加 val */
        public void increment(int l, int r, int val) {
            diff[l] += val;
            if (r + 1 < diff.length) diff[r + 1] -= val;
        }

        public int[] result() {
            int[] res = new int[diff.length];
            res[0] = diff[0];
            for (int i = 1; i < diff.length; i++) res[i] = res[i - 1] + diff[i];
            return res;
        }
    }

    // ==================== 滑动窗口 ====================

    /** 无重复字符的最长子串 */
    public static int lengthOfLongestSubstring(String s) {
        int[] last = new int[128];
        Arrays.fill(last, -1);
        int left = -1, max = 0;
        for (int i = 0; i < s.length(); i++) {
            left = Math.max(left, last[s.charAt(i)]);
            max = Math.max(max, i - left);
            last[s.charAt(i)] = i;
        }
        return max;
    }

    /** 最小覆盖子串 — s 中找涵盖 t 的最短子串 */
    public static String minWindow(String s, String t) {
        int[] need = new int[128];
        int needCnt = 0;
        for (char c : t.toCharArray()) {
            if (need[c] == 0) needCnt++;
            need[c]++;
        }
        int left = 0, minLen = Integer.MAX_VALUE, start = 0;
        int[] window = new int[128];
        int matched = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            window[c]++;
            if (window[c] == need[c]) matched++;
            while (matched == needCnt) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    start = left;
                }
                char d = s.charAt(left);
                if (window[d] == need[d]) matched--;
                window[d]--;
                left++;
            }
        }
        return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
    }

    /** 长度最小的子数组 — 和 ≥ target 的最短连续子数组 */
    public static int minSubArrayLen(int target, int[] nums) {
        int left = 0, sum = 0, minLen = Integer.MAX_VALUE;
        for (int right = 0; right < nums.length; right++) {
            sum += nums[right];
            while (sum >= target) {
                minLen = Math.min(minLen, right - left + 1);
                sum -= nums[left++];
            }
        }
        return minLen == Integer.MAX_VALUE ? 0 : minLen;
    }

    /** 找到字符串中所有字母异位词 */
    public static List<Integer> findAnagrams(String s, String p) {
        List<Integer> res = new ArrayList<>();
        int[] need = new int[26], window = new int[26];
        for (char c : p.toCharArray()) need[c - 'a']++;
        int left = 0, matched = 0;
        for (int right = 0; right < s.length(); right++) {
            int idx = s.charAt(right) - 'a';
            window[idx]++;
            if (window[idx] <= need[idx]) matched++;
            if (right - left + 1 > p.length()) {
                int lIdx = s.charAt(left) - 'a';
                if (window[lIdx] <= need[lIdx]) matched--;
                window[lIdx]--;
                left++;
            }
            if (matched == p.length()) res.add(left);
        }
        return res;
    }
}
