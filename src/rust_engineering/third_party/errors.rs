//! anyhow / thiserror 错误处理
//!
//! 覆盖主题：thiserror 派生库错误类型（`#[from]` 自动转换）、
//! anyhow 的应用层错误（Context 附加说明、ensure/bail 宏）。
//!
//! 典型场景：库代码用 thiserror 定义精确的错误枚举；应用/二进制
//! 用 anyhow 快速传播错误并附加人类可读的上下文。

use anyhow::Context;
use thiserror::Error;

/// 解析类错误枚举
///
/// `#[error(...)]` 定义 Display 文案；`#[from]` 自动为 `ParseIntError`
/// 生成 `From` 实现，使 `?` 可以无样板地把底层错误转换成 `InvalidNumber`。
#[derive(Debug, Error, PartialEq)]
pub enum ParseError {
    #[error("字段 {0} 缺失")]
    MissingField(&'static str),
    #[error("无效数字: {0}")]
    InvalidNumber(#[from] std::num::ParseIntError),
}

/// 解析 "x,y" 形式的坐标点
///
/// 按逗号切分：字段不足 2 个返回 `MissingField`；
/// 否则用 `?` 解析两个 i64（自动经 `#[from]` 转为 `InvalidNumber`）。
pub fn parse_point(s: &str) -> Result<(i64, i64), ParseError> {
    let parts: Vec<&str> = s.split(',').collect();
    if parts.len() < 2 {
        return Err(ParseError::MissingField("需要两个坐标"));
    }
    let x: i64 = parts[0].trim().parse()?;
    let y: i64 = parts[1].trim().parse()?;
    Ok((x, y))
}

/// 读取一个整数并附加错误上下文
///
/// `context` 把底层解析错误包装进 `anyhow::Error` 并附上
/// "无法解析为整数" 的说明，便于定位出错环节。
pub fn read_number(s: &str) -> anyhow::Result<i64> {
    s.trim().parse::<i64>().context("无法解析为整数")
}

/// 校验参数为正数
///
/// `anyhow::ensure!` 不满足条件时直接构造错误返回，
/// 失败信息可携带运行时值（这里打印实际的 n）。
pub fn validate_positive(n: i32) -> anyhow::Result<i32> {
    anyhow::ensure!(n > 0, "n 必须为正数，实际为 {n}");
    Ok(n)
}

/// 演示 `bail!` 立即失败
///
/// `anyhow::bail!` 在当前函数直接返回一个构造好的错误，
/// 常用于条件不满足时的提前退出。
pub fn fail_with_bail() -> anyhow::Result<()> {
    anyhow::bail!("故意失败");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_point_ok() {
        assert_eq!(parse_point("3,4"), Ok((3, 4)));
        assert_eq!(parse_point(" 3 , 4 "), Ok((3, 4)));
    }

    #[test]
    fn test_parse_point_missing() {
        let err = parse_point("3").unwrap_err().to_string();
        assert!(err.contains("缺失"));
    }

    #[test]
    fn test_parse_point_invalid() {
        let err = parse_point("x,4").unwrap_err().to_string();
        assert!(err.contains("无效数字"));
    }

    #[test]
    fn test_read_number() {
        assert_eq!(read_number("42").unwrap(), 42);
        assert!(read_number("abc").is_err());
    }

    #[test]
    fn test_validate_positive() {
        assert_eq!(validate_positive(5).unwrap(), 5);
        assert!(validate_positive(0).is_err());
    }

    #[test]
    fn test_fail_with_bail() {
        assert!(fail_with_bail().is_err());
    }
}
