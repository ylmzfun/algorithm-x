//! 错误处理模式（仅 std）
//!
//! 覆盖主题：
//! - `Result` / `Option` 组合子：`ok_or` / `collect` / `?`
//! - `?` 与 From 自动转换：`ParseIntError` 自动装箱为 `Box<dyn Error>`
//! - 自定义错误类型：实现 `Display` + `std::error::Error`
//! - 动态错误：`Box<dyn std::error::Error>`

/// 解析一行 CSV（逗号分隔的整数）
///
/// `collect::<Result<Vec<_>, _>>()`：任一字段解析失败即整体返回第一个错误
/// （短路），演示 `?` 风格的批量解析。
pub fn parse_csv_row(line: &str) -> Result<Vec<i64>, std::num::ParseIntError> {
    line.split(',').map(|s| s.parse::<i64>()).collect()
}

/// 安全除法
///
/// `checked_div` 在除数为 0 时返回 `None` 而不是 panic（普通 `/` 会 panic）。
pub fn divide(a: i64, b: i64) -> Option<i64> {
    a.checked_div(b)
}

/// 找第一个正数
///
/// `find` 返回第一个满足条件的 `Option<&i32>`，`copied` 解引用出值，
/// `ok_or` 把 `None` 转成带错误信息的 `Err`。复杂度 O(n)。
pub fn first_positive(nums: &[i32]) -> Result<i32, &'static str> {
    nums.iter().find(|&&x| x > 0).copied().ok_or("没有正数")
}

/// 校验范围（0..=100）
///
/// 手写 if/else 返回 `Result`，简单场景用 `&'static str` 作错误类型即可。
pub fn validate_range(n: i32) -> Result<i32, &'static str> {
    if !(0..=100).contains(&n) {
        return Err("超出 0..=100 范围");
    }
    Ok(n)
}

/// 自定义配置错误
///
/// 手工实现 `Display`（用户可见信息）并实现 `std::error::Error`
/// （提供 `source()` 默认实现，并让 `?` 可以把它转成 `Box<dyn Error>`）。
#[derive(Debug, PartialEq, Eq)]
pub enum ConfigError {
    /// 缺少必需字段
    MissingField(&'static str),
    /// 字段无法解析为数字
    BadNumber(String),
}

impl std::fmt::Display for ConfigError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ConfigError::MissingField(name) => write!(f, "缺少字段: {name}"),
            ConfigError::BadNumber(raw) => write!(f, "无法解析数字: {raw}"),
        }
    }
}

impl std::error::Error for ConfigError {}

/// 解析形如 "x,y" 的坐标字符串
///
/// 返回 `Box<dyn Error>` 以便混合多种错误类型：
/// - 字段数不足 → `ConfigError::MissingField`（`.into()` 显式装箱）；
/// - 数字解析失败 → `?` 自动把 `ParseIntError` 装箱（`From` 转换）。
pub fn parse_point(s: &str) -> Result<(i64, i64), Box<dyn std::error::Error>> {
    let parts: Vec<&str> = s.split(',').collect();
    if parts.len() < 2 {
        return Err(ConfigError::MissingField("需要两个坐标").into());
    }
    let x: i64 = parts[0].trim().parse()?;
    let y: i64 = parts[1].trim().parse()?;
    Ok((x, y))
}

/// 安全求平均值
///
/// 空输入返回 `None`（避免除零），否则求和后除以个数。
/// 先转 i64 累加避免 i32 溢出。复杂度 O(n)。
pub fn safe_average(nums: &[i32]) -> Option<f64> {
    if nums.is_empty() {
        return None;
    }
    let sum: i64 = nums.iter().map(|&x| x as i64).sum();
    Some(sum as f64 / nums.len() as f64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_csv_row() {
        assert_eq!(parse_csv_row("1,2,3"), Ok(vec![1, 2, 3]));
        assert!(parse_csv_row("1,x").is_err());
    }

    #[test]
    fn test_divide() {
        assert_eq!(divide(10, 0), None);
        assert_eq!(divide(10, 2), Some(5));
    }

    #[test]
    fn test_first_positive() {
        assert_eq!(first_positive(&[-1, -2, 3]), Ok(3));
        assert_eq!(first_positive(&[-1, -2]), Err("没有正数"));
    }

    #[test]
    fn test_validate_range() {
        assert_eq!(validate_range(5), Ok(5));
        assert_eq!(validate_range(100), Ok(100));
        assert_eq!(validate_range(-1), Err("超出 0..=100 范围"));
    }

    #[test]
    fn test_parse_point() {
        // Box<dyn Error> 未实现 PartialEq，用 unwrap 取出值再比较
        assert_eq!(parse_point("3,4").unwrap(), (3, 4));
        assert!(parse_point("3").is_err()); // 字段不足
        assert!(parse_point("x,4").is_err()); // 数字解析失败
        assert_eq!(parse_point(" 3 , 4 ").unwrap(), (3, 4)); // trim 容忍空白
    }

    #[test]
    fn test_safe_average() {
        assert_eq!(safe_average(&[1, 2, 3]), Some(2.0));
        assert_eq!(safe_average(&[]), None);
    }
}
