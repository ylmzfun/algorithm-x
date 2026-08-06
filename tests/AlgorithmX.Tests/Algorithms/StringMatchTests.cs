namespace AlgorithmX.Tests.Algorithms;

public class StringMatchTests
{
    [Fact]
    public void KmpSearch_ShouldFindAllOccurrences()
    {
        var result = AlgorithmX.Algorithms.String.StringMatch.KmpSearch("ABABABCABABAB", "ABAB");
        Assert.Equal(new[] { 0, 2, 7, 9 }, result);
    }

    [Fact]
    public void KmpSearch_NoMatch_ShouldReturnEmpty()
    {
        var result = AlgorithmX.Algorithms.String.StringMatch.KmpSearch("hello", "world");
        Assert.Empty(result);
    }

    [Fact]
    public void BuildLps_ShouldBeCorrect()
    {
        int[] lps = AlgorithmX.Algorithms.String.StringMatch.BuildLps("ABABCABAB");
        // A B A B C A B A B
        // 0 0 1 2 0 1 2 3 4
        Assert.Equal(new[] { 0, 0, 1, 2, 0, 1, 2, 3, 4 }, lps);
    }

    [Fact]
    public void RabinKarpSearch_ShouldFindAllOccurrences()
    {
        var result = AlgorithmX.Algorithms.String.StringMatch.RabinKarpSearch("ABABABCABABAB", "ABAB");
        Assert.Equal(new[] { 0, 2, 7, 9 }, result);
    }

    [Fact]
    public void LongestPalindrome_Manacher_ShouldFindLongest()
    {
        Assert.Equal("bab", AlgorithmX.Algorithms.String.StringMatch.LongestPalindrome("babad"));
        Assert.Equal("bb", AlgorithmX.Algorithms.String.StringMatch.LongestPalindrome("cbbd"));
    }
}
