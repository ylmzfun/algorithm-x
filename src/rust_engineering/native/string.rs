//! 字符串处理
//!
//! 覆盖主题：
//! - split 家族与空白处理：`split_whitespace`
//! - 字符边界安全：`char_indices`（为什么不能直接 `&s[..n]`）
//! - 过滤与统计：`chars` / `filter` / `filter_map`
//! - 大小写转换与判断：`to_lowercase` / `is_uppercase` / `to_ascii_lowercase`
//!
//! # 字符边界
//!
//! Rust 的 `String` / `&str` 按 UTF-8 字节存储，下标是字节下标。
//! 直接 `&s[..n]` 若切在某个多字节字符中间会 panic（"not a char boundary"），
//! 必须先借助 `char_indices` 找到安全边界。中文每个字符占 3 字节。

/// 统计单词数
///
/// `split_whitespace` 按任意空白（空格、制表符、换行等）切分并跳过连续空白。
/// 复杂度 O(n)。
pub fn count_words(s: &str) -> usize {
    s.split_whitespace().count()
}

/// 反转单词顺序
///
/// `split_whitespace().rev()` 逆序迭代单词后 `join(" ")`。
/// 复杂度 O(n)。典型场景：句子内单词重排。
pub fn reverse_words(s: &str) -> String {
    s.split_whitespace().rev().collect::<Vec<&str>>().join(" ")
}

/// 判断回文（仅字母数字、忽略大小写）
///
/// 先过滤出字母数字并转小写，再比较正序与逆序是否相同。
/// 复杂度 O(n)。
pub fn is_palindrome(s: &str) -> bool {
    let chars: Vec<char> = s
        .chars()
        .filter(|c| c.is_alphanumeric())
        .flat_map(|c| c.to_lowercase())
        .collect();
    chars.iter().eq(chars.iter().rev())
}

/// 提取字符串中的全部数字字符
///
/// `char::to_digit(10)` 把字符转成十进制数字（非数字返回 `None`），
/// 配合 `filter_map` 天然跳过无效字符。复杂度 O(n)。
pub fn extract_digits(s: &str) -> Vec<u32> {
    s.chars().filter_map(|c| c.to_digit(10)).collect()
}

/// 驼峰命名转蛇形命名（helloWorldRust → hello_world_rust）
///
/// 遍历字符，遇大写字母时（非首字符）先插入 `_` 再转小写。
/// 复杂度 O(n)。
pub fn camel_to_snake(s: &str) -> String {
    let mut out = String::new();
    for (i, c) in s.chars().enumerate() {
        if c.is_uppercase() {
            if i > 0 {
                out.push('_');
            }
            out.extend(c.to_lowercase());
        } else {
            out.push(c);
        }
    }
    out
}

/// 统计元音字母个数（a/e/i/o/u，含大小写，仅 ASCII）
///
/// `to_ascii_lowercase` 只规整 ASCII 字符，非 ASCII（如"世界"）原样保留，
/// 因而不会被误判为元音。复杂度 O(n)。
pub fn count_vowels(s: &str) -> usize {
    s.chars()
        .filter(|c| "aeiou".contains(c.to_ascii_lowercase()))
        .count()
}

/// 按字符数安全截断
///
/// `char_indices()` 给出 `(字节下标, 字符)`，取第 `max_chars` 个字符的字节
/// 下标作为切片终点，保证不落在多字节字符中间；字符串不足则原样返回。
/// 复杂度 O(min(n, max_chars))。
pub fn truncate(s: &str, max_chars: usize) -> &str {
    match s.char_indices().nth(max_chars) {
        Some((idx, _)) => &s[..idx],
        None => s,
    }
}

/// 出现次数最多的字符
///
/// `HashMap` 计数后 `max_by_key` 取最大者。空输入没有可返回的字符，
/// 此时返回 `' '`（调用方应先保证输入非空）。复杂度 O(n)。
pub fn most_common_char(s: &str) -> char {
    let mut counts = std::collections::HashMap::new();
    for c in s.chars() {
        *counts.entry(c).or_insert(0usize) += 1;
    }
    match counts.into_iter().max_by_key(|&(_, count)| count) {
        Some((c, _)) => c,
        None => ' ',
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_count_words() {
        assert_eq!(count_words("  hello   world  "), 2);
        assert_eq!(count_words(""), 0);
    }

    #[test]
    fn test_reverse_words() {
        assert_eq!(reverse_words("the sky is blue"), "blue is sky the");
    }

    #[test]
    fn test_is_palindrome() {
        assert!(is_palindrome("A man, a plan, a canal: Panama"));
        assert!(is_palindrome("racecar"));
        assert!(!is_palindrome("hello"));
    }

    #[test]
    fn test_extract_digits() {
        assert_eq!(extract_digits("a1b2c3"), vec![1, 2, 3]);
        assert!(extract_digits("abc").is_empty());
    }

    #[test]
    fn test_camel_to_snake() {
        assert_eq!(camel_to_snake("helloWorldRust"), "hello_world_rust");
        assert_eq!(camel_to_snake("already_snake"), "already_snake");
    }

    #[test]
    fn test_count_vowels() {
        assert_eq!(count_vowels("Hello, 世界"), 2);
        assert_eq!(count_vowels("AEIOU"), 5);
    }

    #[test]
    fn test_truncate() {
        assert_eq!(truncate("你好世界", 2), "你好"); // 中文多字节，边界安全
        assert_eq!(truncate("hello", 3), "hel");
        assert_eq!(truncate("hi", 10), "hi"); // 不足则原样返回
    }

    #[test]
    fn test_most_common_char() {
        assert_eq!(most_common_char("abracadabra"), 'a');
    }
}
