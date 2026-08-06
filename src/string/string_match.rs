/// 字符串匹配算法
///
/// - KMP (Knuth-Morris-Pratt): O(n + m)，利用前缀函数跳过无效匹配
/// - Rabin-Karp: 使用滚动哈希，平均 O(n + m)

// ==================== KMP ====================

/// KMP 字符串查找 — 返回第一个匹配位置
///
/// 核心：构建前缀函数（partial match table），记录 pattern 的最长公共前后缀。
pub fn kmp_search(text: &str, pattern: &str) -> Option<usize> {
    if pattern.is_empty() {
        return Some(0);
    }
    let t: Vec<char> = text.chars().collect();
    let p: Vec<char> = pattern.chars().collect();
    let lps = build_lps(&p);

    let mut j = 0i32; // pattern 的索引
    for i in 0..t.len() {
        while j > 0 && t[i] != p[j as usize] {
            j = lps[(j - 1) as usize];
        }
        if t[i] == p[j as usize] {
            j += 1;
        }
        if j as usize == p.len() {
            return Some(i + 1 - p.len());
        }
    }
    None
}

/// 构建 LPS (Longest Proper Prefix which is also Suffix) 数组
///
/// lps[i] = pattern[0..=i] 的最长公共前后缀长度
fn build_lps(pattern: &[char]) -> Vec<i32> {
    let m = pattern.len();
    let mut lps = vec![0i32; m];
    let mut len = 0i32; // 当前匹配的前缀长度
    let mut i = 1i32;

    while i < m as i32 {
        if pattern[i as usize] == pattern[len as usize] {
            len += 1;
            lps[i as usize] = len;
            i += 1;
        } else if len > 0 {
            len = lps[(len - 1) as usize];
        } else {
            lps[i as usize] = 0;
            i += 1;
        }
    }
    lps
}

/// 返回所有匹配位置
pub fn kmp_search_all(text: &str, pattern: &str) -> Vec<usize> {
    if pattern.is_empty() {
        return (0..=text.len()).collect();
    }
    let t: Vec<char> = text.chars().collect();
    let p: Vec<char> = pattern.chars().collect();
    let lps = build_lps(&p);

    let mut result = Vec::new();
    let mut j = 0i32;

    for i in 0..t.len() {
        while j > 0 && t[i] != p[j as usize] {
            j = lps[(j - 1) as usize];
        }
        if t[i] == p[j as usize] {
            j += 1;
        }
        if j as usize == p.len() {
            result.push(i + 1 - p.len());
            j = lps[(j - 1) as usize];
        }
    }
    result
}

// ==================== Rabin-Karp ====================

const BASE: u64 = 256;
const MOD: u64 = 1_000_000_007;

/// Rabin-Karp 字符串查找
///
/// 使用滚动哈希匹配。返回第一个匹配位置。
pub fn rabin_karp(text: &str, pattern: &str) -> Option<usize> {
    let n = text.len();
    let m = pattern.len();
    if m == 0 {
        return Some(0);
    }
    if n < m {
        return None;
    }

    let t: Vec<u8> = text.bytes().collect();
    let p: Vec<u8> = pattern.bytes().collect();

    // 计算 pattern 的哈希值
    let mut pat_hash = 0u64;
    let mut text_hash = 0u64;
    let mut highest_pow = 1u64;

    for i in 0..m {
        pat_hash = (pat_hash * BASE + p[i] as u64) % MOD;
        text_hash = (text_hash * BASE + t[i] as u64) % MOD;
        if i < m - 1 {
            highest_pow = (highest_pow * BASE) % MOD;
        }
    }

    for i in 0..=n - m {
        if pat_hash == text_hash {
            // 验证（哈希碰撞可能导致误判）
            if t[i..i + m] == p[..] {
                return Some(i);
            }
        }
        if i < n - m {
            // 滑动窗口：移除最左，添加最右
            text_hash = (text_hash + MOD - (t[i] as u64 * highest_pow) % MOD) % MOD;
            text_hash = (text_hash * BASE + t[i + m] as u64) % MOD;
        }
    }
    None
}

/// 计算字符串的 Z 函数值
///
/// z[i] = s 和 s[i..] 的最长公共前缀长度。
/// 用于模式匹配：将 pattern + '$' + text 拼接后求 Z 值。
pub fn z_function(s: &str) -> Vec<usize> {
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len();
    let mut z = vec![0usize; n];
    let mut l = 0;
    let mut r = 0;

    for i in 1..n {
        if i <= r {
            z[i] = z[i - l].min(r - i + 1);
        }
        while i + z[i] < n && chars[z[i]] == chars[i + z[i]] {
            z[i] += 1;
        }
        if i + z[i] - 1 > r {
            l = i;
            r = i + z[i] - 1;
        }
    }
    z
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kmp_search() {
        assert_eq!(kmp_search("hello world", "world"), Some(6));
        assert_eq!(kmp_search("aaaaa", "bba"), None);
        assert_eq!(kmp_search("", ""), Some(0));
        assert_eq!(kmp_search("abc", ""), Some(0));
    }

    #[test]
    fn test_kmp_search_all() {
        assert_eq!(
            kmp_search_all("abababab", "aba"),
            vec![0, 2, 4]
        );
    }

    #[test]
    fn test_rabin_karp() {
        assert_eq!(rabin_karp("hello world", "world"), Some(6));
        assert_eq!(rabin_karp("abcdef", "def"), Some(3));
        assert_eq!(rabin_karp("abcdef", "xyz"), None);
    }

    #[test]
    fn test_z_function() {
        let z = z_function("aabcaabxaa");
        // a a b c a a b x a a
        // z[0]=0(定义), z[1]=1("a"), z[2]=0, z[3]=0, z[4]=3("aab"), z[5]=1...
        assert_eq!(z[0], 0);
        assert_eq!(z[1], 1);
        assert_eq!(z[4], 3);
    }
}
