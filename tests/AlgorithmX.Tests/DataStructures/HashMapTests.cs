namespace AlgorithmX.Tests.DataStructures;

public class HashMapTests
{
    [Fact]
    public void PutAndGet_ShouldWork()
    {
        var map = new AlgorithmX.DataStructures.HashTable.HashMap<string, int>();
        map.Put("a", 1);
        map.Put("b", 2);
        map.Put("c", 3);
        Assert.True(map.TryGetValue("a", out var v1));
        Assert.Equal(1, v1);
        Assert.True(map.TryGetValue("b", out var v2));
        Assert.Equal(2, v2);
    }

    [Fact]
    public void Indexer_ShouldGetAndSet()
    {
        var map = new AlgorithmX.DataStructures.HashTable.HashMap<string, string>();
        map["hello"] = "world";
        Assert.Equal("world", map["hello"]);
        map["hello"] = "updated";
        Assert.Equal("updated", map["hello"]);
    }

    [Fact]
    public void Put_ShouldUpdateExistingKey()
    {
        var map = new AlgorithmX.DataStructures.HashTable.HashMap<int, string>();
        map.Put(1, "one");
        map.Put(1, "ONE");
        Assert.Equal("ONE", map[1]);
        Assert.Equal(1, map.Count);
    }

    [Fact]
    public void Remove_ShouldDeleteKey()
    {
        var map = new AlgorithmX.DataStructures.HashTable.HashMap<string, int>();
        map.Put("x", 10);
        Assert.True(map.Remove("x"));
        Assert.False(map.ContainsKey("x"));
        Assert.Equal(0, map.Count);
    }

    [Fact]
    public void Remove_NonExistent_ShouldReturnFalse()
    {
        var map = new AlgorithmX.DataStructures.HashTable.HashMap<string, int>();
        Assert.False(map.Remove("nonexistent"));
    }

    [Fact]
    public void Resize_ShouldPreserveData()
    {
        var map = new AlgorithmX.DataStructures.HashTable.HashMap<int, int>(4);
        for (int i = 0; i < 100; i++)
            map.Put(i, i * 10);
        Assert.Equal(100, map.Count);
        for (int i = 0; i < 100; i++)
            Assert.Equal(i * 10, map[i]);
    }

    [Fact]
    public void Keys_ShouldReturnAllKeys()
    {
        var map = new AlgorithmX.DataStructures.HashTable.HashMap<string, int>();
        map.Put("x", 1);
        map.Put("y", 2);
        map.Put("z", 3);
        var keys = map.Keys.ToHashSet();
        Assert.Contains("x", keys);
        Assert.Contains("y", keys);
        Assert.Contains("z", keys);
    }

    [Fact]
    public void ContainsKey_ShouldWork()
    {
        var map = new AlgorithmX.DataStructures.HashTable.HashMap<int, string>();
        map.Put(42, "answer");
        Assert.True(map.ContainsKey(42));
        Assert.False(map.ContainsKey(99));
    }
}
