/// 哈希表原理与实现
///
/// - 拉链法 (Separate Chaining)
/// - 开放寻址法 (Open Addressing) 简易演示
///
/// Rust 标准库 `HashMap` 使用 SwissTable（Google 开源的高性能实现），
/// 此处实现简化版以理解核心原理。

const INITIAL_CAPACITY: usize = 16;
const LOAD_FACTOR: f64 = 0.75;

/// 拉链法哈希表
///
/// 每个槽位是一个链表（单向量），冲突时追加到链表尾部。
#[derive(Debug)]
pub struct HashMap<K, V> {
    buckets: Vec<Vec<(K, V)>>,
    len: usize,
}

impl<K: Eq + std::hash::Hash, V> HashMap<K, V> {
    pub fn new() -> Self {
        Self {
            buckets: (0..INITIAL_CAPACITY).map(|_| Vec::new()).collect(),
            len: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn insert(&mut self, key: K, value: V) -> Option<V> {
        if self.load_factor() >= LOAD_FACTOR {
            self.resize(self.buckets.len() * 2);
        }
        let idx = self.bucket_index(&key);
        let bucket = &mut self.buckets[idx];
        for (k, v) in bucket.iter_mut() {
            if *k == key {
                let old = std::mem::replace(v, value);
                return Some(old);
            }
        }
        bucket.push((key, value));
        self.len += 1;
        None
    }

    pub fn get(&self, key: &K) -> Option<&V> {
        let idx = self.bucket_index(key);
        self.buckets[idx]
            .iter()
            .find(|(k, _)| k == key)
            .map(|(_, v)| v)
    }

    pub fn remove(&mut self, key: &K) -> Option<V> {
        let idx = self.bucket_index(key);
        let bucket = &mut self.buckets[idx];
        if let Some(pos) = bucket.iter().position(|(k, _)| k == key) {
            let (_, v) = bucket.remove(pos);
            self.len -= 1;
            Some(v)
        } else {
            None
        }
    }

    pub fn contains_key(&self, key: &K) -> bool {
        self.get(key).is_some()
    }

    fn bucket_index(&self, key: &K) -> usize {
        use std::hash::Hasher;
        let mut hasher = std::collections::hash_map::DefaultHasher::new();
        key.hash(&mut hasher);
        hasher.finish() as usize % self.buckets.len()
    }

    fn load_factor(&self) -> f64 {
        self.len as f64 / self.buckets.len() as f64
    }

    fn resize(&mut self, new_cap: usize) {
        use std::hash::Hasher;
        let mut new_buckets: Vec<Vec<(K, V)>> = (0..new_cap).map(|_| Vec::new()).collect();
        for bucket in self.buckets.iter_mut() {
            for (key, value) in bucket.drain(..) {
                let mut hasher = std::collections::hash_map::DefaultHasher::new();
                key.hash(&mut hasher);
                let idx = hasher.finish() as usize % new_cap;
                new_buckets[idx].push((key, value));
            }
        }
        self.buckets = new_buckets;
    }
}

// ========== 常见 HashMap 模式 ==========

/// 两数之和 — HashMap 经典题
///
/// 给定数组和目标值，返回两个相加等于目标值的元素下标。
pub fn two_sum(nums: &[i32], target: i32) -> Option<(usize, usize)> {
    let mut map = std::collections::HashMap::new();
    for (i, &n) in nums.iter().enumerate() {
        let complement = target - n;
        if let Some(&j) = map.get(&complement) {
            return Some((j, i));
        }
        map.insert(n, i);
    }
    None
}

/// 字符计数 — HashMap 统计频率
pub fn char_frequency(s: &str) -> std::collections::HashMap<char, usize> {
    let mut freq = std::collections::HashMap::new();
    for c in s.chars() {
        *freq.entry(c).or_insert(0) += 1;
    }
    freq
}

/// 分组异位词
///
/// 将字母异位词（组成字母相同但顺序不同）分组。
pub fn group_anagrams(strs: &[&str]) -> Vec<Vec<String>> {
    let mut map: std::collections::HashMap<String, Vec<String>> = std::collections::HashMap::new();
    for &s in strs {
        let mut chars: Vec<char> = s.chars().collect();
        chars.sort();
        let key: String = chars.into_iter().collect();
        map.entry(key).or_default().push(s.to_string());
    }
    map.into_values().collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hashmap_insert_get() {
        let mut map = HashMap::new();
        map.insert("key1", 1);
        map.insert("key2", 2);
        map.insert("key3", 3);
        assert_eq!(map.len(), 3);
        assert_eq!(map.get(&"key1"), Some(&1));
        assert_eq!(map.get(&"key4"), None);
    }

    #[test]
    fn test_hashmap_update() {
        let mut map = HashMap::new();
        assert_eq!(map.insert("key", 1), None);
        assert_eq!(map.insert("key", 100), Some(1));
        assert_eq!(map.get(&"key"), Some(&100));
    }

    #[test]
    fn test_hashmap_remove() {
        let mut map = HashMap::new();
        map.insert("a", 10);
        map.insert("b", 20);
        assert_eq!(map.remove(&"a"), Some(10));
        assert_eq!(map.len(), 1);
        assert!(map.get(&"a").is_none());
    }

    #[test]
    fn test_hashmap_resize() {
        let mut map = HashMap::new();
        for i in 0..100 {
            map.insert(i, i * 2);
        }
        assert_eq!(map.len(), 100);
        assert_eq!(map.get(&50), Some(&100));
    }

    #[test]
    fn test_two_sum() {
        assert_eq!(two_sum(&[2, 7, 11, 15], 9), Some((0, 1)));
        assert_eq!(two_sum(&[3, 2, 4], 6), Some((1, 2)));
        assert_eq!(two_sum(&[3, 3], 6), Some((0, 1)));
    }

    #[test]
    fn test_group_anagrams() {
        let mut result = group_anagrams(&["eat", "tea", "tan", "ate", "nat", "bat"]);
        for group in result.iter_mut() {
            group.sort();
        }
        result.sort_by(|a, b| a[0].cmp(&b[0]));
        assert_eq!(result.len(), 3);
    }
}
