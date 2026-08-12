//! regex 正则表达式
//!
//! 覆盖主题：提取邮箱、统计匹配次数、替换、命名捕获、
//! 按正则切分字符串。
//!
//! 典型场景：日志解析、输入校验、文本清洗；Rust 的 regex 使用
//! RE2 风格语法，保证匹配耗时与文本长度近似线性。

use regex::Regex;

/// 提取字符串中所有邮箱地址
///
/// 用邮箱常见形态的正则配合 `find_iter` 迭代所有非重叠匹配。
/// 复杂度与文本长度近似线性（regex crate 的保证）。
pub fn extract_emails(s: &str) -> Vec<String> {
    let re = Regex::new(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}").unwrap();
    re.find_iter(s).map(|m| m.as_str().to_string()).collect()
}

/// 统计 pattern 在 s 中的匹配次数
///
/// 每次调用动态编译一次正则（高频场景可用 `OnceLock` 缓存复用编译结果）。
pub fn count_matches(s: &str, pattern: &str) -> usize {
    Regex::new(pattern).unwrap().find_iter(s).count()
}

/// 把所有数字替换为 'X'
///
/// `replace_all` 替换全部匹配，`into_owned()` 把 Cow<str> 转为 String。
pub fn replace_digits(s: &str) -> String {
    Regex::new(r"\d").unwrap().replace_all(s, "X").into_owned()
}

/// 捕获 "key = value" 形式的键值对
///
/// `captures` 返回首个匹配，`cap(1)` / `cap(2)` 取出两个捕获组；
/// 无匹配时返回 None。
pub fn capture_key_value(s: &str) -> Option<(String, String)> {
    let re = Regex::new(r"(\w+)\s*=\s*(\w+)").unwrap();
    let caps = re.captures(s)?;
    Some((caps[1].to_string(), caps[2].to_string()))
}

/// 按逗号（可带空白）切分字符串
///
/// `Regex::split` 以正则作为分隔符；分隔模式包含空白，
/// 因此结果元素不含逗号两侧的空格。
pub fn split_commas(s: &str) -> Vec<String> {
    Regex::new(r",\s*")
        .unwrap()
        .split(s)
        .map(|p| p.to_string())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_emails() {
        let got = extract_emails("联系 a@b.com 或 c@d.cn");
        assert_eq!(got, vec!["a@b.com".to_string(), "c@d.cn".to_string()]);
        assert!(extract_emails("无邮箱").is_empty());
    }

    #[test]
    fn test_count_matches() {
        assert_eq!(count_matches("a1b2c3", r"\d"), 3);
    }

    #[test]
    fn test_replace_digits() {
        assert_eq!(replace_digits("a1b2"), "aXbX");
    }

    #[test]
    fn test_capture_key_value() {
        assert_eq!(
            capture_key_value("name = Alice"),
            Some(("name".to_string(), "Alice".to_string()))
        );
        assert_eq!(capture_key_value("没有等号"), None);
    }

    #[test]
    fn test_split_commas() {
        assert_eq!(
            split_commas("a, b, c"),
            vec!["a".to_string(), "b".to_string(), "c".to_string()]
        );
    }
}
