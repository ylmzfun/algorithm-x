namespace AlgorithmX.Tests.Algorithms;

public class MathAlgorithmTests
{
    [Fact]
    public void Gcd_ShouldBeCorrect()
    {
        Assert.Equal(6, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Gcd(12, 18));
        Assert.Equal(1, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Gcd(17, 31));
    }

    [Fact]
    public void Lcm_ShouldBeCorrect()
    {
        Assert.Equal(12, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Lcm(3, 4));
        Assert.Equal(36, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Lcm(12, 18));
    }

    [Fact]
    public void ExtendedGcd_ShouldFindBezoutCoefficients()
    {
        var (gcd, x, y) = AlgorithmX.Algorithms.MathLib.MathAlgorithm.ExtendedGcd(35, 15);
        Assert.Equal(5, gcd);
        Assert.Equal(35 * x + 15 * y, gcd);
    }

    [Fact]
    public void ModInverse_ShouldBeCorrect()
    {
        Assert.Equal(4, AlgorithmX.Algorithms.MathLib.MathAlgorithm.ModInverse(3, 11)); // 3*4=12≡1 mod 11
    }

    [Fact]
    public void IsPrime_ShouldWork()
    {
        Assert.True(AlgorithmX.Algorithms.MathLib.MathAlgorithm.IsPrime(2));
        Assert.True(AlgorithmX.Algorithms.MathLib.MathAlgorithm.IsPrime(17));
        Assert.False(AlgorithmX.Algorithms.MathLib.MathAlgorithm.IsPrime(1));
        Assert.False(AlgorithmX.Algorithms.MathLib.MathAlgorithm.IsPrime(100));
    }

    [Fact]
    public void SieveOfEratosthenes_ShouldFindPrimesToN()
    {
        var primes = AlgorithmX.Algorithms.MathLib.MathAlgorithm.SieveOfEratosthenes(20);
        Assert.Equal(new[] { 2, 3, 5, 7, 11, 13, 17, 19 }, primes);
    }

    [Fact]
    public void LinearSieve_ShouldMatchEratosthenes()
    {
        var s1 = AlgorithmX.Algorithms.MathLib.MathAlgorithm.SieveOfEratosthenes(100);
        var s2 = AlgorithmX.Algorithms.MathLib.MathAlgorithm.LinearSieve(100);
        Assert.Equal(s1, s2);
    }

    [Fact]
    public void ModPow_ShouldBeCorrect()
    {
        Assert.Equal(1, AlgorithmX.Algorithms.MathLib.MathAlgorithm.ModPow(2, 0, 100));
        Assert.Equal(8, AlgorithmX.Algorithms.MathLib.MathAlgorithm.ModPow(2, 3, 100));
        Assert.Equal(1, AlgorithmX.Algorithms.MathLib.MathAlgorithm.ModPow(2, 10, 1023)); // 2^10 = 1024 ≡ 1 (mod 1023)
    }

    [Fact]
    public void ModPow_LargeExponent_ShouldBeCorrect()
    {
        Assert.Equal(1024 % 7, AlgorithmX.Algorithms.MathLib.MathAlgorithm.ModPow(2, 10, 7));
    }

    [Fact]
    public void Combination_ShouldBeCorrect()
    {
        Assert.Equal(10, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Combination(5, 2));
        Assert.Equal(1, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Combination(5, 0));
        Assert.Equal(1, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Combination(5, 5));
    }

    [Fact]
    public void PascalTriangle_ShouldGenerateCorrectly()
    {
        var tri = AlgorithmX.Algorithms.MathLib.MathAlgorithm.PascalTriangle(5);
        Assert.Equal(new long[] { 1, 5, 10, 10, 5, 1 }, tri[5]);
    }

    [Fact]
    public void Catalan_ShouldBeCorrect()
    {
        Assert.Equal(1, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Catalan(0));
        Assert.Equal(1, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Catalan(1));
        Assert.Equal(5, AlgorithmX.Algorithms.MathLib.MathAlgorithm.Catalan(3));
    }
}
