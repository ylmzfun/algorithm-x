//! indexmap / smallvec 集合容器
//!
//! 覆盖主题：保序哈希表（IndexMap）用于首次非重复字符、插入顺序
//! 保持、LRU 缓存模拟；smallvec 栈上小向量。
//!
//! 典型场景：需要"哈希查找 + 插入顺序"两者兼得（如 LRU、去重保序），
//! 以及高频创建小向量的场景（smallvec 在容量内免堆分配）。

use indexmap::IndexMap;
use smallvec::SmallVec;

/// 找到第一个不重复的字符
///
/// 用 `IndexMap<char, usize>` 统计次数：它兼具 HashMap 的 O(1) 查找与
/// 插入顺序保持，因此第一遍统计后按 map 的插入序遍历即字符首次出现
/// 顺序，找到第一个计数为 1 的字符即可；全部重复则返回 None。
pub fn first_non_repeating(s: &str) -> Option<char> {
    let mut counts: IndexMap<char, usize> = IndexMap::new();
    for c in s.chars() {
        *counts.entry(c).or_insert(0) += 1;
    }
    counts.into_iter().find_map(|(c, n)| (n == 1).then_some(c))
}

/// 验证插入顺序被保持
///
/// `IndexMap::insert` 不改变既有元素的相对顺序，新键追加到末尾；
/// `keys()` 按插入顺序产出。
pub fn insertion_order_kept<'a>(items: &[&'a str]) -> Vec<&'a str> {
    let mut map = IndexMap::new();
    for &item in items {
        map.insert(item, ());
    }
    map.keys().copied().collect()
}

/// 用 IndexMap 模拟 LRU 缓存淘汰
///
/// 约定"末尾 = 最近使用"：命中时先 `shift_remove` 再 `insert` 移到末尾；
/// 新键插入后若超出容量，`shift_remove_index(0)` 淘汰最久未用的队首。
/// 返回最终缓存中按键（最久未用在前）。
/// 例：容量 2 依次访问 [1,2,3,1]：1、2 入队 → 访问 3 挤掉 1 → 再访问 1
/// 时 1 重新入队并挤掉 2，最终剩余 [3,1]。
pub fn lru_evict(capacity: usize, accesses: &[i32]) -> Vec<i32> {
    let mut cache: IndexMap<i32, ()> = IndexMap::new();
    for &key in accesses {
        if cache.contains_key(&key) {
            cache.shift_remove(&key);
        }
        cache.insert(key, ());
        if cache.len() > capacity {
            cache.shift_remove_index(0);
        }
    }
    cache.keys().copied().collect()
}

/// smallvec 演示：≤4 个元素内联在栈上
///
/// `SmallVec<[i32; 4]>` 有 4 个元素的内联容量，不超出时零堆分配；
/// `extend_from_slice` 复制进向量，超容才转为堆存储。
pub fn smallvec_demo(values: &[i32]) -> SmallVec<[i32; 4]> {
    let mut v: SmallVec<[i32; 4]> = SmallVec::new();
    v.extend_from_slice(values);
    v
}

/// 查询 smallvec 的内联容量
///
/// `inline_size()` 返回栈上可容纳的元素个数（内部即关联函数
/// `inline_capacity()` 的值），这里应为 4。
pub fn smallvec_inline_capacity() -> usize {
    SmallVec::<[i32; 4]>::new().inline_size()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_first_non_repeating() {
        assert_eq!(first_non_repeating("leetcode"), Some('l'));
        assert_eq!(first_non_repeating("aabb"), None);
    }

    #[test]
    fn test_insertion_order_kept() {
        assert_eq!(insertion_order_kept(&["b", "a", "c"]), vec!["b", "a", "c"]);
    }

    #[test]
    fn test_lru_evict() {
        // 容量 2，访问序列 [1,2,3,1]：
        // 1→[1]  2→[1,2]  3→[2,3]（挤掉 1）  1→[3,1]（挤掉 2）
        assert_eq!(lru_evict(2, &[1, 2, 3, 1]), vec![3, 1]);
    }

    #[test]
    fn test_smallvec_demo() {
        assert_eq!(
            smallvec_demo(&[1, 2, 3, 4, 5]).to_vec(),
            vec![1, 2, 3, 4, 5]
        );
    }

    #[test]
    fn test_smallvec_inline_capacity() {
        assert_eq!(smallvec_inline_capacity(), 4);
    }
}
