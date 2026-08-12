//! 第三方库核心算法及使用
//!
//! - `rayon` — 并行迭代
//! - `itertools` — 迭代器增强
//! - `rand` — 随机数
//! - `petgraph` — 图算法
//! - `num_bigint` — 大整数
//! - `collections` — indexmap / smallvec
//! - `serde` — 序列化
//! - `errors` — anyhow / thiserror
//! - `regex` — 正则表达式
//! - `chrono` — 日期时间
//! - `async_runtime` — tokio / futures

pub mod async_runtime;
pub mod chrono;
pub mod collections;
pub mod errors;
pub mod itertools;
pub mod num_bigint;
pub mod petgraph;
pub mod rand;
pub mod rayon;
pub mod regex;
pub mod serde;
