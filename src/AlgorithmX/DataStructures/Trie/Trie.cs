namespace AlgorithmX.DataStructures.Trie;

/// <summary>
/// 前缀树 (Trie) — 高效字符串插入、搜索、前缀匹配。
/// </summary>
public class Trie
{
    private readonly TrieNode _root;

    public Trie()
    {
        _root = new TrieNode();
    }

    /// <summary>
    /// 插入单词。O(L)，L 为单词长度。
    /// </summary>
    public void Insert(string word)
    {
        var node = _root;
        foreach (char c in word)
        {
            int index = c - 'a';
            node.Children[index] ??= new TrieNode();
            node = node.Children[index]!;
        }
        node.IsEnd = true;
    }

    /// <summary>
    /// 搜索完整单词是否存在。O(L)。
    /// </summary>
    public bool Search(string word)
    {
        var node = SearchPrefix(word);
        return node != null && node.IsEnd;
    }

    /// <summary>
    /// 是否存在以 prefix 为前缀的单词。O(L)。
    /// </summary>
    public bool StartsWith(string prefix)
    {
        return SearchPrefix(prefix) != null;
    }

    /// <summary>
    /// 删除单词。返回 true 表示单词存在并被删除。O(L)。
    /// </summary>
    public bool Remove(string word)
    {
        return Remove(_root, word, 0).found;
    }

    /// <summary>
    /// 获取以 prefix 为前缀的所有单词。O(prefix + result)。
    /// </summary>
    public IEnumerable<string> GetWordsWithPrefix(string prefix)
    {
        var node = SearchPrefix(prefix);
        if (node == null) yield break;

        var stack = new Stack<(TrieNode, string)>();
        stack.Push((node, prefix));

        while (stack.Count > 0)
        {
            var (cur, curWord) = stack.Pop();
            if (cur.IsEnd) yield return curWord;

            for (int i = 25; i >= 0; i--) // 逆序遍历保证字母序
            {
                if (cur.Children[i] != null)
                {
                    char c = (char)('a' + i);
                    stack.Push((cur.Children[i]!, curWord + c));
                }
            }
        }
    }

    private TrieNode? SearchPrefix(string prefix)
    {
        var node = _root;
        foreach (char c in prefix)
        {
            int index = c - 'a';
            if (index < 0 || index >= 26 || node.Children[index] == null)
                return null;
            node = node.Children[index]!;
        }
        return node;
    }

    private (bool found, bool canDelete) Remove(TrieNode node, string word, int depth)
    {
        if (depth == word.Length)
        {
            if (!node.IsEnd) return (false, false);
            node.IsEnd = false;
            return (true, node.Children.All(c => c == null));
        }

        int index = word[depth] - 'a';
        var child = node.Children[index];
        if (child == null) return (false, false);

        var (found, canDelete) = Remove(child, word, depth + 1);
        if (canDelete)
        {
            node.Children[index] = null;
            return (found, !node.IsEnd && node.Children.All(c => c == null));
        }
        return (found, false);
    }

    /// <summary>
    /// Trie 节点。
    /// </summary>
    private sealed class TrieNode
    {
        public TrieNode?[] Children { get; } = new TrieNode?[26];
        public bool IsEnd { get; set; }
    }
}
