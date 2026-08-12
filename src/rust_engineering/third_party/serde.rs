//! serde / serde_json 序列化
//!
//! 覆盖主题：结构体 derive、JSON 序列化/反序列化、
//! `#[serde(default)]` 与 `skip_serializing_if` 属性、通用 Map 解析。
//!
//! 典型场景：Rust 与 JSON 之间互转（REST API、配置文件），
//! 通过属性控制字段的默认值与省略规则，无需手写编解码逻辑。

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// 用户结构体，演示 serde 派生与常用属性
///
/// - `#[serde(default)]`：JSON 缺省该字段时用类型默认值（空 Vec）
/// - `#[serde(skip_serializing_if = "Option::is_none")]`：None 时序列化省略
#[derive(Serialize, Deserialize, Debug, PartialEq)]
pub struct User {
    pub name: String,
    pub age: u8,
    #[serde(default)]
    pub tags: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub email: Option<String>,
}

/// 把用户结构体序列化为 JSON 字符串
///
/// `serde_json::to_string` 依赖 derive 出的 Serialize 实现；
/// 本函数输入必然是合法结构体，因此直接 unwrap。
pub fn user_to_json(user: &User) -> String {
    serde_json::to_string(user).unwrap()
}

/// 从 JSON 字符串反序列化为 User
///
/// `serde_json::from_str` 依赖 derive 出的 Deserialize 实现，
/// 语法错误或类型不匹配时返回带行列位置的错误。
pub fn json_to_user(s: &str) -> Result<User, serde_json::Error> {
    serde_json::from_str(s)
}

/// 解析扁平配置：字符串到整数的映射
///
/// 把 `{"a":1,"b":2}` 之类的 JSON 直接反序列化为 `HashMap<String, i32>`，
/// 无需定义结构体，适合键名不确定的配置场景。
pub fn parse_config(s: &str) -> Result<HashMap<String, i32>, serde_json::Error> {
    serde_json::from_str(s)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn alice() -> User {
        User {
            name: "Alice".into(),
            age: 30,
            tags: vec!["admin".into()],
            email: Some("a@b.c".into()),
        }
    }

    #[test]
    fn test_roundtrip() {
        let user = alice();
        let json = user_to_json(&user);
        assert_eq!(json_to_user(&json).unwrap(), user);
    }

    #[test]
    fn test_skip_serializing_if() {
        let user = User {
            email: None,
            ..alice()
        };
        let json = user_to_json(&user);
        assert!(!json.contains("email"));
    }

    #[test]
    fn test_default_field() {
        let user = json_to_user(r#"{"name":"Bob","age":25}"#).unwrap();
        assert_eq!(user.name, "Bob");
        assert_eq!(user.age, 25);
        assert_eq!(user.tags, Vec::<String>::new());
        assert_eq!(user.email, None);
    }

    #[test]
    fn test_parse_config() {
        let map = parse_config(r#"{"a":1,"b":2}"#).unwrap();
        assert_eq!(map.len(), 2);
        assert_eq!(map.get("a"), Some(&1));
        assert_eq!(map.get("b"), Some(&2));
    }
}
