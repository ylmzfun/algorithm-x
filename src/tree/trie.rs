/// 前缀树 (Trie)
///
/// 用于高效存储和检索字符串集合，常用于：
/// - 自动补全
/// - 拼写检查
/// - IP 路由（最长前缀匹配）
use std::collections::HashMap;

/// Trie 节点 — 使用 HashMap 存子节点
#[derive(Debug, Default)]
pub struct TrieNode {
    children: HashMap<char, TrieNode>,
    is_end: bool,
}

/// 标准前缀树
#[derive(Debug)]
pub struct Trie {
    root: TrieNode,
}

impl Trie {
    pub fn new() -> Self {
        Self {
            root: TrieNode::default(),
        }
    }

    /// 插入单词 O(len)
    pub fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;
        for c in word.chars() {
            node = node.children.entry(c).or_default();
        }
        node.is_end = true;
    }

    /// 精确查找单词 O(len)
    pub fn search(&self, word: &str) -> bool {
        self.walk(word).map_or(false, |n| n.is_end)
    }

    /// 是否存在以此为前缀的单词 O(len)
    pub fn starts_with(&self, prefix: &str) -> bool {
        self.walk(prefix).is_some()
    }

    /// 获取所有以 prefix 为前缀的单词列表
    pub fn words_with_prefix(&self, prefix: &str) -> Vec<String> {
        let mut result = Vec::new();
        if let Some(node) = self.walk(prefix) {
            let mut current = prefix.to_string();
            Self::collect_words(node, &mut current, &mut result);
        }
        result
    }

    /// 删除单词（如果存在）
    pub fn remove(&mut self, word: &str) -> bool {
        Self::remove_recursive(&mut self.root, word, 0)
    }

    fn remove_recursive(node: &mut TrieNode, word: &str, depth: usize) -> bool {
        if depth == word.len() {
            if node.is_end {
                node.is_end = false;
                return true;
            }
            return false;
        }

        let c = word.chars().nth(depth).unwrap();
        if let Some(child) = node.children.get_mut(&c) {
            let found = Self::remove_recursive(child, word, depth + 1);
            if found && child.children.is_empty() && !child.is_end {
                node.children.remove(&c);
            }
            return found;
        }
        false
    }

    fn walk(&self, s: &str) -> Option<&TrieNode> {
        let mut node = &self.root;
        for c in s.chars() {
            node = node.children.get(&c)?;
        }
        Some(node)
    }

    fn collect_words(node: &TrieNode, current: &mut String, result: &mut Vec<String>) {
        if node.is_end {
            result.push(current.clone());
        }
        for (&c, child) in &node.children {
            current.push(c);
            Self::collect_words(child, current, result);
            current.pop();
        }
    }
}

/// 使用 `[Option<Box<TrieNode26>>; 26]` 数组代替 HashMap 的高性能实现
/// 仅支持小写英文字母 a-z
#[derive(Debug)]
pub struct TrieNode26 {
    children: [Option<Box<TrieNode26>>; 26],
    is_end: bool,
}

impl TrieNode26 {
    fn new() -> Self {
        Self {
            children: std::array::from_fn(|_| None),
            is_end: false,
        }
    }
}

#[derive(Debug)]
pub struct Trie26 {
    root: TrieNode26,
}

impl Trie26 {
    pub fn new() -> Self {
        Self {
            root: TrieNode26::new(),
        }
    }

    pub fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;
        for b in word.bytes() {
            let idx = (b - b'a') as usize;
            node = node.children[idx].get_or_insert_with(|| Box::new(TrieNode26::new()));
        }
        node.is_end = true;
    }

    pub fn search(&self, word: &str) -> bool {
        self.walk(word).map_or(false, |n| n.is_end)
    }

    pub fn starts_with(&self, prefix: &str) -> bool {
        self.walk(prefix).is_some()
    }

    fn walk(&self, s: &str) -> Option<&TrieNode26> {
        let mut node = &self.root;
        for b in s.bytes() {
            let idx = (b - b'a') as usize;
            node = node.children[idx].as_ref()?;
        }
        Some(node)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trie_insert_search() {
        let mut trie = Trie::new();
        trie.insert("hello");
        trie.insert("world");
        assert!(trie.search("hello"));
        assert!(trie.search("world"));
        assert!(!trie.search("hell"));
        assert!(!trie.search("worlds"));
    }

    #[test]
    fn test_trie_starts_with() {
        let mut trie = Trie::new();
        trie.insert("apple");
        assert!(trie.starts_with("app"));
        assert!(trie.starts_with("apple"));
        assert!(!trie.starts_with("appx"));
    }

    #[test]
    fn test_trie_words_with_prefix() {
        let mut trie = Trie::new();
        trie.insert("app");
        trie.insert("apple");
        trie.insert("application");
        trie.insert("apricot");
        trie.insert("banana");

        let mut words = trie.words_with_prefix("app");
        words.sort();
        assert_eq!(words, vec!["app", "apple", "application"]);
    }

    #[test]
    fn test_trie_remove() {
        let mut trie = Trie::new();
        trie.insert("apple");
        trie.insert("app");
        assert!(trie.search("apple"));
        assert!(trie.remove("apple"));
        assert!(!trie.search("apple"));
        assert!(trie.search("app")); // app 还在
    }

    #[test]
    fn test_trie26() {
        let mut trie = Trie26::new();
        trie.insert("hello");
        trie.insert("help");
        assert!(trie.search("hello"));
        assert!(trie.starts_with("hel"));
        assert!(!trie.search("hell"));
    }
}
