namespace AlgorithmX.Tests.DataStructures;

public class TrieTests
{
    [Fact]
    public void InsertAndSearch_ShouldWork()
    {
        var trie = new AlgorithmX.DataStructures.Trie.Trie();
        trie.Insert("hello");
        trie.Insert("world");
        Assert.True(trie.Search("hello"));
        Assert.True(trie.Search("world"));
        Assert.False(trie.Search("hell"));
        Assert.False(trie.Search("hello!"));
    }

    [Fact]
    public void StartsWith_ShouldFindPrefix()
    {
        var trie = new AlgorithmX.DataStructures.Trie.Trie();
        trie.Insert("apple");
        Assert.True(trie.StartsWith("app"));
        Assert.True(trie.StartsWith("a"));
        Assert.False(trie.StartsWith("b"));
    }

    [Fact]
    public void Remove_ShouldDeleteWord()
    {
        var trie = new AlgorithmX.DataStructures.Trie.Trie();
        trie.Insert("cat");
        trie.Insert("car");
        trie.Insert("card");
        Assert.True(trie.Remove("car"));
        Assert.False(trie.Search("car"));
        Assert.True(trie.Search("cat"));
        Assert.True(trie.Search("card"));
    }

    [Fact]
    public void Remove_NonExistent_ShouldReturnFalse()
    {
        var trie = new AlgorithmX.DataStructures.Trie.Trie();
        trie.Insert("abc");
        Assert.False(trie.Remove("ab"));
        Assert.False(trie.Remove("xyz"));
    }

    [Fact]
    public void GetWordsWithPrefix_ShouldReturnAllMatches()
    {
        var trie = new AlgorithmX.DataStructures.Trie.Trie();
        trie.Insert("dog");
        trie.Insert("door");
        trie.Insert("dot");
        trie.Insert("cat");

        var words = trie.GetWordsWithPrefix("do").ToList();
        Assert.Equal(3, words.Count);
        Assert.Contains("dog", words);
        Assert.Contains("door", words);
        Assert.Contains("dot", words);
        Assert.DoesNotContain("cat", words);
    }
}
