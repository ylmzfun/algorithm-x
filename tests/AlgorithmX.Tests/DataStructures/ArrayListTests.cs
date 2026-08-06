namespace AlgorithmX.Tests.DataStructures;

public class ArrayListTests
{
    [Fact]
    public void Add_ShouldIncreaseCount()
    {
        var list = new AlgorithmX.DataStructures.Arrays.ArrayList<int>();
        list.Add(1);
        list.Add(2);
        list.Add(3);
        Assert.Equal(3, list.Count);
    }

    [Fact]
    public void Indexer_ShouldGetAndSetValues()
    {
        var list = new AlgorithmX.DataStructures.Arrays.ArrayList<int>();
        list.Add(10);
        list.Add(20);
        Assert.Equal(10, list[0]);
        list[1] = 30;
        Assert.Equal(30, list[1]);
    }

    [Fact]
    public void Insert_ShouldShiftElements()
    {
        var list = new AlgorithmX.DataStructures.Arrays.ArrayList<int>();
        list.Add(1);
        list.Add(3);
        list.Insert(1, 2);
        Assert.Equal(3, list.Count);
        Assert.Equal(1, list[0]);
        Assert.Equal(2, list[1]);
        Assert.Equal(3, list[2]);
    }

    [Fact]
    public void RemoveAt_ShouldShiftElements()
    {
        var list = new AlgorithmX.DataStructures.Arrays.ArrayList<int>();
        list.Add(1);
        list.Add(2);
        list.Add(3);
        int removed = list.RemoveAt(1);
        Assert.Equal(2, removed);
        Assert.Equal(2, list.Count);
        Assert.Equal(3, list[1]);
    }

    [Fact]
    public void Add_BeyondCapacity_ShouldResize()
    {
        var list = new AlgorithmX.DataStructures.Arrays.ArrayList<int>(2);
        for (int i = 0; i < 100; i++)
            list.Add(i);
        Assert.Equal(100, list.Count);
        Assert.Equal(99, list[99]);
    }

    [Fact]
    public void Remove_NonExistent_ShouldReturnFalse()
    {
        var list = new AlgorithmX.DataStructures.Arrays.ArrayList<int>();
        list.Add(1);
        Assert.False(list.Remove(999));
    }

    [Fact]
    public void Clear_ShouldResetCount()
    {
        var list = new AlgorithmX.DataStructures.Arrays.ArrayList<int>();
        list.Add(1);
        list.Add(2);
        list.Clear();
        Assert.Equal(0, list.Count);
        Assert.True(list.IsEmpty);
    }

    [Fact]
    public void Contains_ShouldFindExistingElement()
    {
        var list = new AlgorithmX.DataStructures.Arrays.ArrayList<int>();
        list.Add(5);
        list.Add(10);
        Assert.True(list.Contains(5));
        Assert.False(list.Contains(99));
    }
}
