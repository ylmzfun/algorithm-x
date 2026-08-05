package com.algorithmx.technique.math;

import java.util.*;

/**
 * 数论 & 数学专题
 */
public class NumberTheory {

    // ==================== 最大公约数 / 最小公倍数 ====================

    /** 欧几里得算法 */
    public static int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }

    public static int lcm(int a, int b) { return a / gcd(a, b) * b; }

    /** 扩展欧几里得 — ax + by = gcd(a, b) */
    public static int[] extendedGcd(int a, int b) {
        if (b == 0) return new int[]{a, 1, 0};
        int[] res = extendedGcd(b, a % b);
        return new int[]{res[0], res[2], res[1] - a / b * res[2]};
    }

    // ==================== 快速幂 ====================

    /** 快速幂：x^n % mod */
    public static long fastPow(long x, long n, long mod) {
        long res = 1 % mod;
        x %= mod;
        while (n > 0) {
            if ((n & 1) == 1) res = res * x % mod;
            x = x * x % mod;
            n >>= 1;
        }
        return res;
    }

    /** 矩阵快速幂：Fibonacci O(log n) */
    public static long fibMatrix(long n, long mod) {
        if (n <= 1) return n;
        long[][] res = {{1, 0}, {0, 1}};
        long[][] base = {{1, 1}, {1, 0}};
        long exp = n - 1;
        while (exp > 0) {
            if ((exp & 1) == 1) res = matMul(res, base, mod);
            base = matMul(base, base, mod);
            exp >>= 1;
        }
        return res[0][0];
    }

    private static long[][] matMul(long[][] a, long[][] b, long mod) {
        return new long[][]{
            {(a[0][0] * b[0][0] + a[0][1] * b[1][0]) % mod, (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % mod},
            {(a[1][0] * b[0][0] + a[1][1] * b[1][0]) % mod, (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % mod}
        };
    }

    // ==================== 素数筛法 ====================

    /** 埃氏筛 — 求 [0..n] 所有质数 */
    public static List<Integer> sieveEratosthenes(int n) {
        boolean[] isPrime = new boolean[n + 1];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        for (int i = 2; i * i <= n; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j <= n; j += i) isPrime[j] = false;
            }
        }
        List<Integer> primes = new ArrayList<>();
        for (int i = 2; i <= n; i++) if (isPrime[i]) primes.add(i);
        return primes;
    }

    /** 欧拉线性筛 — O(n) */
    public static List<Integer> sieveEuler(int n) {
        boolean[] isComposite = new boolean[n + 1];
        List<Integer> primes = new ArrayList<>();
        for (int i = 2; i <= n; i++) {
            if (!isComposite[i]) primes.add(i);
            for (int p : primes) {
                if (i * p > n) break;
                isComposite[i * p] = true;
                if (i % p == 0) break; // 每个合数只被最小质因子筛掉
            }
        }
        return primes;
    }

    /** 判断一个数是否为质数 */
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        if (n < 4) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
        }
        return true;
    }

    // ==================== 进制转换 ====================

    /** 十进制转任意进制 */
    public static String toBase(int num, int base) {
        if (num == 0) return "0";
        StringBuilder sb = new StringBuilder();
        while (num > 0) { sb.append(Character.forDigit(num % base, base)); num /= base; }
        return sb.reverse().toString();
    }

    // ==================== 大数运算 ====================

    /** 大数加法（字符串） */
    public static String addStrings(String num1, String num2) {
        StringBuilder sb = new StringBuilder();
        int i = num1.length() - 1, j = num2.length() - 1, carry = 0;
        while (i >= 0 || j >= 0 || carry > 0) {
            int a = i >= 0 ? num1.charAt(i--) - '0' : 0;
            int b = j >= 0 ? num2.charAt(j--) - '0' : 0;
            int sum = a + b + carry;
            sb.append(sum % 10);
            carry = sum / 10;
        }
        return sb.reverse().toString();
    }

    /** 大数乘法（字符串） */
    public static String multiplyStrings(String num1, String num2) {
        if (num1.equals("0") || num2.equals("0")) return "0";
        int m = num1.length(), n = num2.length();
        int[] res = new int[m + n];
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                int mul = (num1.charAt(i) - '0') * (num2.charAt(j) - '0');
                int sum = mul + res[i + j + 1];
                res[i + j + 1] = sum % 10;
                res[i + j] += sum / 10;
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int d : res) if (!(sb.isEmpty() && d == 0)) sb.append(d);
        return sb.toString();
    }
}
