//! chrono 日期时间处理
//!
//! 覆盖主题：日期差、ISO 解析、自定义格式化、周末判断、
//! 周岁计算、闰年日期运算。
//!
//! 典型场景：业务中日期的解析与运算；测试统一用 `NaiveDate` 保证
//! 确定性，真实场景可用 `Utc::now()` / `Local::now()` 取当前时间。

use chrono::{Datelike, NaiveDate};

/// 两个日期相差的天数
///
/// `signed_duration_since` 得到有符号时间差，`num_days` 取整天数；
/// b 早于 a 时结果为负。
pub fn days_between(a: NaiveDate, b: NaiveDate) -> i64 {
    b.signed_duration_since(a).num_days()
}

/// 解析 ISO 8601 日期字符串（YYYY-MM-DD）
///
/// `parse_from_str` 按格式模板解析，格式不符或日期非法（如 2 月 30 日）
/// 时返回 None。
pub fn parse_iso_date(s: &str) -> Option<NaiveDate> {
    NaiveDate::parse_from_str(s, "%Y-%m-%d").ok()
}

/// 格式化为中文日期（2024年01月02日）
///
/// `format` 中 `%Y`/`%m`/`%d` 是格式化指令，其余字符原样输出；
/// 注意 %m、%d 默认补零。
pub fn format_cn(d: &NaiveDate) -> String {
    d.format("%Y年%m月%d日").to_string()
}

/// 判断日期是否为周末
///
/// `weekday()` 返回该日是周几，`Sat`/`Sun` 即周末。
pub fn is_weekend(d: &NaiveDate) -> bool {
    matches!(d.weekday(), chrono::Weekday::Sat | chrono::Weekday::Sun)
}

/// 计算周岁（按公历生日）
///
/// 先取年份差，若今年的生日尚未到（当前月/日早于生日的月/日）再减一。
pub fn age_years(birth: NaiveDate, today: NaiveDate) -> i32 {
    let mut age = today.year() - birth.year();
    if (today.month(), today.day()) < (birth.month(), birth.day()) {
        age -= 1;
    }
    age
}

/// 日期加/减若干天
///
/// `NaiveDate + Duration` 自动处理跨月与闰年（如闰年 2 月 28 日
/// 加一天得到 2 月 29 日）。
pub fn add_days(d: NaiveDate, days: i64) -> NaiveDate {
    d + chrono::Duration::days(days)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn from(y: i32, m: u32, d: u32) -> NaiveDate {
        NaiveDate::from_ymd_opt(y, m, d).unwrap()
    }

    #[test]
    fn test_days_between() {
        assert_eq!(days_between(from(2024, 1, 1), from(2024, 1, 10)), 9);
        assert_eq!(days_between(from(2024, 1, 10), from(2024, 1, 1)), -9);
    }

    #[test]
    fn test_parse_iso_date() {
        assert_eq!(parse_iso_date("2024-06-15"), Some(from(2024, 6, 15)));
        assert!(parse_iso_date("bad").is_none());
        assert!(parse_iso_date("2024-13-01").is_none());
    }

    #[test]
    fn test_format_cn() {
        assert_eq!(format_cn(&from(2024, 1, 2)), "2024年01月02日");
    }

    #[test]
    fn test_is_weekend() {
        // 2024-06-15 是周六，2024-06-17 是周一
        assert!(is_weekend(&from(2024, 6, 15)));
        assert!(!is_weekend(&from(2024, 6, 17)));
    }

    #[test]
    fn test_age_years() {
        assert_eq!(age_years(from(2000, 5, 1), from(2024, 4, 30)), 23);
        assert_eq!(age_years(from(2000, 5, 1), from(2024, 5, 1)), 24);
    }

    #[test]
    fn test_add_days_leap_year() {
        // 2024 是闰年，2 月 28 日 + 1 天 = 2 月 29 日
        assert_eq!(add_days(from(2024, 2, 28), 1), from(2024, 2, 29));
        assert_eq!(add_days(from(2024, 1, 1), 365), from(2024, 12, 31));
    }
}
