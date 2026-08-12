//! rand 0.9 随机数
//!
//! 覆盖主题：均匀整数/浮点采样、洗牌、随机选择、无放回抽样、
//! 随机密码（Alphanumeric）、种子固定可复现的序列。
//!
//! 典型场景：模拟掷骰子、抽奖、生成测试数据；`seeded_sequence`
//! 用固定种子保证结果可复现，便于调试与回归测试。
//!
//! 注意：rand 0.9 中洗牌/选择等是切片上的方法（如 `nums.shuffle(&mut rng)`），
//! 需引入 `rand::seq::{SliceRandom, IndexedRandom}` trait；`random_range`、
//! `random`、`sample_iter` 来自 `rand::Rng` trait；字符分布位于 `rand::distr`。

use rand::Rng;
use rand::SeedableRng;
use rand::distr::Alphanumeric;
use rand::rngs::StdRng;
use rand::seq::{IndexedRandom, SliceRandom};

/// 掷一枚六面骰子
///
/// `random_range(1..=6)` 从闭区间均匀采样一个 i32。复杂度 O(1)。
pub fn roll_d6() -> i32 {
    rand::rng().random_range(1..=6)
}

/// 掷 n 次骰子
///
/// 逐次调用 `roll_d6` 收集结果，返回长度为 n 的向量。
pub fn roll_many(n: usize) -> Vec<i32> {
    (0..n).map(|_| roll_d6()).collect()
}

/// 采样 [0, 1) 区间的随机浮点数
///
/// `random::<f64>()` 返回均匀分布于 [0, 1) 的 f64（含 0 不含 1），
/// 可用于概率判断，如 `x < 0.3` 表示 30% 概率命中。
pub fn random_unit_f64() -> f64 {
    rand::rng().random::<f64>()
}

/// 原地洗牌
///
/// `SliceRandom::shuffle` 对切片做均匀随机排列（Fisher-Yates），
/// 复杂度 O(n)，洗牌后元素集合保持不变。
pub fn shuffle_slice(nums: &mut [i32]) {
    nums.shuffle(&mut rand::rng());
}

/// 从切片中随机选一个元素
///
/// `SliceRandom::choose` 均匀随机返回一个元素的引用；空切片返回 None。
/// 复杂度 O(1)。
pub fn choose_random(nums: &[i32]) -> Option<&i32> {
    nums.choose(&mut rand::rng())
}

/// 无放回随机抽取 k 个元素
///
/// `partial_shuffle` 做部分 Fisher-Yates：只随机化前 k 个位置并返回
/// `(&mut [T], &mut [T])`，元组第一项即随机挑出的 k 个元素。
/// 复杂度 O(k)，比整体洗牌更高效。
pub fn sample_without_replacement(nums: &mut [i32], k: usize) -> Vec<i32> {
    let (picked, _) = nums.partial_shuffle(&mut rand::rng(), k);
    picked.to_vec()
}

/// 生成长度为 len 的随机 ASCII 字母数字密码
///
/// `Alphanumeric` 是 rand 0.9 中位于 `rand::distr` 的字符分布，
/// 用 `sample_iter` 采样并转成 `char`。复杂度 O(len)。
pub fn random_password(len: usize) -> String {
    rand::rng()
        .sample_iter(Alphanumeric)
        .take(len)
        .map(char::from)
        .collect()
}

/// 用固定种子生成可复现的随机序列
///
/// `StdRng::seed_from_u64` 构造确定性随机源，相同 seed 永远产生
/// 相同序列（这里输出 [0, 100) 的整数），便于测试与复现结果。
pub fn seeded_sequence(seed: u64, n: usize) -> Vec<u64> {
    let mut rng = StdRng::seed_from_u64(seed);
    (0..n).map(|_| rng.random_range(0..100)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_roll_d6_range() {
        for _ in 0..100 {
            let v = roll_d6();
            assert!((1..=6).contains(&v));
        }
    }

    #[test]
    fn test_roll_many() {
        let rolls = roll_many(100);
        assert_eq!(rolls.len(), 100);
        assert!(rolls.iter().all(|&v| (1..=6).contains(&v)));
    }

    #[test]
    fn test_random_unit_f64() {
        for _ in 0..100 {
            let x = random_unit_f64();
            assert!((0.0..1.0).contains(&x));
        }
    }

    #[test]
    fn test_shuffle_slice() {
        let mut v = vec![1, 2, 3, 4, 5];
        shuffle_slice(&mut v);
        let mut sorted = v.clone();
        sorted.sort();
        assert_eq!(sorted, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_choose_random() {
        assert_eq!(choose_random(&[7]), Some(&7));
        assert_eq!(choose_random(&[] as &[i32]), None);
    }

    #[test]
    fn test_sample_without_replacement() {
        let mut nums = vec![1, 2, 3, 4, 5];
        let picked = sample_without_replacement(&mut nums, 3);
        assert_eq!(picked.len(), 3);
        assert!(picked.iter().all(|x| nums.contains(x)));
    }

    #[test]
    fn test_random_password() {
        let pwd = random_password(12);
        assert_eq!(pwd.len(), 12);
        assert!(pwd.chars().all(|c| c.is_ascii_alphanumeric()));
    }

    #[test]
    fn test_seeded_sequence_deterministic() {
        assert_eq!(seeded_sequence(42, 5), seeded_sequence(42, 5));
    }
}
