namespace AlgorithmX.Tests.Algorithms;

public class RandomizationTests
{
    [Fact]
    public void Shuffle_ShouldPermuteElements()
    {
        int[] array = { 1, 2, 3, 4, 5, 6, 7, 8 };
        var original = (int[])array.Clone();
        AlgorithmX.Algorithms.Randomization.Randomization.Shuffle(array);
        Assert.Equal(original.OrderBy(x => x), array.OrderBy(x => x));
    }

    [Fact]
    public void ReservoirSample_ShouldReturnKDistinctElements()
    {
        var stream = Enumerable.Range(0, 100);
        var sample = AlgorithmX.Algorithms.Randomization.Randomization.ReservoirSample(stream, 10);
        Assert.Equal(10, sample.Length);
        Assert.Equal(10, sample.Distinct().Count());
    }

    [Fact]
    public void ReservoirSample_SmallStream_ShouldReturnAll()
    {
        var stream = new[] { 1, 2, 3 };
        var sample = AlgorithmX.Algorithms.Randomization.Randomization.ReservoirSample(stream, 10);
        Assert.Equal(3, sample.Length);
    }

    [Fact]
    public void RandomInt_ShouldBeInRange()
    {
        for (int i = 0; i < 100; i++)
        {
            int val = AlgorithmX.Algorithms.Randomization.Randomization.RandomInt(0, 10);
            Assert.InRange(val, 0, 9);
        }
    }
}
